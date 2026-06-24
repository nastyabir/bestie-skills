---
name: llm-council
source_url: https://github.com/nastyabir/llm-council-skill
author: nastyabir — port of Andrej Karpathy's llm-council
author_url: https://github.com/nastyabir
license: MIT
agents:
- claude-code
category: research
tags:
- llm
- multi-model
- openrouter
- peer-review
- ensemble
- ai-productivity
summary: Ask a question to a council of frontier LLMs (GPT 5.5, Gemini 3.1 Pro, Grok
  4.3, Claude Opus 4.8) via OpenRouter; they anonymously peer-review each other's
  answers and a chairman model synthesizes one final answer.
use_cases:
- Get a well-vetted answer to a high-stakes or ambiguous question by polling several
  frontier models instead of trusting one
- Surface disagreement between models — the anonymous peer-review ranking shows where
  they diverge
- Sanity-check an analysis, methodology call, or decision against an ensemble before
  committing
- Reduce single-model blind spots and sycophancy via cross-model critique with a synthesized
  verdict
why: A faithful CLI/skill port of Andrej Karpathy's [llm-council](https://github.com/karpathy/llm-council)
  (the original is a FastAPI + React web app). It encodes the 3-stage council pattern
  — independent answers, anonymous peer-review with shuffled labels so a model can't
  favor its own answer, then chairman synthesis — as a single Claude Code slash command.
  The orchestrator is standard-library-only Python (no pip install), routes every
  model through one OpenRouter key, and degrades gracefully when a member times out.
  All credit for the design goes to @karpathy; this repo is an independent reimplementation.
status: untested
security: manual-review
added_by: nastyabir
added_date: '2026-06-24'
---

Run `/llm-council <question>` in Claude Code, or `python3 scripts/llm_council.py "<question>" --markdown` standalone. Output is the chairman's final answer plus a peer-review ranking table and each member's individual response. The council/chairman lineup and timeouts are an editable config block at the top of the script. Requires an `OPENROUTER_API_KEY` with access to the configured models. Original concept and credit: Andrej Karpathy — https://github.com/karpathy/llm-council
