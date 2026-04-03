"""
storage.py — Save and load contacts from a JSON file.

CONCEPTS COVERED:
  - File I/O with open()
  - JSON serialization (json.dump / json.load)
  - Context Manager with @contextmanager
  - Generator function with yield
  - Exception handling for file errors
"""

import json                          # built-in module for JSON read/write
import os                            # built-in module for file system checks
from contextlib import contextmanager  # helper to build context managers with a function
from models import Contact


DATA_FILE = 'contacts.json'          # default file path for storing contacts


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CONTEXT MANAGER
# A context manager controls setup and teardown around a block of code.
# Using @contextmanager + yield, we can write one as a plain function.
#
# The code BEFORE yield runs on entry (like __enter__)
# The code AFTER yield runs on exit (like __exit__), even if an error occurs
# ─────────────────────────────────────────────────────────────────────────────

@contextmanager
def open_data_file(path: str, mode: str):
    """
    Safely open a file and yield it.
    Guarantees the file is closed even if an error occurs inside the 'with' block.
    """
    f = None
    try:
        f = open(path, mode, encoding='utf-8')  # open the file
        yield f                                  # hand the file to the 'with' block
    except OSError as e:
        # OSError covers FileNotFoundError, PermissionError, etc.
        print(f"File error: {e}")
        yield None                               # yield None so caller can check
    finally:
        # finally ALWAYS runs — this is our cleanup/teardown
        if f:
            f.close()                            # always close the file


# ─────────────────────────────────────────────────────────────────────────────
# SAVE CONTACTS
# Converts each Contact to a dict, then writes the list as JSON.
# ─────────────────────────────────────────────────────────────────────────────

def save_contacts(contacts: list[Contact], path: str = DATA_FILE):
    """Serialize all contacts to a JSON file."""
    # List comprehension: call .to_dict() on every contact
    data = [c.to_dict() for c in contacts]

    with open_data_file(path, 'w') as f:
        if f:                                    # f is None if the file couldn't open
            json.dump(data, f, indent=2)         # indent=2 makes the JSON human-readable


# ─────────────────────────────────────────────────────────────────────────────
# LOAD CONTACTS
# Reads the JSON file and rebuilds Contact objects from the saved dicts.
# ─────────────────────────────────────────────────────────────────────────────

def load_contacts(path: str = DATA_FILE) -> list[Contact]:
    """Load contacts from JSON. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(path):
        return []                                # no file yet — first run

    with open_data_file(path, 'r') as f:
        if f:
            try:
                data = json.load(f)              # parse JSON → list of dicts
                # List comprehension: rebuild each Contact from its dict
                return [Contact.from_dict(d) for d in data]
            except (json.JSONDecodeError, KeyError):
                # JSONDecodeError → file is corrupted/empty
                # KeyError → a required field is missing from the saved data
                print("Warning: corrupted data file, starting fresh.")
                return []
    return []


# ─────────────────────────────────────────────────────────────────────────────
# GENERATOR: STREAM CONTACTS ONE AT A TIME
# Instead of loading everything into memory at once, a generator yields
# one item at a time. Useful for large files.
# 'yield' pauses the function and returns a value; resumes on next call.
# ─────────────────────────────────────────────────────────────────────────────

def iter_contacts(path: str = DATA_FILE):
    """Generator that yields one Contact at a time from the file."""
    if not os.path.exists(path):
        return                                   # empty generator — nothing to yield

    with open_data_file(path, 'r') as f:
        if f:
            try:
                data = json.load(f)
                for item in data:
                    yield Contact.from_dict(item)  # yield one contact, then pause
            except (json.JSONDecodeError, KeyError):
                return                           # stop the generator on bad data
