import argparse

import requests

UPLOAD_URL = "https://5akl5i0fpk.execute-api.us-east-1.amazonaws.com/test/helloworld"
DOWNLOAD_URL = "https://5akl5i0fpk.execute-api.us-east-1.amazonaws.com/test/download"


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, required=True)
parser.add_argument("--upload", action="store_true")
parser.add_argument("--download", action="store_true")
config = parser.parse_args()


def upload(filename: str) -> None:
    presigned = requests.get(UPLOAD_URL, params={"filename": filename}).json()
    with open(filename, "rb") as f:
        files = {"file": (filename, f)}
        requests.post(presigned["url"], data=presigned["fields"], files=files)


def download(filename: str) -> None:
    presigned = requests.get(DOWNLOAD_URL, params={"filename": filename}).json()
    response = requests.get(presigned)
    with open(filename, "wb") as file:
        file.write(response.content)


def main():
    if config.upload:
        upload(config.filename)
    elif config.download:
        download(config.filename)


if __name__ == "__main__":
    main()
