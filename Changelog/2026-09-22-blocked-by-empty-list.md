---
date: 2026-09-22
files:
  - "[[Workflows/actions-index.py]]"
---
# `blocked_by: []` no longer reads as blocked

**Change:** added `"[]"` to `NOT_BLOCKED` in `actions-index.py`.

**Why:** YAML `blocked_by: []` arrives from the frontmatter parser as the literal string `[]`, which was not in the not-blocked set — so every note using the empty-list form printed `blocked`, and `--brief` / Start Here excluded it. Surfaced in the 2026-09-22 17:5x quick refresh: 5 live notes wrongly marked, including the P1 `Connor - Avoid deep-stacking chairs for the 9-27 community-group pod` (due 9/27) and the new `Connor - Set up Rock Group Leader Toolbox and take Boot Camp attendance`. Same bug class as the 2026-08-18 `"none"` fix, different spelling. After the fix only the two genuinely blocked on-hold notes remain marked.

**Second fix, same run — the inverse bug.** `parse_fm` stores YAML block lists under `blocked_by[]`, leaving the `blocked_by` scalar empty, and `load()` only read the scalar. So a note that is genuinely blocked with the multi-line form (`blocked_by:` + `  - "[[...]]"`) printed as **actionable**: `Connor - Add peer-discussion prompts to the 9-27 closing Host item` was showing in Start Here though it waits on Brandon + Simba's prompts. `load()` now falls back to the joined `blocked_by[]` list. Net effect on 2026-09-22: the blocked set went from 7 (5 wrong) to 3 (all real).
