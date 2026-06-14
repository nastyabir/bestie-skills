"""Interactive scaffolder for a new bestie-skills catalog entry.

Run:  python scripts/new_skill.py
Writes entries/<name>.md, regenerates README, and validates.
The catalog stores a link + metadata only — host your skill in your own repo/gist.
"""
import datetime
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = ROOT / "entries"

CATEGORIES = ["coding", "research", "writing", "data", "devops", "workflow", "meta"]
AGENTS = ["claude-code", "codex", "cursor", "any"]
FIELD_ORDER = ["name", "source_url", "author", "license", "agents", "category",
               "summary", "use_cases", "why", "status", "security",
               "added_by", "added_date"]
_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _with_defaults(fields):
    f = dict(fields)
    f.setdefault("status", "untested")
    f.setdefault("security", "manual-review")
    f.setdefault("added_date", datetime.date.today().isoformat())
    return f


def build_entry_text(fields):
    """Render entry markdown (frontmatter + body) from a fields dict."""
    f = _with_defaults(fields)
    fm = {k: f[k] for k in FIELD_ORDER if k in f and f[k] not in (None, "", [])}
    front = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    body = (f.get("body") or "").strip() or \
        "<Add a longer description: example usage, notes, and caveats.>"
    return f"---\n{front}\n---\n\n{body}\n"


def create_entry(fields, entries_dir=ENTRIES_DIR):
    """Write entries/<name>.md. Returns the path. Refuses bad names and overwrites."""
    name = (fields.get("name") or "").strip()
    if not _NAME_RE.match(name):
        raise ValueError(f"invalid skill name {name!r}: use kebab-case [a-z0-9-]")
    path = Path(entries_dir) / f"{name}.md"
    if path.exists():
        raise FileExistsError(f"entries/{name}.md already exists")
    path.write_text(build_entry_text(fields), encoding="utf-8")
    return path


def split_list(text):
    """Split a comma- or newline-separated string into a clean list."""
    parts = re.split(r"[,\n]", text or "")
    return [p.strip() for p in parts if p.strip()]


def _prompt(label, *, required=True, choices=None):
    while True:
        val = input(f"{label}: ").strip()
        if not val and not required:
            return ""
        if not val:
            print("  required — please enter a value.")
            continue
        if choices and val not in choices:
            print(f"  must be one of {choices}")
            continue
        return val


def main():
    print("Add a new skill to the bestie-skills catalog.")
    print("We store a link + metadata only — host your skill in your own repo/gist.\n")
    fields = {}
    fields["name"] = _prompt("Skill name (kebab-case)")
    fields["source_url"] = _prompt("Source URL (link to your skill)")
    fields["author"] = _prompt("Author (name / handle)")
    fields["license"] = _prompt("License (or 'unknown')")
    print(f"Agents — choose from {AGENTS} (comma-separated):")
    agents = []
    while not agents:
        agents = [a for a in split_list(input("  agents: ")) if a in AGENTS]
        if not agents:
            print(f"  pick at least one of {AGENTS}")
    fields["agents"] = agents
    fields["category"] = _prompt(f"Category {CATEGORIES}", choices=CATEGORIES)
    fields["summary"] = _prompt("One-line summary")
    use_cases = split_list(input("Use cases (comma- or newline-separated): "))
    fields["use_cases"] = use_cases or [_prompt("One use case")]
    fields["why"] = _prompt("Why is it recommended?")
    fields["added_by"] = _prompt("Your handle (added_by)")
    body = input("Longer description (optional, Enter to skip): ").strip()
    if body:
        fields["body"] = body

    try:
        path = create_entry(fields)
    except (ValueError, FileExistsError) as exc:
        print(f"\nError: {exc}")
        return 1
    print(f"\nWrote {path.relative_to(ROOT)}")

    import build_readme
    import validate_entries
    build_readme.main([])
    errors = validate_entries.validate_dir(ENTRIES_DIR)
    if errors:
        print("Validation issues:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nValidated OK. Next steps:")
    print(f"  git add entries/{fields['name']}.md README.md")
    print(f"  git commit -m 'add skill: {fields['name']}'")
    print("  git push  &&  open a pull request")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
