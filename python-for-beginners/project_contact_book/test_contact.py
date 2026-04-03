"""
test_contact.py — Unit tests for the Contact Book project.
Concepts: unittest, setUp, assertRaises, assertEqual, assertTrue
Run with: python -m pytest test_contact.py -v
      or: python -m unittest test_contact.py -v
"""

import unittest
from models import Contact, Email, Phone
from validators import (
    validate_email, validate_phone, validate_name,
    ValidationError, DuplicateContactError, ContactNotFoundError
)
from utils import search_contacts, sort_contacts, get_all_tags, filter_by_tag


# ── Helper ────────────────────────────────────────────────────────────────────

def make_contact(name='Alice Smith', email='alice@example.com', phone='+1234567890', tags=None):
    return Contact(name=name, email=Email(email), phone=Phone(phone), tags=tags or [])


# ── Validator Tests ───────────────────────────────────────────────────────────

class TestValidators(unittest.TestCase):

    def test_valid_email(self):
        self.assertEqual(validate_email('Alice@Example.COM'), 'alice@example.com')

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            validate_email('not-an-email')

    def test_valid_phone(self):
        self.assertEqual(validate_phone('+1234567890'), '+1234567890')

    def test_invalid_phone(self):
        with self.assertRaises(ValidationError):
            validate_phone('abc')

    def test_valid_name(self):
        self.assertEqual(validate_name('alice smith'), 'Alice Smith')

    def test_invalid_name_too_short(self):
        with self.assertRaises(ValidationError):
            validate_name('A')


# ── Value Object Tests ────────────────────────────────────────────────────────

class TestValueObjects(unittest.TestCase):

    def test_email_equality(self):
        e1 = Email('alice@example.com')
        e2 = Email('alice@example.com')
        self.assertEqual(e1, e2)

    def test_email_immutable(self):
        e = Email('alice@example.com')
        with self.assertRaises(Exception):
            e.value = 'other@example.com'  # frozen dataclass

    def test_phone_str(self):
        p = Phone('+1234567890')
        self.assertEqual(str(p), '+1234567890')


# ── Contact Tests ─────────────────────────────────────────────────────────────

class TestContact(unittest.TestCase):

    def setUp(self):
        self.contact = make_contact()

    def test_contact_name_titlecase(self):
        self.assertEqual(self.contact.name, 'Alice Smith')

    def test_contact_equality_by_email(self):
        c1 = make_contact(name='Alice Smith', email='alice@example.com')
        c2 = make_contact(name='Different Name', email='alice@example.com')
        self.assertEqual(c1, c2)

    def test_add_tag(self):
        self.contact.add_tag('friend')
        self.assertIn('friend', self.contact.tags)

    def test_add_duplicate_tag(self):
        self.contact.add_tag('friend')
        self.contact.add_tag('friend')
        self.assertEqual(self.contact.tags.count('friend'), 1)

    def test_to_dict_and_from_dict(self):
        d = self.contact.to_dict()
        restored = Contact.from_dict(d)
        self.assertEqual(self.contact, restored)


# ── Utils Tests ───────────────────────────────────────────────────────────────

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.contacts = [
            make_contact('Alice Smith', 'alice@example.com', '+1111111111', ['friend', 'work']),
            make_contact('Bob Jones',   'bob@example.com',   '+2222222222', ['family']),
            make_contact('Charlie Brown','charlie@example.com','+3333333333', ['friend']),
        ]

    def test_search_by_name(self):
        results = search_contacts(self.contacts, 'alice')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Alice Smith')

    def test_search_by_tag(self):
        results = search_contacts(self.contacts, 'friend')
        self.assertEqual(len(results), 2)

    def test_search_no_results(self):
        results = search_contacts(self.contacts, 'zzz')
        self.assertEqual(results, [])

    def test_sort_by_name(self):
        sorted_c = sort_contacts(self.contacts)
        names = [c.name for c in sorted_c]
        self.assertEqual(names, sorted(names))

    def test_get_all_tags(self):
        tags = get_all_tags(self.contacts)
        self.assertIn('friend', tags)
        self.assertIn('family', tags)
        self.assertIn('work', tags)

    def test_filter_by_tag(self):
        results = filter_by_tag(self.contacts, 'family')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Bob Jones')


if __name__ == '__main__':
    unittest.main(verbosity=2)
