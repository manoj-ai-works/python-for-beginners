"""
main.py — To-Do List CLI.

CONCEPTS COVERED:
  - Functions (small, focused helpers)
  - while True loop for the menu
  - if/elif/else control flow
  - try/except for safe user input handling
  - for loop with enumerate()
  - List comprehension for tag parsing
"""

from todo_item import TodoItem, Priority, DueDate
from todo_manager import TodoManager


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# Each function does one small job — this keeps run() clean and readable.
# ─────────────────────────────────────────────────────────────────────────────

def print_menu():
    """Print the main menu."""
    print('\n===== To-Do List =====')
    print('1. Add task')
    print('2. Complete task')
    print('3. Remove task')
    print('4. List all tasks')
    print('5. List pending')
    print('6. List overdue')
    print('7. Search tasks')
    print('8. Show summary')
    print('0. Exit')


def pick_priority() -> Priority:
    """Show priority options and return the user's choice."""
    print('  1. LOW  2. MEDIUM  3. HIGH')
    choice = input('Priority (default 2): ').strip()
    # Dict maps input string to Priority enum member
    mapping = {'1': Priority.LOW, '2': Priority.MEDIUM, '3': Priority.HIGH}
    # .get(choice, Priority.MEDIUM) returns MEDIUM if choice isn't in the dict
    return mapping.get(choice, Priority.MEDIUM)


def print_items(items: list, label: str = ''):
    """Print a numbered list of TodoItems with an optional header."""
    if label:
        print(f'\n--- {label} ---')
    if not items:
        print('  (none)')
        return
    # enumerate(items, 1) gives (1, item), (2, item), ...
    for i, item in enumerate(items, 1):
        print(f'  {i}. {item}')   # calls TodoItem.__str__()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# while True keeps the app running until the user picks '0'.
# try/except around each action prevents crashes from bad input.
# ─────────────────────────────────────────────────────────────────────────────

def run():
    # Create the manager — loads any previously saved tasks from disk
    manager = TodoManager()

    while True:
        print_menu()
        choice = input('Choose: ').strip()

        if choice == '1':
            # Add a new task
            try:
                title    = input('Title   : ').strip()
                priority = pick_priority()
                due_raw  = input('Due date (YYYY-MM-DD, optional): ').strip()
                tags_raw = input('Tags (comma-separated, optional): ').strip()

                # Only create DueDate if the user entered something
                due  = DueDate.from_string(due_raw) if due_raw else None
                # List comprehension: split by comma, strip spaces, skip empty strings
                tags = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]

                item = TodoItem(title=title, priority=priority, due_date=due, tags=tags)
                manager.add(item)
                print(f"Added: '{title}'")
            except (ValueError, TypeError) as e:
                # ValueError from empty title, bad date format, duplicate task
                # TypeError from invalid date type
                print(f'Error: {e}')

        elif choice == '2':
            # Mark a task as done
            title = input('Task title to complete: ').strip()
            try:
                manager.complete(title)
                print(f"Marked done: '{title}'")
            except ValueError as e:
                print(f'Error: {e}')

        elif choice == '3':
            # Remove a task
            title = input('Task title to remove: ').strip()
            try:
                manager.remove(title)
                print(f"Removed: '{title}'")
            except ValueError as e:
                print(f'Error: {e}')

        elif choice == '4':
            # Show all tasks sorted by priority then title
            print_items(manager.all(), 'All Tasks')

        elif choice == '5':
            # Show only tasks not yet completed
            print_items(manager.pending(), 'Pending Tasks')

        elif choice == '6':
            # Show tasks whose due date has passed
            print_items(manager.overdue(), 'Overdue Tasks')

        elif choice == '7':
            # Search by keyword in title or tags
            query = input('Search: ').strip()
            print_items(manager.search(query), f'Results for "{query}"')

        elif choice == '8':
            # Show counts by status and priority
            s = manager.summary()
            print('\n--- Summary ---')
            print(f"  Total    : {s['total']}")
            print(f"  Pending  : {s['pending']}")
            print(f"  Completed: {s['completed']}")
            print(f"  Overdue  : {s['overdue']}")
            print('  By priority:')
            for p, count in s['by_priority'].items():
                # f'{p:<8}' left-aligns p in an 8-char wide column
                print(f'    {p:<8}: {count}')

        elif choice == '0':
            print('Goodbye!')
            break   # exit the while loop

        else:
            print('Invalid choice.')


# Run only when executed directly, not when imported as a module
if __name__ == '__main__':
    run()
