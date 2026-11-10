---
type: changelog
date: 2026-08-12
tier: 1
touches: ["[[Logs/refresh-run-log]]","[[Workflows/grace-quick-refresh]]"]
trigger: "Connor"
---
# Refresh run log gains `report Xm` and `wrote N KB`; existing fields unchanged

Instrumentation stopped at Phase 3, but on 2026-08-12 the report and verification cost ~8m — more than Phase 3 — invisibly. Added a fifth timestamp. Separately, the existing `out:` field counts the *size of the files touched*, which overstates cost by an order of magnitude (a 27 KB note receiving a one-line append reads as 27 KB); `wrote N KB` records bytes actually added. Both additive at Connor's instruction — nothing existing changed.

Calibration recorded in the log so nobody theorizes about I/O again: chat.db copy **2.38s**, immutable-URI query **0.01s**, actions-index over 139 notes **0.047s**. The 8/11 "a minimum-window guard would have paid for itself" claim was retracted on this basis.
