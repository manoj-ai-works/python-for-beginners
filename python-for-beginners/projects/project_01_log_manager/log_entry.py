"""
log_entry.py — LogEntry model and LogLevel enum.

CONCEPTS COVERED:
  - Enum — a fixed set of named constants
  - @dataclass — auto-generates __init__, __repr__, __eq__
  - field(default_factory=...) — safe mutable/callable defaults
  - Dunder methods: __str__, __repr__, __lt__, __post_init__
  - @classmethod — alternative constructor
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum            # Enum gives us named, ordered constants


# ─────────────────────────────────────────────────────────────────────────────
# ENUM: LOG LEVELS
# An Enum is a set of symbolic names bound to unique values.
# Using an Enum instead of plain strings prevents typos like "ERORR".
# Each member has a .name (string) and .value (int).
# ─────────────────────────────────────────────────────────────────────────────

class LogLevel(Enum):
    DEBUG    = 1   # lowest severity — detailed diagnostic info
    INFO     = 2   # general information about normal operation
    WARNING  = 3   # something unexpected, but not an error
    ERROR    = 4   # a real problem occurred
    CRITICAL = 5   # highest severity — app may not recover

    def __str__(self):
        # Called when we do str(level) or f"{level}"
        # Returns 'DEBUG', 'INFO', etc. instead of 'LogLevel.DEBUG'
        return self.name

    def __lt__(self, other):
        # Allows comparison: LogLevel.DEBUG < LogLevel.ERROR → True
        # Used to filter entries below a minimum level
        return self.value < other.value


# ─────────────────────────────────────────────────────────────────────────────
# DATACLASS: LOG ENTRY
# @dataclass auto-generates __init__ and __repr__ from the field annotations.
# We only need to write the methods that have custom logic.
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class LogEntry:
    """Represents a single log entry with level, message, source, and timestamp."""

    level:   LogLevel          # severity level (DEBUG, INFO, etc.)
    message: str               # the log message text
    source:  str = 'app'       # which part of the app logged this (default: 'app')
    # field(default_factory=datetime.now) calls datetime.now() for EACH new instance
    # Never use timestamp: datetime = datetime.now() — that captures one time for all!
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # __post_init__ runs automatically after __init__
        # Use it for validation that can't be expressed in the type annotation
        if not self.message.strip():
            raise ValueError('Log message cannot be empty')

    def __str__(self):
        # Human-readable format: [2024-01-15 10:30:00] [INFO] [app] Server started
        ts = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')   # format the datetime
        return f'[{ts}] [{self.level}] [{self.source}] {self.message}'

    def __repr__(self):
        # Developer-readable format — shown in REPL and inside collections
        return f'LogEntry(level={self.level}, message={self.message!r})'

    def __lt__(self, other):
        # Allows sorting entries by time: sorted(entries) works automatically
        return self.timestamp < other.timestamp

    # ── Serialization ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Convert to a plain dict for JSON serialization."""
        return {
            'timestamp': self.timestamp.isoformat(),  # ISO format: '2024-01-15T10:30:00'
            'level':     self.level.name,             # store the name string, not the int
            'source':    self.source,
            'message':   self.message,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'LogEntry':
        """
        Rebuild a LogEntry from a dict (e.g. loaded from JSON).
        @classmethod receives the class (cls) instead of an instance (self).
        """
        return cls(
            level=LogLevel[data['level']],                    # 'INFO' → LogLevel.INFO
            message=data['message'],
            source=data.get('source', 'app'),                 # default if key missing
            timestamp=datetime.fromisoformat(data['timestamp']),  # parse ISO string back
        )
