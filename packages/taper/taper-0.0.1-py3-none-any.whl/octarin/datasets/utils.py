import logging
import tempfile
import os
import requests
import shutil
import re

import dill

from octarin.errors import AlreadyExistsError, AuthenticationError
from octarin.utils_hash import checksum, save_checksum, md5
from octarin.datasets.base_dataset import OctarinDataset
from octarin.params import (
    CACHE,
    OCTARIN_ACCESS_KEY,
    OCTARIN_USERNAME,
    UPLOAD_NAMED_URL,
    UPLOAD_URL,
    WRITE_HASH_URL,
)

logging.basicConfig(level=logging.INFO)


def mainify(obj: OctarinDataset) -> None:
    """If obj is not defined in __main__ then redefine it in
    main so that dill will serialize the definition along with
    the object

    Parameters
    ----------
    obj (OctarinDataset): Dataset to save
    """
    if obj.__module__ != "__main__":
        import inspect

        import __main__

        s = inspect.getsource(obj)
        co = compile(s, "<string>", "exec")
        exec(co, __main__.__dict__)


def upload_dataset_instance(
    dataset: OctarinDataset, public: bool = False
) -> OctarinDataset:
    """Uploads an initialized instance of a dataset.
    Public datasets require authentication, will be
    retained indefinitely and can be uploaded with fixed
    names.
    Non-public datasets do not require authentication,
    will only be retained for 7 days and will be assigned
    a random name.
    Uploading a dataset might change certain parameters
    e.g. name and version may be updated.
    TODO: List out possible changes when uploading

    Parameters
    ----------
    dataset (OctarinDataset): Dataset to upload
    public (bool): Whether dataset is meant to be public

    Returns
    -------
    dataset (OctarinDataset): Dataset that was uploaded
    """
    # mainify(dataset.__class__)
    if checksum(dataset, verbose=False):
        logging.info(
            f"Dataset {dataset.obj_name} seems to be unchanged. To force update, we suggest changing the version."
        )
    else:
        if public:
            try:
                dataset = upload_dataset_public(dataset)
                logging.info(f"Uploaded dataset with ID {dataset.obj_name}")
            except AlreadyExistsError:
                logging.warning(
                    f"Not uploading {dataset.obj_name} since a dataset with the same name already exists."
                )
        else:
            dataset = upload_dataset(dataset)
            logging.info(f"Uploaded dataset with ID {dataset.obj_name}")
    return dataset


def reload_dataset(dataset: OctarinDataset) -> OctarinDataset:
    """Hack to work around bug where reloading the first time changes hash.
    Hack works by reloading before computing the hash.
    TODO: figure out why the bug is actually happening

    Parameters
    ----------
    dataset (OctarinDataset): Dataset to reload

    Returns
    -------
    dataset (OctarinDataset): Dataset that was reloaded
    """
    tmp = tempfile.NamedTemporaryFile(dir=CACHE, delete=False)
    dill.dump(dataset, tmp, recurse=False)
    tmp.close()
    with open(tmp.name, "rb") as file:
        dataset = dill.load(file)
    os.unlink(tmp.name)
    return dataset


def save_dataset_checksum(dataset: OctarinDataset, checksum: str) -> None:
    """Uploads checksum to an online table and also save checksum
    to a local HashTable.

    Parameters:
    -----------
    dataset (OctarinDataset): Dataset that was checksum-ed
    checksum (str): Corresponding checksum
    """
    requests.get(
        WRITE_HASH_URL
        + f"?obj_name={dataset.obj_name}&name={dataset.name}&hash={checksum}"
    )
    save_checksum(dataset.obj_name, checksum)


def upload_dataset(dataset: OctarinDataset) -> OctarinDataset:
    """Upload a non-public dataset.
    This will assign a random name to dataset.name and
    set dataset.version to None.

    Parameters
    ----------
    dataset (OctarinDataset): Dataset to upload

    Returns
    -------
    dataset (OctarinDataset): Dataset that was uploaded
    """
    presigned = requests.get(UPLOAD_URL + f"?filename={'random'}")

    if not presigned:
        raise ConnectionError(f'Connection error with response {presigned}: {presigned.json()}')
    else:
        presigned = presigned.json()

    obj_name = presigned["obj_name"]
    if obj_name.endswith(".data"):
        obj_name = obj_name[:-5]

    dataset.name = obj_name
    dataset.version = None

    dataset = reload_dataset(dataset)

    tmp = tempfile.NamedTemporaryFile(dir=CACHE, delete=False)
    dill.dump(dataset, tmp, recurse=False)
    tmp.close()
    checksum = md5(tmp.name)

    with open(tmp.name, "rb") as f:
        files = {"file": (presigned["obj_name"], f)}
        post_response = requests.post(presigned["url"], data=presigned["fields"], files=files)
        assert post_response.status_code == 204, f'Response failed with {post_response}'

    save_dataset_checksum(dataset, checksum)

    shutil.copyfile(tmp.name, CACHE / f"{dataset.obj_name}.data")
    os.unlink(tmp.name)

    return dataset


def upload_dataset_public(dataset: OctarinDataset) -> OctarinDataset:
    """Uploads a public dataset.
    Does not overwrite if object with same name already exists.
    Requires authentication and applies name restrictions.

    Parameters
    ----------
    dataset (OctarinDataset): Dataset to upload

    Returns
    -------
    dataset (OctarinDataset): Dataset that was uploaded
    """
    if dataset.name.startswith("tmp-"):
        raise ValueError(f'Dataset name ({dataset.name}) cannot begin with "tmp-"')
    if dataset.version == "latest":
        raise ValueError('Dataset version cannot be "latest"')

    if dataset.name is None:
        raise ValueError("Dataset name should not be None")
    elif dataset.version is None:
        logging.warning(f"Found version None in {dataset.name}, defaulting to 1")
        dataset.version = 1
    elif re.findall(r"[^a-zA-Z\d\s:\.]", dataset.name):
        invalid = re.findall(r"[^a-zA-Z\d\s:\.]", dataset.name)
        raise ValueError(
            f"Invalid character {invalid[0]} found in dataset name, only alphanumerics and periods are allowed"
        )
    elif re.findall(r"[^a-zA-Z\d\s:\.]", dataset.version):
        invalid = re.findall(r"[^a-zA-Z\d\s:\.]", dataset.version)
        raise ValueError(
            f"Invalid character {invalid[0]} found in dataset version, only alphanumerics and periods are allowed"
        )

    presigned = requests.get(
        UPLOAD_NAMED_URL
        + f"?filename={dataset.obj_name}.data&username={OCTARIN_USERNAME}&access_key={OCTARIN_ACCESS_KEY}"
    )

    if not presigned:
        raise ConnectionError(f'Connection error with response {presigned}: {presigned.json()}')
    else:
        presigned = presigned.json()

    dataset = reload_dataset(dataset)

    tmp = tempfile.NamedTemporaryFile(dir=CACHE, delete=False)
    dill.dump(dataset, tmp, recurse=False)
    tmp.close()
    checksum = md5(tmp.name)

    with open(tmp.name, "rb") as f:
        files = {"file": (f"{dataset.obj_name}.data", f)}
        post_response = requests.post(
            presigned["url"], data=presigned["fields"], files=files
        )
        assert post_response.status_code == 204, f'Response failed with {post_response}'

    save_dataset_checksum(dataset, checksum)

    shutil.copyfile(tmp.name, CACHE / f"{dataset.obj_name}.data")
    os.unlink(tmp.name)

    return dataset
