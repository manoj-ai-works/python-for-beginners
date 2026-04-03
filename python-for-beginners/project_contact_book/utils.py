"""
utils.py — Helper utilities.

CONCEPTS COVERED:
  - Decorator pattern with @wraps
  - List comprehension (filter + transform)
  - Dict comprehension
  - Set comprehension
  - Lambda functions
  - sorted() with a key function
  - Generator with yield
"""

import time
from functools import wraps   # preserves the original function's name/docstring
from models import Contact


# ─────────────────────────────────────────────────────────────────────────────
# DECORATOR
# A decorator wraps a function to add behaviour before/after it runs.
# @wraps(func) copies the original function's __name__ and __doc__ to wrapper,
# so it doesn't look like every function is called "wrapper".
# ─────────────────────────────────────────────────────────────────────────────

def log_action(func):
    """Decorator: prints how long the wrapped function took to run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()                      # record start time
        result = func(*args, **kwargs)           # call the original function
        elapsed = time.time() - start            # calculate elapsed time
        print(f"[{func.__name__}] completed in {elapsed:.4f}s")
        return result                            # return whatever the original returned
    return wrapper                               # return the wrapper, not the result


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH — LIST COMPREHENSION
# [expression for item in iterable if condition]
# Reads as: "give me c, for each c in contacts, if any condition matches"
# ─────────────────────────────────────────────────────────────────────────────

def search_contacts(contacts: list[Contact], query: str) -> list[Contact]:
    """Search contacts by name, email, or any tag."""
    q = query.strip().lower()
    return [
        c for c in contacts
        if q in c.name.lower()           # match in name
        or q in str(c.email)             # match in email
        or any(q in tag for tag in c.tags)  # match in any tag (generator expression)
    ]


def filter_by_tag(contacts: list[Contact], tag: str) -> list[Contact]:
    """Return only contacts that have the given tag."""
    # List comprehension with a simple condition
    return [c for c in contacts if tag.lower() in c.tags]


# ─────────────────────────────────────────────────────────────────────────────
# SET COMPREHENSION
# {expression for item in iterable}
# Like list comprehension but produces a set — automatically removes duplicates.
# ─────────────────────────────────────────────────────────────────────────────

def get_all_tags(contacts: list[Contact]) -> set:
    """Collect every unique tag used across all contacts."""
    # Nested comprehension: loop over contacts, then loop over each contact's tags
    return {tag for c in contacts for tag in c.tags}


# ─────────────────────────────────────────────────────────────────────────────
# DICT COMPREHENSION
# {key_expr: value_expr for item in iterable}
# ─────────────────────────────────────────────────────────────────────────────

def contacts_summary(contacts: list[Contact]) -> dict:
    """Build a {name: email} summary dict for all contacts."""
    return {c.name: str(c.email) for c in contacts}


# ─────────────────────────────────────────────────────────────────────────────
# LAMBDA + sorted()
# lambda is an anonymous one-line function: lambda args: expression
# sorted(iterable, key=fn) sorts by the value returned by fn for each item.
# ─────────────────────────────────────────────────────────────────────────────

def sort_contacts(contacts: list[Contact], by: str = 'name') -> list[Contact]:
    """Sort contacts by 'name' or 'email'. Defaults to name."""
    # Dict of lambda functions — pick the right one based on 'by'
    key_map = {
        'name':  lambda c: c.name.lower(),   # sort alphabetically, case-insensitive
        'email': lambda c: str(c.email),
    }
    key_fn = key_map.get(by, key_map['name'])  # fall back to name if unknown key
    return sorted(contacts, key=key_fn)


# ─────────────────────────────────────────────────────────────────────────────
# GENERATOR
# A generator function uses 'yield' instead of 'return'.
# It produces values one at a time — doesn't build the whole list in memory.
# Each call to next() resumes from where it left off.
# ─────────────────────────────────────────────────────────────────────────────

def paginate(contacts: list[Contact], page_size: int = 5):
    """Yield one page (slice) of contacts at a time."""
    for i in range(0, len(contacts), page_size):
        yield contacts[i:i + page_size]   # yield a slice, then pause until next()
