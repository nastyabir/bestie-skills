# Contributing to bestie-skills

Thanks for adding a skill! This is a **links-only catalog**. The golden rule:

> **Link, never copy.** Do not paste a third-party skill's code into this repo.
> Add metadata and a link to the original source, crediting its author and license.

## Add a skill

1. Create `entries/<skill-name>.md` (kebab-case; `<skill-name>` must equal the
   `name` field).
2. Fill the frontmatter. All fields are required:

   | Field | Meaning |
   | --- | --- |
   | `name` | kebab-case id, matches the filename |
   | `source_url` | canonical link to the skill (repo or raw file) |
   | `author` | original author + handle |
   | `license` | the source's license (or `unknown`) |
   | `agents` | any of: `claude-code`, `codex`, `cursor`, `any` |
   | `category` | `coding`, `research`, `writing`, `data`, `devops`, `workflow`, `meta` |
   | `summary` | one line |
   | `use_cases` | when to use it (>=1) |
   | `why` | why it is recommended |
   | `status` | leave as `untested` (maintainer promotes it) |
   | `security` | leave as `manual-review` (CI/maintainer sets it) |
   | `added_by` | your handle |
   | `added_date` | `YYYY-MM-DD` |

3. Regenerate the README:

   ```bash
   python scripts/build_readme.py
   ```

4. Validate locally:

   ```bash
   python scripts/validate_entries.py entries/
   python scripts/security_scan.py entries/
   ```

5. Open a PR. CI runs validation, the README freshness check, and the security
   scan. A maintainer reviews and merges.

## Review criteria

- Source, author, and license are cited; no third-party code is copied.
- `why` and `use_cases` are specific and informative.
- The security scan is clean (no prompt-injection / exfiltration patterns).
