import os 
import json
import random
import string
from cryptography.fernet import Fernet
key = None
def create_directory():
    directory_name = "my_new_directory"
    try: 
        os.mkdir(directory_name)
        print(f"Directory {directory_name} created successfully.")
    except FileExistsError:
        print(f"Directory {directory_name} already exists.")

def generate_key():
    """Generates a random encryption key."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)
    return key

def encrypt_password(password, key):
    """Encrypts a password using the provided key."""
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password

def add_password(account, username, password):
    """Adds a new password to the password store."""
    
    # Generate a key if it doesn't exist
    try:
        with open("key.key", "rb") as f:
            key = f.read()
    except FileNotFoundError:
        key = generate_key()

    encrypted_password = encrypt_password(password, key)

    # Load existing passwords from the file (if it exists)
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        passwords = {}

    # Add the new password to the dictionary
    passwords[account] = {"username": username, "password": encrypted_password}

    # Save the updated passwords to the file
    with open("passwords.json", "w") as f:
        json.dump(passwords, f, indent=4)

    print("Password added successfully!") 

def decrypt_password(encrypted_password, key):
    """Decrypts an encrypted password using the provided key.

    Args:
        encrypted_password (bytes): The encrypted password.
        key (bytes): The encryption key.

    Returns:
        str: The decrypted password.
    """

    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password).decode()
    return decrypted_password

def retrieve_password(account):
    """Retrieves a saved password based on the account name.

    Args:
        account (str): The name of the account.

    Returns:
        str: The decrypted password, or None if not found.
    """

    # Load the passwords from the JSON file
    with open("passwords.json", "r") as f:
        passwords = json.load(f)

    # Check if the account exists
    if account in passwords:
        encrypted_password = passwords[account]["password"]
        decrypted_password = decrypt_password(encrypted_password)
        return decrypted_password
    else:
        print("Account not found.")
        return None
    
def delete_password(account):
    """Deletes a saved password based on the account name.

    Args:
        account (str): The name of the account to delete.
    """

    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)

        if account in passwords:
            del passwords[account]

            with open("passwords.json", "w") as f:
                json.dump(passwords, f, indent=4)

            print(f"Password for '{account}' deleted successfully.")
        else:
            print("Account not found.")
    except FileNotFoundError:
        print("Password file not found.")

def generate_password(length=12, include_special_chars=True):
    """Generates a strong random password.

    Args:
        length (int): The desired length of the password.
        include_special_chars (bool): Whether to include special characters.

    Returns:
        str: The generated password.
    """

    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters)for _ in range(length))
    return password


def assess_password_strength(password):
    """Assesses the strength of a password based on length and complexity.

    Args:
        password (str): The password to evaluate.

    Returns:
        int: A strength score (0-3).
    """
    strength = 0

    if len(password) >= 8:
        strength += 1

    if any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password) and any(not c.isalnum() for c in password):
        strength += 2

    return strength

def view_passwords(master_password):
    """Views all saved passwords after authentication.

    Args:
        master_password (str): The user's master password.
    """

    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)

        # Decrypt the stored master password
        encrypted_master_password = passwords["master_password"]
        decrypted_master_password = decrypt_password(encrypted_master_password)

        # Verify the master password
        if decrypted_master_password == master_password:
            print("Saved Passwords:")
            for account, data in passwords.items():
                if account != "master_password":  # Skip the master password itself
                    print(f"Account: {account}")
                    print(f"Username: {data['username']}")
                    decrypted_password = decrypt_password(data['password'])
                    print(f"Password: {decrypted_password}")
        else:
            print("Incorrect master password.")
    except FileNotFoundError:
        print("Password file not found.")


def main():
    while True:
        print("Password Manager")
        print("1. Add password")
        print("2. Retrieve password")
        print("3. Delete password")
        print("4. View saved passwords")
        print("5. Generate password")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # ... (call add_password function)
        elif choice == "2":
            # ... (call retrieve_password function)
        elif choice == "3":
            # ... (call delete_password function)
        elif choice == "4":
            # ... (call view_passwords function)
        elif choice == "5":
            # ... (call generate_password function)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()