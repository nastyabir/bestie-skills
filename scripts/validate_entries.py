"""Validate entry frontmatter against schema, plus name/filename and uniqueness rules."""
import json
import sys
from pathlib import Path

from jsonschema import Draft7Validator

from entry import load_entry

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "entry.schema.json"


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_entry(entry, schema):
    """Return a list of error strings for one loaded entry ([] == valid)."""
    fm = entry["frontmatter"]
    path = Path(entry["path"])
    errors = []
    validator = Draft7Validator(schema)
    for err in sorted(validator.iter_errors(fm), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "(root)"
        errors.append(f"{path.name}: {loc}: {err.message}")
    if fm.get("name") and fm["name"] != path.stem:
        errors.append(
            f"{path.name}: name '{fm.get('name')}' must match filename stem '{path.stem}'"
        )
    return errors


def validate_dir(entries_dir, schema=None):
    """Validate every entries/*.md file and check name uniqueness."""
    schema = schema or load_schema()
    entries_dir = Path(entries_dir)
    errors = []
    seen = {}
    for path in sorted(entries_dir.glob("*.md")):
        try:
            entry = load_entry(path)
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        errors.extend(validate_entry(entry, schema))
        name = entry["frontmatter"].get("name")
        if name in seen:
            errors.append(f"{path.name}: duplicate name '{name}' (also in {seen[name]})")
        elif name:
            seen[name] = path.name
    return errors


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    entries_dir = Path(argv[0]) if argv else ROOT / "entries"
    errors = validate_dir(entries_dir)
    if errors:
        print(f"FAIL: {len(errors)} validation error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: all entries valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
