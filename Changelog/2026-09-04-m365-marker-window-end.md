---
type: changelog
date: 2026-09-04
tier: 2
touches: ["[[Workflows/stamp.py]]", "[[Workflows/m365-to-obsidian-sync]]", "[[Workflows/grace-quick-refresh]]"]
trigger: "Connor"
---
# m365 sync marker now records scan-window end, not run-completion time

`stamp.py mark --m365` used to always stamp the moment the command ran — the run's completion time. The workflow's own § Source & window treats the marker as "the point mail has been scanned through," and those two only coincide when analysis and writing are simultaneous; `grace-quick-refresh` splits them into Phase 1 and Phase 2, so a slow write phase was quietly eating into the next run's 30-minute overlap buffer every time (measured: a 2h25m dead zone on 2026-08-25). `mark --m365` now takes `--window-end "YYYY-MM-DD HH:MM"` and writes that instead; a missing flag falls back to the old behavior with a printed warning rather than crashing. See [[Archive/Actions/Connor - Decide whether the m365 sync marker should record scan-window end instead of run-completion time]] for the decision and defect history.
