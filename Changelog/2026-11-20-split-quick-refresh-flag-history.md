---
date: 2026-11-20
type: changelog
tier: 1
---
# Split dated history out of the grace-quick-refresh flag note (again)

- **What:** after appending this week's heartbeat block, ran `python3 "Workflows/split-note-log.py"` on [[Trackers/Actions/Connor - Reconcile grace-quick-refresh between the live scheduler and the Automation tracker]]. 2 blocks moved to its [[Trackers/Action-Logs/Connor - Reconcile grace-quick-refresh between the live scheduler and the Automation tracker-Log|Action-Log]]; the newest stay live.
- **Why:** same as [[Changelog/2026-11-13-split-quick-refresh-flag-history]]. The weekly heartbeat adds a dated block to this note every Friday, so it re-accretes history weekly until Connor resolves the mismatch.
- **By:** weekly-synthesis scheduler heartbeat (Tier 1, done by the script).
