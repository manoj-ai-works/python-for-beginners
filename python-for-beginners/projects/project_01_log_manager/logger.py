"""
logger.py — Logger class with filtering, decorators, comprehensions.

CONCEPTS COVERED:
  - Decorator with @wraps
  - Class with private methods (prefix _)
  - List comprehension for filtering
  - Dict comprehension for summary
  - Generator with yield
  - File I/O + JSON persistence
  - Exception handling
"""

import json
import os
from functools import wraps       # preserves wrapped function's metadata
from log_entry import LogEntry, LogLevel


LOG_FILE = 'logs.json'            # file where log entries are saved


# ─────────────────────────────────────────────────────────────────────────────
# DECORATOR: @timed
# Wraps any function to measure and print its execution time.
# @wraps(func) ensures the wrapper looks like the original function.
# ─────────────────────────────────────────────────────────────────────────────

def timed(func):
    """Decorator that prints how many milliseconds the function took."""
    import time
    @wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.time()                  # record time before
        result = func(*args, **kwargs)        # call the real function
        ms     = (time.time() - start) * 1000
        print(f'  [{func.__name__}] {ms:.2f}ms')
        return result
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# LOGGER CLASS
# Stores log entries in memory and persists them to a JSON file.
# min_level acts as a filter — entries below it are silently ignored.
# ─────────────────────────────────────────────────────────────────────────────

class Logger:
    """In-memory logger with file persistence and level-based filtering."""

    def __init__(self, source: str = 'app', min_level: LogLevel = LogLevel.DEBUG):
        self.source    = source       # label for where logs come from
        self.min_level = min_level    # entries below this level are ignored
        # Load any previously saved entries from disk on startup
        self._entries: list[LogEntry] = self._load()

    # ── Core log method ───────────────────────────────────────────────────────

    def _log(self, level: LogLevel, message: str):
        """Internal method: create and store a log entry if level is high enough."""
        # Skip entries that are below the minimum level
        # e.g. if min_level=WARNING, DEBUG and INFO are ignored
        if level < self.min_level:
            return

        entry = LogEntry(level=level, message=message, source=self.source)
        self._entries.append(entry)
        print(entry)       # print to console immediately
        self._save()       # persist to disk

    # ── Public convenience methods ────────────────────────────────────────────
    # Each just calls _log with the appropriate level

    def debug(self, msg: str):    self._log(LogLevel.DEBUG, msg)
    def info(self, msg: str):     self._log(LogLevel.INFO, msg)
    def warning(self, msg: str):  self._log(LogLevel.WARNING, msg)
    def error(self, msg: str):    self._log(LogLevel.ERROR, msg)
    def critical(self, msg: str): self._log(LogLevel.CRITICAL, msg)

    # ── Filtering with list comprehensions ────────────────────────────────────

    def get_by_level(self, level: LogLevel) -> list[LogEntry]:
        """Return all entries that match exactly the given level."""
        # List comprehension: [item for item in list if condition]
        return [e for e in self._entries if e.level == level]

    def get_errors_and_above(self) -> list[LogEntry]:
        """Return all ERROR and CRITICAL entries."""
        # >= works because we defined __lt__ on LogLevel (Enum comparison)
        return [e for e in self._entries if e.level >= LogLevel.ERROR]

    def search(self, keyword: str) -> list[LogEntry]:
        """Return entries whose message contains the keyword (case-insensitive)."""
        kw = keyword.lower()
        return [e for e in self._entries if kw in e.message.lower()]

    def summary(self) -> dict:
        """Return a dict of {level_name: count} for all levels."""
        # Dict comprehension: {key: value for item in iterable}
        # For each LogLevel, count how many entries match it
        return {
            level.name: len([e for e in self._entries if e.level == level])
            for level in LogLevel   # iterate over all enum members
        }

    # ── Generator ─────────────────────────────────────────────────────────────

    def stream(self, level: LogLevel = None):
        """
        Generator that yields entries one at a time, sorted by timestamp.
        If level is given, only yields entries of that level.

        Usage:
            for entry in logger.stream():
                print(entry)
        """
        for entry in sorted(self._entries):   # sorted() uses __lt__ (timestamp order)
            if level is None or entry.level == level:
                yield entry   # pause here, return entry, resume on next iteration

    # ── Persistence ───────────────────────────────────────────────────────────

    @timed   # measure how long saving takes
    def _save(self):
        """Write all entries to the JSON file."""
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            # List comprehension: convert each LogEntry to a dict
            json.dump([e.to_dict() for e in self._entries], f, indent=2)

    def _load(self) -> list[LogEntry]:
        """Read entries from the JSON file. Returns [] if file doesn't exist."""
        if not os.path.exists(LOG_FILE):
            return []   # first run — no file yet
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                # List comprehension: rebuild each LogEntry from its saved dict
                return [LogEntry.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, KeyError):
            # JSONDecodeError → file is empty or corrupted
            # KeyError → a required field is missing from saved data
            return []

    def clear(self):
        """Remove all entries from memory and delete the file."""
        self._entries = []
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
