# Workflow: Event Planning Note

## Purpose
Standard format for planning notes created for any Grace event — concerts, internal events, Sunday night services, one-offs. One note per event. Stored in a subfolder under `/Events/` named `YYYY-MM-DD-Event-Name/` (e.g. `/Archive/2026-07-19-World-Cup/`). All files for a given event (planning note, day-of planner, drafts, registrant tracker, etc.) live in that subfolder.

## When to Create
Create a planning note when:
- An event has a confirmed or tentative date
- Planning work has begun (volunteers, logistics, marketing)
- The event appears in a transcript or action item

## Filename Convention
`YYYY-MM-DD-Event-Name-Slug.md`
Example: `2026-07-19-World-Cup-Viewing-Party.md`

**If the event date changes, rename the file to match the new date** and update every inbound `[[link]]` (Events tracker, agendas, form drafts, transcript references). A filename date that disagrees with the frontmatter `date` is a defect. Renaming is an ask-first change per CLAUDE.md.

## YAML Frontmatter Schema

```yaml
---
event: "Full event name"
date: YYYY-MM-DD
time: "HH:MM or TBD"
type: internal | external
status: planning | confirmed | active | complete | cancelled
venue: "Room or location"
ticket_price: free | $X | TBD
owners:
  - "Name: Role"
tags: [event]
---
```

**type** — `internal` = Grace-built crew from scratch (World Cup, boot camps); `external` = self-organizing via Sign Up Genius, contractor sound, ticket sales (concerts)

**status** ladder:
- `planning` — date tentative or logistics not yet assigned
- `confirmed` — date/time locked, key roles assigned
- `active` — within 2 weeks of event, in execution mode
- `complete` — event has occurred
- `cancelled` — no longer happening

## Note Body Sections

### Summary
2–4 sentences at the top of the note. Cover: what the event is, who it's for, key format/logistics highlights, and anything unusual (e.g., conditional extensions, fully subsidized, outside vendors). Should let someone get oriented in 15 seconds without reading the full note.

### Logistics
Key operational assignments. Use checkboxes for items not yet confirmed.

| Role | Owner | Status |
|------|-------|--------|
| Sound tech | Name | confirmed / TBD |
| Projection / screen setup | Name — confirm source (HDMI laptop, streaming device, cable input) and test before event | confirmed / TBD |
| ProPresenter | Name | confirmed / TBD |
| Security / Officers | Name | confirmed / TBD |
| Custodian | Name | confirmed / TBD |
| Room setup/teardown | Connor (default through Dec 2026 — pre-fill, don't leave TBD) | confirmed / TBD |

### Volunteers
- Volunteer sourcing method: Sign Up Genius | internal recruitment | both
- Link to Sign Up Genius (if applicable):
- Known gaps:

### Food & Concessions
- Partner(s): e.g., Chick-fil-A, Timber Pizza, none
- Notes:

### Marketing & Comms
- [ ] Comms request submitted through Rock
- [ ] Website/event page submitted to Derek
- [ ] Social media
- [ ] Internal announcement
- Notes:

### Open Questions
Unresolved decisions blocking planning progress. Remove items once resolved.

### Action Items
Format: `Owner: Action by Deadline`

**Register every action item in `/Trackers/Open Actions.md` as soon as it is created — never gated behind the event reaching `active` or `complete` status.** A long lead time is not a reason to leave an action off the tracker; it is a reason to give it a low **Priority** band (per [[Workflows/Open-Actions-Reference]] → ## Priority), where it sorts correctly against nearer-term work instead of being invisible until the event is imminent. Keep the event note and the tracker in sync: when you add, resolve, or re-prioritize an action here, mirror the change in the tracker (and vice versa). The tracker stays the single source of truth for cross-event status and priority.

### Event-Day Checklist
Reference the appropriate checklist for day-of execution:
- External concerts → [[Workflows/Concert-Checklist]]
- Internal events → [[Workflows/Internal-Event-Checklist]]

**This is an automatic agent task — NOT a Connor action.** When a non-cancelled event comes **within 1 week** of its date, the agent automatically (a) stands up the Day-Of Planner companion note (see below) and (b) copies the relevant checklist — Concert for `type: external`, Internal for `type: internal` — into that planner, then links the planner from this section. Do **NOT** register a "copy the checklist" item in `/Trackers/Open Actions.md`; the daily `event-checklist-autocopy` scheduled task owns this. Until an event is within 1 week, this section just points to the template links above.

### Notes
Freeform context, links to relevant transcripts, decisions log. **Keep this section to standing context** — dated run-by-run updates go in the companion log below.

### Status Update Log (companion note)
*This is one instance of a vault-wide rule — a note read on every run must not carry its own append-only history. See [[Workflows/note-history-splitting]] for the convention, the tool (`split-note-log.py`), and why event logs sit beside the plan note while action logs go to `/Trackers/Action-Logs/`. Note that a large event note is **not** automatically a split candidate: measure first — the 9/20 Launch note is 51 KB but only 1.7 KB of that is history.*

Dated `### Status updates — <date> (<source>)` sections are **append-only history and do not live in the plan note.** They go in a sibling file named `<event-filename>-Log.md` (frontmatter `type: log` + an `event:` link back), newest first, with a short `## 🗒️ Status update history` pointer left at the bottom of the plan note.

**Why:** every sync run that appends one line to a plan note reads the whole file first. The Sunday Night Service plan note reached **93 KB, 78% of it status history**, and was 44% of all bytes the 2026-08-11 quick refresh touched. Same fix as the 2026-08-10 /Logs split. Create the companion the first time an event note's history passes ~15 KB; don't pre-create it for new events.

---

## Day-Of Planner (optional companion note)

The agent **automatically** stands up a **Day-Of Planner** for every non-cancelled event when it comes **within 1 week** of its date (via the daily `event-checklist-autocopy` task) — this is not a Connor action. A planner may also be created **earlier, manually**, when the run-of-show is complex enough to warrant a countdown (a service launch, a multi-hour event with load-in).

Rules:
- **Filename:** same base as the event note + ` Planner` (e.g. `2026-09-20-Sunday-Night-Service-Planner.md`).
- **Frontmatter:** mirror the event note's `event`/`date`/`time`/`type`/`venue`, plus `companion_note: "[[event note]]"` and `tags: [event, planner]`. If a structure doc applies (e.g. service structure), link it with `structure:`.
- **Division of labor:** strategy, decisions, open questions, and action items stay in the **event note**. The planner holds only execution: countdown timeline, staffing roster, draft run-of-show, and day-of reminders. Don't duplicate decisions — link to them.
- The day-of checklist ([[Workflows/Concert-Checklist]] for external, [[Workflows/Internal-Event-Checklist]] for internal) is copied into the planner **automatically at the 1-week mark** by the `event-checklist-autocopy` task; the event note's Event-Day Checklist section links here rather than duplicating it.

---

## After the Event
1. Set `status: complete` in frontmatter
2. Add brief outcome note under Notes
3. Update `/Trackers/Events.md` status column
4. Reconcile unresolved action items in `/Trackers/Open Actions.md` — they should already be there from creation (see ### Action Items); confirm none were missed and update their status/priority

---

## Changelog

History lives in [[Changelog/_history/event-planning-note-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
