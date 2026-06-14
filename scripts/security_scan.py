"""Layered security scan for entries: regex patterns -> source fetch -> Claude review."""
import re
from urllib.parse import urlparse

import requests

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


_GH_BLOB = re.compile(
    r"^https://github\.com/([^/]+)/([^/]+)/blob/(.+)$")


def raw_url_for(source_url):
    """Return a directly-fetchable raw URL for a skill file, or None.

    Handles GitHub blob URLs and plain links to .md files. A repo root (no
    direct file) returns None -> the entry must go to manual review.
    """
    m = _GH_BLOB.match(source_url)
    if m:
        owner, repo, rest = m.groups()
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{rest}"
    path = urlparse(source_url).path
    if path.endswith(".md") or "raw.githubusercontent.com" in source_url:
        return source_url
    return None


def fetch_source(source_url, *, timeout=10):
    """Fetch raw skill text read-only. Returns text, or None if not fetchable."""
    raw = raw_url_for(source_url)
    if raw is None:
        return None
    try:
        resp = requests.get(raw, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    return resp.text
