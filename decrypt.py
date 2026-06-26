"""
decrypt.py
----------
Handles decrypting a previously encrypted file, with integrity
verification BEFORE the decrypted result is trusted.

The flow is:
1. Look up the encrypted file's metadata record (original hash, etc.)
2. Read the encrypted bytes from disk
3. Decrypt them using the saved Fernet key
   - Fernet automatically checks an internal authentication tag.
     If the encrypted file was tampered with, decryption will fail here.
4. As an EXTRA layer of integrity verification, calculate the SHA256
   hash of the freshly decrypted data and compare it with the hash
   stored in metadata.json at encryption time.
5. Only write the decrypted file to disk if both checks pass.
"""

from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

from utils import calculate_sha256, file_exists
import metadata

ENCRYPTED_FOLDER = "encrypted_files"
DECRYPTED_FOLDER = "decrypted_files"
KEY_FILE = "secret.key"


def load_key():
    """
    Load the existing encryption key from secret.key.

    Returns:
        bytes or None: the key bytes, or None if the key file is missing.
    """
    key_path = Path(KEY_FILE)

    if not key_path.is_file():
        print("Error: secret.key not found. Cannot decrypt without the original key.")
        return None

    with open(key_path, "rb") as f:
        return f.read()


def decrypt_file(encrypted_filename):
    """
    Decrypt a file that was previously encrypted by this program.

    Args:
        encrypted_filename (str): name of the file inside encrypted_files/
            (e.g. "notes.txt.enc").

    Returns:
        bool: True if decryption succeeded, False otherwise.
    """
    encrypted_path = Path(ENCRYPTED_FOLDER) / encrypted_filename

    # --- Step 1: Validate the encrypted file exists ---
    if not file_exists(encrypted_path):
        print(f"Error: '{encrypted_filename}' not found in '{ENCRYPTED_FOLDER}/'.")
        return False

    # --- Step 2: Look up metadata for this file ---
    record = metadata.get_file_record(encrypted_filename)
    if record is None:
        print("Error: No metadata found for this file. Cannot verify integrity.")
        return False

    expected_hash = record["sha256"]
    original_filename = record["original_filename"]

    # --- Step 3: Load the key and read the encrypted bytes ---
    key = load_key()
    if key is None:
        return False

    fernet = Fernet(key)

    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    # --- Step 4: Attempt decryption ---
    # Fernet itself verifies an authentication tag baked into the
    # encrypted data. If even one byte was changed, this raises
    # InvalidToken and we stop immediately — nothing is trusted or saved.
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        print("Integrity verification failed. File may have been modified.")
        return False

    # --- Step 5: Double-check integrity with SHA256 ---
    # This compares the hash of the decrypted content against the hash
    # we stored back when the file was originally encrypted.
    actual_hash = calculate_sha256_of_bytes(decrypted_data)

    if actual_hash != expected_hash:
        print("Integrity verification failed. File may have been modified.")
        return False

    # --- Step 6: Save the decrypted file ---
    Path(DECRYPTED_FOLDER).mkdir(exist_ok=True)
    output_path = Path(DECRYPTED_FOLDER) / original_filename

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    print("Integrity verified successfully. Hashes match.")
    print(f"File decrypted and saved to: {output_path}")
    return True


def calculate_sha256_of_bytes(data):
    """
    Calculate the SHA256 hash of raw bytes already in memory
    (instead of reading from a file path, like utils.calculate_sha256 does).

    Args:
        data (bytes): the data to hash.

    Returns:
        str: the hex digest of the SHA256 hash.
    """
    import hashlib
    return hashlib.sha256(data).hexdigest()
