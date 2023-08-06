import dill
import torch
from typing import Any, Dict, Optional, Tuple

from aglioolio.params import CACHE
from aglioolio.utils import download
from aglioolio.utils_hash import checksum


def load(
    obj_name: str, force_download: bool = False, progress: bool = False
) -> "Dataset":
    """Loads an object.
    Downloads file first if not found locally.
    obj_name should not include CACHE folder.

    Parameters
    ----------
    obj_name (str): Name of object to load
    force_download (bool): Whether to force download
    progress (bool): Whether to show progress bar

    Returns
    -------
    dataset (Dataset): Loaded dataset
    """
    if force_download or not (CACHE / obj_name).exists():
        # Download saved file
        download(obj_name, progress)
    # Unpickle and load
    with open(CACHE / obj_name, "rb") as file:
        dataset = dill.load(file)
    return dataset


class Dataset(torch.utils.data.Dataset):
    """Base Dataset class that supports publishing and loading.

    Args:
        name (str): Name of dataset
        version (str): Version of dataset
        metadata (dict): Any associated metadata like publication or link
    """

    def __init__(
        self,
        name: Optional[str] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        super(Dataset, self).__init__()
        self.name = name
        self.version = version
        self.metadata = metadata

    @property
    def obj_name(self) -> str:
        """Returns object name.

        Returns
        -------
        obj_name (str): Concatenation of self.name
            and self.version.
        """
        if self.version:
            return f"{self.name}_{self.version}"
        return self.name

    def publish(self, public: bool = False) -> Tuple["Dataset", str]:
        """Publish this dataset online.
        This should be overwritten by child classes.

        Parameters
        ----------
        public (bool): Whether dataset is public.

        Returns
        -------
        dataset (Dataset): The uploaded dataset, which may be a
            modified version of self.
        obj_name (str): The corresponding object name.
        """
        raise NotImplementedError

    @staticmethod
    def load(
        obj_name: str, force_download: bool = False, progress: bool = True
    ) -> "Dataset":
        """Load dataset via object name.

        Parameters
        ----------
        obj_name (str): Object name corresponding to dataset.
        force_download (bool): Whether to force download.
        progress (bool): Whether to show progress bar.

        Returns
        -------
        dataset (Dataset): Loaded dataset
        """
        dst_path = CACHE / f"{obj_name}.data"
        if not force_download and dst_path.exists():
            with open(dst_path, "rb") as file:
                obj = dill.load(file)
            checksum(obj)
            return obj
        obj = load(f"{obj_name}.data", force_download, progress)
        checksum(obj)
        obj.load_children()
        return obj

    def load_children(self, force_download: bool = False) -> None:
        """Load children components, whether datasets or binaries.
        This should be overwritten by child classes.

        Parameters
        ----------
        force_download (bool): Whether to force download.
        """
        raise NotImplementedError
