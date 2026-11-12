---
type: changelog
date: 2026-11-11
tier: 2
touches: ["[[Workflows/grace-quick-refresh]]", "[[Workflows/inbox-sort]]", "[[Trackers/Automation]]"]
trigger: "Connor"
---
# Quick refresh now sorts read Inbox mail into Outlook folders

New Phase 3b ([[Workflows/inbox-sort]]) lists read Inbox mail through the M365 connector, classifies it against Connor's existing folders (Admin, Events › 4th Service / Boot Camp / Concerts / Volunteers / World Cup › Registrations, Sermon Outlines, YoPro Ministry), and moves it in Outlook web via Claude in Chrome. Connor's calls: move automatically with no approval step; unmatched mail stays in Inbox, and 3+ unmatched emails on one theme get a proposed new folder. It runs after the email sync's writes and only moves mail from before the sync's window-end, so the sync never misses anything that was moved. A reply-triage draft written earlier the same day was replaced before it ever ran. Connor wanted folder sorting, not a list of replies owed.

First run, same night: moved 71 of 92 Inbox emails. The workflow's first folder map was built from the folder pane's top level and missed the nested subfolders (Admin › Announcements/Bank/Facility/Procurement/Software/Staff Meetings; 4th Service › Scheduling & Volunteers/Connect Cards/Comms & Promo/Worship & Music/Discussion Guides/Attendance & Systems/NYC Recon). The map was rebuilt from what Connor had already filed in each folder before anything moved. Outlook-web mechanics learned on that run are now in the workflow: the Focused/Other split, the virtualized list, the "Create new" trap, and the reading pane marking mail read after a move.
