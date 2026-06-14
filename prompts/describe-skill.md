# Prompt: describe your skill for the catalog

Adding your own skill? Don't hand-write the form — let your agent read your repo and fill
it in for you. Open your skill's repository in **Claude Code** (or any coding agent), paste
the prompt below, then copy the result into the
[Add a skill form](https://github.com/nastyabir/bestie-skills/issues/new?template=add-skill.yml).

---

```
You are preparing a submission to the bestie-skills catalog — a links-only index of
AI-agent skills. Read THIS repository, especially the skill definition (a SKILL.md, a
.claude/commands/*.md slash command, an AGENTS.md, or the main prompt/instructions file),
and produce the catalog entry fields below. Ground every claim in the actual file
contents — do not invent capabilities.

Output exactly these fields and nothing else:

- name: a kebab-case id (lowercase a-z, 0-9, hyphens), e.g. my-cool-skill
- source_url: the canonical PUBLIC url to the skill (this repo, or the raw skill file)
- author: name and/or @handle
- author_url: link to the author's profile (optional, e.g. a GitHub profile)
- license: the repo's license, or "unknown"
- agents: which agents it works with — any of: claude-code, codex, cursor, any
- category: exactly one of: coding, research, writing, data, devops, workflow, meta
- tags: 2–5 topic tags, comma-separated, lowercase-with-hyphens
        (e.g. marketing, design, ai-productivity, data-analysis)
- summary: one sentence — what it does
- use_cases: 3–5 bullets — concrete situations where you'd reach for it
- why: 2–3 sentences — what makes it good, what failure modes it prevents, what's distinctive
- description: one short paragraph — how it works, its modes, notable details and caveats

Before you finish, scan the skill for org-specific names, internal URLs, client names, or
secrets. If you find any, STOP and list them so I can scrub them before publishing publicly.

Be specific and honest — a reader should know exactly when to use this skill.
```

---

The catalog stores a **link and metadata only** — host the skill in your own repo or gist;
we never copy its code. After you submit the form, a bot validates your entry, runs the
security scan, and opens a pull request for a maintainer to review.
