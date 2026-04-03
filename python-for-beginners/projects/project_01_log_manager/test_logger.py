"""
test_logger.py — Unit tests for Log Manager.
Run: python -m unittest test_logger.py -v
"""

import unittest
import os
from log_entry import LogEntry, LogLevel
from logger import Logger

TEST_FILE = 'test_logs.json'


class TestLogEntry(unittest.TestCase):

    def test_str_format(self):
        entry = LogEntry(LogLevel.INFO, 'Server started', 'api')
        self.assertIn('[INFO]', str(entry))
        self.assertIn('Server started', str(entry))

    def test_empty_message_raises(self):
        with self.assertRaises(ValueError):
            LogEntry(LogLevel.ERROR, '   ')

    def test_to_dict_and_from_dict(self):
        entry = LogEntry(LogLevel.WARNING, 'Low memory', 'system')
        restored = LogEntry.from_dict(entry.to_dict())
        self.assertEqual(entry.level, restored.level)
        self.assertEqual(entry.message, restored.message)

    def test_ordering(self):
        e1 = LogEntry(LogLevel.DEBUG, 'first')
        e2 = LogEntry(LogLevel.ERROR, 'second')
        self.assertLess(e1, e2)  # e1 was created first


class TestLogger(unittest.TestCase):

    def setUp(self):
        # Use a temp file so tests don't pollute real logs
        import logger as lg
        lg.LOG_FILE = TEST_FILE
        self.logger = Logger(source='test')
        self.logger.clear()

    def tearDown(self):
        self.logger.clear()

    def test_log_info(self):
        self.logger.info('hello')
        entries = self.logger.get_by_level(LogLevel.INFO)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].message, 'hello')

    def test_min_level_filters(self):
        self.logger.min_level = LogLevel.WARNING
        self.logger.debug('ignored')
        self.logger.warning('kept')
        self.assertEqual(len(self.logger._entries), 1)

    def test_search(self):
        self.logger.info('user logged in')
        self.logger.error('user not found')
        self.logger.info('system ready')
        results = self.logger.search('user')
        self.assertEqual(len(results), 2)

    def test_get_errors_and_above(self):
        self.logger.info('ok')
        self.logger.error('bad')
        self.logger.critical('very bad')
        results = self.logger.get_errors_and_above()
        self.assertEqual(len(results), 2)

    def test_summary_keys(self):
        self.logger.info('a')
        self.logger.warning('b')
        summary = self.logger.summary()
        self.assertIn('INFO', summary)
        self.assertIn('WARNING', summary)
        self.assertEqual(summary['INFO'], 1)

    def test_stream_generator(self):
        self.logger.info('one')
        self.logger.info('two')
        streamed = list(self.logger.stream(LogLevel.INFO))
        self.assertEqual(len(streamed), 2)

    def test_clear(self):
        self.logger.info('temp')
        self.logger.clear()
        self.assertEqual(len(self.logger._entries), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
