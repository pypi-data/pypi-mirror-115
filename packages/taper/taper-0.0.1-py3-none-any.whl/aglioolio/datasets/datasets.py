import bisect
import copy
import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Union

import pandas as pd

from aglioolio.params import BINARIES, CACHE
from aglioolio.utils import (
    download_objects,
    upload_objects,
)
from aglioolio.utils_hash import md5
from aglioolio.datasets.base_dataset import Dataset
from aglioolio.datasets.utils import upload_dataset_instance


class CustomDataset(Dataset):
    """CustomDataset supports loading from common dataset objects like
    pandas DataFrame, csv, txt and json files.

    This can be initialized from an iterable or via a load_* function
    for loading from one of the above dataset objects e.g. load_json().

    Args:
        dataset (Iterable): The actual dataset
        name (str): Name of dataset
        version (str): Version of dataset
        metadata (dict): Any associated metadata like publication or link
    """

    def __init__(
        self,
        dataset: Iterable[Any],
        name: Optional[str] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super(CustomDataset, self).__init__(name, version, metadata)
        self.dataset = dataset

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Any:
        return self.dataset.iloc[idx]

    @classmethod
    def load_dataframe(
        cls, dataframe: pd.DataFrame, name: Optional[str] = None
    ) -> "CustomDataset":
        """Loads from pandas DataFrame"""
        return cls(dataframe, name)

    @classmethod
    def load_csv(cls, filename: str, name=None) -> "CustomDataset":
        """Loads from csv file.
        This is a wrapper over pd.read_csv.
        """
        df = pd.read_csv(filename)
        return cls(df, name)

    @classmethod
    def load_json(
        cls,
        filename: str,
        loader: Optional[Callable] = None,
        name: Optional[str] = None,
    ) -> "CustomDataset":
        """Loads from json file with optional loader"""
        with open(filename, "r") as file:
            data = json.load(file)
        if loader:
            data = loader(data)
        df = pd.DataFrame(data)
        return cls(df, name)

    @classmethod
    def load_txt(cls, filename: str, header="data", name=None) -> "CustomDataset":
        """Loads from txt file where each line corresponds to one sample"""
        samples = []
        with open(filename, "r") as file:
            for line in file:
                samples.append(line)
        df = pd.DataFrame(samples, columns=[header])
        return cls(df, name)

    def publish(self, public: bool = False) -> Tuple["CustomDataset", str]:
        """See Dataset.publish"""
        obj = upload_dataset_instance(self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        """See Dataset.load_children"""
        return None


class SingleFolder(Dataset):
    """SingleFolder supports loading datasets best defined by a directory.

    This may be a single class e.g. if the folder comprise of images from a single class.
    Or the files may be mapped to various classes via the mapping_fn.
    This also supports a limited globbing feature supported by pathlib Path.glob.

    TODO: Think about overlaps between loader and mapping_fn (and maybe transform)

    Args:
        folder (str): Folder comprising of files in the dataset
        loader (Callable): Function applied to filename that outputs the sample
        name (str): Name of dataset
        version (str): Version of dataset
        metadata (dict): Any associated metadata like publication or link
        label (Any): Maps the entire dataset to a single label
        mapping_fn (Callable): Function applied to loader output for the actual output
        exts (Iterable or str): If supplied SingleFolder will only load files with these extensions
        recursive (bool): Whether to search through the folder recursively
        glob (str): Glob string for more nuanced filtering, this is supported by pathlib Path.glob
        filename2id (Callable): This maps filenames to sample IDs, which is used for joining datasets
    """

    def __init__(
        self,
        folder: str,
        loader: Callable[[str], Any],
        name: Optional[str] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        label: Optional[Any] = None,
        mapping_fn: Optional[Callable] = None,
        exts: Optional[Union[Iterable[str], str]] = None,
        recursive: bool = True,
        glob: Optional[str] = None,
        filename2id: Optional[Callable] = None,
    ):
        super(SingleFolder, self).__init__(name, version, metadata)
        self.folder = folder
        self.loader = loader
        self.label = label
        self.mapping_fn = mapping_fn  # Maps (idx, id, obj) to a tuple
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
        """See Dataset.publish"""
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
        """See Dataset.load_children"""
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
            print(CACHE / self.obj_name / filehash)


class ConcatDataset(Dataset):
    """Adapted from torch's ConcatDataset class.

    Dataset as a concatenation of multiple datasets.

    This class is useful to assemble different existing datasets.

    Args:
        datasets (sequence): List of datasets to be concatenated
        name (str): Name of dataset
        version (str): Version of dataset
        metadata (dict): Any associated metadata like publication or link
    """

    @staticmethod
    def cumsum(sequence):
        sizes, length_sum = [], 0
        for e in sequence:
            length = len(e)
            sizes.append(length + length_sum)
            length_sum += length
        return sizes

    def __init__(
        self,
        datasets: Iterable[Dataset],
        name: Optional[str] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        super(ConcatDataset, self).__init__(name, version, metadata)
        assert len(datasets) > 0, "datasets should not be an empty iterable"
        self.datasets = list(datasets)
        self.cumulative_sizes = self.cumsum(self.datasets)

    def __len__(self):
        return self.cumulative_sizes[-1]

    def __getitem__(self, idx):
        if idx < 0:
            if -idx > len(self):
                raise ValueError(
                    "absolute value of index should not exceed dataset length"
                )
            idx = len(self) + idx
        dataset_idx = bisect.bisect_right(self.cumulative_sizes, idx)
        if dataset_idx == 0:
            sample_idx = idx
        else:
            sample_idx = idx - self.cumulative_sizes[dataset_idx - 1]
        return self.datasets[dataset_idx][sample_idx]

    def publish(self, public: bool = False) -> Tuple["ConcatDataset", str]:
        """See Dataset.publish"""
        copy_self = copy.deepcopy(self)
        # Upload constituent datasets
        copy_datasets_dict = OrderedDict()
        copy_datasets = []
        for ds in self.datasets:
            ds_copy, ds_name = ds.publish(public=public)
            copy_datasets_dict[ds_name] = ds_copy
            copy_datasets.append(ds_copy)
        copy_self.datasets_dict = copy_datasets_dict
        copy_self.datasets = copy_datasets
        # self.hash = f'{self.name}.data'
        # upload_dataset(copy_self, f'{self.name}.data')
        obj = upload_dataset_instance(copy_self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        """See Dataset.load_children"""
        for ds_name, ds in self.datasets_dict.items():
            if isinstance(ds, SingleFolder):
                SingleFolder.load(ds_name, force_download)
            elif isinstance(ds, CustomDataset):
                CustomDataset.load(ds_name, force_download)


class JoinDataset(Dataset):
    """JoinDataset acts like an SQL join between datasets based on
    sample IDs. Specifically does a left-join based on the first dataset.

    Args:
        datasets (sequence): List of datasets to be concatenated
        name (str): Name of dataset
        version (str): Version of dataset
        metadata (dict): Any associated metadata like publication or link
    """

    def __init__(
        self,
        datasets: Iterable[Dataset],
        name: Optional[str] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super(JoinDataset, self).__init__(name, version, metadata)
        self.datasets = datasets

    def __len__(self) -> int:
        # Follow length of first dataset
        return len(self.datasets[0])

    def __getitem__(self, idx: int) -> Any:
        selected_id = list(self.datasets)[0].ids[idx]
        return tuple(ds[ds.ids.index(selected_id)] for ds in self.datasets)

    def publish(self, public: bool = False) -> Tuple["JoinDataset", str]:
        copy_self = copy.deepcopy(self)
        # Upload constituent datasets
        copy_datasets_dict = OrderedDict()
        copy_datasets = []
        for ds in self.datasets:
            ds_copy, ds_name = ds.publish(public=public)
            copy_datasets_dict[ds_name] = ds_copy
            copy_datasets.append(ds_copy)
        copy_self.datasets = copy_datasets
        copy_self.datasets_dict = copy_datasets_dict
        # copy_self.hash = f'{self.name}.data'
        obj = upload_dataset_instance(copy_self, public)
        return obj, obj.obj_name

    def load_children(self, force_download: bool = False) -> None:
        for ds_name, ds in self.datasets_dict.items():
            if isinstance(ds, SingleFolder):
                SingleFolder.load(ds_name, force_download)
            elif isinstance(ds, CustomDataset):
                CustomDataset.load(ds_name, force_download)
