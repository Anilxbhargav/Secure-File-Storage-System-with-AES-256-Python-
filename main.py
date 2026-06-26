"""
main.py
-------
Entry point for the Secure File Storage System.

Run this file to start the CLI:
    python main.py

This file only handles the menu and user interaction.
The actual logic lives in encrypt.py, decrypt.py, metadata.py, and utils.py.
"""

from pathlib import Path

import encrypt
import decrypt
import metadata
from utils import print_separator

ENCRYPTED_FOLDER = "encrypted_files"


def show_menu():
    """Print the main menu options."""
    print_separator()
    print("SECURE FILE STORAGE SYSTEM")
    print_separator()
    print("1. Encrypt File")
    print("2. Decrypt File")
    print("3. View Stored Files")
    print("4. View Metadata")
    print("5. Exit")
    print_separator()


def handle_encrypt():
    """Ask the user for a file path and encrypt it."""
    file_path = input("Enter the path of the file to encrypt: ").strip()

    if not file_path:
        print("Error: No file path entered.")
        return

    encrypt.encrypt_file(file_path)


def handle_decrypt():
    """Show available encrypted files and decrypt the chosen one."""
    encrypted_folder = Path(ENCRYPTED_FOLDER)

    if not encrypted_folder.is_dir() or not any(encrypted_folder.glob("*.enc")):
        print("No encrypted files found yet. Encrypt a file first.")
        return

    print("\nAvailable encrypted files:")
    files = sorted(f.name for f in encrypted_folder.iterdir() if f.is_file() and f.suffix == ".enc")
    for i, name in enumerate(files, start=1):
        print(f"  {i}. {name}")

    choice = input("\nEnter the filename to decrypt (e.g. notes.txt.enc): ").strip()

    if not choice:
        print("Error: No filename entered.")
        return

    decrypt.decrypt_file(choice)


def handle_view_stored_files():
    """List all files currently stored in encrypted_files/."""
    encrypted_folder = Path(ENCRYPTED_FOLDER)

    if not encrypted_folder.is_dir() or not any(encrypted_folder.glob("*.enc")):
        print("No encrypted files found yet.")
        return

    print("\nFiles in encrypted_files/:")
    for f in sorted(encrypted_folder.glob("*.enc")):
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.2f} KB)")


def handle_view_metadata():
    """Print all stored metadata records in a readable format."""
    records = metadata.list_all_records()

    if not records:
        print("No metadata found yet. Encrypt a file first.")
        return

    print("\nStored Metadata:")
    for encrypted_filename, record in records.items():
        print_separator()
        print(f"Encrypted filename : {record.get('encrypted_filename')}")
        print(f"Original filename  : {record.get('original_filename')}")
        print(f"SHA256 hash        : {record.get('sha256')}")
        print(f"Encryption time    : {record.get('encryption_time')}")
        print(f"File size (bytes)  : {record.get('file_size_bytes')}")
    print_separator()


def main():
    """Main loop: show the menu and respond to user choices."""
    print("Welcome to the Secure File Storage System!")

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            handle_encrypt()
        elif choice == "2":
            handle_decrypt()
        elif choice == "3":
            handle_view_stored_files()
        elif choice == "4":
            handle_view_metadata()
        elif choice == "5":
            print("Goodbye! Stay secure.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
