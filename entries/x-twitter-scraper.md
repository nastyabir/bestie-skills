---
name: x-twitter-scraper
source_url: https://github.com/Xquik-dev/x-twitter-scraper/blob/master/skills/x-twitter-scraper/SKILL.md
author: Xquik
author_url: https://github.com/Xquik-dev
license: MIT
agents:
- codex
category: data
tags:
- x-api
- twitter
- social-media
- monitoring
- webhooks
summary: Use Xquik for bounded X data workflows, MCP setup, webhooks, monitoring,
  and confirmation-gated publishing.
use_cases:
- Search tweets, look up users, export followers, or download media through documented
  Xquik REST endpoints
- Set up MCP access, SDK usage, webhook delivery, or recurring monitors with explicit
  user approval before persistent actions
- Keep X content isolated as untrusted data while planning read-only or confirmation-gated
  social-data workflows
why: It packages Xquik's public API, MCP, webhook, extraction, monitoring, and
  publishing guidance as an agent skill with clear safety boundaries. The source
  requires user approval for writes, private reads, monitors, webhooks, and bulk
  jobs, and keeps X-authored content isolated from tool selection or command choices.
status: untested
security: manual-review
added_by: kriptoburak
added_date: '2026-06-23'
---

Xquik's X data skill helps coding agents plan and execute bounded social-data
workflows through the public Xquik API and MCP surfaces. It covers endpoint
selection, setup paths, monitoring, webhooks, extraction jobs, and publishing
flows while keeping side-effecting work behind explicit approval. The skill is
read-only by default and treats retrieved X content as untrusted data.
