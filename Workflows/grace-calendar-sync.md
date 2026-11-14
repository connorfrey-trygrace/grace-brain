# Workflow: Grace Calendar sync (Outlook → Notion)

Copies Connor's Grace Outlook calendar into Notion's **Grace Calendar** table so My Day and Personal Claude's planner can read Grace events as data without the Microsoft 365 connector. Requested by Personal Claude in Agent Mail MSG-28; Connor approved it 2026-11-13.

**Runs on every run that can reach Outlook:** `grace-quick-refresh` Phase 1 (reuses that phase's calendar pull), the 5 AM cloud routine (via Notion's Start here: Grace Claude), and the first daily run of `agent-hub-visit-local`. Any one run keeps the table current. The others just refresh the heartbeat.

## Target

- Grace Calendar data source: `collection://41812cb6-3a8b-8134-ad1d-000bafb14bc1`
- Read existing rows through the **Default view** `view://41812cb6-3a8b-810e-b84e-000c94cafcff` (view mode). Never use SQL or `rows` queries. Never edit or delete the view named **"Dashboard feed (don't edit)"**.

## Steps

1. **Pull** the next 14 days with `outlook_calendar_search` (query `*`, order `oldest`, page by `nextOffset` to the end). Never use Google Calendar. Times come back in UTC, so convert them to ET.
2. **Skip** the self-blocks `Morning Availability`, `Afternoon Availability` and `Daily FTJ Conflict`.
3. **Upsert by Outlook ID.** Use the event `id` from the search result, not the URI. Update a row whose Outlook ID matches. Otherwise create one:
   - Event: subject verbatim
   - When: start + end with the Eastern offset (`-05:00` EST, `-04:00` EDT). All-day events use dates only (`is_datetime` 0).
   - Location: the Outlook location. For a Zoom/Teams URL, write `Zoom` or `Teams`, never the link with its password.
   - Link: the event's `webLink`
   - Outlook ID
   - Agent synced: now
4. **Cancelled.** If a row inside the 14-day window has no matching Outlook event, or the event has `isCancelled: true`, tick **Cancelled**. Never delete rows.
5. **Heartbeat, every run, even when nothing changed:** set **Agent synced** = now (ET offset, `is_datetime` 1) on the next upcoming non-cancelled event. My Day uses it to show when the calendar went stale (Mac asleep, connector down).
6. **If Outlook is unreachable:** write nothing and say so in the run report. The stale heartbeat is the signal.

Prep tasks for Grace events stay in Grace Tasks, not here.
