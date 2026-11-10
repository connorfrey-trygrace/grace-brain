---
type: changelog
date: 2026-09-09
tier: 2
touches: ["[[Workflows/Speaker-Identification]]"]
trigger: "Connor, 2026-09-09 — reviewing the 9/9 Connor–Derek transcript synthesis: \"make sure we are checking sources in the right order to avoid token usage\", then \"It might be worth refreshing the calendar window before processing\""
---
# Speaker identification now has an explicit, cost-ordered source-check sequence

## What happened

Identifying the two unlabeled speakers on the 2026-09-09 11.32 transcript took several ad hoc grep passes across `/People`, `/Trackers/Actions`, and `/Trackers/Calendar-Window` before landing on the right names — workable, but undocumented, so the next transcript would repeat the same trial-and-error at the same token cost. Separately, `/Trackers/Calendar-Window.md` had been generated the evening *before* this transcript's date (it's only refreshed by Phase 1 of `grace-quick-refresh`/`grace-weekly-refresh`, and this was a standalone "process latest" request) — so a same-day ad hoc meeting wouldn't have shown up in it even if checked.

## What changed

[[Workflows/Speaker-Identification]] gained a new **Step 1.5**, giving an explicit, cheapest-first order to check when the transcript body's own clues (Step 1) don't resolve every speaker:

1. `/People/*.md` (small, curated, cheap)
2. `/Trackers/Calendar-Window.md` — with a staleness rule: run `calendar-window.py --check` first (free), and refresh live only if the window's `generated` date is before the transcript's own `date`, or if `--check` reports its own staleness. Falls back to the stale cache (noted) if the connector fails, rather than blocking. Refresh once per run, not once per transcript, in a batch.
3. `/Trackers/Actions/` (grep only, large folder but cheap to search — often the most decisive source, since it names specific people against specific dated tasks)
4. Prior `/Transcripts` (grep, only if still ambiguous)
5. Live connectors (Outlook calendar/email search) — last resort, external round-trip

Calendar coverage is explicitly flagged as partial (not every real meeting is on Connor's Outlook calendar), so a miss there is not treated as evidence a meeting didn't happen.
