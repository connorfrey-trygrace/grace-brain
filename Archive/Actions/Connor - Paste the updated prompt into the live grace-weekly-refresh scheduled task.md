---
name: "⚙️ Connor: Paste the updated prompt into the live grace-weekly-refresh scheduled task"
status: completed
priority: P1
owner: "Connor"
added: 2026-09-02
deadline: none
needs_by: none
resolved: 2026-09-12
last_mentioned: "2026-09-12"
flagged: ""
source: "[[Trackers/Automation]] 2026-08-11 entry, re-surfaced 2026-09-02 while wiring token-usage tracking into the same workflow"
projects:
  - "Grace automation"
---

# ⚙️ Connor: Paste the updated prompt into the live grace-weekly-refresh scheduled task

- [x] Moot — `grace-weekly-refresh` is retired as a schedule (2026-09-12); there is no live prompt to sync.

- **Status**: **Closed 2026-09-12 — dismissed, not delivered.** Connor retired `grace-weekly-refresh` as a schedule rather than fixing the live prompt; the sync gap this item tracked no longer matters.
- **Priority rationale**: every enhancement made to the weekly-refresh procedure since 2026-08-11 — per-phase timing, and now token-usage logging (2026-09-02) — has been written into the workflow file and the safety-kernel prompt block *inside* that file, but if the **live scheduled task** never got the 8/11 rewrite in the first place, none of it has ever actually reached the Monday 6 AM run. This isn't a one-off gap; it's silently absorbing every subsequent change to this job.
- **Source**: [[Trackers/Automation]]'s own 2026-08-11 changelog entry ends *"⚠️ Action still needed — Connor must paste the new prompt into the live scheduled task; until he does, the Monday run follows the old inline prompt."* No later entry in that file, or anywhere else searched 2026-09-02, records it having been done.
- **Why I can't just do this myself**: this session's scheduled-tasks tool (`list_scheduled_tasks`) returns **zero tasks** — no visibility into, or write access to, whatever actually hosts `~/Claude/Scheduled/` from here. This is Connor's action, not something a refresh run can pick up on its own.
- **What to check while there**: confirm the task's cron is still `0 6 * * 1` and it's enabled, then verify the prompt matches [[Workflows/grace-weekly-refresh]] § Scheduled-task prompt **verbatim** — that block is deliberately kept in sync with the safety kernel every time the workflow changes (most recently 2026-09-02, adding the `usage-report.py` step). A stale prompt means every future edit to this file quietly does nothing unattended, which defeats the entire point of having Connor present only for the on-demand routine.
- **Notes**: none yet
- **Blocked by**: none · **Blocks**: nothing hard, but every unattended Monday run's actual behavior until this is done

### 2026-09-02 (quick refresh, token-usage build) — created
Re-discovered while wiring `usage-report.py` into `grace-weekly-refresh`'s safety-kernel prompt — the same 8/11 gap this note documents means that edit, like every edit since, may not be reaching the live Monday run either. Nothing in the vault shows this was ever resolved.
[Source: [[Trackers/Automation]] 2026-08-11 entry]

### 2026-09-10 (quick refresh, sweep, Step 3) — flagged
- 8 days quiet, P1, no blocker — this is a five-minute paste-and-verify Connor is the only one who can do. No field changed beyond `flagged`.

### 2026-09-12 (Connor, live session) — closed, not fixed
- Connor: "I changed my mind on the automation for weekly refreshes, I can run those manually." `grace-weekly-refresh` retired as a schedule instead — see [[Trackers/Automation]].
- → status: active → completed. If a live `grace-weekly-refresh` task still exists at `~/Claude/Scheduled/`, Connor still needs to disable/delete it there directly — this session has no visibility into that host.
