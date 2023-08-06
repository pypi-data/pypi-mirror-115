import copy
import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Tuple, Union

import pandas as pd

from octarin.params import BINARIES, CACHE
from octarin.utils import (
    download_objects,
    upload_objects,
)
from octarin.utils_hash import md5
from octarin.datasets.base_dataset import OctarinDataset
from octarin.datasets.utils import upload_dataset_instance


class CustomDataset(OctarinDataset):
    def __init__(
        self,
        dataset: Iterable[Any],
        name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.dataset = dataset
        self.name = name
        self.version = version

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Any:
        return self.dataset.iloc[idx]

    @classmethod
    def load_dataframe(
        cls, dataframe: pd.DataFrame, name: Optional[str] = None
    ) -> "CustomDataset":
        return cls(dataframe, name)

    @classmethod
    def load_csv(cls, filename: str, name=None) -> "CustomDataset":
        df = pd.read_csv(filename)
        return cls(df, name)

    @classmethod
    def load_json(
        cls, filename: str, loader=Callable, name: Optional[str] = None
    ) -> "CustomDataset":
        with open(filename, "r") as file:
            data = json.load(file)
        if loader:
            data = loader(data)
        df = pd.DataFrame(data)
        return cls(df, name)

    @classmethod
    def load_txt(cls, filename: str, header="data", name=None) -> "CustomDataset":
        samples = []
        with open(filename, "r") as file:
            for line in file:
                samples.append(line)
        df = pd.DataFrame(samples, columns=[header])
        return cls(df, name)

    def publish(self, public: bool = False) -> Tuple["CustomDataset", str]:
        obj = upload_dataset_instance(self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        return None


class SingleFolder(OctarinDataset):
    def __init__(
        self,
        folder: str,
        loader: Callable,
        name: Optional[str] = None,
        version: Optional[str] = None,
        label: Any = None,
        mapping_fn: Optional[Callable] = None,
        transform: Optional[Callable] = None,
        exts: Optional[Union[Iterable[str], str]] = None,
        recursive: bool = True,
        glob: Optional[str] = None,
        filename2id: Optional[Callable] = None,
    ):
        self.folder = folder
        self.loader = loader
        self.name = name
        self.version = version
        self.label = label
        self.mapping_fn = mapping_fn  # Maps (idx, id, obj) to a tuple
        self.transform = transform
        self.exts = exts or []
        if isinstance(self.exts, str):
            self.exts = [self.exts]
        self.exts = [ext.strip(".") for ext in self.exts]
        self.recursive = recursive
        self.glob = glob
        self.filename2id = filename2id
        self._hash = None
        self._hashes = None

    def __len__(self) -> int:
        return len(self.files)

    def __getitem__(self, idx: int) -> Any:
        selected_id = self.ids[idx]
        obj = self.loader(str(self.files[idx]))
        if self.label is not None:
            return obj, self.label
        elif self.mapping_fn is not None:
            return self.mapping_fn(idx, selected_id, obj)
        return obj

    @property
    def dir_path(self) -> Path:
        return Path(self.folder)

    @property
    def files(self) -> Iterable[Path]:
        files = []
        if self._hashes:
            files = list(BINARIES / k for k in self._hashes.keys())
        elif self.glob:
            files += list(self.dir_path.glob(self.glob))
        else:
            if self.recursive:
                prefix = "**/"
            else:
                prefix = ""
            if self.exts:
                for ext in self.exts:
                    files += list(self.dir_path.glob(f"{prefix}*.{ext}"))
            else:
                files += list(self.dir_path.glob(f"{prefix}*"))
        files = [f for f in files if f.is_file()]
        files.sort()
        return files

    @property
    def ids(self) -> Iterable[str]:
        if self._hashes:
            ids = [Path(self._hashes[f.stem]).stem for f in self.files]
        else:
            ids = [f.stem for f in self.files]
        if self.filename2id:
            ids = [self.filename2id(f) for f in ids]
        return ids

    def publish(self, public: bool = False) -> Tuple["SingleFolder", str]:
        copy_self = copy.deepcopy(self)
        # Hash files
        hashes = OrderedDict()
        src_paths, obj_names = [], []
        for file in self.files:
            filehash = md5(file)
            src_paths.append(file)
            obj_names.append(f"binaries/{filehash}")
            hashes[filehash] = str(file)
        upload_objects(src_paths, obj_names)
        # Remap directory
        copy_self._hashes = hashes
        # Upload instance
        obj = upload_dataset_instance(copy_self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        to_download = []
        for filehash in self._hashes:
            if force_download or not (BINARIES / filehash).exists():
                to_download.append(f"binaries/{filehash}")
            elif md5(BINARIES / filehash) != filehash:
                logging.error(
                    f"Checksum failed for file {filehash}, downloading again..."
                )
                to_download.append(f"binaries/{filehash}")
        if len(to_download):
            download_objects(to_download)
        # Verify checksum
        for filehash in self._hashes:
            if md5(BINARIES / filehash) != filehash:
                logging.error(f"Checksum failed for file {filehash}")
        # Create symlinks to organize cache folder
        (CACHE / self.obj_name).mkdir(parents=True, exist_ok=True)
        for filehash in self._hashes:
            (CACHE / self.obj_name / filehash).symlink_to(BINARIES / filehash)


class ConcatDataset(OctarinDataset):
    def __init__(
        self,
        datasets: Iterable[OctarinDataset],
        name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        super(ConcatDataset, self).__init__(datasets)
        self.name = name
        self.version = version

    def publish(self, public: bool = False) -> Tuple["ConcatDataset", str]:
        copy_self = copy.deepcopy(self)
        # Upload constituent datasets
        copy_datasets = OrderedDict()
        for ds in self.datasets:
            ds_copy, ds_name = ds.publish(public=public)
            copy_datasets[ds_name] = ds_copy
        copy_self.datasets = copy_datasets
        # self.hash = f'{self.name}.data'
        # upload_dataset(copy_self, f'{self.name}.data')
        obj = upload_dataset_instance(copy_self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        for ds_name, ds in self.datasets.items():
            if isinstance(ds, SingleFolder):
                SingleFolder.load(ds_name, force_download)
            elif isinstance(ds, CustomDataset):
                CustomDataset.load(ds_name, force_download)


class JoinDataset(OctarinDataset):
    def __init__(
        self,
        datasets: Iterable[OctarinDataset],
        name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        self.name = name
        self.version = version
        # Assume all datasets have the same IDs
        self.datasets = datasets

    def __len__(self) -> int:
        # Follow length of first dataset
        return len(self.datasets[0])

    def __getitem__(self, idx: int) -> Any:
        selected_id = list(self.datasets.values())[0].ids[idx]
        return tuple(ds[ds.ids.index(selected_id)] for ds in self.datasets.values())

    def publish(self, public: bool = False) -> Tuple["JoinDataset", str]:
        copy_self = copy.deepcopy(self)
        # Upload constituent datasets
        copy_datasets = OrderedDict()
        for ds in self.datasets:
            ds_copy, ds_name = ds.publish(public=public)
            copy_datasets[ds_name] = ds_copy
        copy_self.datasets = copy_datasets
        # copy_self.hash = f'{self.name}.data'
        obj = upload_dataset_instance(copy_self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        for ds_name, ds in self.datasets.items():
            if isinstance(ds, SingleFolder):
                SingleFolder.load(ds_name, force_download)
            elif isinstance(ds, CustomDataset):
                CustomDataset.load(ds_name, force_download)
