from pathlib import Path
import json


MANIFEST_PATH = Path("storage/manifest.json")


def load_manifest():

    if not MANIFEST_PATH.exists():
        return {}

    with open(MANIFEST_PATH, "r") as file:
        return json.load(file)


def save_manifest(manifest):

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(MANIFEST_PATH, "w") as file:
        json.dump(manifest, file, indent=4)


def is_file_indexed(manifest, filename, file_hash):
    if filename not in manifest:
        return False

    return manifest[filename]["hash"] == file_hash        
def update_manifest(manifest, filename, file_hash):
    manifest[filename] = {
        "hash": file_hash
    }