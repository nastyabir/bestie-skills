from pathlib import Path

import pytest

from entry import parse_entry, load_entry

VALID = """---
name: demo
agents:
  - claude-code
use_cases:
  - Do a thing
---

Body line one.
Body line two.
"""


def test_parse_entry_splits_frontmatter_and_body():
    fm, body = parse_entry(VALID)
    assert fm["name"] == "demo"
    assert fm["agents"] == ["claude-code"]
    assert body.strip() == "Body line one.\nBody line two."


def test_parse_entry_without_frontmatter_raises():
    with pytest.raises(ValueError):
        parse_entry("no frontmatter here")


def test_load_entry_reads_file(tmp_path):
    p = tmp_path / "demo.md"
    p.write_text(VALID, encoding="utf-8")
    entry = load_entry(p)
    assert entry["frontmatter"]["name"] == "demo"
    assert entry["path"] == p
    assert "Body line one." in entry["body"]
