---
date: 2026-08-12
governs: "[[Workflows/actions-index.py]]"
related: "[[Workflows/Open-Actions-Tracker]]"
---
# actions-index.py — `chase_by` comparison is now time-aware

## What changed

`chase_by` was compared with `first_date()`, which regex-matches `YYYY-MM-DD` and **discards any time component**. The sweep then tested `cb <= today`, so a `chase_by` naming a time **later today** reported as *passed* from 00:00 that morning. Same defect independently in `brief()`.

Added `first_dt()` (date **and** time, returns `None` when the field carries no time) and used it in both places. Fields with no time still fire on the day, exactly as before — this only changes fields that name an hour.

`--brief` now distinguishes the two states rather than collapsing them: a fuse still ahead reads `chase-by 1:00 PM — live fuse`, a fuse behind reads `chase-by 2026-08-12 passed`. Both stay in the **Overdue or due today** bucket, which is correct — a fuse burning down today is exactly what belongs at the top of a work queue.

## Why it matters

[[Workflows/Open-Actions-Tracker]] Step 3 is explicit that short-fuse items are swept **"on the clock, not the calendar,"** and it gives two opposite instructions keyed on that comparison: if `chase_by` has passed, **flag immediately**; if it has not, **"leave the item entirely alone this sweep."** The index was answering that question on the calendar, so it steered the sweep into the wrong branch for the whole of the fuse's live day.

Found on the 2026-08-12 12:24 ET quick refresh, where **both** of the day's `chase_by` items surfaced as passed:

- `Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags` — `chase_by 2026-08-12 13:00 ET`, **36 minutes in the future**
- `Jennifer Claffey - Planning Center support Zoom on PCO tag creation + Rock sync (8-12 12-15 PM)` — `chase_by 2026-08-12 17:00 ET`, **4.5 hours in the future**

Flagging either would have been wrong twice over: it records a chase that never happened, and per Step 3 a flag suppresses the *real* flag later (`not n["flagged"]` gates the check), so the fuse that actually matters would go unswept when it did burn down.

The failure mode is quiet and self-limiting — it only misfires on days when a fuse is set, which is why it survived since `chase_by` was introduced. The 8/11 12:00 fuse on the Kay item is the one prior instance, and it happened to be genuinely passed by the time that sweep ran.

## Scope

Two functions in one script. No note bodies touched, no statuses changed, no procedure text edited — the procedure was already right and the code disagreed with it.
