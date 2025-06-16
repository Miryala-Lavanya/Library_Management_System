import json
from datetime import datetime, timedelta

DATA_FILE = "library_data.json"

# Load existing data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"books": {}, "issued": {}}

# Save current data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Add a book
def add_book(data):
    book_id = input("Enter Book ID: ")
    title = input("Enter Book Title: ")
    if book_id in data["books"]:
        print("Book ID already exists!")
    else:
        data["books"][book_id] = title
        print("Book added.")

# Remove a book
def remove_book(data):
    book_id = input("Enter Book ID to remove: ")
    if book_id in data["books"]:
        del data["books"][book_id]
        print("Book removed.")
    else:
        print("Book not found.")

# Issue book to student
def issue_book(data):
    book_id = input("Enter Book ID to issue: ")
    student = input("Enter Student Name: ")
    if book_id not in data["books"]:
        print("Book not found.")
    elif book_id in data["issued"]:
        print("Book already issued.")
    else:
        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        data["issued"][book_id] = {"student": student, "issue_date": issue_date, "due_date": due_date}
        print(f"Issued to {student}, due on {due_date}.")

# Return a book and calculate fine
def return_book(data):
    book_id = input("Enter Book ID to return: ")
    if book_id in data["issued"]:
        due_date_str = data["issued"][book_id]["due_date"]
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        today = datetime.now()
        days_late = (today - due_date).days
        fine = 0
        if days_late > 0:
            fine = days_late * 2  # Rs.2 per day
        del data["issued"][book_id]
        print("Book returned.")
        if fine > 0:
            print(f"Late by {days_late} days. Fine: ₹{fine}")
    else:
        print("Book was not issued.")

# Show all books
def show_books(data):
    print("\nAvailable Books:")
    for book_id, title in data["books"].items():
        print(f"{book_id}: {title}")
    print()

# Main Menu
def main():
    data = load_data()
    while True:
        print("\n--- Library Menu ---")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Show Books")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_book(data)
        elif choice == "2":
            remove_book(data)
        elif choice == "3":
            issue_book(data)
        elif choice == "4":
            return_book(data)
        elif choice == "5":
            show_books(data)
        elif choice == "6":
            save_data(data)
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

main()
