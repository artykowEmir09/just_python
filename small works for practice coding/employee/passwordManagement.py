import json
import os
import random
import string
import getpass

FILE_NAME = "passwords.json"
MASTER_FILE = "master.json"


def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def setup_master_password():
    data = load_data(MASTER_FILE)

    if "password" not in data:
        print("\nNo master password found.")
        print("Create your master password.")

        password = getpass.getpass("New master password: ")
        confirm = getpass.getpass("Confirm password: ")

        if password != confirm:
            print("Passwords do not match.")
            return False

        if len(password) < 6:
            print("Password must be at least 6 characters.")
            return False

        save_data(MASTER_FILE, {"password": password})

        print("Master password created successfully!")
        return True

    return True


def login():
    data = load_data(MASTER_FILE)

    print("\n=========================")
    print("      PASSWORD MANAGER")
    print("=========================")

    for attempt in range(3):
        password = getpass.getpass("Master password: ")

        if password == data["password"]:
            print("Login successful!")
            return True

        print("Incorrect password.")

    print("Too many failed attempts.")
    return False


def add_password(passwords):
    print("\n--- Add Password ---")

    website = input("Website: ").strip()
    username = input("Username/Email: ").strip()

    if not website or not username:
        print("Website and username cannot be empty.")
        return

    password = getpass.getpass("Password: ")

    if website in passwords:
        print("An account for this website already exists.")
        return

    passwords[website] = {
        "username": username,
        "password": password
    }

    save_data(FILE_NAME, passwords)

    print("Password saved successfully!")


def view_passwords(passwords):
    print("\n--- Saved Accounts ---")

    if not passwords:
        print("No passwords saved.")
        return

    for number, (website, account) in enumerate(passwords.items(), 1):
        print(f"\n{number}. {website}")
        print(f"   Username: {account['username']}")
        print(f"   Password: {account['password']}")


def search_account(passwords):
    print("\n--- Search Account ---")

    keyword = input("Enter website: ").lower().strip()

    found = False

    for website, account in passwords.items():
        if keyword in website.lower():
            print(f"\nWebsite: {website}")
            print(f"Username: {account['username']}")
            print(f"Password: {account['password']}")
            found = True

    if not found:
        print("No matching account found.")


def generate_password():
    print("\n--- Password Generator ---")

    try:
        length = int(input("Password length: "))
    except ValueError:
        print("Please enter a number.")
        return

    if length < 8:
        print("Password should be at least 8 characters.")
        return

    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    password = "".join(
        random.choice(characters)
        for _ in range(length)
    )

    print("\nGenerated password:")
    print(password)

    return password


def update_password(passwords):
    print("\n--- Update Password ---")

    website = input("Website: ").strip()

    if website not in passwords:
        print("Account not found.")
        return

    print(f"Account found: {website}")
    print(f"Username: {passwords[website]['username']}")

    new_password = getpass.getpass("New password: ")

    if not new_password:
        print("Password cannot be empty.")
        return

    passwords[website]["password"] = new_password

    save_data(FILE_NAME, passwords)

    print("Password updated successfully!")


def delete_password(passwords):
    print("\n--- Delete Account ---")

    website = input("Website: ").strip()

    if website not in passwords:
        print("Account not found.")
        return

    confirm = input(
        f"Are you sure you want to delete {website}? (y/n): "
    ).lower()

    if confirm == "y":
        del passwords[website]
        save_data(FILE_NAME, passwords)
        print("Account deleted successfully!")
    else:
        print("Deletion cancelled.")


def change_master_password():
    print("\n--- Change Master Password ---")

    data = load_data(MASTER_FILE)

    current = getpass.getpass("Current master password: ")

    if current != data["password"]:
        print("Incorrect master password.")
        return

    new_password = getpass.getpass("New master password: ")
    confirm = getpass.getpass("Confirm new password: ")

    if new_password != confirm:
        print("Passwords do not match.")
        return

    if len(new_password) < 6:
        print("Password must be at least 6 characters.")
        return

    data["password"] = new_password

    save_data(MASTER_FILE, data)

    print("Master password changed successfully!")


def main():
    if not setup_master_password():
        return

    if not login():
        return

    passwords = load_data(FILE_NAME)

    while True:

        print("\n=========================")
        print("      PASSWORD MANAGER")
        print("=========================")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Search Account")
        print("4. Generate Password")
        print("5. Update Password")
        print("6. Delete Account")
        print("7. Change Master Password")
        print("8. Exit")
        print("=========================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_password(passwords)

        elif choice == "2":
            view_passwords(passwords)

        elif choice == "3":
            search_account(passwords)

        elif choice == "4":
            generate_password()

        elif choice == "5":
            update_password(passwords)

        elif choice == "6":
            delete_password(passwords)

        elif choice == "7":
            change_master_password()

        elif choice == "8":
            print("Exiting Password Manager...")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()