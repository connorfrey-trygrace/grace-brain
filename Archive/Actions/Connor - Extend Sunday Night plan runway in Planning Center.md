---
name: "📅 Connor: Extend Sunday Night plan runway in Planning Center"
status: completed
resolved: 2026-09-22
priority: P1
owner: "Connor"
added: 2026-09-21
deadline: none
needs_by: 2026-09-28
last_mentioned: "2026-09-22"
source: "PCO Services, service type 1804248 (Sunday Night), snl-week-ahead scheduled check"
projects:
  - "Sunday Night Launch"
---
# 📅 Connor: Extend Sunday Night plan runway in Planning Center

- [ ] Run the `snl-extend-plans` ad-hoc task (browser-driven, one click) to bulk-create SNL plans past 2026-10-11.

- **Priority rationale**: short runway blocks recruiting before it blocks anything else — volunteers can't be scheduled against plans that don't exist yet.
- **Source**: PCO Services, service type 1804248 ("Sunday Night") — id 1814753 is an empty duplicate, ignore.
- **Needs-by rationale**: recurring risk, not a one-time deadline — re-check weekly via `snl-week-ahead`; flagged now because runway has fallen under 6 weeks.
- **Status**: **Completed 2026-09-22** — `snl-extend-plans` created 9 plans (10/18–12/13, 6 PM); API-verified; runway now ends 2026-12-13.

### 2026-09-21 (snl-week-ahead, scheduled check) — created
- Furthest plan: 2026-10-11, ~3 weeks out (need 6+)
- Next step named: run `snl-extend-plans`

### 2026-09-22 (Connor, chat) — done
- Connor: "Done" — `snl-extend-plans` run
- → status: active → completed
