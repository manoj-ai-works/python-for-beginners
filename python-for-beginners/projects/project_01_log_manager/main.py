"""
main.py — Log Manager CLI.

CONCEPTS COVERED:
  - Functions (small, focused, one job each)
  - while loop for the menu
  - if/elif/else control flow
  - try/except for safe user input
  - for loop to display results
  - Enum iteration
"""

from logger import Logger
from log_entry import LogLevel


# ─────────────────────────────────────────────────────────────────────────────
# MENU HELPERS
# Small functions — each does exactly one thing.
# This keeps run() clean and readable.
# ─────────────────────────────────────────────────────────────────────────────

def print_menu():
    """Print the available menu options."""
    print('\n===== Log Manager =====')
    print('1. Add log entry')
    print('2. View all logs')
    print('3. Filter by level')
    print('4. Search logs')
    print('5. Show summary')
    print('6. Clear all logs')
    print('0. Exit')


def pick_level() -> LogLevel:
    """
    Show all log levels and let the user pick one.
    Returns a LogLevel enum member.
    """
    levels = list(LogLevel)   # convert enum to a list so we can index it
    for i, lvl in enumerate(levels, 1):
        print(f'  {i}. {lvl}')   # print: 1. DEBUG, 2. INFO, etc.
    choice = input('Pick level (1-5): ').strip()
    try:
        # int(choice) - 1 converts '1' → index 0 → LogLevel.DEBUG
        return levels[int(choice) - 1]
    except (ValueError, IndexError):
        # ValueError if input isn't a number, IndexError if out of range
        print('Invalid, defaulting to INFO')
        return LogLevel.INFO


# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# while True keeps the app running until the user chooses '0'.
# Each menu option is handled in its own elif block.
# try/except around user actions prevents crashes from bad input.
# ─────────────────────────────────────────────────────────────────────────────

def run():
    # Create the logger — loads any previously saved entries from disk
    logger = Logger(source='cli-app')

    while True:
        print_menu()
        choice = input('Choose: ').strip()

        if choice == '1':
            # Add a new log entry
            level = pick_level()
            msg = input('Message: ').strip()
            try:
                logger._log(level, msg)   # raises ValueError if message is empty
            except ValueError as e:
                print(f'Error: {e}')

        elif choice == '2':
            # View all logs — use the generator to get entries in time order
            entries = list(logger.stream())   # list() exhausts the generator
            if not entries:
                print('No logs yet.')
            for e in entries:
                print(e)   # calls LogEntry.__str__()

        elif choice == '3':
            # Filter by a specific level
            level = pick_level()
            entries = logger.get_by_level(level)
            if not entries:
                print(f'No {level} entries.')
            for e in entries:
                print(e)

        elif choice == '4':
            # Search by keyword
            kw = input('Keyword: ').strip()
            results = logger.search(kw)
            print(f'Found {len(results)} result(s):')
            for e in results:
                print(e)

        elif choice == '5':
            # Show count per level — summary() returns a dict
            summary = logger.summary()
            print('\n--- Log Summary ---')
            for level, count in summary.items():
                # f'{level:<10}' left-aligns the text in a 10-char wide column
                print(f'  {level:<10}: {count}')

        elif choice == '6':
            logger.clear()
            print('Logs cleared.')

        elif choice == '0':
            print('Goodbye!')
            break   # exit the while loop

        else:
            print('Invalid choice.')


# Only run when this file is executed directly, not when imported
if __name__ == '__main__':
    run()
