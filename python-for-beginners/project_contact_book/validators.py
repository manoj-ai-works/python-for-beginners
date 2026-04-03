"""
validators.py — Regex-based validation + custom exceptions.

CONCEPTS COVERED:
  - re module (regex patterns)
  - Custom Exception classes
  - Raising exceptions with helpful messages
"""

import re  # Python's built-in module for regular expressions


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM EXCEPTIONS
# Instead of raising generic ValueError, we define our own exception types.
# This makes it easy to catch specific errors in other parts of the code.
# All three inherit from Exception — the base class for all Python exceptions.
# ─────────────────────────────────────────────────────────────────────────────

class ValidationError(Exception):
    """Raised when user input fails a format check (e.g. bad email)."""
    pass  # 'pass' means no extra code needed — the class name says it all


class DuplicateContactError(Exception):
    """Raised when trying to add a contact whose email already exists."""
    pass


class ContactNotFoundError(Exception):
    """Raised when searching for a contact that doesn't exist."""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# REGEX PATTERNS
# re.compile() pre-compiles the pattern for reuse — faster than re.match() each time.
#
# Pattern breakdown for EMAIL_PATTERN:  ^[\w.-]+@[\w.-]+\.\w{2,}$
#   ^           → start of string
#   [\w.-]+     → one or more word chars, dots, or hyphens (the username part)
#   @           → literal @ symbol
#   [\w.-]+     → domain name
#   \.          → literal dot
#   \w{2,}      → TLD like 'com', 'org' (at least 2 chars)
#   $           → end of string
# ─────────────────────────────────────────────────────────────────────────────

EMAIL_PATTERN = re.compile(r'^[\w.-]+@[\w.-]+\.\w{2,}$')

# Phone: optional +, then 7-15 digits/spaces/hyphens
PHONE_PATTERN = re.compile(r'^\+?[\d\s\-]{7,15}$')

# Name: letters, spaces, apostrophes, hyphens — 2 to 50 chars
NAME_PATTERN  = re.compile(r'^[A-Za-z\s\'-]{2,50}$')


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATOR FUNCTIONS
# Each function cleans the input, checks it against a regex,
# and either returns the cleaned value or raises a ValidationError.
# ─────────────────────────────────────────────────────────────────────────────

def validate_email(email: str) -> str:
    """
    Validate and return a cleaned (lowercase, stripped) email.
    Raises ValidationError if the format is wrong.
    """
    email = email.strip().lower()           # remove spaces, normalize to lowercase
    if not EMAIL_PATTERN.match(email):      # .match() checks from the start of the string
        raise ValidationError(f"Invalid email: '{email}'")
    return email                            # return the cleaned value


def validate_phone(phone: str) -> str:
    """
    Validate and return a cleaned phone number.
    Raises ValidationError if the format is wrong.
    """
    phone = phone.strip()
    if not PHONE_PATTERN.match(phone):
        raise ValidationError(f"Invalid phone: '{phone}'")
    return phone


def validate_name(name: str) -> str:
    """
    Validate and return a title-cased name (e.g. 'alice smith' → 'Alice Smith').
    Raises ValidationError if the format is wrong.
    """
    name = name.strip().title()             # .title() capitalizes each word
    if not NAME_PATTERN.match(name):
        raise ValidationError(f"Invalid name: '{name}'")
    return name
