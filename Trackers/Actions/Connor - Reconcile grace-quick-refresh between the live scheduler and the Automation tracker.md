---
name: "🤖 Connor: Reconcile grace-quick-refresh between the live scheduler and the Automation tracker"
status: active
priority: P3
owner: "Connor"
added: 2026-09-25
deadline: none
needs_by: none
last_mentioned: "2026-11-06"
flagged: "2026-09-25 — reason: scheduler heartbeat — live-scheduler/inventory mismatch (grace-quick-refresh listed ✅ in Automation.md, absent from list_scheduled_tasks)"
source: "[[Workflows/weekly-synthesis]] scheduler heartbeat, 2026-09-25"
projects: []
people:
  - "[[People/Connor Frey]]"
blocked_by: []
blocks: []
---
# 🤖 Connor: Reconcile grace-quick-refresh between the live scheduler and the Automation tracker

- [ ] Pick one: (a) re-deploy `grace-quick-refresh` into `~/.claude/scheduled-tasks/` as a manual-only task (like `snl-extend-plans`), or (b) edit its [[Trackers/Automation]] row to say it's run by asking in chat and has no live scheduler entry.

- **Source**: [[Synthesis/Weekly 2026-09-25]] § System Health Check. `list_scheduled_tasks` on 2026-09-25 returned 5 Grace tasks (`weekly-synthesis`, `derek-sync-agenda`, `snl-week-ahead`, `snl-service-prep`, `snl-extend-plans`). `grace-quick-refresh` exists only in the legacy `~/Claude/Scheduled/` store. [[Trackers/Automation]] marks it ✅ with "click Run now," and its header says all Grace jobs were re-deployed to the visible store on 2026-09-16.
- **Priority rationale**: documentation mismatch only. On-demand refreshes are clearly running: [[Logs/m365-sync-run-log]] has entries through 2026-09-25 16:07 ET. Nothing is blocked.
- **Blocked by**: none · **Blocks**: nothing

### 2026-10-02 (weekly-synthesis heartbeat) — still unresolved
`list_scheduled_tasks` again returns the same 5 Grace tasks; `grace-quick-refresh` is still absent while [[Trackers/Automation]] marks it ✅. Run Log shows on-demand runs through 2026-10-02 11:58 ET, so nothing is broken — documentation mismatch only. No duplicate flag created.

### 2026-10-09 (weekly-synthesis heartbeat) — still unresolved, third week
`list_scheduled_tasks` returns 6 Grace tasks (adds `snl-thursday-alignment`, which matches its Automation.md row); `grace-quick-refresh` still absent while [[Trackers/Automation]] marks it ✅. Run Log shows on-demand runs through 2026-10-08 17:12 ET. Documentation mismatch only. No duplicate flag created.

### 2026-10-16 (weekly-synthesis heartbeat) — still unresolved, fourth week
`list_scheduled_tasks` returns the same 6 Grace tasks, all within cycle; `grace-quick-refresh` still absent while [[Trackers/Automation]] marks it ✅. Run Log shows on-demand runs through 2026-10-15 12:21 ET. Documentation mismatch only. No duplicate flag created.

### 2026-10-23 (weekly-synthesis heartbeat) — still unresolved, fifth week
`list_scheduled_tasks` returns 7 Grace tasks (adds `tuesday-seth-pco-reminder`, which matches its Automation.md row), all within cycle; `grace-quick-refresh` still absent while [[Trackers/Automation]] marks it ✅. Run Log shows on-demand runs through 2026-10-22 16:08 ET. Documentation mismatch only. No duplicate flag created.

### 2026-10-30 (weekly-synthesis heartbeat) — still unresolved, sixth week
`list_scheduled_tasks` returns the same 7 Grace tasks, all within cycle (`tuesday-seth-pco-reminder` fired 10/27 as scheduled); `grace-quick-refresh` still absent while [[Trackers/Automation]] marks it ✅. Run Log shows on-demand runs through 2026-10-28 13:44 ET. Documentation mismatch only. No duplicate flag created.

### 2026-11-06 (weekly-synthesis heartbeat) — still unresolved, seventh week
`list_scheduled_tasks` returns 8 Grace tasks (adds `agent-hub-visit-local`, which matches its Automation.md row), all within cycle; `grace-quick-refresh` still absent while [[Trackers/Automation]] marks it ✅. Run Log shows on-demand quick refreshes through 2026-11-06 10:50 ET. Documentation mismatch only. No duplicate flag created.
