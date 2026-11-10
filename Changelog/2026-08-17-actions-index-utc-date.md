---
type: changelog
date: 2026-08-17
tier: 2
touches: ["[[Workflows/actions-index.py]]", "[[Workflows/Open-Actions-Tracker]]"]
trigger: "Step 0 index reported a live chase_by as passed, at 22:30 ET"
---
# actions-index.py computed every date off the UTC system clock

## What happened

The 22:30 ET quick refresh ran Step 0 and got:

```
## CHASE-BY PASSED (Step 3 — flag immediately, on the clock not the calendar)
  - Connor - Ask Heather Noble whether NFC tapping will be ready for Sept 20 (chase_by 2026-08-18 passed)
```

`chase_by` is 2026-08-18. It was 2026-08-17 22:30 ET. The chase had not fired; it fires in 90 minutes. The note's own two most recent entries both say so in terms — *"`chase_by` 8/18 fires tomorrow"* — which is how the contradiction was visible at all.

Step 3 says a passed `chase_by` is flagged **immediately**, jumping the 7-day rule, and leads the report. Had the index been trusted, this run would have written a `flagged:` property onto a healthy item and led Connor's work queue with a chase that wasn't due.

## Root cause

`main()` computed `today = datetime.date.today()` and `now = datetime.datetime.now()` — both naive, both off the system clock. This vault's execution shell reports **UTC**. Every evening between 20:00 and 24:00 ET the script therefore ran a day ahead.

That is not one wrong list. `today` feeds **every** date computation in the file: `CHASE-BY PASSED`, `NEGLECT CANDIDATES` (the 7-day arithmetic), `ESCALATION CANDIDATES` (the 21-day and 7-day windows), `ON-HOLD RELEASE CHECKS`, and the `--brief` buckets — including *overdue or due today*, which is the first thing Connor reads. On this run the Callie item also computed as **0 days to needs_by** instead of 1.

This is the same class of defect as [[Changelog/2026-08-17-timezone-marker-defect]] — the shell reports UTC and the code believed it — but that one was corrected by re-reading a marker with `TZ=America/New_York`. This one was in code, so it was fixed in code and measured.

## The change

```python
from zoneinfo import ZoneInfo
ET = ZoneInfo("America/New_York")
...
_et_now = datetime.datetime.now(ET).replace(tzinfo=None)
today = _et_now.date()
now   = _et_now
```

`now` stays naive so it still compares against the naive datetimes `chase_by: YYYY-MM-DD HH:MM` parses into. The `--today` override is untouched.

## Measured, not asserted

Same vault, same second, old script vs. new:

| | `CHASE-BY PASSED` | Callie escalation |
|---|---|---|
| naive (UTC) | Heather Noble NFC — *passed* | 0 days to needs_by |
| ET | **(none)** | 1 day to needs_by |

## Blast radius

Any sweep run after ~20:00 ET since the script was written read dates one day early. Morning and afternoon runs — which is nearly all of them, including the 6 AM Monday `grace-weekly-refresh` — were correct, so no historical flag is presumed wrong; this was not audited backwards. Worth knowing if a past evening run's flag looks unfounded.
