---
type: changelog
date: 2026-11-11
tier: 2
touches: ["[[Workflows/attendance-pull]]", "[[Workflows/grace-quick-refresh]]", "[[Trackers/Automation]]", "[[Trackers/Attendance]]"]
trigger: "Connor"
---
# Weekly Rock attendance now copied into the vault

Connor asked for Rock's weekly attendance metrics to be fetched weekly and stored, as an indicator to track. Added `attendance-update.py` (CSV store + generated view) and a gated Phase 1 step in the quick refresh: a cheap `stale` check runs every refresh, and Rock is opened only when a Sunday is missing. The store was seeded with Kay's 2026-10-21 export (300 rows, 10/20/2024–10/18/2026); the first live Rock pull the same day added 10/25, 11/1 and 11/8, and the 10/11 and 10/18 overlap matched exactly (0 changed).
