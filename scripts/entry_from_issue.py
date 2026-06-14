"""Build a catalog entry from a GitHub issue-form submission (used by CI).

Reads the rendered issue body from $ISSUE_BODY and the submitter from
$ISSUE_AUTHOR, writes entries/<name>.md, and prints the skill name on stdout.
"""
import os

from new_skill import create_entry, split_list, split_lines, normalize_tags

LABEL_TO_FIELD = {
    "Skill name": "name",
    "Source URL": "source_url",
    "Author": "author",
    "License": "license",
    "Agents": "agents",
    "Category": "category",
    "Tags": "tags",
    "Summary": "summary",
    "Use cases": "use_cases",
    "Why recommend it": "why",
    "Description": "body",
}


def parse_issue_form(body):
    """Parse a rendered GitHub issue-form body into {field_id: value}."""
    out, current, buf = {}, None, []

    def flush():
        if current is not None:
            val = "\n".join(buf).strip()
            out[current] = "" if val == "_No response_" else val

    for line in (body or "").splitlines():
        if line.startswith("### "):
            flush()
            current = LABEL_TO_FIELD.get(line[4:].strip())
            buf = []
        elif current is not None:
            buf.append(line)
    flush()
    return out


def fields_from_issue(parsed, *, added_by):
    """Map parsed issue fields to entry fields."""
    return {
        "name": parsed.get("name", "").strip(),
        "source_url": parsed.get("source_url", "").strip(),
        "author": parsed.get("author", "").strip(),
        "license": parsed.get("license", "").strip() or "unknown",
        "agents": split_list(parsed.get("agents", "")),
        "category": parsed.get("category", "").strip(),
        "tags": normalize_tags(split_list(parsed.get("tags", ""))),
        "summary": parsed.get("summary", "").strip(),
        "use_cases": split_lines(parsed.get("use_cases", "")),
        "why": parsed.get("why", "").strip(),
        "added_by": added_by,
        "body": parsed.get("body", "").strip(),
    }


def main():
    body = os.environ.get("ISSUE_BODY", "")
    added_by = os.environ.get("ISSUE_AUTHOR", "").strip() or "unknown"
    fields = fields_from_issue(parse_issue_form(body), added_by=added_by)
    create_entry(fields)
    print(fields["name"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
