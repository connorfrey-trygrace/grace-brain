---
type: changelog
date: 2026-09-09
tier: 2
touches: ["[[Workflows/grace-quick-refresh]]", "[[Workflows/grace-quick-refresh-reference]]", "[[Workflows/grace-weekly-refresh]]", "[[Workflows/text-message-sync]]", "[[Workflows/text-message-sync-reference]]", "[[Workflows/m365-to-obsidian-sync]]", "[[Workflows/m365-to-obsidian-sync-reference]]", "[[Workflows/m365-run-log-health-check]]", "[[Workflows/Open-Actions-Tracker]]"]
trigger: "Connor"
---
# Split inline incident narratives out of the three per-run workflow files, and moved the m365 weekly-only health check to its own file

Connor asked why a routine refresh's token usage (12.2M traffic that run) was so high. The dominant cost wasn't the refresh's own work — it was re-reading, on every turn, the long dated "why this rule exists" narratives embedded in [[Workflows/grace-quick-refresh]], [[Workflows/text-message-sync]], and [[Workflows/m365-to-obsidian-sync]], all three of which are read in full on every quick-refresh (and weekly-refresh) run. These are distinct from the `## Changelog` sections every workflow file already points out of the read path — this was inline defect/decision history sitting in the middle of otherwise-operational procedure text.

Applied the existing text-message-sync-reference.md pattern (and [[Workflows/Open-Actions-Reference]]'s) to all three files: kept every enforceable rule and command inline, replaced each incident narrative with a one-clause "why" plus a pointer, and moved the full story to a new `-reference.md` file per workflow (extended the existing one for text-message-sync). Nothing was deleted — everything moved. Also split m365-to-obsidian-sync.md's "Run Log health check" section (a `grace-weekly-refresh`-only procedure, never used by `grace-quick-refresh`) into its own file, [[Workflows/m365-run-log-health-check]], since the main file was previously read in full by every on-demand quick-refresh even though that section never applies there. Updated the two stale pointers this created ([[Workflows/grace-weekly-refresh]] § Weekly-only duties, [[Workflows/Open-Actions-Tracker]] § Standalone-sweep side duties).

Measurable effect: m365-to-obsidian-sync.md went from 109 to 75 lines (Run Log health check, ~37 lines, no longer read by quick-refresh at all); the other two files lost their heaviest paragraphs while keeping every rule and guard intact. No operational behavior changed — this is a read-cost fix, not a logic change.
