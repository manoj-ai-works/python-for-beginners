"""
todo_item.py — TodoItem model, Priority enum, and DueDate value object.

CONCEPTS COVERED:
  - Enum for fixed constants
  - @dataclass(frozen=True) — immutable Value Object
  - Regex for date format validation
  - @property — computed attribute
  - Dunder methods: __str__, __repr__, __eq__, __post_init__
  - @classmethod — alternative constructor
  - field(default_factory=...) — safe list default
"""

import re
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# ENUM: PRIORITY
# Using an Enum prevents invalid values like priority='urgent' or priority=99.
# Members are ordered by value so we can compare: Priority.HIGH > Priority.LOW
# ─────────────────────────────────────────────────────────────────────────────

class Priority(Enum):
    LOW    = 1
    MEDIUM = 2
    HIGH   = 3

    def __str__(self):
        return self.name   # 'LOW', 'MEDIUM', 'HIGH'

    def __lt__(self, other):
        # Enables sorting and comparison: Priority.LOW < Priority.HIGH → True
        return self.value < other.value


# ─────────────────────────────────────────────────────────────────────────────
# VALUE OBJECT: DUE DATE
# frozen=True makes this immutable — once created, the date can't change.
# Equality is based on value: DueDate('2030-01-01') == DueDate('2030-01-01')
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class DueDate:
    """Immutable value object representing a task due date."""
    value: date   # stores a Python date object

    def __post_init__(self):
        # Validate that value is actually a date object
        if not isinstance(self.value, date):
            raise TypeError('DueDate.value must be a date object')

    @classmethod
    def from_string(cls, s: str) -> 'DueDate':
        """
        Create a DueDate from a 'YYYY-MM-DD' string.
        Regex validates the format before parsing.
        """
        # Regex: ^ start, \d{4} four digits, - literal dash, \d{2} two digits, $ end
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', s):
            raise ValueError(f"Invalid date format '{s}'. Use YYYY-MM-DD.")
        return cls(value=date.fromisoformat(s))   # parse '2030-01-01' → date object

    @property
    def is_overdue(self) -> bool:
        """
        @property makes this a computed attribute — access it like due.is_overdue
        instead of calling due.is_overdue().
        Returns True if the due date is in the past.
        """
        return self.value < date.today()

    def __str__(self):
        return self.value.isoformat()   # '2030-01-01'


# ─────────────────────────────────────────────────────────────────────────────
# DATACLASS: TODO ITEM
# Represents one task. Mutable (not frozen) because tasks can be completed.
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class TodoItem:
    """A single to-do task with title, priority, optional due date, and tags."""

    title:    str
    priority: Priority         = Priority.MEDIUM   # default priority
    due_date: Optional[DueDate] = None             # Optional means it can be None
    # field(default_factory=list) creates a fresh [] for each instance
    tags:     list             = field(default_factory=list)
    done:     bool             = False             # False = not completed yet

    def __post_init__(self):
        # Strip whitespace and validate title is not empty
        self.title = self.title.strip()
        if not self.title:
            raise ValueError('Title cannot be empty')

    def __str__(self):
        # Build a readable one-line representation of the task
        status   = '✓' if self.done else '○'   # tick or circle
        due      = f' | due: {self.due_date}' if self.due_date else ''
        # Show [OVERDUE] only if there's a due date, it's past, and task isn't done
        overdue  = ' [OVERDUE]' if self.due_date and self.due_date.is_overdue and not self.done else ''
        tags_str = f' | tags: {", ".join(self.tags)}' if self.tags else ''
        return f'[{status}] [{self.priority}]{due}{overdue} — {self.title}{tags_str}'

    def __repr__(self):
        # Developer-readable format for debugging
        return f'TodoItem(title={self.title!r}, priority={self.priority}, done={self.done})'

    def __eq__(self, other):
        # Two tasks are equal if they have the same title (case-insensitive)
        # This prevents adding duplicate tasks
        if not isinstance(other, TodoItem):
            return NotImplemented
        return self.title.lower() == other.title.lower()

    def complete(self):
        """Mark this task as done."""
        self.done = True

    def to_dict(self) -> dict:
        """Convert to a plain dict for JSON serialization."""
        return {
            'title':    self.title,
            'priority': self.priority.name,                    # 'HIGH', not 3
            'due_date': str(self.due_date) if self.due_date else None,
            'tags':     self.tags,
            'done':     self.done,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TodoItem':
        """Rebuild a TodoItem from a dict (e.g. loaded from JSON)."""
        # Only create DueDate if the value is not None
        due = DueDate.from_string(data['due_date']) if data.get('due_date') else None
        return cls(
            title=data['title'],
            priority=Priority[data['priority']],   # 'HIGH' → Priority.HIGH
            due_date=due,
            tags=data.get('tags', []),             # default to [] if key missing
            done=data.get('done', False),
        )
