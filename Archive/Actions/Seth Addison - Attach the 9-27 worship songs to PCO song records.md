---
name: "🎵 Seth Addison: Attach the 9-27 worship songs to PCO song records"
status: completed
priority: P1
owner: "Seth Addison"
added: 2026-09-21
deadline: 2026-10-04
needs_by: 2026-09-29
last_mentioned: "2026-10-04"
resolved: 2026-10-04
source: "PCO Services, plans 91453887 (9/27) and 91455422 (10/4), worship items"
projects:
  - "Sunday Night Launch"
people:
  - "[[People/Seth Addison]]"
  - "[[People/Connor Frey]]"
  - "[[People/Michael Vacca]]"
---
# 🎵 Seth Addison: Attach the 9-27 worship songs to PCO song records

- [ ] Link the 10/4 worship items (seq 7, 9, 11) to real PCO song library records — rolled forward from 9/27, which ran unlinked. Originally: link all three 9/27 worship items to real PCO song library records (not just free-text titles), so lyrics/arrangement flow to Michael Vacca's slides.

- **Priority rationale**: lyrics have to reach ProPresenter early in the week (per the Monday service-prep check's own rationale) and the deadline is this Sunday — inside the 1-week escalation window.
- **Source**: weekly SNL service-prep check (scheduled task), 2026-09-21 run — PCO plan 91453887, `services_plan_items` with `include: song` returned `song: null` for all three worship items:
  - seq 7, "Song: Medley (Can't Help Falling In Love / Jireh)"
  - seq 9, "Song: Home"
  - seq 11, "Song: Medley (Cast Them All / Great Are You Lord / Graves Into Gardens / Gratitude)"
  All three have full titles typed into the free-text description/title only — none carries a song relationship. This is the same failure mode flagged on the 9/20 plan (also 0-for-0 there), now confirmed again on 9/27.
- **Deadline rationale**: 10/4 service (rolled from 9/27).
- **Needs-by rationale**: worship-content deadline is "around Tuesday" per the standing Monday check rationale — slides/lyrics need the week's runway.
- **Status**: **Completed 2026-10-04** — Connor confirmed closed in live session.

### 2026-09-21 (weekly SNL service-prep check) — created
- Confirmed via `services_plan_items` (`include: ["song"]`) that all three worship items on the 9/27 plan have `song: null`.

### 2026-09-23 (email) — Seth sharing docs
- 10:29 AM · Seth shared Google Doc "Worship Medley 9/27"; 11:05 AM · "The Vine" — both with edit access
- Doesn't evidence the PCO song-record linking; still open
[Source: Email, Google Drive share notifications (Seth Addison), 2026-09-23]

### 2026-09-28 (weekly SNL service-prep check) — rolled to 10/4
- 9/27 plan (91453887): Worship Medley / The Vine still `song: null` — ran unlinked
- 10/4 plan (91455422): seq 7 Medley (Can't Help Falling In Love / Jireh), seq 9 Home, seq 11 Medley (Cast Them All / Great Are You Lord / Graves Into Gardens / Gratitude) — all `song: null`
- These titles match the 9/20 set, not a new 10/4 set — see [[Archive/Actions/Michael Vacca - Correct stale week-1 content in the 10-4 PCO plan]]
- → deadline: 2026-09-27 → 2026-10-04; needs_by: 2026-09-22 → 2026-09-29

### 2026-10-04 (Connor, chat) — closed
- Connor: "9/27 is closed." Closed.
