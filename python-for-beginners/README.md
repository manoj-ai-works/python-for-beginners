# Python for Beginners — From Basics to Advanced

> We're all using AI to write code now. But somewhere along the way, we stopped *understanding* it.
> This repo is a reminder of what's actually happening under the hood.

A structured, hands-on Python learning resource — built for **beginners** who want a clear path, and **working professionals** who want a quick refresh on the fundamentals they've been outsourcing to AI.

Every notebook has working code with inline comments that explain the **why**, not just the what. Every project shows how all the concepts connect in real code.

---

## Who is this for?

**Beginners** — follow the numbered folders top to bottom. Each topic builds on the last.

**Working professionals** — jump to any topic you want to revisit. Each notebook is self-contained.

---

## Learning Path

### Basics
| Folder | Topics |
|--------|--------|
| `01_basics` | Variables, data types, type conversion, operators, strings, user input |
| `02_control_flow` | if/elif/else, for loops, while loops, break, continue, pass |
| `03_functions` | Defining functions, return values, default params, *args, **kwargs, lambda |
| `04_data_structures` | Lists, tuples, dictionaries, sets |
| `05_modules_and_files` | Imports, standard library, file I/O, JSON |
| `06_error_handling` | try/except/finally, raising exceptions, custom exceptions |

### Object-Oriented Programming
| Folder | Topics |
|--------|--------|
| `07_oop` | Classes, objects, inheritance, encapsulation, polymorphism, dunder methods, dataclasses |

### Advanced
| Folder | Topics |
|--------|--------|
| `08_advanced` | List/dict/set comprehensions, generators, iterators, decorators, context managers, lambda |
| `11_regex` | Regex patterns, re.match/search/findall/sub, validation |
| `12_value_objects` | Immutable value objects with frozen dataclasses |
| `13_unit_testing` | unittest, setUp/tearDown, assertRaises, test structure |

---

## Projects

Two real projects that use every concept together — so you see how it all connects.

### Project 1 — Log Manager (`projects/project_01_log_manager/`)
A CLI app for logging and filtering messages by severity level.

| File | Concepts |
|------|----------|
| `log_entry.py` | Enum, dataclass, dunder methods, `__post_init__`, `@classmethod` |
| `logger.py` | Decorator, list/dict comprehensions, generator, file I/O, JSON |
| `main.py` | Functions, while loop, if/elif/else, try/except |
| `test_logger.py` | unittest, setUp, tearDown, assertRaises |

```bash
cd projects/project_01_log_manager
python main.py
python -m unittest test_logger.py -v
```

### Project 2 — To-Do List (`projects/project_02_todo_list/`)
A CLI task manager with priorities, due dates, tags, and filtering.

| File | Concepts |
|------|----------|
| `todo_item.py` | Enum, frozen dataclass (Value Object), regex, dunder methods, `@property` |
| `todo_manager.py` | Decorator, context manager, list/dict comprehensions, lambda, generator |
| `main.py` | Functions, while loop, if/elif/else, try/except |
| `test_todo.py` | unittest, setUp, tearDown, assertRaises |

```bash
cd projects/project_02_todo_list
python main.py
python -m unittest test_todo.py -v
```

### Bonus — Contact Book (`project_contact_book/`)
An earlier project covering regex validation, value objects, and all core concepts.

---

## Concepts Coverage

| Concept | Notebook | Project |
|---------|----------|---------|
| Variables & Types | `01_basics` | — |
| Control Flow | `02_control_flow` | all `main.py` files |
| Functions | `03_functions` | all files |
| Data Structures | `04_data_structures` | — |
| File I/O + JSON | `05_modules_and_files/03` | `storage.py`, `logger.py` |
| Exception Handling | `06_error_handling/01` | all `main.py` files |
| Custom Exceptions | `06_error_handling/02` | `validators.py` |
| Classes & OOP | `07_oop/01-03` | all model files |
| Dunder Methods | `07_oop/04` | `log_entry.py`, `todo_item.py` |
| Dataclasses | `07_oop/05` | `log_entry.py`, `todo_item.py` |
| Comprehensions | `08_advanced/01, 05` | `logger.py`, `todo_manager.py` |
| Generators | `08_advanced/02` | `logger.py`, `storage.py` |
| Decorators | `08_advanced/03` | `logger.py`, `todo_manager.py` |
| Context Managers | `08_advanced/04` | `storage.py`, `todo_manager.py` |
| Lambda | `08_advanced/06` | `todo_manager.py`, `utils.py` |
| Regex | `11_regex` | `validators.py`, `todo_item.py` |
| Value Objects | `12_value_objects` | `todo_item.py`, `models.py` |
| Unit Testing | `13_unit_testing` | `test_logger.py`, `test_todo.py` |

---

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/your-username/python-for-beginners.git
cd python-for-beginners
```

**2. Install Jupyter**
```bash
pip install notebook
```

**3. Open any notebook**
```bash
jupyter notebook
```

Or open directly in VS Code — it has built-in notebook support.

**4. Run the projects**
```bash
cd projects/project_01_log_manager
python main.py
```

No external dependencies. Everything uses Python's standard library.

---

## Structure

```
python-for-beginners/
├── 01_basics/
├── 02_control_flow/
├── 03_functions/
├── 04_data_structures/
├── 05_modules_and_files/
├── 06_error_handling/
├── 07_oop/
├── 08_advanced/
├── 11_regex/
├── 12_value_objects/
├── 13_unit_testing/
├── projects/
│   ├── project_01_log_manager/
│   └── project_02_todo_list/
├── project_contact_book/
├── README.md
```

---

> Tools change. Fundamentals don't.
