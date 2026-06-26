"""
utils.py
--------
Small helper functions used across the project.

Keeping these in one place avoids repeating the same code in
encrypt.py, decrypt.py, and metadata.py.
"""

import hashlib
from pathlib import Path


def calculate_sha256(file_path):
    """
    Calculate the SHA256 hash of a file.

    We read the file in small chunks (4096 bytes at a time) instead of
    loading the whole file into memory. This keeps the program working
    fine even for large files.

    Args:
        file_path (str or Path): path to the file.

    Returns:
        str: the hex digest (a long string of letters/numbers) representing
             the file's hash. Even a 1-byte change in the file will produce
             a completely different hash.
    """
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        # Read the file in chunks so we don't run out of memory on big files
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def get_file_size(file_path):
    """
    Return the size of a file in bytes.

    Args:
        file_path (str or Path): path to the file.

    Returns:
        int: size of the file in bytes.
    """
    return Path(file_path).stat().st_size


def file_exists(file_path):
    """
    Check whether a given file actually exists on disk.

    Args:
        file_path (str or Path): path to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return Path(file_path).is_file()


def print_separator():
    """Print a simple line separator to make CLI output easier to read."""
    print("-" * 50)
