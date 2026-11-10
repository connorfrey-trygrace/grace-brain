---
type: changelog
date: 2026-09-16
tier: 2
touches: ["[[Trackers/Actions]]","[[Archive/Actions]]"]
trigger: "Connor, via 2026-09-15 deep system audit (item C)"
---
# 96 completed action notes moved to /Archive/Actions; 705 wikilinks repointed (second occurrence)

`/Trackers/Actions/` held 140 notes, **96 of them `status: completed`** (1.1 MB) — the 2026-08-12 cleanup had fully recurred. Moved to `/Archive/Actions/` (nothing deleted), 705 link instances repointed across 158 live files plus 41 inside Archive itself (177 files touched total). Live folder: 140 → 44 notes, 1.1 MB → 352 KB. Archive folder: 97 → 193 notes. Dangling-link check clean; 4-note spot check of inbound links confirmed resolution. 13 of the 96 archived notes had zero inbound wikilinks anywhere in the vault (never referenced elsewhere) — not an error, just noted. `-Log.md` companions were left in `/Trackers/Action-Logs/` untouched, matching the 8/12 precedent (confirmed by inspection: none of the 97 notes already in `/Archive/Actions/` from that round carry a `-Log.md` beside them there).

This is the **second occurrence** of this exact cleanup in five weeks — the 2026-08-12 sweep was a one-time hygiene pass, not a standing rule, so the folder simply grew back. Fixed at the root this time: a `COMPLETED, UN-ARCHIVED` flag was added to `Workflows/actions-index.py` (and documented in `Workflows/Open-Actions-Tracker.md`) the same day, which surfaces any `completed` note still sitting in the live folder more than `ARCHIVE_DAYS` (14) after its `resolved` date. Future recurrences should get caught and cleared incrementally by that flag instead of accumulating into a third one-off sweep.

Also noticed in passing, unrelated to this cleanup: a stray `Trackers/Actions/Logs/` subfolder holds one misfiled companion log (`Connor - Recruit Sunday night worship team (1–2 leaders, separate from morning) - Log.md`) that belongs in `/Trackers/Action-Logs/` per convention. Left untouched — out of scope here.
