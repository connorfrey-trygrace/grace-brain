---
type: changelog
date: 2026-08-21
tier: 2
touches: ["[[Workflows/actions-index.py]]", "[[Workflows/grace-quick-refresh]]"]
trigger: "Connor, 2026-08-21 — \"We need to fix the 'start here' to prioritize 14 days, not 7 days\""
---
# Start Here looks 14 days ahead, not 7 — and the horizon is now a named constant, not a bare literal

`--brief`'s date-urgency window was a hardcoded `7` on one line inside `brief()`. It is now `HORIZON_DAYS = 14`.

**Why.** At 7 days the 2026-08-21 morning queue could not see the **8/30 formation lunch nine days out with no invite sent** — Connor: *"So I have no open actions? That can't be right."* That run's post-mortem blamed the today-only gate stacking on top of `--brief`, which was half the story; the other half is that the candidate window itself was too narrow to contain the thing that mattered.

**Measured before changing anything: 6 items were hidden by the 7-day window** — the 8/30 formation lunch, its deck, the PCO roster, the Sunday-night marketing item (needs_by 8/30), and the two Boot Camp items at needs_by 9/02. Four of the six are 8/30-dated, i.e. the single busiest date on the board was entirely outside the horizon.

## Three unrelated 7s, and only one of them moved

The number was easy to get wrong because the file held three sevens that mean different things. They are now distinguished in the source:

| constant | meaning | changed |
|---|---|---|
| `HORIZON_DAYS` | how far ahead Start Here looks | **7 → 14** |
| `NEGLECT_DAYS` | how long silence is tolerated before flagging | unchanged |
| `P1_WINDOW` | banding window for escalation to P1 | unchanged |

Verified by regression: the **full sweep view is byte-identical** before and after, so neglect flagging and escalation banding are provably untouched. Only `--brief` changed.

## Two consequences handled rather than discovered later

- **The horizon bucket now sorts by date, not by band.** At 7 days, band-first ordering was harmless. At 14 it would print a P1 due in 13 days above a P2 due in 8 — the wrong reading order for a list whose entire meaning is *what is coming at me and when*. Other buckets still sort by band.
- **Cap raised 8 → 12 for that section.** The measured result was exactly 8 rows, sitting precisely on the old cap, so the first useful widening would have been swallowed by `... +N more`.
- Label changed from "This week" to "Next 14 days", since it is no longer a week.
- Side effect, and an improvement: flagged items that also carry a date in the 8–14 day range now surface in the dated bucket instead of under **Flagged / stalled** (which fell 10 → 8). A date is more actionable than *"stalled 8 days."*

## What this does not change

**The today-only gate still applies and is still a subtraction.** A wider horizon means *more* candidates reaching that gate, not fewer judgment calls — an item 12 days out with no action available today still does not go in Start Here. This change fixes what the gate gets to choose from; it does not loosen the gate.
