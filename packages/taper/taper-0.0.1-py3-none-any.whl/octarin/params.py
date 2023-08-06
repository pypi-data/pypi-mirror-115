import json
from pathlib import Path

OCTARIN_USERNAME = "greentfrapp"
OCTARIN_ACCESS_KEY = "greentfrapp"

UPLOAD_URL = "https://5akl5i0fpk.execute-api.us-east-1.amazonaws.com/prod/upload"
UPLOAD_NAMED_URL = "https://5akl5i0fpk.execute-api.us-east-1.amazonaws.com/prod/upload_public"
DOWNLOAD_URL = "https://5akl5i0fpk.execute-api.us-east-1.amazonaws.com/prod/download"
CACHE = Path.home() / ".cache" / "octarin"
CACHE.mkdir(parents=True, exist_ok=True)
BINARIES = CACHE / "binaries"
BINARIES.mkdir(parents=True, exist_ok=True)
WRITE_HASH_URL = (
    "https://5akl5i0fpk.execute-api.us-east-1.amazonaws.com/test/update_checksum"
)
HASHTABLE_PATH = CACHE / "hashtable"
if not HASHTABLE_PATH.is_file():
    with open(HASHTABLE_PATH, "w") as f:
        json.dump({}, f)
