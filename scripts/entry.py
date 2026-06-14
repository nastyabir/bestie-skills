"""Parse and load bestie-skills entry files (YAML frontmatter + markdown body)."""
import datetime
from pathlib import Path

import yaml

_DELIM = "---"


def _normalize_scalar(value):
    # PyYAML resolves unquoted ISO dates to datetime.date; the schema wants strings.
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


def parse_entry(text):
    """Split a raw entry into (frontmatter dict, body str).

    Raises ValueError if the text does not start with a YAML frontmatter block.
    """
    if not text.lstrip().startswith(_DELIM):
        raise ValueError("entry must start with a '---' frontmatter block")
    after_open = text.split(_DELIM, 2)
    if len(after_open) < 3:
        raise ValueError("frontmatter block is not closed with '---'")
    _, raw_fm, body = after_open
    frontmatter = yaml.safe_load(raw_fm) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    frontmatter = {k: _normalize_scalar(v) for k, v in frontmatter.items()}
    return frontmatter, body


def load_entry(path):
    """Read an entry file and return {'frontmatter', 'body', 'path'}."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_entry(text)
    return {"frontmatter": frontmatter, "body": body, "path": path}
