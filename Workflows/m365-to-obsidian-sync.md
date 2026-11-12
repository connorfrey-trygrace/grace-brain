# Workflow: M365 → Obsidian Sync (Outlook email → trackers)

Governs the **M365 email sync** (see [[Trackers/Automation]] for the authoritative schedule). Since 2026-07-21 it runs on a **weekly floor plus on-demand** model, not a fixed daily cadence: the `grace-weekly-refresh` task fires it every **Monday 6 AM** as a safety net, and [[Workflows/grace-quick-refresh]] runs it whenever Connor sits down to do Grace work. The retired schedule was 8 AM / 12 PM / 4 PM daily — noted only because older run-log entries and cross-references still assume it. Folds new Outlook email — inbound **and sent** — into the existing trackers and event notes. Email is a first-class Grace source alongside transcripts and texts. Can also be run on-demand. **Since 2026-11-02 it also runs daily at 5 AM ET** as Step 2 of the cloud routine `Grace Claude: Agent Hub visit (5am)`, reaching the vault through Dropbox; it shares this file's marker, so the quick refresh only picks up mail since that run.

This is distinct from [[Workflows/weekly-synthesis]], whose source is *only* /Transcripts. This job is the sanctioned channel by which email reaches the trackers; weekly synthesis still never pulls from email itself.

**Reference material** — the incident write-ups behind the rules below (Sent Items scoping, the overlap buffer, marker semantics) — lives in [[Workflows/m365-to-obsidian-sync-reference]]. Do not read it speculatively.

## Source & window
- Use the **Microsoft 365 connector** (Outlook) — never Gmail (see [[CLAUDE.md]] EMAIL rule). Search **both Inbox and Sent Items**.
- **Query Sent Items with an explicit `folderName`, and never pass a bare `order`.** Passing `order` to `outlook_email_search` **without** `folderName` silently scopes the search to Inbox, so the Sent leg returns a `sent 0` that is indistinguishable from a real null. Sent leg: `folderName: "Sent Items"`. All-folders leg: omit `order` entirely. Incident that found this in reference.
- **Window = (last successful run − 30 min overlap buffer) → now.** Read the **## Last successful run** marker at the bottom of this file and scan from **30 minutes before** that timestamp forward — not a fixed lookback keyed to the 8/12/4 schedule. This makes the window self-correcting: if a run is late, skipped, or errors out (task didn't fire, connector/mount was down), the next run's window automatically stretches back to cover the gap instead of silently losing it. **Why 30 minutes, not 0:** search indexing lags delivery by a few minutes, so a run right at the boundary can miss an email that arrived just before its marker; the buffer re-scans that lag zone every run, safely, because the dedup guardrail (§Guardrails) skips anything already reflected in its target note. Incident this prevents in reference.
- ⚠️ **`outlook_email_search`'s `afterDateTime`/`beforeDateTime` read a bare `YYYY-MM-DD HH:MM` string as UTC, not America/New_York — verified 2026-09-11.** A window computed in ET (per this file's own convention) and passed to the tool literally gets silently re-anchored ~4h earlier than intended (EDT is UTC−4) — e.g. passing `"2026-09-11 15:00"` returns mail actually received at 15:00 **UTC** (11:00 AM ET), not 3:00 PM ET. **Convert the ET window to UTC (append `Z`) before calling the tool** — e.g. compute the ET bound, then pass its UTC equivalent (`...T19:00:00Z` for 15:00 ET during EDT). Because both the marker-write and the next run's marker-read apply this same conversion consistently, the bug does not silently drop mail permanently — but skipping the conversion on any single run shifts that run's actual coverage ~4h stale without any error surfacing. See [[Changelog/2026-09-11-m365-search-utc-conversion]].
- **No marker yet (first run ever), or marker unreadable/corrupted:** fall back to an 18h lookback from now, then record the marker as normal so subsequent runs are gap-based.
- **Sent email is often the most actionable** — it carries Connor's commitments, confirmations, and decisions.

## What to capture (priority order)
1. Commitments in sent mail ("works for me", "I'll follow up Thursday", "let's do X").
2. Confirmations / decisions reached in reply threads.
3. New deadlines or scheduled dates.
4. Information that updates or corrects something already in a note.

## Where it goes
- Action items / commitments / deadlines → [[Trackers/Open Actions.base]] (that file's entry schema).
- Event status / logistics → [[Trackers/Events]] and the relevant [[Events]] note.
  - **Status-update history goes to the event's `-Log.md` companion, not the plan note** (e.g. [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Launch-Log]]). Only changes to the *live plan* — owners, dates, scope, open questions — are folded into the plan note itself. Convention added 2026-08-11; see [[Workflows/event-planning-note]].
- **Prefer updating existing notes.** Do **not** create new notes unless a clearly new standalone topic warrants it.
- **Entry format is mandatory: terse timestamped lines — see [[Workflows/Open-Actions-Tracker]] § Entry format.** One line per event, no verbatim quotes, no analysis; judgment goes in the run report, not the note.

### Registration notifications → registrant trackers
Rock emails a per-registration notification to Connor (as Registration Contact) whenever someone registers for an event with notifications enabled. Route these by event:

Event-scoped routing rules are temporary by nature — each carries an **active through** date; after that date, move the expired rule into the changelog (never delete) rather than leaving dead routing for every future run to read.

**4th Service Volunteering** — *open-ended — no end date (Connor, 2026-10-05; it is a standing interest form, so registrations keep arriving after the 9/20 launch).*
- **Sender** `info@trygrace.org`, **subject** "4th Service Volunteering Registration". Rock instance **542** (admin: https://trygrace.rockcloud.com/RegistrationInstance/542).
- **Route to** [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] — append a row to the **Full roster** table and bump the registration/registrant counts in the header.
- ⚠️ **The notification email carries only name, email, and mobile.** The five substantive answers (serving areas, frequency, already-serving, age range, free text) are **not** in the email — they only exist in Rock. So this rule can add a *row*, but cannot fill it in. When new registrants accumulate, re-pull instance 542 rather than trusting the roster to be complete from email alone; mark email-only rows as such.
- Form record: [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteering-Rock-Form]].

**Young Professionals connect cards** — *standing rule (Connor, 2026-11-01).*
- **Sender** `info@trygrace.org`, **subject** "<Name> has filled out a Young Professionals connect card".
- **Always create a P1 action note** `Connor - Invite <Name> (YP connect card) to Sunday Night`, unless Sent Items already shows the invite. Also add a [[People/Good Noodles]] roster row and a Launch-Log line.
- The invite mirrors Connor's "Invitation to Sunday Night" sends (10/26): "Hey <Name>!!", the 6pm Sunday evening service for young professionals, the hosts, the YP Discord link, "So glad you're with us." Draft it for his approval. Never send it unapproved.

*(Expired routing rules — World Cup Final Viewing Party, 7/19 Vision Setting Lunch — are in reference, not here.)*

## Resolve, don't just log
When an email (or related calendar event) shows an existing Open Actions item is done — a "schedule X" whose meeting is now on the calendar / invite accepted, an action confirmed "submitted/sent/confirmed", or a "waiting on" item where the awaited party says "that's everything" — set `status: completed` on that note per [[Workflows/Open-Actions-Tracker]] (add a `resolved: YYYY-MM-DD` line citing the email/calendar evidence) and clear it from any other note's `blocked_by`, surfacing anything newly unblocked. Writing completion evidence into Status/Notes while leaving `status: active` is the exact gap to avoid. If completion is genuinely ambiguous, do **not** auto-close: update Notes and set `status: closure-candidate` on the target note (evidence + what to verify), so the likely-completion stays visible in the Closure Candidates view of [[Trackers/Open Actions.base]] for Connor to confirm or dismiss, rather than being buried in this run's report. See [[Workflows/Open-Actions-Reference]] → ### Closure Candidates — entry and exit.

## Guardrails
- Additive and conservative: skip an email rather than make a spurious update; leave an item in place rather than auto-close on an ambiguous signal.
- Avoid duplicates: **windows now overlap by design** (the 30-min buffer above, plus any fallback on first run / unreadable marker) — so this dedup check is load-bearing, not just a fallback safeguard. Before adding anything, confirm the target note doesn't already reflect the email and skip if it does.
- **Same duplicate-check applies to new Open Actions items, not just re-processing the same email twice.** Before creating a new note, check every note in `/Trackers/Actions/` (all statuses) for a substantively identical existing item and update that one instead — use `python3 "Workflows/actions-index.py" --titles` for this (status+filename per note), not a folder read (added 2026-08-10) — per [[Workflows/Open-Actions-Transcript-Steps]] Step 1 (added 2026-07-21 after two near-duplicate "missed m365-sync-run" items, for the 7/15 and 7/16 slots, were logged as separate headings instead of one item updated twice).
- **A finding with its own named deadline is never note-only.** If an email contains an explicit commitment tied to a specific day/date, give it its own new note in `/Trackers/Actions/` with `status: active` — even when it's clearly a sub-step of a broader item already being tracked. Cross-reference the parent item with a `blocked_by`/`blocks` wikilink or a one-line pointer; don't bury the dated commitment inside the parent's Notes field. (Same failure mode caught in the text-sync job on 2026-07-03 — mirrored here since email carries commitments just as often as texts.)
- Follow [[CLAUDE.md]] rules: never edit transcript bodies, never write to /Raw From Grace, ask before merging/archiving.

## Report
Emails processed (inbox + sent); notes updated and what changed; items set to `status: completed` (with evidence) and anything newly unblocked; emails that matched no note; and ambiguous completions left in place — now set to `status: closure-candidate` (visible in that view of [[Trackers/Open Actions.base]]; re-list them here too).

## Update the marker
After a run **completes successfully**, update the **## Last successful run** marker below with **the end of the scanned window** — not the run's completion time. Call `python3 "Workflows/stamp.py" mark --m365 --window-end "YYYY-MM-DD HH:MM"`, passing the same `beforeDateTime`/now-bound you gave `outlook_email_search` for this run's search (America/New_York, no seconds). If the run errored, was interrupted, or a required mount (connector/Office folder) was missing partway through, **do not update the marker** — leave the old timestamp in place so the next run's window still covers the missed gap.

⚠️ **Window-end, not completion time** (changed 2026-09-04, Connor's call) — `grace-quick-refresh` splits analysis (Phase 1) from writing (Phase 2), so a run that takes several minutes to fold findings into trackers would otherwise donate that gap to the next window's overlap buffer. `stamp.py` refuses a missing `--window-end` outright (falls back to completion time with a printed warning) so an un-updated caller degrades loudly rather than crashing. Defect history in reference.

## Run Log

**Entries live in [[Logs/m365-sync-run-log]]** — split out of this file on 2026-08-10 because this procedure file is read in full on every run and the log is not. Every run that reaches this step appends **one line** there (success, zero-finding, or caught-error alike); the line format, the `dups` field, and the rationale for the log's existence are documented at the top of that file. **Every line carries an `elapsed Xm` field**: stamp `date '+%s'` when the job starts and again before writing the line, and report whole minutes (`<1m` if under). Added 2026-08-11 — Connor asked why a refresh took ~30 minutes and nothing anywhere recorded elapsed time, so the answer had to be reconstructed from file mtimes. **Do not append entries here.**

## Run Log health check (run by `grace-weekly-refresh` only)
Full procedure: [[Workflows/m365-run-log-health-check]]. **Not part of a normal (quick-refresh) read** — split out 2026-09-09 because this file is read in full by every quick-refresh email-sync pass, and this check only ever runs from `grace-weekly-refresh`.

## Last successful run
- timestamp: 2026-11-11 19:36 ET
  *(Written by `Workflows/stamp.py` from `ZoneInfo("America/New_York")`, never from the shell clock — the shell reports UTC. Prior value: `2026-11-11 15:03 ET`.)*

> ⛔ **This marker is written by `python3 "Workflows/stamp.py" mark --m365`, never by hand** — the shell reports UTC, `ZoneInfo` does not. Verified every run by `Workflows/clock-check.py`, which compares the stamp against the file's real mtime. Retired the prose guard that stood here 8/17–8/21 and did not prevent the 8/21 recurrence: [[Changelog/2026-08-21-clock-enforced-in-code]].

## Changelog

History lives in [[Changelog/_history/m365-to-obsidian-sync-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
