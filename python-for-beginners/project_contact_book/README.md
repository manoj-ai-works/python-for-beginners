# Contact Book — Python Concepts Project

A CLI contact manager that demonstrates every core Python concept in one real project.

## Concepts Used

| File | Concepts |
|---|---|
| `validators.py` | Regex, Custom Exceptions |
| `models.py` | Classes, Value Objects, Dunder methods, Encapsulation, dataclass |
| `storage.py` | File Handling, JSON, Context Managers, Generators |
| `utils.py` | Decorators, List/Dict/Set Comprehensions, Lambda, Generators |
| `main.py` | Functions, Control Flow, Loops, Exception Handling |
| `test_contact.py` | Unit Tests, setUp, assertRaises |

## Run the App

```bash
cd project_contact_book
python main.py
```

## Run Tests

```bash
python -m unittest test_contact.py -v
```

## Project Structure

```
project_contact_book/
├── models.py       ← Contact, Email, Phone (Value Objects)
├── validators.py   ← Regex validators + custom exceptions
├── storage.py      ← JSON file persistence + context manager
├── utils.py        ← Search, sort, filter, decorators, comprehensions
├── main.py         ← CLI app entry point
└── test_contact.py ← Unit tests
```
