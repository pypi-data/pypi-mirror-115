import hashlib
import json
import logging
from typing import Optional

from .params import CACHE, HASHTABLE_PATH


class HashTable:
    """Local storage for checksums."""

    def __init__(self):
        with open(HASHTABLE_PATH, "r") as f:
            self._table = json.load(f)

    def get_checksum(self, obj_name: str) -> Optional[str]:
        """Returns stored checksum for a given object.

        Parameters
        ----------
        obj_name (str): Object name

        Returns
        -------
        checksum (str): Corresponding checksum
        """
        checksum = self._table.get(obj_name, None)
        return checksum

    def put_checksum(self, obj_name: str, checksum: str) -> None:
        """Stores checksum for a given object.

        Parameters
        ----------
        obj_name (str): Object name
        checksum (str): Corresponding checksum
        """
        self._table[obj_name] = checksum
        with open(HASHTABLE_PATH, "w") as f:
            json.dump(self._table, f)

    def del_checksum(self, obj_name: str) -> None:
        """Deletes checksum for a given object from local hashtable.

        Parameters
        ----------
        obj_name (str): Object name
        """
        self._table.pop(obj_name, None)
        with open(HASHTABLE_PATH, "w") as f:
            json.dump(self._table, f)


def md5(filename: str) -> str:
    """Computes md5 checksum for a file.

    Parameters
    ----------
    filename (str): Filename

    Returns
    -------
    checksum (str): Corresponding checksum
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    checksum = hash_md5.hexdigest()
    return checksum


def save_checksum(obj_name: str, checksum: str) -> None:
    """Save checksum to local HashTable.

    Parameters
    ----------
    obj_name (str): Object name
    checksum (str): Corresponding checksum
    """
    table = HashTable()
    table.put_checksum(obj_name, checksum)


def del_checksum(obj_name: str) -> None:
    """Delete checksum from local HashTable.

    Parameters
    ----------
    obj_name (str): Object name
    """
    table = HashTable()
    table.del_checksum(obj_name)


def checksum(dataset, verbose: bool = True) -> Optional[bool]:
    """Run checksum for a dataset.

    Parameters
    ----------
    dataset (Dataset): Dataset
    verbose (bool): Whether to log messages (defaults to True)

    Returns
    -------
    pass (Optional[bool]): None if checksum not found, otherwise
        bool indicating if checksum passes
    """
    table = HashTable()
    obj_hash = table.get_checksum(dataset.obj_name)
    if obj_hash is None:
        return None

    file_hash = md5(CACHE / f"{dataset.obj_name}.data")

    if file_hash == obj_hash:
        if verbose:
            logging.info(f"Checksum passed for file {dataset.obj_name}")
        return True
    else:
        if verbose:
            logging.info(f"Checksum failed for file {dataset.obj_name}")
        return False
