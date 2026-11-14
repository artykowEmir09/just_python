import json

FILE_NAME = "contacts.json"


def load_contacts():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_contacts(contacts):
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)


def add_contact(contacts):
    print("\n--- Add Contact ---")

    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")

    contact = {
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)

    print("Contact added successfully!")


def view_contacts(contacts):
    print("\n--- Contact List ---")

    if not contacts:
        print("No contacts found.")
        return

    for i, contact in enumerate(contacts, start=1):
        print(f"\n{i}. {contact['name']}")
        print(f"   Phone: {contact['phone']}")
        print(f"   Email: {contact['email']}")


def search_contact(contacts):
    print("\n--- Search Contact ---")

    keyword = input("Enter name or phone: ").lower()

    found = False

    for contact in contacts:
        if (
            keyword in contact["name"].lower()
            or keyword in contact["phone"].lower()
        ):
            print("\nContact found:")
            print(f"Name: {contact['name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
            found = True

    if not found:
        print("No contact found.")


def edit_contact(contacts):
    print("\n--- Edit Contact ---")

    if not contacts:
        print("No contacts found.")
        return

    view_contacts(contacts)

    try:
        number = int(input("\nEnter contact number to edit: "))

        if number < 1 or number > len(contacts):
            print("Invalid contact number.")
            return

        contact = contacts[number - 1]

        print("\nPress Enter to keep the current value.")

        new_name = input(f"Name [{contact['name']}]: ")
        new_phone = input(f"Phone [{contact['phone']}]: ")
        new_email = input(f"Email [{contact['email']}]: ")

        if new_name:
            contact["name"] = new_name

        if new_phone:
            contact["phone"] = new_phone

        if new_email:
            contact["email"] = new_email

        save_contacts(contacts)

        print("Contact updated successfully!")

    except ValueError:
        print("Please enter a valid number.")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")

    if not contacts:
        print("No contacts found.")
        return

    view_contacts(contacts)

    try:
        number = int(input("\nEnter contact number to delete: "))

        if number < 1 or number > len(contacts):
            print("Invalid contact number.")
            return

        deleted = contacts.pop(number - 1)

        save_contacts(contacts)

        print(f"{deleted['name']} has been deleted.")

    except ValueError:
        print("Please enter a valid number.")


def main():
    contacts = load_contacts()

    while True:
        print("\n" + "=" * 40)
        print("           CONTACT BOOK")
        print("=" * 40)
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("=" * 40)

        choice = input("Choose an option: ")

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            view_contacts(contacts)

        elif choice == "3":
            search_contact(contacts)

        elif choice == "4":
            edit_contact(contacts)

        elif choice == "5":
            delete_contact(contacts)

        elif choice == "6":
            print("\nGoodbye! 👋")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()