---
date: 2026-11-13
type: changelog
tier: 1
---
# Split dated history out of the grace-quick-refresh flag note

- **What:** ran `python3 "Workflows/split-note-log.py"` on [[Trackers/Actions/Connor - Reconcile grace-quick-refresh between the live scheduler and the Automation tracker]]. The 4 oldest weekly heartbeat entries (10/02–10/23) moved to [[Trackers/Action-Logs/Connor - Reconcile grace-quick-refresh between the live scheduler and the Automation tracker-Log]]. The 2 newest stay in the live note, per [[Workflows/note-history-splitting]].
- **Why:** the note had picked up a dated block every Friday since 9/25, which goes against the vault rule that a note read on every run must not carry its own append-only history. It was under the 15 KB oversized threshold, so `actions-index.py` didn't surface it.
- **By:** weekly-synthesis light audit (Tier 1, mechanical, done by the script).
