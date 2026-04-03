"""
test_todo.py — Unit tests for To-Do List project.
Run: python -m unittest test_todo.py -v
"""

import unittest
from datetime import date, timedelta
from todo_item import TodoItem, Priority, DueDate
from todo_manager import TodoManager


class TestDueDate(unittest.TestCase):

    def test_valid_date(self):
        d = DueDate.from_string('2030-12-31')
        self.assertEqual(str(d), '2030-12-31')

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            DueDate.from_string('31-12-2030')

    def test_overdue(self):
        past = DueDate(value=date.today() - timedelta(days=1))
        self.assertTrue(past.is_overdue)

    def test_not_overdue(self):
        future = DueDate(value=date.today() + timedelta(days=10))
        self.assertFalse(future.is_overdue)


class TestTodoItem(unittest.TestCase):

    def test_empty_title_raises(self):
        with self.assertRaises(ValueError):
            TodoItem(title='   ')

    def test_complete(self):
        item = TodoItem('Buy milk')
        self.assertFalse(item.done)
        item.complete()
        self.assertTrue(item.done)

    def test_equality_case_insensitive(self):
        a = TodoItem('Buy Milk')
        b = TodoItem('buy milk')
        self.assertEqual(a, b)

    def test_to_dict_from_dict(self):
        item = TodoItem('Read book', Priority.HIGH, DueDate.from_string('2030-01-01'), ['learning'])
        restored = TodoItem.from_dict(item.to_dict())
        self.assertEqual(item.title, restored.title)
        self.assertEqual(item.priority, restored.priority)
        self.assertEqual(item.tags, restored.tags)


class TestTodoManager(unittest.TestCase):

    def setUp(self):
        import todo_manager as tm
        tm.DATA_FILE = 'test_todos.json'
        self.manager = TodoManager()
        self.manager.clear()

    def tearDown(self):
        self.manager.clear()

    def _add(self, title, priority=Priority.MEDIUM, tags=None):
        self.manager.add(TodoItem(title=title, priority=priority, tags=tags or []))

    def test_add_and_list(self):
        self._add('Task A')
        self.assertEqual(len(self.manager.all()), 1)

    def test_duplicate_raises(self):
        self._add('Task A')
        with self.assertRaises(ValueError):
            self._add('Task A')

    def test_complete_task(self):
        self._add('Task A')
        self.manager.complete('Task A')
        self.assertTrue(self.manager._find('Task A').done)

    def test_remove_task(self):
        self._add('Task A')
        self.manager.remove('Task A')
        self.assertEqual(len(self.manager.all()), 0)

    def test_remove_not_found(self):
        with self.assertRaises(ValueError):
            self.manager.remove('Ghost Task')

    def test_pending_and_completed(self):
        self._add('Task A')
        self._add('Task B')
        self.manager.complete('Task A')
        self.assertEqual(len(self.manager.pending()), 1)
        self.assertEqual(len(self.manager.completed()), 1)

    def test_search(self):
        self._add('Buy groceries')
        self._add('Buy tickets')
        self._add('Read book')
        results = self.manager.search('buy')
        self.assertEqual(len(results), 2)

    def test_by_priority(self):
        self._add('High task', Priority.HIGH)
        self._add('Low task', Priority.LOW)
        self.assertEqual(len(self.manager.by_priority(Priority.HIGH)), 1)

    def test_by_tag(self):
        self._add('Task A', tags=['work'])
        self._add('Task B', tags=['personal'])
        self._add('Task C', tags=['work'])
        self.assertEqual(len(self.manager.by_tag('work')), 2)

    def test_summary(self):
        self._add('Task A')
        self._add('Task B')
        self.manager.complete('Task A')
        s = self.manager.summary()
        self.assertEqual(s['total'], 2)
        self.assertEqual(s['pending'], 1)
        self.assertEqual(s['completed'], 1)

    def test_overdue(self):
        past = DueDate(value=date.today() - timedelta(days=1))
        self.manager.add(TodoItem('Old task', due_date=past))
        self.assertEqual(len(self.manager.overdue()), 1)

    def test_paginate(self):
        for i in range(12):
            self._add(f'Task {i}')
        pages = list(self.manager.paginate(page_size=5))
        self.assertEqual(len(pages), 3)
        self.assertEqual(len(pages[0]), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
