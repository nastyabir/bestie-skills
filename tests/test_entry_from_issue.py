from pathlib import Path

from entry_from_issue import parse_issue_form, fields_from_issue
from new_skill import build_entry_text
from entry import parse_entry
from validate_entries import load_schema, validate_entry

BODY = """### Skill name

my-skill

### Source URL

https://github.com/me/my-skill

### Author

me (Me)

### License

MIT

### Agents

claude-code, codex

### Category

workflow

### Tags

ai-productivity, Marketing

### Summary

Does a useful thing.

### Use cases

Size the experiment: baseline, MDE, alpha and power
Analyze results with the right test

### Why recommend it

It is great.

### Description

_No response_
"""


def test_parse_issue_form_maps_labels_and_handles_no_response():
    p = parse_issue_form(BODY)
    assert p["name"] == "my-skill"
    assert p["agents"] == "claude-code, codex"
    assert p["use_cases"] == "Size the experiment: baseline, MDE, alpha and power\nAnalyze results with the right test"
    assert p["body"] == ""


def test_fields_from_issue_builds_schema_valid_entry():
    fields = fields_from_issue(parse_issue_form(BODY), added_by="nastyabir")
    fields["added_date"] = "2026-06-15"
    text = build_entry_text(fields)
    fm, body = parse_entry(text)
    entry = {"frontmatter": fm, "body": body, "path": Path("entries/my-skill.md")}
    assert validate_entry(entry, load_schema()) == []
    assert fm["agents"] == ["claude-code", "codex"]
    # a use case containing commas stays ONE item (newline-split, not comma-split)
    assert fm["use_cases"] == [
        "Size the experiment: baseline, MDE, alpha and power",
        "Analyze results with the right test",
    ]
    assert fm["tags"] == ["ai-productivity", "marketing"]
