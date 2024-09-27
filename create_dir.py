import os
import json
import random
import string
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)
    return key

def encrypt_password(password, key):
    cipher = Fernet(key)
    return cipher.encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password).decode()

def create_directory(directory_name="my_new_directory"):
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        pass

def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f, indent=4)

def add_password():
    account = input("Enter the account name: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    try:
        key = open("key.key", "rb").read()
    except FileNotFoundError:
        key = generate_key()

    encrypted_password = encrypt_password(password, key)
    passwords = load_passwords()
    passwords[account] = {"username": username, "password": encrypted_password}
    save_passwords(passwords)

def retrieve_password():
    account = input("Enter the account name: ")
    passwords = load_passwords()
    if account in passwords:
        encrypted_password = passwords[account]["password"]
        try:
            key = open("key.key", "rb").read()
            return decrypt_password(encrypted_password, key)
        except FileNotFoundError:
            print("Error: Encryption key not found.")
            return None
    else:
        print("Account not found.")
        return None

def delete_password():
    account = input("Enter the account name to delete: ")
    passwords = load_passwords()
    if account in passwords:
        del passwords[account]
        save_passwords(passwords)
        print(f"Password for '{account}' deleted successfully.")
    else:
        print("Account not found.")

def generate_password(length=12, include_special_chars=True):
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def assess_password_strength(password):
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password) and any(not c.isalnum() for c in password):   

        strength += 2
    return strength

def view_passwords(master_password):
    passwords = load_passwords()
    try:
        encrypted_master_password = passwords["master_password"]
        decrypted_master_password = decrypt_password(encrypted_master_password, open("key.key", "rb").read())
    except (FileNotFoundError, KeyError):
        print("Error: Password file or master password not found.")
        return

    if decrypted_master_password == master_password:
        print("Saved Passwords:")
        for account, data in passwords.items():
            if account != "master_password":
                decrypted_password = decrypt_password(data['password'], open("key.key", "rb").read())
                print(f"Account: {account}")
                print(f"Username: {data['username']}")
                print(f"Password: {decrypted_password}")

def main():
    while True:
        print("Hello this is a password manager app menu driven program")
        print("select any on of the below options")
        print("Password Manager")
        print("1. Add password")
        print("2. Retrieve password")
        print("3. Delete password")
        print("4. View saved passwords")
        print("5. Generate password")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            retrieve_password()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            master_password = input("Enter master password: ")
            view_passwords(master_password)
        elif choice == "5":
            password = generate_password()
            print(f"Generated password: {password}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
