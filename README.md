# Secure File Storage System

A simple, local command-line tool written in Python that encrypts and decrypts files using **AES-256** (via the `cryptography` library's `Fernet` recipe), with **SHA-256 integrity verification** to detect tampering before any file is decrypted.

Built as a beginner-friendly, interview-ready project — no databases, no web framework, no cloud services. Everything runs locally from the terminal.

---

## Overview

This project lets you:

- Encrypt any local file and store it safely as a `.enc` file.
- Decrypt it back to its original form whenever you need it.
- Automatically verify that an encrypted file hasn't been tampered with **before** trusting the decrypted output.
- Keep a simple, human-readable log (`metadata.json`) of everything you've encrypted — including hashes, timestamps, and file sizes.

It's a great hands-on way to learn how symmetric encryption, key management, and integrity verification work together in a real (if small-scale) system.

---

## Features

- **AES-256 encryption** of any file, via the `cryptography` library's `Fernet` implementation
- **Decryption** of previously encrypted files
- **SHA-256 integrity verification** before every decryption
- **Tamper detection** — if a `.enc` file has been modified, decryption is refused with a clear error message
- **Metadata tracking** in `metadata.json` (original filename, encrypted filename, hash, encryption time, file size)
- **Simple CLI menu** — no need to remember command-line flags
- **Modular, well-commented code** that's easy to read and explain in an interview
- **Automatic key generation** — a `secret.key` file is created on first use

---

## Technologies Used

- **Python 3**
- [`cryptography`](https://pypi.org/project/cryptography/) — for Fernet (AES-256) encryption
- `hashlib` — for SHA-256 hashing
- `pathlib` — for clean, cross-platform file path handling
- `json` — for metadata storage
- `os`, `datetime` — for file operations and timestamps

---

## Folder Structure

```
Secure-File-Storage-System/
│
├── main.py              # CLI entry point and menu logic
├── encrypt.py            # Encryption logic
├── decrypt.py             # Decryption + integrity verification logic
├── metadata.py             # Reading/writing metadata.json
├── utils.py                 # Shared helper functions (hashing, file checks)
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── metadata.json            # Auto-generated metadata log
│
├── encrypted_files/          # Encrypted (.enc) files are stored here
├── sample_files/              # Sample file for testing
└── screenshots/                 # CLI screenshots for documentation
```

> **Note:** `secret.key` (your encryption key) and `decrypted_files/` are generated the first time you run the program. Both are excluded from version control via `.gitignore` — never commit your `secret.key` to a public repository.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Secure-File-Storage-System.git
   cd Secure-File-Storage-System
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the program:

```bash
python main.py
```

You'll see a menu like this:

```
--------------------------------------------------
SECURE FILE STORAGE SYSTEM
--------------------------------------------------
1. Encrypt File
2. Decrypt File
3. View Stored Files
4. View Metadata
5. Exit
--------------------------------------------------
```

### Example: encrypting the sample file

1. Choose option `1`
2. Enter: `sample_files/sample.txt`
3. The encrypted file is saved to `encrypted_files/sample.txt.enc`

### Example: decrypting it back

1. Choose option `2`
2. Enter: `sample.txt.enc`
3. If the file wasn't tampered with, it's decrypted into `decrypted_files/sample.txt`

### What happens if a file is tampered with?

If anyone modifies the contents of a `.enc` file directly, the next decryption attempt will stop and print:

```
Integrity verification failed. File may have been modified.
```

No partial or corrupted output is ever written to disk.

---

## How Integrity Verification Works

1. When a file is encrypted, its **SHA-256 hash** is calculated and saved in `metadata.json`.
2. Fernet encryption itself includes a built-in authentication check — if the encrypted bytes are altered in any way, decryption fails immediately.
3. As a second layer of defense, after decryption succeeds, the program re-hashes the decrypted data and compares it against the hash stored at encryption time.
4. The file is only written to `decrypted_files/` if **both** checks pass.

This "defense in depth" approach means a single point of failure can't silently corrupt your data.

---

## Screenshots

> Add screenshots of the CLI in action here, for example:
> - Encrypting a file
> - Decrypting a file successfully
> - The tamper-detection error message

(See the `screenshots/` folder.)

---

## Future Improvements

- Password-protected encryption key (derive the key from a user password instead of storing it in plaintext)
- A simple PyQt5 GUI as an alternative to the CLI
- Multiple user support, with separate keys per user
- Search/filter encrypted files by name or date
- Export metadata to CSV for reporting

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Built as an educational/internship project to demonstrate practical, beginner-friendly application of AES-256 encryption, SHA-256 integrity verification, and clean Python project structure.

Feel free to fork, study, and build on it!
