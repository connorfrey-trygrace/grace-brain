# Workflow: Event Checklist Auto-Copy (Day-Of Planner spin-up)

⛔ **Retired as a scheduled task 2026-08-29 — see [[Trackers/Automation]].** Built for discrete one-off events (World Cup, Boot Camp Summer Camp); those are now Callie Taylor's remit, and Connor's remaining "events" are recurring services (Sunday Night, Boot Camp) that a one-shot day-of checklist copy doesn't fit. Task disabled at the user level, not deleted — re-enable if a discrete Connor-owned event ever reappears. The procedure below is left intact for that case; it no longer fires on any cadence.

~~Governs the automated task `event-checklist-autocopy` (runs 7:02 AM daily; see [[Trackers/Automation]]).~~ When an event is within one week of its date, it stands up the event's **Day-Of Planner** and copies the right checklist in. This **replaces a former manual Connor action** — do not create or re-create any "copy the checklist" item in [[Trackers/Open Actions.base]]. Follows [[CLAUDE.md]] and the Day-Of Planner spec in [[Workflows/event-planning-note]].

## Selection
1. Today's date = `date +%F`.
2. List event **planning** notes in /Events (frontmatter has `event:`, `date:`, `status:`). **Ignore:** anything in /Archive; sub-notes (form-submission drafts, invite drafts, halftime/props plans); and existing files whose name contains "Planner".
3. Process a note **only** when `0 ≤ (date − today) ≤ 7` days. **Skip** if `status` is `complete`/`cancelled`, the date is past, or it's more than 7 days out.

## Per qualifying event
- **Checklist by `type`:** `external` → [[Workflows/Concert-Checklist]]; `internal` (or blank/other) → [[Workflows/Internal-Event-Checklist]].
- **Planner file:** event base name + `-Planner.md` (e.g. `2026-07-19-World-Cup-Viewing-Party.md` → `2026-07-19-World-Cup-Viewing-Party-Planner.md`). Before creating, search /Events for a file sharing the date prefix and containing "Planner" — reuse it if found; never create a duplicate. If creating, follow the event-planning-note Day-Of Planner spec: frontmatter mirroring the event note's `event`/`date`/`time`/`type`/`venue`, plus `companion_note: "[[<event note>]]"` and `tags: [event, planner]`; body with countdown timeline, staffing roster, draft run-of-show, day-of reminders (link decisions back to the event note, don't duplicate).
- **Copy the checklist:** full body below the checklist's H1, **excluding** that file's `## Changelog`, into the planner under `## 📋 Event-Day Checklist`. **Idempotent:** if that heading already has real checklist content (not just a template link), do nothing further.
- **Repoint the event note:** in its Event-Day Checklist section, replace the template pointer with `Day-of checklist lives in [[<planner>]] (auto-copied <today>).`
- **Status:** if the event note is `planning` or `confirmed`, set it to `active`.

## Guardrails
Never write to /Raw From Grace; never delete (move to /Archive if ever needed); add no new assigned action to Open Actions for this work.

## Report
Per event: processed (planner created/reused, checklist copied, status changed) or skipped + why. If nothing is within a week: "No events within 1 week — nothing to do."

## Changelog

History lives in [[Changelog/_history/event-checklist-autocopy-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
