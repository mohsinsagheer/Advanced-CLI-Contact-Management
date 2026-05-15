import json
import csv
import os
import re
from datetime import datetime
from math import ceil

# ================= CONFIG ================= #
DATA_FILE = "contacts.json"
CSV_FILE = "contacts_export.csv"
PAGE_SIZE = 5

# ================= FILE HANDLING ================= #
def load_contacts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


def save_contacts(contacts):
    with open(DATA_FILE, "w") as file:
        json.dump(contacts, file, indent=4)


# ================= VALIDATION ================= #
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def validate_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone)


# ================= UTILITIES ================= #
def generate_id(contacts):
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1


def truncate(text, length=18):
    if len(str(text)) > length:
        return str(text)[:length - 3] + "..."
    return str(text)


def contact_exists(contacts, phone, email):
    for c in contacts:
        if c["phone"] == phone:
            print("Error: Phone number already exists.")
            return True

        if c["email"].lower() == email.lower():
            print("Error: Email already exists.")
            return True

    return False


# ================= CORE FEATURES ================= #
def add_contact(contacts):
    print("\n========== ADD CONTACT ==========")

    name = input("Full Name: ").strip()
    phone = input("Phone Number: ").strip()
    email = input("Email Address: ").strip()
    city = input("City: ").strip()
    company = input("Company: ").strip()

    if not all([name, phone, email, city, company]):
        print("Error: All fields are required.")
        return

    if not validate_email(email):
        print("Error: Invalid email format.")
        return

    if not validate_phone(phone):
        print("Error: Invalid phone number.")
        return

    if contact_exists(contacts, phone, email):
        return

    contact = {
        "id": generate_id(contacts),
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "company": company,
        "favorite": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": None
    }

    contacts.append(contact)
    save_contacts(contacts)

    print("Contact added successfully.")


# ================= DISPLAY ================= #
def display_table(data):
    print("-" * 120)

    print(
        f"{'ID':<5}"
        f"{'Name':<20}"
        f"{'Phone':<18}"
        f"{'Email':<25}"
        f"{'City':<15}"
        f"{'Company':<20}"
        f"{'Fav':<5}"
    )

    print("-" * 120)

    for c in data:
        print(
            f"{c['id']:<5}"
            f"{truncate(c['name'], 20):<20}"
            f"{truncate(c['phone'], 18):<18}"
            f"{truncate(c['email'], 25):<25}"
            f"{truncate(c['city'], 15):<15}"
            f"{truncate(c['company'], 20):<20}"
            f"{'★' if c['favorite'] else '':<5}"
        )

    print("-" * 120)


def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    total_pages = ceil(len(contacts) / PAGE_SIZE)
    current_page = 1

    while True:
        start = (current_page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE

        page_data = contacts[start:end]

        print(f"\n========== CONTACT LIST (Page {current_page}/{total_pages}) ==========")

        display_table(page_data)

        print("N = Next Page | P = Previous Page | Q = Quit")

        choice = input("Choice: ").lower()

        if choice == "n":
            if current_page < total_pages:
                current_page += 1
            else:
                print("Already on last page.")

        elif choice == "p":
            if current_page > 1:
                current_page -= 1
            else:
                print("Already on first page.")

        elif choice == "q":
            break

        else:
            print("Invalid option.")


# ================= SEARCH ================= #
def search_contacts(contacts):
    keyword = input("Enter name, phone, or email to search: ").lower()

    results = [
        c for c in contacts
        if keyword in c['name'].lower()
        or keyword in c['phone']
        or keyword in c['email'].lower()
    ]

    if results:
        display_table(results)
    else:
        print("No matching contacts found.")


# ================= FILTER ================= #
def filter_contacts(contacts):
    print("\n1. Filter by City")
    print("2. Filter by Company")
    print("3. Show Favorites")

    choice = input("Choose option: ")

    if choice == "1":
        keyword = input("Enter city: ").lower()

        results = [
            c for c in contacts
            if keyword in c['city'].lower()
        ]

    elif choice == "2":
        keyword = input("Enter company: ").lower()

        results = [
            c for c in contacts
            if keyword in c['company'].lower()
        ]

    elif choice == "3":
        results = [
            c for c in contacts
            if c['favorite']
        ]

    else:
        print("Invalid option.")
        return

    if results:
        display_table(results)
    else:
        print("No matching contacts found.")


# ================= UPDATE ================= #
def update_contact(contacts):
    try:
        cid = int(input("Enter contact ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    for c in contacts:
        if c['id'] == cid:

            print("Leave blank to keep existing values.")

            new_name = input(f"Name ({c['name']}): ").strip() or c['name']
            new_phone = input(f"Phone ({c['phone']}): ").strip() or c['phone']
            new_email = input(f"Email ({c['email']}): ").strip() or c['email']
            new_city = input(f"City ({c['city']}): ").strip() or c['city']
            new_company = input(f"Company ({c['company']}): ").strip() or c['company']

            if not validate_email(new_email):
                print("Invalid email format.")
                return

            if not validate_phone(new_phone):
                print("Invalid phone number.")
                return

            for other in contacts:
                if other['id'] != cid:
                    if other['phone'] == new_phone:
                        print("Phone number already exists.")
                        return

                    if other['email'].lower() == new_email.lower():
                        print("Email already exists.")
                        return

            c['name'] = new_name
            c['phone'] = new_phone
            c['email'] = new_email
            c['city'] = new_city
            c['company'] = new_company
            c['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            save_contacts(contacts)

            print("Contact updated successfully.")
            return

    print("Contact not found.")


# ================= DELETE ================= #
def delete_contact(contacts):
    identifier = input("Enter Contact ID or Name to delete: ")

    for c in contacts:
        if str(c['id']) == identifier or c['name'].lower() == identifier.lower():

            confirm = input(
                f"Are you sure you want to delete {c['name']}? (y/n): "
            ).lower()

            if confirm == "y":
                contacts.remove(c)
                save_contacts(contacts)
                print("Contact deleted successfully.")
            else:
                print("Deletion cancelled.")

            return

    print("Contact not found.")


# ================= FAVORITE ================= #
def toggle_favorite(contacts):
    try:
        cid = int(input("Enter contact ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for c in contacts:
        if c['id'] == cid:

            c['favorite'] = not c['favorite']

            save_contacts(contacts)

            status = "favorited" if c['favorite'] else "removed from favorites"

            print(f"Contact {status}.")
            return

    print("Contact not found.")


# ================= SORT ================= #
def sort_contacts(contacts):
    print("\n1. Sort by Name")
    print("2. Sort by City")
    print("3. Sort by Company")

    choice = input("Choose option: ")

    if choice == "1":
        contacts.sort(key=lambda x: x['name'].lower())

    elif choice == "2":
        contacts.sort(key=lambda x: x['city'].lower())

    elif choice == "3":
        contacts.sort(key=lambda x: x['company'].lower())

    else:
        print("Invalid option.")
        return

    print("Contacts sorted successfully.")
    display_table(contacts)


# ================= EXPORT ================= #
def export_csv(contacts):
    if not contacts:
        print("No contacts available to export.")
        return

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=contacts[0].keys()
        )

        writer.writeheader()
        writer.writerows(contacts)

    print(f"Contacts exported successfully to '{CSV_FILE}'")


# ================= STATS ================= #
def show_statistics(contacts):
    total = len(contacts)

    favorites = len([
        c for c in contacts
        if c['favorite']
    ])

    cities = set([
        c['city']
        for c in contacts
    ])

    companies = set([
        c['company']
        for c in contacts
    ])

    print("\n========== STATISTICS ==========")

    print(f"Total Contacts   : {total}")
    print(f"Favorite Contacts: {favorites}")
    print(f"Unique Cities    : {len(cities)}")
    print(f"Unique Companies : {len(companies)}")


# ================= MAIN MENU ================= #
def menu():
    contacts = load_contacts()

    while True:

        print("\n")
        print("=" * 45)
        print("     CONTACT MANAGEMENT SYSTEM")
        print("=" * 45)

        print("1.  Add Contact")
        print("2.  View Contacts")
        print("3.  Search Contacts")
        print("4.  Filter Contacts")
        print("5.  Update Contact")
        print("6.  Delete Contact")
        print("7.  Star / Unstar Contact")
        print("8.  Export to CSV")
        print("9.  Sort Contacts")
        print("10. Show Statistics")
        print("0.  Exit")

        choice = input("\nEnter your choice: ")

        try:
            if choice == "1":
                add_contact(contacts)

            elif choice == "2":
                view_contacts(contacts)

            elif choice == "3":
                search_contacts(contacts)

            elif choice == "4":
                filter_contacts(contacts)

            elif choice == "5":
                update_contact(contacts)

            elif choice == "6":
                delete_contact(contacts)

            elif choice == "7":
                toggle_favorite(contacts)

            elif choice == "8":
                export_csv(contacts)

            elif choice == "9":
                sort_contacts(contacts)

            elif choice == "10":
                show_statistics(contacts)

            elif choice == "0":
                print("Goodbye.")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"An error occurred: {e}")


# ================= ENTRY POINT ================= #
if __name__ == "__main__":
    menu()