---
name: ab-test
source_url: https://github.com/nastyabir/ab-test-skill/blob/main/ab-test.md
author: nastyabir
license: MIT
agents:
- claude-code
category: data
tags:
- ab-testing
- statistics
- experimentation
- data-analysis
- product-analytics
summary: Design and analyze A/B tests rigorously — sample-size/MDE calculation plus
  a full statistical-analysis pipeline that picks the statistically correct test instead
  of a naive default.
use_cases:
- 'Size an experiment before launch: per-group sample size from baseline, MDE, alpha
  and power, plus fixed-horizon vs. sequential choice'
- 'Analyze results correctly: pick the right test (z-test, Welch t-test, Mann-Whitney,
  bootstrap) from metric type and distribution diagnostics'
- Handle money / heavy-tailed metrics with bootstrap and decile comparison to catch
  cannibalization
- Correct for multiple comparisons (BH / FDR) when testing 3+ variants
why: 'It encodes a complete, opinionated A/B-testing methodology (the experiment-fest
  guidebook) with 10 "golden rules" and ready-to-run Python, so the agent chooses
  statistically correct procedures rather than defaulting to a t-test. It covers the
  failure modes teams actually hit: peeking, non-normal revenue, unequal variances,
  and multiple-comparison inflation.'
status: untested
security: manual-review
added_by: nastyabir
added_date: '2026-06-14'
---

A Claude Code slash command with two modes. **design** collects experiment parameters and computes sample size (Cohen's h/d effect sizes), recommends fixed-horizon vs. sequential (mSPRT) testing, and emits a pre-launch design card with a randomization checklist. **analyze** runs descriptive stats, normality (Shapiro-Wilk/KS) and variance-homogeneity (Levene) diagnostics, selects and runs the appropriate test, buckets >1M observations, does decile comparison for heterogeneous effects, multiple-comparison correction (BH/Bonferroni), and post-hoc power analysis — then a verdict with recommendations. Includes a formula/definitions reference. The skill text and outputs are in Russian.
