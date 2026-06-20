---
name: ax-extract-workflow
source_url: https://github.com/Necmttn/ax/blob/main/skills/ax-extract-workflow/SKILL.md
author: Necmttn
author_url: https://github.com/Necmttn
license: AGPL-3.0-only
agents:
  - claude-code
  - codex
category: workflow
tags:
  - workflow
  - ai-productivity
  - observability
  - session-recall
summary: Reconstruct shipped coding-agent workflows from local ax sessions, commits, skills, and subagent delegations.
use_cases:
  - Reconstruct how a PR, feature, demo, or artifact was shipped from a date, commit, or topic.
  - Turn local session, commit, skill, and subagent evidence into an ordered workflow narrative.
  - Draft a reusable workflow recipe from a successful agent run while keeping transcripts local.
why: It links workflow recall to local evidence instead of memory or guesswork, which helps agents explain how a shipped result was produced and how to repeat it.
status: untested
security: manual-review
added_by: Necmttn
added_date: "2026-06-20"
---

A workflow reconstruction skill for ax users. It resolves a date, commit, or topic, queries local ax session and recall data, inspects relevant sessions, and returns an ordered skill arc plus key decisions. The catalog entry links to the upstream skill only; no skill code is copied here.
