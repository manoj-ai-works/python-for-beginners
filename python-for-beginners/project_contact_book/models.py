"""
models.py — Value Objects and Contact class.

CONCEPTS COVERED:
  - @dataclass — auto-generates __init__, __repr__, __eq__
  - frozen=True — makes a dataclass immutable (Value Object pattern)
  - Dunder methods: __str__, __repr__, __eq__, __hash__
  - @classmethod — alternative constructor
  - field(default_factory=...) — safe mutable defaults
"""

from dataclasses import dataclass, field
from typing import Optional
from validators import validate_name, validate_email, validate_phone


# ─────────────────────────────────────────────────────────────────────────────
# VALUE OBJECTS
# A Value Object is an immutable object whose identity is its value.
# Two Email objects with the same address are considered equal.
# frozen=True prevents any attribute from being changed after creation.
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)   # frozen=True → immutable, also makes it hashable
class Email:
    """Immutable value object that holds a validated email address."""
    value: str

    def __post_init__(self):
        # __post_init__ runs right after __init__
        # Because frozen=True, we can't do self.value = ... directly
        # object.__setattr__ bypasses the freeze — only use in __post_init__
        object.__setattr__(self, 'value', validate_email(self.value))

    def __str__(self):
        # Called when you do print(email) or f"{email}"
        return self.value


@dataclass(frozen=True)
class Phone:
    """Immutable value object that holds a validated phone number."""
    value: str

    def __post_init__(self):
        object.__setattr__(self, 'value', validate_phone(self.value))

    def __str__(self):
        return self.value


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT CLASS
# A regular (mutable) dataclass that represents one contact entry.
# Uses Email and Phone value objects to ensure data is always valid.
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Contact:
    """Represents a contact with name, email, phone, and optional tags."""
    name:  str
    email: Email
    phone: Phone
    # field(default_factory=list) creates a NEW empty list for each instance
    # Never use tags: list = [] — that shares one list across all instances!
    tags:  list = field(default_factory=list)

    def __post_init__(self):
        # Validate and normalize the name on creation
        self.name = validate_name(self.name)

    # ── Dunder methods ────────────────────────────────────────────────────────

    def __str__(self):
        # Called by print(contact) — human-readable format
        tags_str = ', '.join(self.tags) if self.tags else 'none'
        return (
            f"Name : {self.name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Tags : {tags_str}"
        )

    def __repr__(self):
        # Called in the REPL or when inside a list — developer-readable format
        return f"Contact(name={self.name!r}, email={self.email!r}, phone={self.phone!r})"

    def __eq__(self, other):
        # Two contacts are equal if they share the same email (unique identifier)
        if not isinstance(other, Contact):
            return NotImplemented   # let Python handle comparison with other types
        return self.email == other.email

    def __hash__(self):
        # Required when __eq__ is defined — allows Contact to be used in sets/dicts
        return hash(self.email)

    # ── Instance methods ──────────────────────────────────────────────────────

    def add_tag(self, tag: str):
        """Add a tag if it's not already present."""
        tag = tag.strip().lower()
        if tag and tag not in self.tags:  # avoid empty strings and duplicates
            self.tags.append(tag)

    def to_dict(self) -> dict:
        """Convert to a plain dict so it can be saved as JSON."""
        return {
            'name':  self.name,
            'email': str(self.email),   # str() calls __str__ on the Email object
            'phone': str(self.phone),
            'tags':  self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Contact':
        """
        Alternative constructor — create a Contact from a dict (e.g. loaded from JSON).
        @classmethod receives the class itself as first arg (cls), not an instance.
        """
        return cls(
            name=data['name'],
            email=Email(data['email']),  # re-wrap in value objects for validation
            phone=Phone(data['phone']),
            tags=data.get('tags', []),   # .get() returns [] if 'tags' key is missing
        )
