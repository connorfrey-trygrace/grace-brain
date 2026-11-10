---
type: changelog-history
governs: "[[Workflows/system-audit]]"
tags: [changelog]
---
# system-audit-changelog — changelog (pre-2026-08-12 history)

Split out of the procedure file on **2026-08-12** so procedure text stays cheap to read. **Never read on a normal run.** New changes go in their own dated file under `/Changelog/`, not here.

---

## Changelog
- 2026-06-15: Initial creation — turns the one-off 2026-06-15 audit into a repeatable health check (light weekly + deep on-demand). Tier 3 (new workflow file). Trigger: Connor's request to schedule the audit.
- 2026-07-16: Added light-check item 9 (**Watcher check**) — the weekly synthesis health check now confirms `daily-stale-sweep` ran that week, closing the "who watches the watcher" loop from the 2026-07-16 advisory-board audit (Finding 1). Tier 2 (new check). Trigger: advisory-board audit, approved by Connor.
- 2026-07-24: Re-scoped item 9 (**Watcher check**) from the retired `daily-stale-sweep` to `grace-weekly-refresh`, which absorbed the watchdog duties (m365 Run Log health check + scheduler heartbeat) in the 2026-07-21 scheduling-model change; added a note that a missing `lastRunAt` before the first scheduled fire is expected, not a miss. Tier 2 (changed check target). Trigger: 2026-07-24 weekly-synthesis health check found item 9 pointing at a deleted task; approved by Connor.
