---
name: "🔎 Kay Carter-Corker: Investigate why the Connect Form report shows no submitted data"
status: completed
resolved: 2026-09-22
priority: P1
owner: "Kay Carter-Corker"
added: 2026-09-21
deadline: none
needs_by: 2026-09-27
last_mentioned: "2026-09-22"
waiting_on: "Kay Carter-Corker since 2026-09-21 — she is asking Melissa why the report returns nothing. Connor has already done his side (test submission)."
source: "Outlook thread 'Connect form responses!?!', Connor ↔ Kay Carter-Corker, 2026-09-20 10:29 PM → 2026-09-21 12:31 PM ET"
projects:
  - "Sunday Night Launch"
people:
  - "[[People/Kay Carter-Corker]]"
  - "[[People/Connor Frey]]"
---

# 🔎 Kay Carter-Corker: Investigate why the Connect Form report shows no submitted data

- [ ] Kay to ask Melissa why Rock report 219 returns no rows despite per-submission notification emails firing correctly.

- **Priority rationale**: P2 — the Connect form is the Sunday-night funnel's only measurement instrument. 149 people attended 9/20 and the report can see none of them. It is not service-blocking, but every week it stays broken is a week of launch data that cannot be recovered.
- **Needs-by rationale**: 2026-09-27 — the next service. A second week of unreadable data compounds the loss.
- **Source**: Outlook thread *"Connect form responses!?!"*, 2026-09-20 10:29 PM ET (Connor opens) → 2026-09-21 6:17 / 7:59 / 8:31 AM and 12:31 PM ET.
- **Status**: **Completed 2026-09-22** — not a bug, low response (Connor confirmed in chat).

### What is actually known
- **149 people** at the 9/20 6 PM service.
- Rock report: **https://trygrace.rockcloud.com/reporting/reports/219** — Kay confirmed she sees **zero submissions** in it.
- **Per-submission notification emails work fine.** Two arrived in the window: `Trixie Fake-Carter-Corker` (2026-09-21 6:40 AM ET, Kay's own test) and `Connor Frey` (7:58 AM ET, Connor's test at Kay's request). So the form captures and notifies; only the **report** is blind.
- That split — notifications firing, report empty — points at the report definition or its data view, not at the form. Worth saying to Melissa explicitly so the diagnosis starts in the right place.

### Connor-side, already done
- Test-submitted the QR form 9/21 7:58 AM at Kay's request ("Just submitted a test... maybe nobody filled one out last night" — since disproved by the notification emails).

### Connor-side, still open
- **Connor lacks Rock report permissions** and flagged it in this thread. Not yet its own item; it rides along here because the same conversation with Kay resolves both. If Kay's fix lands and Connor still can't open report 219 himself, that becomes its own note.
- Connor's standing ask for the report to **auto-run at 9 PM Sundays** is also unresolved in this thread.

- **Blocked by**: none · **Blocks**: any attendance/connect measurement of the launch series

### 2026-09-21 (quick refresh, sweep, Step 3.5) — re-banded P2 → P1
- Escalation window: mechanical raise against `needs_by`/`deadline`. No other field changed.

### 2026-09-22 (Connor) — not a bug, just low response
- Connor: the report/notification split wasn't Kay's fault — there was only one real submission from the 9/20 room.
- → status: waiting-on → closure-candidate

### 2026-09-22 (Connor, chat) — closure confirmed
- → status: closure-candidate → completed
