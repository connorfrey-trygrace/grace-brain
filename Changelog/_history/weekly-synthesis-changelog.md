---
type: changelog-history
governs: "[[Workflows/weekly-synthesis]]"
tags: [changelog]
---
# weekly-synthesis-changelog — changelog (pre-2026-08-12 history)

Split out of the procedure file on **2026-08-12** so procedure text stays cheap to read. **Never read on a normal run.** New changes go in their own dated file under `/Changelog/`, not here.

---

## Changelog
- 2026-06-03: Initial creation. Tier 3 (new workflow file). Triggered by Connor's request.
- 2026-06-03: Step 1 updated to prefer `processed_date` frontmatter field for scope determination; mtime retained as fallback only. Tier 2. Trigger: observation during first weekly synthesis run (mtime proxy identified as fragile).
- 2026-06-07: Added "Source of truth" section explicitly prohibiting calendar or other non-transcript sources. Tier 2. Trigger: scheduled task incorrectly pulled from Google Calendar when vault folder was not mounted.
- 2026-06-15: Added a "System health check" step (Step 3) that runs the light system audit per [[Workflows/system-audit]] and appends results to the weekly note; added it to the Step 5 report. Folds the recurring health check into the existing Friday run. Tier 2 (new procedural step). Trigger: Connor's request to schedule the audit (chose weekly cadence, folded into synthesis).
- 2026-07-24: Repointed Step 2 and Step 3 (aging report) from the retired `/Trackers/Open Actions.md` to the current storage — per-action notes in `/Trackers/Actions/` aggregated by `/Trackers/Open Actions.base` — following the 2026-07-21 Bases migration; mapped the old "Stale" list to the frontmatter-driven "Flagged / Needs Review" view. Tier 1 (stale reference / broken pointer in the governing workflow). Trigger: first weekly synthesis after the migration surfaced the dead reference during the light health check.
