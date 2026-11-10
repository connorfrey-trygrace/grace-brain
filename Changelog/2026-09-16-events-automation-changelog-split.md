---
type: changelog
date: 2026-09-16
tier: 2
touches: ["[[Trackers/Events]]", "[[Trackers/Automation]]", "[[Workflows/note-history-splitting]]"]
trigger: "Connor, via 2026-09-15 deep system audit (item F)"
---
# Events.md and Automation.md's inline changelogs moved to /Changelog/_history

Both trackers are read on every relevant check (tracker-freshness, automation-state) yet carried a growing `## Changelog` section in the live file — the exact failure class `note-history-splitting.md` exists to catch. Moved both verbatim to `/Changelog/_history/Events-changelog.md` and `/Changelog/_history/Automation-changelog.md`, replaced with a one-line pointer (same pattern CLAUDE.md already uses). `split-note-log.py` wasn't used — its classifier targets action-note/event-log's interleaved-fields problem, which neither file has (both had a clean, undecorated `## Changelog` heading with nothing live below it) — so this followed the CLAUDE.md precedent instead. Also updated `note-history-splitting.md`'s "do NOT split" list: removed `Automation.md` (its listed reasoning had gone stale — most of its bulk was prose changelog, not current-state data) and logged this split in its history table.
