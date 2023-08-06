import json
from pathlib import Path

USERNAME = "greentfrapp"
ACCESS_KEY = "greentfrapp"

UPLOAD_URL = "https://api.agliool.io/prod/upload"
UPLOAD_NAMED_URL = (
    "https://api.agliool.io/prod/upload_public"
)
DOWNLOAD_URL = "https://api.agliool.io/prod/download"
CACHE = Path.home() / ".cache" / "aglioolio"
CACHE.mkdir(parents=True, exist_ok=True)
BINARIES = CACHE / "binaries"
BINARIES.mkdir(parents=True, exist_ok=True)
WRITE_HASH_URL = (
    "https://api.agliool.io/prod/update_checksum"
)
HASHTABLE_PATH = CACHE / "hashtable"
if not HASHTABLE_PATH.is_file():
    with open(HASHTABLE_PATH, "w") as f:
        json.dump({}, f)
