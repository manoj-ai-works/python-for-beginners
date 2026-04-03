"""
todo_manager.py — TodoManager class.

CONCEPTS COVERED:
  - Decorator (@auto_save) applied to multiple methods
  - @contextmanager for safe file access
  - List comprehensions for filtering
  - Dict comprehension for summary
  - Lambda in sorted() for custom sort order
  - Generator with yield for pagination
  - JSON file persistence
  - Exception handling
"""

import json
import os
from contextlib import contextmanager   # lets us write context managers as functions
from functools import wraps
from todo_item import TodoItem, Priority


DATA_FILE = 'todos.json'


# ─────────────────────────────────────────────────────────────────────────────
# DECORATOR: @auto_save
# Applied to any method that changes the list (add, remove, complete).
# After the method runs, it automatically calls self._save() to persist changes.
# This way we never forget to save after a mutation.
# ─────────────────────────────────────────────────────────────────────────────

def auto_save(func):
    """Decorator: calls self._save() after the wrapped method completes."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)   # run the original method first
        self._save()                           # then save automatically
        return result
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# CONTEXT MANAGER: safe_file
# @contextmanager turns a generator function into a context manager.
# Code before 'yield' = setup (open file)
# Code after  'yield' = teardown (close file) — runs even if an error occurs
# ─────────────────────────────────────────────────────────────────────────────

@contextmanager
def safe_file(path: str, mode: str):
    """Open a file safely — always closes it, even if an error occurs."""
    f = None
    try:
        f = open(path, mode, encoding='utf-8')
        yield f          # hand the file object to the 'with' block
    except OSError as e:
        print(f'File error: {e}')
        yield None       # yield None so the caller can check with 'if f:'
    finally:
        if f:
            f.close()    # always close — this is the teardown


# ─────────────────────────────────────────────────────────────────────────────
# TODO MANAGER CLASS
# Holds all tasks in self._items and provides CRUD + query methods.
# ─────────────────────────────────────────────────────────────────────────────

class TodoManager:
    """Manages a collection of TodoItems with CRUD, filtering, and persistence."""

    def __init__(self):
        # Load any previously saved tasks from disk when the app starts
        self._items: list[TodoItem] = self._load()

    # ── CRUD ──────────────────────────────────────────────────────────────────

    @auto_save   # saves automatically after adding
    def add(self, item: TodoItem):
        """Add a task. Raises ValueError if a task with the same title exists."""
        # __eq__ on TodoItem compares by title (case-insensitive)
        if item in self._items:
            raise ValueError(f"Task '{item.title}' already exists.")
        self._items.append(item)

    @auto_save   # saves automatically after removing
    def remove(self, title: str):
        """Remove a task by title. Raises ValueError if not found."""
        target = self._find(title)   # find raises ValueError if not found
        self._items.remove(target)

    @auto_save   # saves automatically after completing
    def complete(self, title: str):
        """Mark a task as done. Raises ValueError if not found."""
        self._find(title).complete()   # .complete() sets done=True

    def _find(self, title: str) -> TodoItem:
        """Find a task by title (case-insensitive). Raises ValueError if missing."""
        title = title.strip().lower()
        # next() returns the first match, or None if nothing matches
        # Generator expression inside next(): (item for item in list if condition)
        match = next((i for i in self._items if i.title.lower() == title), None)
        if not match:
            raise ValueError(f"Task '{title}' not found.")
        return match

    # ── Queries using list comprehensions ─────────────────────────────────────

    def all(self) -> list[TodoItem]:
        """Return all tasks sorted by priority (HIGH first), then title."""
        # Lambda: anonymous function — sort by negative priority (so HIGH=3 comes first)
        # then by title alphabetically as a tiebreaker
        return sorted(self._items, key=lambda i: (-i.priority.value, i.title.lower()))

    def pending(self) -> list[TodoItem]:
        """Return tasks that are not yet done."""
        return [i for i in self._items if not i.done]

    def completed(self) -> list[TodoItem]:
        """Return tasks that are marked done."""
        return [i for i in self._items if i.done]

    def overdue(self) -> list[TodoItem]:
        """Return pending tasks whose due date has passed."""
        return [
            i for i in self._items
            if i.due_date              # has a due date
            and i.due_date.is_overdue  # that date is in the past
            and not i.done             # and the task isn't done yet
        ]

    def by_priority(self, priority: Priority) -> list[TodoItem]:
        """Return tasks matching the given priority level."""
        return [i for i in self._items if i.priority == priority]

    def by_tag(self, tag: str) -> list[TodoItem]:
        """Return tasks that have the given tag."""
        return [i for i in self._items if tag.lower() in i.tags]

    def search(self, query: str) -> list[TodoItem]:
        """Search tasks by title or tag (case-insensitive)."""
        q = query.lower()
        return [
            i for i in self._items
            if q in i.title.lower()          # match in title
            or any(q in t for t in i.tags)   # match in any tag
        ]

    def summary(self) -> dict:
        """Return a summary dict with counts by status and priority."""
        return {
            'total':     len(self._items),
            'pending':   len(self.pending()),
            'completed': len(self.completed()),
            'overdue':   len(self.overdue()),
            # Dict comprehension: {priority_name: count} for each Priority member
            'by_priority': {p.name: len(self.by_priority(p)) for p in Priority},
        }

    # ── Generator: pagination ─────────────────────────────────────────────────

    def paginate(self, page_size: int = 5):
        """
        Generator that yields one page of tasks at a time.
        Useful for displaying large lists without loading everything at once.

        Usage:
            for page in manager.paginate(page_size=3):
                for item in page:
                    print(item)
        """
        items = self.all()
        for i in range(0, len(items), page_size):
            yield items[i:i + page_size]   # yield a slice, then pause

    # ── Persistence ───────────────────────────────────────────────────────────

    def _save(self):
        """Write all tasks to the JSON file."""
        with safe_file(DATA_FILE, 'w') as f:
            if f:   # f is None if the file couldn't be opened
                # List comprehension: convert each TodoItem to a dict
                json.dump([i.to_dict() for i in self._items], f, indent=2)

    def _load(self) -> list[TodoItem]:
        """Read tasks from the JSON file. Returns [] if file doesn't exist."""
        if not os.path.exists(DATA_FILE):
            return []   # first run — no file yet
        with safe_file(DATA_FILE, 'r') as f:
            if f:
                try:
                    # List comprehension: rebuild each TodoItem from its saved dict
                    return [TodoItem.from_dict(d) for d in json.load(f)]
                except (json.JSONDecodeError, KeyError, ValueError):
                    # File is corrupted or has unexpected structure — start fresh
                    return []

    @auto_save
    def clear(self):
        """Remove all tasks from memory and delete the file."""
        self._items = []
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
