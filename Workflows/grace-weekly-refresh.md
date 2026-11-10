# Workflow: Grace Weekly Refresh (manual — retired as a schedule 2026-09-12)

⛔ **Retired as an automatic Monday 6 AM job, 2026-09-12 — Connor's call: he'll run refreshes manually instead of relying on a scheduled safety net.** See [[Trackers/Automation]] changelog, same date. This file still describes a real, useful procedure — the phases, the watchdog duties, the prompt block — for whenever Connor explicitly asks for a weekly-style pass (the three watchdog duties below are the reason to reach for this file instead of just [[Workflows/grace-quick-refresh]]). It just no longer fires on its own. If a live scheduled task named `grace-weekly-refresh` still exists at `~/Claude/Scheduled/`, it is not visible to this session's `list_scheduled_tasks` and needs to be disabled/deleted by Connor directly.

~~The **weekly safety net** under [[Workflows/grace-quick-refresh]]. Fires **Monday 6:00 AM** (`0 6 * * 1`) whether or not Connor has asked for a refresh that week, so nothing goes silently stale~~ — see [[Trackers/Automation]] for the authoritative schedule.

**Connor is not present when this runs.** That single fact drives every difference between this file and the on-demand routine: no question can be asked inline, so anything ambiguous is deferred and flagged rather than guessed.

## What it runs

**Phases 0–3 are identical to [[Workflows/grace-quick-refresh]] — read that file for the detail; it is not duplicated here.** ⛔ That includes Phase 2's clock gate: timestamps are written by `Workflows/stamp.py`, never typed, and `python3 "Workflows/clock-check.py"` must exit 0 before Phase 3. **This matters more here than in the on-demand run** — nobody is watching an unattended Monday 6 AM job, so a corrupted marker would silently eat the next window rather than being caught in conversation. In short: Phase 0 process new transcripts → Phase 1 text scan ∥ email sync (analysis only, concurrent) → Phase 2 apply writes sequentially (email first, then text) → Phase 3 Open Actions sweep.

**Phase 1 begins with the calendar pull** (added 2026-08-20) — one `outlook_calendar_search` call, next ~3 weeks, written to [[Trackers/Calendar-Window]]. It runs here too, unchanged: the fact this file exists to make present is needed *more* in an unattended run, not less, because no one is around to catch an invented meeting. Detail and rationale in [[Workflows/grace-quick-refresh]] § Phase 1.

Two behavioral differences, both from running unattended:

1. **Phase 0 speaker gate.** Process only transcripts where *every* speaker is high-confidence from in-transcript evidence plus the known roster ([[People/People]] + [[People/Good Noodles]] + expected attendees). Leave every ambiguous one `unprocessed` and list it in the report under **"needs speaker confirmation."** **Never guess a speaker in an unattended run** — a wrong name propagates into /People, /Events, and action items, and nothing downstream will catch it.
2. **No inline confirmations anywhere.** Anything that would prompt Connor in the on-demand routine — an ambiguous completion, a contradiction between sources, a judgment call the procedure doesn't cover — becomes a line in the report or a flagged note, never a decision made on his behalf.

## Timing

Same requirement as [[Workflows/grace-quick-refresh]] § Timing, and it applies here too: run `date '+%s'` at the top of Phase 0 and again at each phase boundary, then append one line to [[Logs/refresh-run-log]] in the format documented at the top of that file (total + per-phase minutes, `unmeasured` rather than a guess if a stamp was missed). Each sync additionally carries its own `elapsed Xm` on its own Run Log line. **Token usage too** — same section, `Workflows/usage-report.py` with your own session id and the phase-0/final stamps, folded into the same refresh-run-log line. Nobody is watching this run to notice a token spike any more than a time one; log it the same way regardless.

**Why it matters more here than on-demand:** Connor watches a quick refresh happen and can feel when it drags. Nobody watches this one. A weekly line in the refresh log is the only way a Monday run that has quietly doubled in cost becomes visible before it becomes a complaint.

## Weekly-only duties

These three audit the automation system itself rather than Connor's data, so they run **here and nowhere else** ([[Workflows/grace-quick-refresh]] deliberately skips all three — running them several times a day produces "the scheduler looks healthy" noise).

1. **m365 Run Log health check** — the procedure in [[Workflows/m365-run-log-health-check]] (8-day staleness threshold, 4 days in event week, plus the two-consecutive-`ERROR:` check). Reads [[Logs/m365-sync-run-log]].
2. **Frontmatter/body drift check** — `python3 "Workflows/actions-index.py" --drift`. **STATUS CONTRADICTIONS** are real findings to adjudicate; the rest is stale body text to refresh when the note is next edited. Per [[Workflows/Open-Actions-Reference]] § Field authority, frontmatter wins.
3. **Scheduler heartbeat** — one `list_scheduled_tasks` call comparing each Grace task's `lastRunAt` against its cadence per [[Trackers/Automation]]. Flag any job overdue by more than one full cycle as an Active note in `/Trackers/Actions/`; check for an existing flag on the same job first; ignore non-Grace and expired-temporary tasks.

All three follow the same rule: **flag only when something is actually wrong.** A clean week produces no output from this section.

## Report

Same two-part shape as [[Workflows/grace-quick-refresh]] § Report — work queue first (`python3 "Workflows/actions-index.py" --brief`, naming the next physical action rather than the item title), then what changed this run. **All three of that section's Part 1 rules apply here unchanged, including the gate: an item with no Connor-side next action does not go in the report at all** (added 2026-08-18). That gate matters *more* in an unattended run, not less — Connor reads this one cold, with no chance to push back mid-report. Two additions specific to this job:

- **"Needs speaker confirmation"** — every transcript Phase 0 deferred, with the ambiguous speaker labels named, so clearing it is a one-line answer from Connor.
- **Watchdog findings** — only if a duty above actually flagged something.

Counts, windows scanned, and "the sync looks healthy" belong in `/Logs`, not the report.

## Scheduled-task prompt

The live task's prompt is a **thin pointer to this file** — the procedure lives here so it can change without touching the scheduler. This block is the mirror of that prompt; **any edit to one must be made to both in the same pass** (same rule as [[Trackers/Automation]] and [[Workflows/m365-sync-task-prompt]]).

```text
You are running the automated grace-weekly-refresh for Connor's Grace Brain vault, Monday 6:00 AM local. Connor is NOT present — run autonomously, make reasonable choices, and note them in your output. End with <run-summary>one or two sentences</run-summary>.

The full, authoritative procedure lives in the vault at /Workflows/grace-weekly-refresh.md, which delegates phases 0-3 to /Workflows/grace-quick-refresh.md. Read both first and follow them exactly — phases, timing, the weekly-only watchdog duties, and where every finding goes are defined there and may change without this prompt changing. This prompt is only the safety kernel.

Safety kernel — these hold even if the workflow files are unavailable or misread:

1. Unattended means never guess a speaker. Process only transcripts whose speakers are ALL high-confidence; leave the rest tagged unprocessed and list them under "needs speaker confirmation."
2. Email is Outlook via the M365 connector, never Gmail — Inbox AND Sent Items. Texts come from chat.db: locate the mount by globbing for the directory that actually contains chat.db (never trust a literal path), and never read, decode, or surface the 1:1 thread with Sky (handle ending 9087980030, matched on the last 10 digits). Group chats that include Sky ARE in scope and are processed normally — the exclusion is the direct thread only.
3. Analysis may overlap; writes may not. Run the text scan and email sync concurrently for analysis only, then apply email findings first, then text, then the Open Actions sweep.
4. Markers advance only on a successful run (## Last scan, ## Last successful run). Every job appends its Run Log line — including the elapsed Xm field — on every run, including zero-finding and errored ones.
5. Stamp `date '+%s'` at the top of Phase 0 and at each phase boundary, and append one line to /Logs/refresh-run-log.md per the format at the top of that file. If a stamp was missed, write "unmeasured" for that phase rather than a guess. Also run Workflows/usage-report.py with your own session id and those same two stamps, and fold its output into the same log line.
6. Be conservative: never auto-close an item on an ambiguous signal (raise a closure candidate instead), and give any finding with its own named deadline its own action note rather than burying it in another note's body.
7. Vault rules: never delete (move to /Archive), never edit transcript bodies — renaming the file and editing frontmatter during synthesis is allowed — never write to /Raw From Grace, ask before merging or archiving anything non-additive.
8. Run the three weekly-only duties (m365 Run Log health check, actions-index.py --drift, scheduler heartbeat) and report only what they actually flag.
9. Never assert a meeting. Phase 1 writes /Trackers/Calendar-Window.md from Outlook; before writing any "raise it at X" / "bring it to X" / "wait for X" sentence into a note or the report, query it with python3 "Workflows/calendar-window.py" --who "<Name>". "unknown" means the person could not be resolved and is NOT the same as "none". Connor works remotely — never recommend in person, in the room, or dropping by; the channels are text, then call, then Teams/Zoom.

Report tersely: the work queue first (python3 "Workflows/actions-index.py" --brief), then what changed this run, then transcripts left unprocessed pending speaker confirmation, then closure candidates awaiting Connor's confirm/dismiss, then any flags raised. Counts, windows, and health chatter go to the logs, not the report. If everything is clean, say "Weekly refresh clean" in one line.
```

## Changelog

History lives in [[Changelog/_history/grace-weekly-refresh-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
