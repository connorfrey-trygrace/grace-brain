---
type: changelog
date: 2026-11-03
tier: 2
touches: ["[[Workflows/grace-quick-refresh]]", "[[Workflows/m365-to-obsidian-sync]]", "[[Trackers/Automation]]", "[[CLAUDE.md]]"]
trigger: "Connor"
---
# Email sync runs daily in the 5 AM cloud routine; quick refresh now ends with the Agent Hub visit

Connor added Outlook to the 5 AM cloud routine ("that's a pretty big part of this"), so it now runs the M365 email sync before the Agent Hub visit, sharing the sync's marker with the quick refresh so neither re-processes the other's mail. He also asked for the visit to run on every quick refresh: it is Phase 4 there, after the sweep, and it is where the Mac-only text-message check happens (the cloud can't read Messages). recipe-grab stays out of both; it is moving to Personal Claude.
