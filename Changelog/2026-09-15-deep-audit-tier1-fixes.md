---
type: changelog
date: 2026-09-15
tier: 1
touches: ["[[Events/2026-09-16-Boot-Camp-Fall-Relaunch/2026-09-16-Boot-Camp-Fall-Relaunch]]", "[[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Run-of-Show-Experiment-Plan]]", "[[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Role-Ask-List]]", "[[Transcripts/2026-08-30 13.10 Sunday Night Formation Lunch — Team Assembled, Captain Roles Unfilled]]", "[[Welcome]]", "[[Workflows/event-checklist-autocopy]]"]
trigger: "2026-09-15 deep system audit (Connor's request)"
---
# Deep-audit Tier-1 fixes: 3 oversized notes split, 6 broken people-links repointed, 2 stale docs corrected

Per [[Workflows/system-audit]] deep mode and [[Workflows/note-history-splitting]]'s standing duty ("when a note is named oversized, split it — don't note it and move on"), split three live notes that `split-note-log.py --scan` flagged with movable dated-history blocks, all via the script (never by hand):

- `2026-09-16-Boot-Camp-Fall-Relaunch.md` — 3 blocks moved to a new companion `-Log.md` (live 49→48 KB).
- `2026-09-20-Sunday-Night-Service-Run-of-Show-Experiment-Plan.md` — 2 blocks moved (live 25→24 KB).
- `2026-09-20-Sunday-Night-Service-Role-Ask-List.md` — 7 blocks moved (live 19→10 KB).

(`4th-Service-Volunteer-Signups.md` also showed 1 movable block in the generic scan, but [[Workflows/note-history-splitting]] explicitly excludes it as a data cache — left untouched, matching the documented exception.)

Also repointed 6 broken frontmatter `people:` links in the `2026-08-30 13.10 Sunday Night Formation Lunch` transcript — `[[People/Sean Liesegang]]`, `[[People/Emily Horneffer]]`, `[[People/Liz Goodiel]]`, `[[People/Brandon Geddes]]`, `[[People/Simba Kanjanda]]`, `[[People/Brian Sulc]]` all pointed at standalone person notes that don't exist (all six are Good Noodles-roster-only). Repointed to the established piped form `[[People/Good Noodles|Name]]`, matching the exact precedent set 2026-08-14 and 2026-08-28. This was an isolated defect in that one processing run — the four other transcripts checked since (9/9, 9/11, 9/13, 9/14) all correctly fold peripheral names into a single collective `[[People/Good Noodles]]` link per [[Workflows/people-notes]] rule 2.

Refreshed `Welcome.md`'s Map section, which still listed only 3 files under `/Trackers` (Open Actions.base, Events, Hours) and omitted `/Trackers/Automation.md`, `/Trackers/Subscriptions.md`, `/Trackers/Calendar-Window.md`, `/People`, `/Logs`, and `/Changelog` entirely, despite all being live, governed parts of the system for weeks.

Added a retirement banner to `Workflows/event-checklist-autocopy.md`, which still opened by describing itself as "runs 7:02 AM daily" — [[Trackers/Automation]] shows this task was retired 2026-08-29 (Callie Taylor now owns discrete events). Mirrors the banner pattern already used on `grace-weekly-refresh.md` for its own 2026-09-12 retirement.

Full findings, including everything proposed but not applied, in [[System-Audit-2026-09-15]].
