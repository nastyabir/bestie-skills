from pathlib import Path

import pytest

from new_skill import build_entry_text, create_entry, split_list
from entry import parse_entry
from validate_entries import load_schema, validate_entry

GOOD = {
    "name": "demo", "source_url": "https://e.com/s", "author": "a",
    "license": "MIT", "agents": ["claude-code"], "category": "workflow",
    "summary": "s", "use_cases": ["u1", "u2"], "why": "w",
    "added_by": "nastyabir", "added_date": "2026-06-15", "body": "hello world",
}


def test_split_list_handles_commas_and_newlines():
    assert split_list("a, b\nc ,, d") == ["a", "b", "c", "d"]


def test_build_entry_text_is_schema_valid():
    text = build_entry_text(GOOD)
    fm, body = parse_entry(text)
    entry = {"frontmatter": fm, "body": body, "path": Path("entries/demo.md")}
    assert validate_entry(entry, load_schema()) == []
    assert "hello world" in body


def test_build_entry_text_injects_defaults():
    f = dict(GOOD)
    del f["added_date"]
    text = build_entry_text(f)
    assert "status: untested" in text
    assert "security: manual-review" in text
    assert "added_date:" in text


def test_create_entry_writes_then_refuses_overwrite(tmp_path):
    p = create_entry(GOOD, entries_dir=tmp_path)
    assert p.exists()
    with pytest.raises(FileExistsError):
        create_entry(GOOD, entries_dir=tmp_path)


def test_create_entry_rejects_bad_name(tmp_path):
    with pytest.raises(ValueError):
        create_entry(dict(GOOD, name="../evil"), entries_dir=tmp_path)
