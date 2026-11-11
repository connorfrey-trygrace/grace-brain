# 🤖 Automation Tracker

Durable inventory of the scheduled tasks that run automatically against this vault. **This is the source of truth for what runs, when, and which workflow governs it** — it replaces the temporary inventory that lived in `_Migration/` (archived 2026-06-25).

Scheduled tasks live at the user level, not inside the vault, so they keep running regardless of the project and are **not** visible by browsing the vault. When a schedule or task changes, update this file in the same pass (Tier 1).

**Two stores — this resolves the "can't see the scheduler" gap that sat open 2026-08-10 → 2026-09-16.** `list_scheduled_tasks` kept returning "No scheduled tasks found," and three audits recorded that as an unexplained visibility defect. It was never a defect: there are two separate task stores, and the tool only reads one.

| Store | Created by | Visible to `list_scheduled_tasks`? |
|---|---|---|
| `~/.claude/scheduled-tasks/` | Claude Code (`create_scheduled_task`) | ✅ yes — this is where all live Grace jobs now sit |
| `~/Claude/Scheduled/` | the older desktop-app task surface | ❌ no — legacy SKILL.md files, kept for prompt recovery |

All Grace jobs were re-deployed into the visible store on **2026-09-16**. The heartbeat in [[Workflows/weekly-synthesis]] can therefore actually see them now. Anything still sitting in `~/Claude/Scheduled/` is inert history — do not treat its absence from a listing as a missed run.

**Runs depend on the app being open.** A task due while Claude is closed fires on next launch instead, so a run can legitimately land hours or days late without anything being broken. Judge misses by "overdue more than one full cycle," never by an exact timestamp.

---

## Active scheduled tasks (Grace)

| Task id | Cadence | Enabled | Governing workflow | Reads | Writes |
| --- | --- | --- | --- | --- | --- |
| `weekly-synthesis` | Fri 4:09 PM (`0 16 * * 5`) | ✅ **Re-deployed 2026-09-16** into `~/.claude/scheduled-tasks/` | [[Workflows/weekly-synthesis]] | /Transcripts (the week's processed notes); [[Logs/m365-sync-run-log]]; `list_scheduled_tasks` | /Synthesis weekly note + a `## System Health Check` subsection carrying **all three watchdog duties** (light [[Workflows/system-audit]], the m365 Run Log health check, and the scheduler heartbeat), inherited from the retired `grace-weekly-refresh`. **This is now the system's only scheduled watchdog** — and its own receipt: a missing `/Synthesis/Weekly …` note for a given Friday means that week's watchdog didn't run. |
| `grace-weekly-refresh` | ~~Mon 6:00 AM (`0 6 * * 1`)~~ **manual only, on request** | ❌ **Retired 2026-09-12 (Connor's call)** | [[Workflows/grace-weekly-refresh]] — Phase 0 [[Workflows/speaker-identification]] + [[Workflows/transcript-synthesis]], then [[Workflows/text-message-sync]] + [[Workflows/m365-to-obsidian-sync]] + [[Workflows/Open-Actions-Tracker]] (standalone-sweep mode + side duties) | `/Transcripts/` (`unprocessed` notes); `~/Library/Messages/chat.db`; Outlook inbox + sent (M365 connector); **Outlook calendar, next ~3 weeks (Phase 1 pull, added 2026-08-20)**; `/Trackers/Actions/`; the m365 sync's Run Log; `actions-index.py --drift`; the live scheduler (`list_scheduled_tasks`) | **[[Trackers/Calendar-Window]] (regenerated every run)**; processed transcripts (rename + frontmatter, unambiguous speakers only); `/People/` notes + Good Noodles (additive); `/Trackers/Actions/` notes (new/updated items, re-band, sweep/closure); relevant [[Events]] notes (additive); a flagged note if the m365 Run Log shows a suspected missed run; a flagged note if the scheduler heartbeat finds any Grace job overdue >1 full cycle; corrections for any **status contradiction** the drift check finds (frontmatter vs body) |
| `grace-quick-refresh` | **On-demand only** — ask any time, or click "Run now" | ✅ | [[Workflows/grace-quick-refresh]] — 4 phases: Phase 0 transcript processing ([[Workflows/speaker-identification]] + [[Workflows/transcript-synthesis]]) → text scan ∥ email sync (concurrent analysis) → sequential writes → [[Workflows/Open-Actions-Tracker]] standalone sweep (Step 0 first), minus the watchdog duties | `/Transcripts/` (`unprocessed` notes) + same sources as `grace-weekly-refresh` (**including the Phase 1 Outlook calendar pull**), minus the Run Log/scheduler checks | **[[Trackers/Calendar-Window]]** + processed transcripts + `/People/` + same as `grace-weekly-refresh`, minus the two watchdog flags. Phase 0 difference: this on-demand run asks Connor to confirm an ambiguous speaker inline; the weekly run defers + flags instead |
| `event-checklist-autocopy` | 7:02 AM daily (`0 7 * * *`) | ❌ **Retired 2026-08-29** | [[Workflows/event-checklist-autocopy]] | /Events note dates; /Raw From Grace + [[Workflows/Internal-Event-Checklist]] / [[Workflows/Concert-Checklist]] | creates the event's Day-Of Planner when it's ≤1 week out. ⛔ **Disabled in scheduler + retired.** Built for discrete one-off events (World Cup, Boot Camp Summer Camp) — those are now Callie Taylor's remit. Connor's remaining "events" are recurring *services* (Sunday Night, Boot Camp Wednesday series), which a one-shot day-of checklist doesn't fit. Task left disabled at the user level (not deleted); re-enable if a discrete Connor-owned event ever reappears. |
| *(step, not a task)* weekly attendance pull | **Inside `grace-quick-refresh` Phase 1**, gated by `attendance-update.py stale` — pulls only when a Sunday is missing | ✅ Added 2026-11-11 | [[Workflows/attendance-pull]] | Rock › Reporting › Metrics via Claude in Chrome (Connor's Rock sign-in) | [[Trackers/Attendance-Data.csv]] (upsert) + [[Trackers/Attendance]] (regenerated) |
| `derek-sync-agenda` *(replaces `derek-weekly-sync-agenda`)* | Mon 2:06 PM (`0 14 * * 1`) — **fires weekly, but gates on the calendar** | ✅ **Re-deployed 2026-09-16** into `~/.claude/scheduled-tasks/` | [[Workflows/agenda-note]] | **Outlook calendar first** (is there a Connor–Derek sync *today*?); then [[Trackers/Open Actions.base]] via `actions-index.py`, recent /Transcripts, /Synthesis, /Events, and Connor↔Derek Outlook email | /Agendas — an agenda **only on days the calendar actually shows a sync**; otherwise it exits quietly having written nothing. **Cadence confirmed by Connor 2026-09-16:** bi-weekly, Mondays 4:00–4:45 PM — settling the question Automation.md had been holding open since 2026-09-08 ("re-cron once he confirms"). No re-cron was needed: the gate already handles it, and on off-weeks the job spends one cheap calendar check and writes nothing. Agenda lands 2 PM, two hours ahead of the meeting — Connor confirmed he wants it in advance (2026-09-16), superseding the older "generate it *at* meeting time" preference from when the sync was 2 PM. **Why the gate:** the cadence has now changed twice (weekly Tue → bi-weekly Mon), and the old fixed cron drifted off the meeting each time. The cron now only decides *when to check*; the calendar decides whether an agenda is due, so the next cadence change needs no re-cron. |
| `persona-refresh-quarterly-sweep` | ~~Quarterly, 1st of Jan/Apr/Jul/Oct, 9:15 AM (`15 9 1 1,4,7,10 *`)~~ | ❌ **Not re-deployed 2026-09-16 — deliberate, Connor's call pending** | persona-refresh skill (full-sweep mode) | [[Workflows/advisory-board-panel]]; each advisor's public material since their last-touched date | [[Workflows/advisory-board-panel]] — proposals only; never edits Positions/Panel dynamics directly. **Why held back:** a full manual board refresh ran 2026-09-16 (all 10 advisors, 6 refined), so the next quarterly slot — 2026-10-01, two weeks later — would near-certainly find nothing. Re-deploy when the gap is worth a run; say the word and it's one call. |

## Sunday Night Service — weekly readiness (added 2026-09-16, service launches 2026-09-20)

Three jobs, split by **lead time**, not by topic — Connor's framing: "Thursday is too late for volunteers, and too late for getting things into the slides for Vacca." PCO service type is **`Sunday Night`, id 1804248**; service type 1814753 ("Sunday Night Services") is an **empty duplicate with zero plans** and should be deleted — every prompt is told to ignore it.

**The PCO connector is read-only for Services.** There is no create-plan tool and `pco_unsupported_request` is only a telemetry stub, so plan creation has to go through the browser — which is why the write half is ad-hoc rather than scheduled.

| Task id | Cadence | Enabled | Governing procedure | Reads | Writes |
| --- | --- | --- | --- | --- | --- |
| `snl-week-ahead` | Mon 9:06 AM (`0 9 * * 1`) | ✅ | prompt-defined (see note below) | PCO `services_plans` + `services_plan_people` for service type 1804248, **looking 2–3 Sundays ahead** | Action notes for (a) plan runway under 6 weeks and (b) unfilled positions / declined people by team. Silent when healthy. |
| `snl-service-prep` | Mon 9:22 AM (`15 9 * * 1`) | ✅ | prompt-defined | PCO `services_plan_items` for the **next** plan only; Outlook sent mail since prior Wednesday (landing-page check) | Action notes for the five known content gaps: QOTN placeholder, worship songs not attached as PCO song records (titles in the description don't count), missing confidence-monitor notes, missing/unverified scripture slide, missing discussion prompts + off-ramp line, **and (added 2026-10-11) whether this week's Sunday Night landing-page content went to Heather Noble/Amanda — due EOD Tuesday weekly** (checks Outlook sent mail; keeps one standing Connor action note). Routed to Vacca / John Slye / Seth Addison / Connor; Connor chases. Silent when clean. |
| `snl-thursday-alignment` | Thu 9:02 AM (`0 9 * * 4`) | ✅ Created 2026-10-04 | prompt-defined | PCO next Sunday Night plan (people + items); recent Seth/Jean Paul texts/email | Report to Connor; drafts (never sends) a confirm text to Seth + Jean Paul if gaps. Added after a same-day Seth/Jean Paul exchange on 10/4 came too late. |
| `tuesday-seth-pco-reminder` | Tue 8:00 PM (`0 20 * * 2`) | ✅ Created 2026-10-22 | prompt-defined | — | Push notification to Connor: remind Seth to get Sunday's worship set into PCO. Rolls `deadline` on [[Trackers/Actions/Connor - Remind Seth to fill out PCO every Tuesday night]] +7 days. Never contacts Seth itself. |
| `snl-extend-plans` | **Ad-hoc — manual trigger only, no cron** | ✅ | prompt-defined | PCO plans (API) then PCO web UI in a browser | Bulk-creates missing Sunday 6 PM plans out to ~12 weeks. **Gated: it must show Connor the exact dates and get an explicit yes before submitting**, and verifies afterward via the API rather than trusting the screen. Appends a line to the SNL Launch-Log. |

**Why the write is not scheduled.** Connor approved using Claude in Chrome for PCO in a scheduled task, with the caveat that permissions shouldn't be fully auto. An unattended browser run would either stall on a permission prompt (doing nothing) or act unsupervised in shared church software that other staff and volunteers depend on — and wrong-dated or duplicate plans are much harder to unpick than to prevent. So detection is scheduled and reliable (read-only API), while the write is staged and one click from done: `snl-week-ahead` names `snl-extend-plans` in its action note when runway runs short.

**Prompt-defined, deliberately.** These three have no `/Workflows` file yet: the service has not run once, so there is no observed procedure to codify — writing the workflow doc first would just enshrine guesses. Give them a governing workflow once a few real runs show what the checks actually catch, and thin the prompts to pointers at that point (the house pattern the m365 job follows).

## Agent Hub — temporary local bridge

| Task id | Cadence | Enabled | Governing workflow | Reads | Writes |
| --- | --- | --- | --- | --- | --- |
| `agent-hub-visit-local` ("Grace: text scan (local, 4 AM + noon)") | 4 AM + noon daily (`0 4,12 * * *`, app adds a few minutes). Noon is the catch-up when the Mac slept at 4; the scan is incremental, so a quiet noon run is a one-liner | ✅ Narrowed 2026-11-10 to texts only, since the 5 AM cloud routine took over email + the rest of the Hub visit | [[Workflows/text-message-sync]] + the "Text-message check" section of Notion's Start here: Grace Claude | `chat.db` via `query-messages.py`; Notion Personal/St Onge Dashboard feed views | Text marker + run log (`stamp.py`); closure candidates in vault notes; Personal Tasks plans; Agent Mail FYIs. Needs the Mac awake and the app open |

## Cloud routines (claude.ai — run with the Mac off)

Not in either local store: these live at https://claude.ai/code/routines and run in Anthropic's cloud. They reach the vault only through the **Dropbox connector** (no local files, no Messages, no scripts beyond what they download).

| Routine | Cadence | Enabled | Governing procedure | Reads | Writes |
| --- | --- | --- | --- | --- | --- |
| `Grace Claude: Agent Hub visit (5am)` (`trig_01FRTcmfLV86McxXg5h2Q16e`) | Daily 10:00 UTC (`0 10 * * *`) = **5:00 AM ET** in winter, 6:00 AM during daylight time | ✅ Created 2026-11-02; Outlook added same night — **Working end to end since 2026-11-10 5:45 PM:** works on a git clone of `connorfrey-trygrace/grace-brain` and pushes to main (Claude GitHub App installed); Notion via connector. Before this, no run since 11/2 had synced email (the Dropbox connector can't overwrite) | Step 2 = [[Workflows/m365-to-obsidian-sync]] (shares its marker with the quick refresh); Step 3 = Notion Hub Protocol + Start here: Grace Claude, minus the text check (Mac-only; runs in [[Workflows/grace-quick-refresh]] Phase 4) | Outlook (M365 connector, read-only); vault + /Office via Dropbox; Notion Agent Mail + Grace Tasks | Vault action/event notes from email, the m365 marker + run-log line (`stamp.py`); Notion Grace Tasks + Agent Mail. Never sends email/texts, never deletes |

## Non-Grace (listed for completeness)

| Task id | Cadence | Enabled | Notes |
| --- | --- | --- | --- |
| `daily-finance-scan` | 6:04 AM daily (`0 6 * * *`) | ✅ (unverified) | Targets the separate **Personal Finance** vault via Gmail/Google Calendar. Not Grace; do not touch from this project. **Invisibility explained 2026-09-16:** it lives in the legacy `~/Claude/Scheduled/` store, which `list_scheduled_tasks` does not read — not project-scoping, as the 2026-07-16 audit guessed. Verify state from the Personal Finance project; the Grace scheduler heartbeat deliberately ignores it. |

---

## Required mounts

Some tasks fail silently without the right folder mounted at run time:

- `grace-weekly-refresh` / `grace-quick-refresh` → **Messages** (`~/Library/Messages`) for `chat.db` (may need Full Disk Access for the Claude app) AND the **M365 connector** (Outlook) AND **Office** (`~/Library/CloudStorage/Dropbox/Office`) for the canonical staff-name list — both jobs run the full text+email chain now.
- All tasks → this **vault** mounted.

If a task reads empty or errors, check its mount first.

## Operating note (2026-06-25, extended 2026-07-21)

Connor's standing preference: prefer **daily or on-demand** cadences over hourly — hourly runs are unnecessary and costly. The text scan was moved hourly → daily 8 AM on 2026-06-25 on that basis.

**Extended 2026-07-21:** the daily/3x-daily cadences for text scan and email sync turned out to have the same problem one level down — Connor found them "sometimes less than I need and very often more than I need," and still had to manually kick off a scan before working sessions that fell between scheduled runs anyway. The fix generalizes the bias further: for *maintenance/catch-up* jobs specifically (not jobs tied to a real calendar deadline, like `event-checklist-autocopy` or `derek-weekly-sync-agenda`), prefer **on-demand, triggered by the actual work session, with a low-frequency scheduled floor underneath it as a safety net** — rather than any fixed intraday cadence. Apply this bias to any future maintenance job.

## Changelog

History lives in [[Changelog/_history/Automation-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**

## Vault ↔ GitHub sync (added 2026-11-10)

| What | When | Status | Governs | Reads | Writes |
|---|---|---|---|---|---|
| `Workflows/vault-git-sync.sh` via Claude Code hooks (`SessionStart` async + `SessionEnd`, in `.claude/settings.local.json`) | Every Claude session in this vault, scheduled tasks included | ✅ Live 2026-11-10 | [[Reference/Vault-Git-Sync-Plan]] | Vault working files; git data at `~/GraceBrain.git` | Commits + pushes to private repo `connorfrey-trygrace/grace-brain`; log `~/Library/Logs/grace-brain-sync.log`. Never force-pushes; on conflict it aborts the merge and shows a notification |
