"""
password-manager.py
A terminal-based password manager with real encryption at rest.

Your saved passwords are encrypted using a key derived from a master
password you choose (via PBKDF2 + Fernet/AES). Nothing is stored in
plain text on disk — not even your master password (only a salted
hash-derived key is used to unlock the vault each time).

Requires: cryptography
    pip install cryptography --break-system-packages
"""

import sys
import os
import json
import base64
import secrets
import string
import getpass

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("This tool requires the 'cryptography' package. Install it with:")
    print("    pip install cryptography --break-system-packages")
    sys.exit(1)

VAULT_FILE = "vault.enc"
SALT_FILE = "vault.salt"
PBKDF2_ITERATIONS = 480_000

def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    key_bytes = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key_bytes)

def load_or_create_salt():
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = secrets.token_bytes(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def load_vault(fernet):
    if not os.path.exists(VAULT_FILE):
        return {}

    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)
    except InvalidToken:
        print("\n Incorrect master password, or the vault file is corrupted.")
        sys.exit(1)

def save_vault(fernet, vault):
    data = json.dumps(vault).encode()
    encrypted_data = fernet.encrypt(data)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)

def unlock_vault():
    salt = load_or_create_salt()
    is_new_vault = not os.path.exists(VAULT_FILE)

    if is_new_vault:
        print("No vault found — let's create one.")
        while True:
            pw1 = getpass.getpass("Choose a master password: ")
            pw2 = getpass.getpass("Confirm master password: ")
            if pw1 != pw2:
                print("Passwords don't match. Try again.")
                continue
            if len(pw1) < 8:
                print("Use at least 8 characters for your master password.")
                continue
            master_password = pw1
            break
    else:
        master_password = getpass.getpass("Enter your master password: ")

    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    if is_new_vault:
        save_vault(fernet, {})

    vault = load_vault(fernet)
    return fernet, vault

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))

def add_entry(vault, fernet):
    print("\n--- Add New Entry ---")
    service = input("Service/site name: ").strip()
    if not service:
        print("Cancelled.")
        return

    username = input("Username/email: ").strip()

    use_generated = input("Generate a strong random password? (y/n): ").strip().lower()
    if use_generated == "y":
        length_input = input("Length (default 16): ").strip()
        length = int(length_input) if length_input.isdigit() else 16
        password = generate_password(length)
        print(f"Generated password: {password}")
    else:
        password = getpass.getpass("Password: ")

    vault[service] = {"username": username, "password": password}
    save_vault(fernet, vault)
    print(f"Saved entry for '{service}'.")

def view_entry(vault):
    print("\n--- View Entry ---")
    if not vault:
        print("Vault is empty.")
        return

    service = input("Service/site name: ").strip()
    entry = vault.get(service)

    if entry is None:
        print(f"No entry found for '{service}'.")
        return

    print(f"\nService:  {service}")
    print(f"Username: {entry['username']}")
    print(f"Password: {entry['password']}")

def list_services(vault):
    print("\n--- Saved Services ---")
    if not vault:
        print("Vault is empty.")
        return
    for service in sorted(vault.keys()):
        print(f"  - {service}")

def delete_entry(vault, fernet):
    print("\n--- Delete Entry ---")
    if not vault:
        print("Vault is empty.")
        return

    service = input("Service/site name to delete: ").strip()
    if service not in vault:
        print(f"No entry found for '{service}'.")
        return

    confirm = input(f"Delete the entry for '{service}'? (y/n): ").strip().lower()
    if confirm == "y":
        del vault[service]
        save_vault(fernet, vault)
        print("Deleted.")
    else:
        print("Cancelled.")

MENU = """
==========================
      PASSWORD MANAGER
==========================
1. Add a new entry
2. View an entry
3. List all saved services
4. Delete an entry
5. Generate a random password (without saving)
6. Exit
"""

def main():
    print("=" * 26)
    print("  ENCRYPTED PASSWORD VAULT")
    print("=" * 26)

    fernet, vault = unlock_vault()
    print("\n🔓 Vault unlocked.")

    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_entry(vault, fernet)
        elif choice == "2":
            view_entry(vault)
        elif choice == "3":
            list_services(vault)
        elif choice == "4":
            delete_entry(vault, fernet)
        elif choice == "5":
            length_input = input("Length (default 16): ").strip()
            length = int(length_input) if length_input.isdigit() else 16
            print(f"Generated password: {generate_password(length)}")
        elif choice == "6":
            print("Vault locked. Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()