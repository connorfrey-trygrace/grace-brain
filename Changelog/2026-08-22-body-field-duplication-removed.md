---
type: changelog
date: 2026-08-22
tier: 3
touches: ["[[Workflows/actions-index.py]]", "[[Workflows/split-note-log.py]]", "[[Workflows/Open-Actions-Reference]]", "[[Workflows/Open-Actions-Tracker]]", "[[Workflows/Open-Actions-Transcript-Steps]]", "[[Workflows/text-message-sync]]", "[[Workflows/m365-to-obsidian-sync]]", "[[Workflows/note-history-splitting]]"]
trigger: "Connor, 2026-08-22 — \"strip em and make sure no workflows recreate this problem\""
---
# Frontmatter values no longer live in note bodies — the duplication is deleted, and the schema that produced it is fixed

**The defect was structural, not cosmetic.** Every action note carried its frontmatter values a second time as body bullets (`- **Priority**: P2 — …`, `- **Last mentioned**: 2026-08-12`). Syncs update frontmatter and leave the prose, so the two copies drift. The 2026-08-10 response was a *field-authority rule* — frontmatter wins — which settled who wins an argument without stopping the arguments. **47 rows had drifted by 2026-08-22.**

## What was removed, and what was kept

Rationale was never the problem; the restated literal was. Measured first: **82 Priority bullets, and 0 of them were value-only** — a blanket strip would have deleted 82 pieces of reasoning. So the transformation preserves the prose and drops the value.

| gone | replaced by | count |
|---|---|---|
| `- **Priority**: P2 — <why>` | `- **Priority rationale**: <why>` | 82 |
| `- **Deadline**: <date> — <why>` | `- **Deadline rationale**: <why>` | 69 |
| `- **Needs-by**: <date> — <why>` | `- **Needs-by rationale**: <why>` | 24 |
| `- **Last mentioned**: <date>` | deleted (47 of 50 held no reasoning at all) | 50 |
| `- **Added**: <date>` | deleted, or `- **Status history**:` where it carried move history | 59 |
| `- **On hold**:` / `- **Waiting on**:` | `- **Status history**:` | 2 |

**149 renamed, 114 deleted, 8 compound bullets split, 16 merged into an existing rationale line, 1 kept as a `- **Note**:`.** `- **Deadline rationale**:` and `- **Needs-by rationale**:` were not invented here — 18 and 23 notes already used them; this makes the convention universal.

**Deliberately kept:** the prose `- **Status**:` bullet (narrative, not a value, and guarded by its own contradiction check) and `- **Blocked by**:` / `- **Blocks**:`, which carry wikilinked dependency edges that [[Workflows/split-note-log]] reads as live state. Those remain a known duplication and a deliberate exception.

## The check is now presence, not comparison

`--drift` compared body values against frontmatter — so it could only ever find the ones that had *already* gone wrong, and it ran only in the weekly refresh. It is replaced by `redundant_body_fields()`, which fires on the **existence** of a banned bullet, and prints in the **default** index output as well as `--drift`. Step 0 is not optional in either sweep mode, so a reintroduced bullet surfaces on the very next run rather than after it has drifted.

Verified: **10/10 unit cases** on the detector (fires on Priority/Last mentioned/Needs-by/Added/Chase-by bullets; silent on the rationale forms, on `- **Status**:`, on `- **Blocked by**:`, and on a date mentioned in ordinary prose). Full sweep output diffed against the pre-patch script: **the only difference is the new block.** Drift is **0 rows across 82 notes**.

## Every path that could recreate it

Fixing the notes without fixing the schema would have refilled the folder within a week. Five places prescribed these bullets and all five now prescribe the rationale form: the item-body schema in [[Workflows/Open-Actions-Reference]], the drift-handling guidance and Step 0 notes in [[Workflows/Open-Actions-Tracker]], the priority-override instruction in [[Workflows/Open-Actions-Transcript-Steps]], the item-schema line in [[Workflows/text-message-sync]], and the **literal note template** in [[Workflows/m365-to-obsidian-sync]]'s Run Log health check — which was the worst offender, since it emitted four banned bullets every time it fired.

## One thing that would have broken silently

[[Workflows/split-note-log]] classifies "structural bullets" — live state that must not be swept into the log — by an explicit name list. `Priority rationale`, `Status history` and `Note` were not on it, so the renamed live fields would have been moved into the companion log as if they were dated history, on the next note big enough to split. Added, with the old names kept for archived notes. Regression-diffed across all 82 notes: **one intended difference** — the Marketing note's converted `Waiting on` line now correctly stays live instead of being swept into the log.
