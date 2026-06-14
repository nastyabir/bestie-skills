from pathlib import Path

from validate_entries import validate_entry, validate_dir, load_schema

SCHEMA = load_schema()

GOOD_FM = {
    "name": "demo",
    "source_url": "https://example.com/skill",
    "author": "someone",
    "license": "MIT",
    "agents": ["claude-code"],
    "category": "workflow",
    "tags": ["workflow"],
    "summary": "A demo skill.",
    "use_cases": ["Do a thing"],
    "why": "It is useful.",
    "status": "untested",
    "security": "manual-review",
    "added_by": "nastyabir",
    "added_date": "2026-06-15",
}


def _entry(fm, name="demo"):
    return {"frontmatter": fm, "body": "x", "path": Path(f"entries/{name}.md")}


def test_valid_entry_has_no_errors():
    assert validate_entry(_entry(GOOD_FM), SCHEMA) == []


def test_missing_field_is_reported():
    fm = dict(GOOD_FM)
    del fm["why"]
    errors = validate_entry(_entry(fm), SCHEMA)
    assert any("why" in e for e in errors)


def test_bad_enum_is_reported():
    fm = dict(GOOD_FM, category="nonsense")
    errors = validate_entry(_entry(fm), SCHEMA)
    assert any("category" in e for e in errors)


def test_bad_author_url_is_reported():
    fm = dict(GOOD_FM, author_url="not-a-url")
    errors = validate_entry(_entry(fm), SCHEMA)
    assert any("author_url" in e for e in errors)


def test_missing_tags_is_reported():
    fm = dict(GOOD_FM)
    del fm["tags"]
    errors = validate_entry(_entry(fm), SCHEMA)
    assert any("tags" in e for e in errors)


def test_bad_tag_slug_is_reported():
    fm = dict(GOOD_FM, tags=["Not A Slug"])
    errors = validate_entry(_entry(fm), SCHEMA)
    assert any("tags" in e for e in errors)


def test_name_must_match_filename():
    errors = validate_entry(_entry(GOOD_FM, name="other"), SCHEMA)
    assert any("filename" in e for e in errors)


def test_duplicate_names_reported(tmp_path):
    body = (
        "---\nname: dup\nsource_url: https://e.com\nauthor: a\nlicense: MIT\n"
        "agents: [claude-code]\ncategory: workflow\ntags: [workflow]\nsummary: s\nuse_cases: [u]\n"
        "why: w\nstatus: untested\nsecurity: manual-review\nadded_by: n\n"
        "added_date: 2026-06-15\n---\nbody\n"
    )
    (tmp_path / "a.md").write_text(body, encoding="utf-8")
    (tmp_path / "b.md").write_text(body, encoding="utf-8")
    errors = validate_dir(tmp_path, SCHEMA)
    assert any("duplicate" in e.lower() for e in errors)
