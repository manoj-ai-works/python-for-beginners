"""
main.py — CLI entry point for the Contact Book app.

CONCEPTS COVERED:
  - Classes with methods
  - @decorator usage
  - while loop for the menu
  - if/elif/else control flow
  - try/except for error handling
  - List comprehension for tag parsing
  - Generator expression inside next()
"""

# Import our own modules — Python looks in the same folder first
from models import Contact, Email, Phone
from validators import ValidationError, DuplicateContactError, ContactNotFoundError
from storage import save_contacts, load_contacts
from utils import search_contacts, sort_contacts, get_all_tags, log_action


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT BOOK CLASS
# Holds all contacts in memory (_contacts list) and provides methods
# to add, remove, search, and display them.
# ─────────────────────────────────────────────────────────────────────────────

class ContactBook:
    """Main application class — wraps the contact list with business logic."""

    def __init__(self):
        # Load existing contacts from the JSON file when the app starts
        self._contacts: list[Contact] = load_contacts()

    # ── CRUD methods ──────────────────────────────────────────────────────────

    @log_action   # this decorator will print how long add() takes
    def add(self, name: str, email: str, phone: str, tags: list = None):
        """Create and store a new contact. Raises error if email already exists."""
        # Build the Contact — validation happens inside Email, Phone, and Contact
        new_contact = Contact(
            name=name,
            email=Email(email),
            phone=Phone(phone),
            tags=tags or [],   # 'or []' handles the case where tags=None
        )
        # __eq__ on Contact compares by email, so 'in' checks for duplicate email
        if new_contact in self._contacts:
            raise DuplicateContactError(f"Contact with email '{email}' already exists.")
        self._contacts.append(new_contact)
        save_contacts(self._contacts)   # persist to disk after every change
        print(f"Added: {new_contact.name}")

    @log_action
    def remove(self, email: str):
        """Find and remove a contact by email address."""
        # next() returns the first match, or None if nothing matches
        # Generator expression: (c for c in list if condition)
        target = next((c for c in self._contacts if str(c.email) == email.lower()), None)
        if not target:
            raise ContactNotFoundError(f"No contact with email '{email}'.")
        self._contacts.remove(target)
        save_contacts(self._contacts)
        print(f"Removed: {target.name}")

    def list_all(self):
        """Print all contacts sorted alphabetically by name."""
        if not self._contacts:
            print("No contacts found.")
            return
        # enumerate(iterable, start=1) gives (1, item), (2, item), ...
        for i, contact in enumerate(sort_contacts(self._contacts), 1):
            print(f"\n--- Contact {i} ---")
            print(contact)   # calls Contact.__str__()

    def search(self, query: str):
        """Search and print contacts matching the query."""
        results = search_contacts(self._contacts, query)
        if not results:
            print(f"No results for '{query}'.")
        for contact in results:
            print(f"\n{contact}")

    def show_tags(self):
        """Print all unique tags currently in use."""
        tags = get_all_tags(self._contacts)   # returns a set
        print("Tags:", ', '.join(sorted(tags)) if tags else 'none')


# ─────────────────────────────────────────────────────────────────────────────
# CLI HELPER FUNCTIONS
# Small, focused functions — each does one thing.
# ─────────────────────────────────────────────────────────────────────────────

def print_menu():
    """Print the main menu options."""
    print("\n===== Contact Book =====")
    print("1. Add contact")
    print("2. Remove contact")
    print("3. List all contacts")
    print("4. Search contacts")
    print("5. Show all tags")
    print("0. Exit")


def get_input(prompt: str) -> str:
    """Read user input and strip leading/trailing whitespace."""
    return input(prompt).strip()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# while True creates an infinite loop — we break out when user picks '0'.
# try/except around each action catches errors without crashing the app.
# ─────────────────────────────────────────────────────────────────────────────

def run():
    book = ContactBook()   # create the app — loads existing contacts

    while True:            # keep showing the menu until user exits
        print_menu()
        choice = get_input("Choose: ")

        if choice == '1':
            try:
                name  = get_input("Name  : ")
                email = get_input("Email : ")
                phone = get_input("Phone : ")
                tags  = get_input("Tags (comma-separated, optional): ")
                # List comprehension: split by comma, strip spaces, skip empty strings
                tag_list = [t.strip() for t in tags.split(',') if t.strip()]
                book.add(name, email, phone, tag_list)
            except (ValidationError, DuplicateContactError) as e:
                # Catch our custom exceptions and show a friendly message
                print(f"Error: {e}")

        elif choice == '2':
            try:
                email = get_input("Email to remove: ")
                book.remove(email)
            except ContactNotFoundError as e:
                print(f"Error: {e}")

        elif choice == '3':
            book.list_all()

        elif choice == '4':
            query = get_input("Search query: ")
            book.search(query)

        elif choice == '5':
            book.show_tags()

        elif choice == '0':
            print("Goodbye!")
            break          # exit the while loop

        else:
            print("Invalid choice. Try again.")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# __name__ == '__main__' is True only when this file is run directly.
# If another file imports this module, run() won't be called automatically.
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    run()
