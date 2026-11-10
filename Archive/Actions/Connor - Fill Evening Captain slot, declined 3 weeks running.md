---
name: "🪑 Connor: Fill Evening Captain slot — declined 3 weeks running"
status: completed
priority: P1
owner: "Connor"
added: 2026-09-21
deadline: 2026-09-27
needs_by: 2026-09-24
last_mentioned: "2026-09-21"
resolved: 2026-09-21
source: "PCO Services, service type 1804248 (Sunday Night), snl-week-ahead scheduled check"
projects:
  - "Sunday Night Launch"
people:
  - "[[People/Connor Frey]]"
---
# 🪑 Connor: Fill Evening Captain slot — declined 3 weeks running

- [ ] Name a Captain (or accept the slot himself) for 9/27, 10/4, 10/11 — currently the only person on the Captain team is Connor, declined on all three.

- **Priority rationale**: Captain is the on-site lead role; three straight Sundays with nobody covering it is a real gap, not a scheduling artifact.
- **Source**: PCO Services roster pulls for plans 91453887 (9/27), 91455422 (10/4), 91781260 (10/11).
- **Needs-by rationale**: enough runway to recruit/confirm before the nearest affected Sunday, 9/27.
- **Status**: **Completed 2026-09-21** — Connor took the slot himself on all three plans, at his instruction. Flipped declined → confirmed in PCO and verified through the API (`status_updated_at` 2026-09-21 19:48–19:49Z): 9/27 plan 91453887, 10/4 plan 91455422, 10/11 plan 91781260.
- **Notes**: 10/4 plan also has a decline cluster worth watching — Sean Liesegang (Usher), Elizabeth Goodiel (Front Doors), Michael Vacca (Slides), Emily Horneffer (Host) all declined that week, vs. all 14 confirmed on the 9/20 baseline. 9/27 and 10/11 don't show this pattern (1-2 declines each, Captain only or Captain + one Usher).
- **Blocked by**: none

### 2026-09-21 (snl-week-ahead, scheduled check) — created
- Captain declined by Connor on 9/27, 10/4, 10/11 — only person on that team each week
- 10/4 additional declines: Sean Liesegang, Elizabeth Goodiel, Michael Vacca, Emily Horneffer

### 2026-09-21 (quick refresh, sweep, Step 0) — malformed date field corrected
- `deadline` was free text (`"2026-09-27, first of the three affected plans"`), which the index flags because prose in a date field silently fabricates deadlines.
- **Deadline rationale**: 2026-09-27 — the first of the three affected plans. Prose moved here; the field is now a bare date.

### 2026-09-21 (Connor, live session)
- Connor: confirm him as Captain for all three weeks
- Captain flipped declined → confirmed on 9/27, 10/4, 10/11; API-verified
- → status: active → completed
- ⚠️ Each plan still shows a blockout on Connor for that 6:00 PM slot, and Captain still reads 1 Needed on 9/27 and 10/4
