import json
import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, Optional

import dill
import requests
from tqdm import tqdm

from aglioolio.errors import AlreadyExistsError
from aglioolio.params import (
    BINARIES,
    CACHE,
    DOWNLOAD_URL,
    HASHTABLE_PATH,
    UPLOAD_URL,
)
from aglioolio.utils_hash import save_checksum


def clear_cache() -> None:
    """Clears cache folder."""
    for f in CACHE.iterdir():
        try:
            if f.is_file() or f.is_symlink():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)
        except Exception as e:
            logging.error(f"Failed to delete {f}. Reason: {e}")
    BINARIES.mkdir(parents=True, exist_ok=True)
    if not HASHTABLE_PATH.is_file():
        with open(HASHTABLE_PATH, "w") as f:
            json.dump({}, f)


def save_dataset(dataset) -> None:
    with open(CACHE / f"{dataset.obj_name}.data", "wb") as f:
        dill.dump(dataset, f, recurse=True)


def delete_dataset(dataset) -> None:
    os.unlink(CACHE / f"{dataset.obj_name}.data")


def upload(
    src_path: str, obj_name: Optional[str] = None, test: bool = False
) -> Optional[str]:
    """Uploads an object.

    Parameters
    ----------
    src_path (str): Path to file object
    obj_name (str): Name of object

    Returns
    -------
    obj_name (str): None if object with same name already exists, else
        returns object name
    """
    if test:
        presigned = requests.get(
            UPLOAD_URL, params={"filename": obj_name, "test": True}
        ).json()
    else:
        presigned = requests.get(UPLOAD_URL, params={"filename": obj_name}).json()
    if isinstance(presigned, str) and presigned.startswith("Object with same key"):
        raise AlreadyExistsError(f"Object with same key {obj_name} already exists.")
    with open(src_path, "rb") as f:
        files = {"file": (presigned["obj_name"], f)}
        request_response = requests.post(
            presigned["url"], data=presigned["fields"], files=files
        )
    if not request_response:
        raise ConnectionError
    obj_name = presigned["obj_name"]
    if obj_name.endswith(".data"):
        obj_name = obj_name[:-5]
    return obj_name


def download(obj_name: str, progress: bool = False) -> None:
    """Downloads an object to cache.
    Does not check if object with same name already exists locally
    and will overwrite.
    obj_name should not include CACHE folder.

    Parameters
    ----------
    obj_name (str): Name of object
    progress (bool): Whether to show progress bar
    """
    dst_path = CACHE / obj_name
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    presigned = requests.get(DOWNLOAD_URL, params={"filename": obj_name}).json()

    response = requests.get(presigned["url"])
    if progress:
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1kb
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(dst_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    else:
        with open(dst_path, "wb") as file:
            file.write(response.content)

    if not obj_name.startswith("binaries"):
        save_checksum(presigned["obj_name"], presigned["hash"])
    return presigned["obj_name"]


def upload_objects(
    src_paths: Iterable[str], obj_names: Iterable[str], test: bool = False
) -> Iterable[str]:
    """Multithreaded uploads.

    Parameters
    ----------
    src_paths (Iterable): Paths to file objects
    obj_names (Iterable): Names of objects

    Returns
    -------
    new_obj_names (Iterable): Names of uploaded objects
    """
    with tqdm(desc="Uploading objects", total=len(src_paths)) as pbar:
        with ThreadPoolExecutor() as executor:
            futures = {}
            for src_path, obj_name in zip(src_paths, obj_names):
                future = executor.submit(upload, src_path, obj_name, test)
                futures[future] = (src_path, obj_name)
            new_obj_names = []
            for future in as_completed(futures):
                try:
                    new_obj_name = future.result()
                    new_obj_names.append(new_obj_name)
                    src_path, _ = futures[future]
                    shutil.copyfile(src_path, CACHE / new_obj_name)
                except Exception as e:
                    logging.error(e)
                pbar.update(1)
    return new_obj_names


def download_objects(obj_names: Iterable[str]) -> Iterable[str]:
    """Multithreaded downloads.
    obj_name should not include CACHE folder.

    Parameters
    ----------
    obj_names (str): Names of objects
    """
    with tqdm(desc="Downloading objects", total=len(obj_names)) as pbar:
        with ThreadPoolExecutor() as executor:
            futures = {}
            for obj_name in obj_names:
                future = executor.submit(download, obj_name)
                futures[future] = obj_name
            new_obj_names = []
            for future in as_completed(futures):
                try:
                    new_obj_names.append(future.result())
                except Exception as e:
                    logging.error(e)
                pbar.update(1)
    return new_obj_names
