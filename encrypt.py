"""
encrypt.py
----------
Handles encrypting a file using Fernet (which internally uses AES-128
in CBC mode with HMAC for authentication; it is the standard,
beginner-friendly symmetric encryption tool provided by the
'cryptography' library and is suitable for this educational project).

The general flow is:
1. Calculate the SHA256 hash of the original file (for integrity checks later)
2. Read the original file's bytes
3. Encrypt those bytes using a Fernet key
4. Save the encrypted bytes to encrypted_files/<filename>.enc
5. Save metadata (filename, hash, size, time) to metadata.json
"""

from pathlib import Path
from datetime import datetime

from cryptography.fernet import Fernet

from utils import calculate_sha256, get_file_size, file_exists
import metadata

ENCRYPTED_FOLDER = "encrypted_files"
KEY_FILE = "secret.key"


def load_or_create_key():
    """
    Load the encryption key from secret.key, or create a new one if it
    doesn't exist yet.

    IMPORTANT: secret.key is what locks/unlocks all your encrypted files.
    If you lose it, you cannot decrypt your files. Keep it private and
    never upload it to GitHub (it's already listed in .gitignore).

    Returns:
        bytes: the Fernet key.
    """
    key_path = Path(KEY_FILE)

    if key_path.is_file():
        with open(key_path, "rb") as f:
            return f.read()

    # No key yet -> generate one and save it for future use
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)

    print(f"New encryption key generated and saved to '{KEY_FILE}'.")
    print("Keep this file safe — without it, encrypted files cannot be decrypted!")
    return key


def encrypt_file(input_path):
    """
    Encrypt a single file and store it inside encrypted_files/.

    Args:
        input_path (str): path to the file the user wants to encrypt.

    Returns:
        bool: True if encryption succeeded, False otherwise.
    """
    # --- Step 1: Validate input ---
    if not file_exists(input_path):
        print(f"Error: File '{input_path}' does not exist.")
        return False

    input_path = Path(input_path)

    # Make sure the encrypted_files folder exists
    Path(ENCRYPTED_FOLDER).mkdir(exist_ok=True)

    # --- Step 2: Calculate hash and size BEFORE encrypting ---
    # We hash the ORIGINAL file so we can later confirm the decrypted
    # output matches exactly what was originally encrypted.
    original_hash = calculate_sha256(input_path)
    original_size = get_file_size(input_path)

    # --- Step 3: Load the encryption key ---
    key = load_or_create_key()
    fernet = Fernet(key)

    # --- Step 4: Read original file and encrypt it ---
    try:
        with open(input_path, "rb") as f:
            original_data = f.read()
    except OSError as e:
        print(f"Error: Could not read file. {e}")
        return False

    encrypted_data = fernet.encrypt(original_data)

    # --- Step 5: Save encrypted file with .enc extension ---
    encrypted_filename = input_path.name + ".enc"
    encrypted_path = Path(ENCRYPTED_FOLDER) / encrypted_filename

    try:
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
    except OSError as e:
        print(f"Error: Could not write encrypted file. {e}")
        return False

    # --- Step 6: Save metadata ---
    record = {
        "original_filename": input_path.name,
        "encrypted_filename": encrypted_filename,
        "sha256": original_hash,
        "encryption_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file_size_bytes": original_size,
    }
    metadata.add_file_record(encrypted_filename, record)

    print(f"Success! '{input_path.name}' was encrypted.")
    print(f"Encrypted file saved at: {encrypted_path}")
    return True
