"""
metadata.py
-----------
Handles reading and writing metadata.json.

metadata.json keeps track of every file we've encrypted:
- the original filename
- the encrypted filename
- the SHA256 hash (used later to verify integrity)
- when it was encrypted
- the original file size

We use a simple JSON file instead of a database to keep this project
beginner-friendly and dependency-free.
"""

import json
from pathlib import Path

METADATA_FILE = "metadata.json"


def load_metadata():
    """
    Load metadata.json from disk.

    If the file doesn't exist yet (first run), we return an empty
    dictionary instead of crashing.

    Returns:
        dict: metadata records, keyed by encrypted filename.
    """
    metadata_path = Path(METADATA_FILE)

    if not metadata_path.is_file():
        return {}

    try:
        with open(metadata_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # If the file is corrupted or unreadable, start fresh instead
        # of crashing the whole program.
        print("Warning: metadata.json could not be read. Starting fresh.")
        return {}


def save_metadata(metadata):
    """
    Save the metadata dictionary back to metadata.json.

    Args:
        metadata (dict): the full metadata dictionary to save.
    """
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)


def add_file_record(encrypted_filename, record):
    """
    Add (or update) a single file's metadata record and save it.

    Args:
        encrypted_filename (str): key used to identify this entry
            (the name of the encrypted file).
        record (dict): metadata about the file, e.g.
            {
                "original_filename": "notes.txt",
                "encrypted_filename": "notes.txt.enc",
                "sha256": "...",
                "encryption_time": "2026-06-26 10:00:00",
                "file_size_bytes": 1024
            }
    """
    metadata = load_metadata()
    metadata[encrypted_filename] = record
    save_metadata(metadata)


def get_file_record(encrypted_filename):
    """
    Retrieve metadata for one encrypted file.

    Args:
        encrypted_filename (str): the encrypted file's name.

    Returns:
        dict or None: the metadata record, or None if not found.
    """
    metadata = load_metadata()
    return metadata.get(encrypted_filename)


def list_all_records():
    """
    Return all stored metadata records.

    Returns:
        dict: all metadata records.
    """
    return load_metadata()
