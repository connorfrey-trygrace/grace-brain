---
type: changelog-history
governs: "[[Workflows/event-planning-note]]"
tags: [changelog]
---
# event-planning-note-changelog — changelog (pre-2026-08-12 history)

Split out of the procedure file on **2026-08-12** so procedure text stays cheap to read. **Never read on a normal run.** New changes go in their own dated file under `/Changelog/`, not here.

---

## Changelog
- 2026-08-11: Added **§ Status Update Log (companion note)** — dated status-update sections are append-only history and belong in a sibling `-Log.md`, not the plan note, once history passes ~15 KB. Tier 2 (new section convention). Trigger: the 2026-09-20 launch note hit 93 KB (78% history) and dominated the 2026-08-11 quick refresh's read cost.
- 2026-06-21: Made the Event-Day Checklist copy + Day-Of Planner standup an **automatic agent task** triggered when an event comes **within 1 week** of its date, rather than a Connor action item. The daily `event-checklist-autocopy` scheduled task copies the right checklist (Concert/Internal by `type`) into an auto-created planner and links it from the event note; it must NOT be registered as an action in /Trackers/Open Actions.md. Manual early planner creation still allowed for complex events. Tier 2 (procedure + ownership change). Trigger: Connor's request.
- 2026-06-05: Initial workflow created, Tier 1, trigger: Connor's request
- 2026-06-05: Added Event-Day Checklist section referencing Concert and Internal Event checklists, Tier 1, trigger: concert checklist synthesis
- 2026-06-08: Added "Projection / screen setup" as standard Logistics row, Tier 2, trigger: Connor's request — projection detail was missing from World Cup planning note
- 2026-06-08: Added Summary section as first body section, Tier 2, trigger: Connor's request — brief overview needed at top of every event note
- 2026-06-09: Added "Comms request submitted through Rock" as standard Marketing & Comms checkbox, Tier 2, trigger: Connor's request — required for every event
- 2026-06-15: Added rename-on-date-change rule to Filename Convention; defaulted Room setup/teardown owner to Connor (through Dec 2026); added Day-Of Planner companion-note spec. Tier 2 (new procedural rules + schema). Trigger: 2026-06-15 system audit, approved by Connor.
- 2026-06-16: Event action items must be registered in /Trackers/Open Actions.md at creation, not gated behind `active`/`complete` status — long lead time means a low Priority band, not omission. Reframed "After the Event" step 4 from "ensure they appear" to a final reconciliation. Tier 2 (new procedural rule). Trigger: Connor's request — Sunday Night Service launch actions were sitting only in the event note, invisible on the tracker.
