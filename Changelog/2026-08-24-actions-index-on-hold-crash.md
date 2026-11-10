---
date: 2026-08-24
file: Workflows/actions-index.py
kind: defect fix
found_by: grace-weekly-refresh (Mon 6 AM safety net)
---

# actions-index.py crashed on the first on-hold release date that wasn't phrased "trigger:"

## What happened

`python3 "Workflows/actions-index.py"` died with:

```
AttributeError: 'NoneType' object has no attribute 'group'
  File "Workflows/actions-index.py", line 551, in main
    % (n["file"], max(hits), (m.group(1) or "")[:70].strip()))
```

It printed the 53-row live-item table and then stopped. **Every candidate list came after that point** — `CHASE-BY PASSED`, `NEGLECT CANDIDATES`, `ESCALATION CANDIDATES`, `ON-HOLD RELEASE CHECKS`, `OPEN CLOSURE CANDIDATES`, `WAITING-ON WITH NO SHARED OCCASION`, `REDUNDANT BODY FIELDS`, `STATUS CONTRADICTIONS`, `OVERSIZED NOTES`, `MALFORMED DATE FIELDS`.

Step 0 of [[Workflows/Open-Actions-Tracker]] is not optional and every later step keys off those lists, so **the whole sweep was unrunnable** until this was fixed.

## Cause

The on-hold branch assumed `on_hold_since` always spells the release condition as `trigger: ...`:

```python
m = re.search(r"trigger:\s*(.*)$", n["on_hold_since"], re.S | re.I)
release.append(... (m.group(1) or "") ...)
```

Three notes don't use that keyword. [[Archive/Actions/Connor - Send JeanPaul the Sunday-night services general timeline (call times, run-throughs, service, closing)]] phrases it as **`Wake-up: 2026-08-24`**; the other two say *"re-activate on the day of launch"* and *"Date-locked: re-activate 2026-12-01"*.

**Nothing had crashed before because the crash needs two conditions at once:** no `trigger:` keyword **and** a date in the field that is `<= today`. Today, 2026-08-24, is the JeanPaul wake-up date — the first day both held. The bug was written whenever that branch was, and sat dormant.

That is the shape worth remembering: a formatting assumption in the sweep's own tooling, latent for weeks, that fires on the exact day the item it guards comes due — the day the sweep most needs to work.

## Fix

Match `wake-up:` as well as `trigger:`, and fall back to the raw field instead of assuming the keyword is there:

```python
m = re.search(r"(?:trigger|wake-?up)\s*:\s*(.*)$", n["on_hold_since"], re.S | re.I)
why = (m.group(1) if m else n["on_hold_since"]) or ""
```

**Verified by running it, not by reading it** (per [[feedback_verify_fixes_by_measurement]]): the index now completes, and `ON-HOLD RELEASE CHECKS` correctly names the JeanPaul item with its wake-up date. `--drift` also completes: 0 status contradictions, 0 redundant body fields across 82 notes.

## Not done, deliberately

The three notes were **not** rewritten to use `trigger:`. Normalizing the prose would fix today's crash and leave the next unanticipated phrasing to crash again — the parser should tolerate the field, not the field conform to the parser. If Connor wants a canonical phrasing for `on_hold_since` that is a separate convention decision, and it belongs in [[Workflows/Open-Actions-Reference]], not in a defect fix.
