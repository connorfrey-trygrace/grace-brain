---
type: changelog
date: 2026-08-12
tier: 3
touches: ["[[Workflows/actions-index.py]]","[[Trackers/Actions]]"]
trigger: "Connor"
---
# `deadline`, `needs_by` and `chase_by` are now a bare date, `YYYY-MM-DD HH:MM`, or `none`

The fields were free text, and `first_date()` takes the first date **anywhere** in the string — so `deadline: "Unstated — named as this week's Priority 3 (week of 2026-08-10)"` parsed as a deadline of 8/10 and the item reported as overdue. The sweep spent a full body read re-diagnosing the same false positive on three consecutive runs (8/11 13:16, 8/11 13:46, 8/12 00:16).

44 of 45 live notes migrated; prose moved to a `- **<Field> rationale**:` body bullet, nothing lost. Zero unresolved — every value parsed. `actions-index.py` gained a **MALFORMED DATE FIELDS** section so the structure can't silently rot back. Verified: the feedback-form item no longer appears as overdue.
