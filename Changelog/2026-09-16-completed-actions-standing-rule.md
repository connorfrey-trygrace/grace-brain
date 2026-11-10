---
type: changelog
date: 2026-09-16
tier: 2
touches: ["[[Workflows/actions-index.py]]", "[[Workflows/Open-Actions-Tracker]]"]
trigger: "Connor, via 2026-09-15 deep system audit (item C)"
---
# Standing rule: `actions-index.py` now flags stale completed notes for archiving

The 2026-08-12 cleanup (94 completed notes archived) was a one-time manual sweep, not a rule — by 2026-09-15 it had fully recurred (96 of 140). Added a new `COMPLETED, UN-ARCHIVED` section to `actions-index.py`'s report, printed on every run: any `status: completed` note whose `resolved` date is more than `ARCHIVE_DAYS` (14, new constant) in the past and still sitting in `/Trackers/Actions/`. Documented in `Open-Actions-Tracker.md` alongside `OVERSIZED NOTES`, with the same "fix it in the run that surfaces it" instruction pointing to the 2026-08-12 changelog for method. A second, one-time repeat sweep to clear the current 96 is tracked separately — see `2026-09-16-archive-completed-actions-round-2.md`.
