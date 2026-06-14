"""Layered security scan for entries: regex patterns -> source fetch -> Claude review."""
import re

# (flag name, compiled regex). Case-insensitive where it matters.
INJECTION_PATTERNS = [
    ("instruction-override", re.compile(
        r"ignore\s+(all\s+|the\s+)?(previous|above|prior)\s+instructions"
        r"|disregard\s+(the\s+)?(above|previous)", re.IGNORECASE)),
    ("data-exfiltration", re.compile(
        r"(send|post|exfiltrate|upload|leak)\b[^.\n]{0,40}\b"
        r"(api[_\s-]?key|token|secret|password|credentials?)", re.IGNORECASE)),
    ("system-prompt-probe", re.compile(
        r"(reveal|print|repeat|show)\b[^.\n]{0,30}\b(system\s+prompt|instructions)",
        re.IGNORECASE)),
    ("hidden-characters", re.compile("[​‌‍⁠﻿]")),
]


def scan_text(text):
    """Return a sorted list of flag names triggered by the text ([] == clean)."""
    flags = set()
    for name, pattern in INJECTION_PATTERNS:
        if pattern.search(text):
            flags.add(name)
    return sorted(flags)
