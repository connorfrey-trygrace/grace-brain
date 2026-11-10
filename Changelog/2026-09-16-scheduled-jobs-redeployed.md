---
type: changelog
date: 2026-09-16
tier: 2
touches: ["[[Trackers/Automation]]", "[[Workflows/weekly-synthesis]]", "[[Workflows/system-audit]]"]
trigger: "Connor — turned the scheduled runs off to save tokens; authorized redeployment at Claude Code's lower cost, best judgement"
---
# Two scheduled jobs redeployed into the visible task store; the 5-week "scheduler visibility gap" turned out not to be a defect

**Root cause found.** `list_scheduled_tasks` returned "No scheduled tasks found" across three audits (2026-08-10, 09-12, 09-15, 09-16), each recording it as an unexplained visibility defect blocking verification of scheduler state. There are simply **two stores**: Claude Code's `create_scheduled_task` reads/writes `~/.claude/scheduled-tasks/` (which did not yet exist), while the vault's original jobs were created in the older desktop-app store at `~/Claude/Scheduled/`, which that tool does not read. Not project-scoping, as the 2026-07-16 audit guessed. Documented in Automation.md's header.

**Context that dissolves the 2026-09-16 advisory audit's Finding 1.** The board flagged the missing `Synthesis/Weekly 2026-09-11.md` as a scheduled job silently going dark. Connor turned the scheduled runs off deliberately, to save tokens. No defect — but Automation.md still listed `weekly-synthesis` and `derek-weekly-sync-agenda` as ✅ Enabled, so the vault's own source of truth disagreed with reality and an audit spent its top finding on a non-defect. That inventory drift was the real finding; these rows are now correct.

**Deployed** (both in `~/.claude/scheduled-tasks/`, both confirmed visible to `list_scheduled_tasks`):
- `weekly-synthesis` — Fri 4:09 PM, unchanged cadence, but now carrying **all three watchdog duties** (light system audit, m365 Run Log health check, scheduler heartbeat) inherited from the retired `grace-weekly-refresh`. This is the advisory board's own converged recommendation — Austin/Karpathy and Cat/Dylan split on whether to restore a watchdog at all, but all four accepted folding one into an existing job over reviving a separate one. Duties defined authoritatively in `Workflows/weekly-synthesis.md` § System health check; the task prompt is a thin safety kernel pointing at it, per the house pattern.
- `derek-sync-agenda` (replaces `derek-weekly-sync-agenda`) — Mon 2:06 PM, but **gated on the calendar**: it checks whether a Connor–Derek sync actually exists that day and exits quietly if not. The meeting's cadence changed twice (weekly Tue → bi-weekly Mon 4:00–4:45, confirmed on Outlook through 2026-11-09) and the old fixed cron drifted off it both times. The cron now decides only when to check; the calendar decides whether an agenda is due, so the next cadence change needs no re-cron.

**Deliberately not redeployed:** `grace-weekly-refresh` (Connor runs `grace-quick-refresh` manually and heavily — 9 runs in 6 days — so resurrecting it fails the ROI test; its watchdog duties went to `weekly-synthesis` instead), `event-checklist-autocopy` (retired 2026-08-29, Callie Taylor owns discrete events), `persona-refresh-quarterly-sweep` (a full manual board refresh ran today, so the 2026-10-01 slot would find nothing).

**Also fixed:** `system-audit.md`'s watcher check (light-check item 9) still named the retired `grace-weekly-refresh` — the advisory audit's Finding 4. Rewritten around what the job can actually verify: a receipt check (does last Friday's Synthesis note exist) plus the heartbeat, with the honest note that the check cannot catch its own job dying, so the missing-note signal is the durable backstop.
