---
type: changelog
date: 2026-08-17
tier: 2
touches: ["[[Workflows/m365-to-obsidian-sync]]", "[[Workflows/text-message-sync]]", "[[Logs/refresh-run-log]]", "[[Logs/m365-sync-run-log]]", "[[Logs/text-message-sync-run-log]]"]
trigger: "grace-quick-refresh, 2026-08-17 11:19 ET run"
---
# Sync timestamps must be read with `TZ=America/New_York`, and a marker in the future is a defect to correct rather than a window to honour

The `grace-quick-refresh` run that completed earlier on 2026-08-17 stamped **UTC readings and labelled them ET** — roughly 4 hours ahead (EDT is UTC−04:00). The device shell reports UTC, and a bare `date` call was used for human-facing timestamps.

**The consequential half was the m365 marker.** It was written as `2026-08-17 11:40 ET` when the real completion time was `07:49 ET`. Honoured literally, the next run's window — marker minus the 30-minute overlap buffer — would have opened **~4 hours in the future**, and every email arriving during today would have fallen into a dead zone belonging to no window and been **permanently skipped**. That is precisely the failure mode the overlap buffer was added on 2026-07-15 to prevent (the Derek 7/14 Staff Mtg Recap case), reintroduced through the clock rather than through the window arithmetic. The marker was overridden manually for the 11:19 ET run — which then found two relevant emails, including a Rock registration and Kay's Rock-restart notice, both of which the bad marker would have lost — and reset to the real time.

**Fixes landed.** Both [[Workflows/m365-to-obsidian-sync]] § Last successful run and [[Workflows/text-message-sync]] § Last scan now carry a guard next to the marker: read timestamps with `TZ=America/New_York date '+%Y-%m-%d %H:%M ET'` because the execution shell reports UTC, and treat a marker timestamped in the future as a defect to correct rather than a window to honour. The corrupted timestamps in [[Logs/refresh-run-log]] (`11:52 ET` → `~07:52 ET`), [[Logs/m365-sync-run-log]] and [[Logs/text-message-sync-run-log]] (both `12:05 ET` → `~08:05 ET`) were **amended in place with an inline note, not deleted or rewritten** — the line content is untouched, only the timestamps are corrected, so the trace of the defect survives.

**What this does not fix:** nothing enforces the rule mechanically. The guard is a procedure note, and a future run that reaches for a bare `date` will reproduce the defect. Worth Connor's attention as a candidate for the same treatment the Sent-Items scoping defect got — a stated rule that was documented and still live until someone measured (see [[Changelog/2026-08-12-m365-sent-items-scoping-fix]]).
