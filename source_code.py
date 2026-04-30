import json
import csv
import os
import re
from datetime import datetime

DATA_FILE = "contacts.json"
CSV_FILE = "contacts_export.csv"

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

# ---------------- Validation ---------------- #
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_phone(phone):
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, phone)


# ---------------- Core Features ---------------- #
def generate_id(contacts):
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1

def add_contact(contacts):
    print("\n--- Add Contact ---")
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

    contact = {
        "id": generate_id(contacts),
        "name": name,
        "phone": phone,
        "email": email,
        "city": city,
        "company": company,
        "favorite": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully.")

def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    print("\n--- Contact List ---")
    print(f"{'ID':<5}{'Name':<20}{'Phone':<18}{'Email':<25}{'City':<15}{'Company':<20}{'Fav':<5}")
    print("-" * 110)

    for c in contacts:
        print(f"{c['id']:<5}{c['name']:<20}{c['phone']:<18}{c['email']:<25}{c['city']:<15}{c['company']:<20}{str(c['favorite']):<5}")

def search_contacts(contacts):
    keyword = input("Enter name, phone, or email to search: ").lower()
    results = [c for c in contacts if keyword in c['name'].lower() or keyword in c['phone'] or keyword in c['email'].lower()]

    if results:
        view_contacts(results)
    else:
        print("No matching contacts found.")

def filter_contacts(contacts):
    choice = input("Filter by (1) City or (2) Company: ")
    keyword = input("Enter filter keyword: ").lower()

    if choice == "1":
        results = [c for c in contacts if keyword in c['city'].lower()]
    elif choice == "2":
        results = [c for c in contacts if keyword in c['company'].lower()]
    else:
        print("Invalid option.")
        return

    if results:
        view_contacts(results)
    else:
        print("No contacts match this filter.")

def update_contact(contacts):
    try:
        cid = int(input("Enter contact ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    for c in contacts:
        if c['id'] == cid:
            print("Leave blank to keep existing value.")
            c['name'] = input(f"Name ({c['name']}): ") or c['name']
            c['phone'] = input(f"Phone ({c['phone']}): ") or c['phone']
            c['email'] = input(f"Email ({c['email']}): ") or c['email']
            c['city'] = input(f"City ({c['city']}): ") or c['city']
            c['company'] = input(f"Company ({c['company']}): ") or c['company']
            save_contacts(contacts)
            print("Contact updated.")
            return

    print("Contact not found.")

def delete_contact(contacts):
    identifier = input("Enter contact ID or Name to delete: ")

    for c in contacts:
        if str(c['id']) == identifier or c['name'].lower() == identifier.lower():
            contacts.remove(c)
            save_contacts(contacts)
            print("Contact deleted.")
            return

    print("Contact not found.")

def toggle_favorite(contacts):
    try:
        cid = int(input("Enter contact ID to star/unstar: "))
    except ValueError:
        print("Invalid ID.")
        return

    for c in contacts:
        if c['id'] == cid:
            c['favorite'] = not c['favorite']
            save_contacts(contacts)
            print("Favorite status updated.")
            return

    print("Contact not found.")

def export_csv(contacts):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=contacts[0].keys())
        writer.writeheader()
        writer.writerows(contacts)
    print(f"Contacts exported to {CSV_FILE}")

def sort_contacts(contacts):
    contacts.sort(key=lambda x: x['name'].lower())
    print("Contacts sorted A-Z.")
    view_contacts(contacts)

# ---------------- CLI Menu ---------------- #
def menu():
    contacts = load_contacts()

    while True:
        print("\n===== Contact Management System =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contacts")
        print("4. Filter Contacts")
        print("5. Update Contact")
        print("6. Delete Contact")
        print("7. Star/Unstar Contact")
        print("8. Export to CSV")
        print("9. Sort Contacts")
        print("0. Exit")

        choice = input("Enter your choice: ")

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
                if contacts:
                    export_csv(contacts)
                else:
                    print("No contacts to export.")
            elif choice == "9":
                sort_contacts(contacts)
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    menu()
