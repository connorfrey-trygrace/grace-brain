---
name: 2026-09-15-pending-drafts-check-built
---

# Built the approval-pending nudge; closed the internal-escalation item

**What happened:** [[Archive/Actions/Connor - Fix internal escalation — flagged findings and parked drafts don't reach Connor]] had sat as an undesigned problem statement since 2026-07-28, flagged for neglect on 2026-08-20. Connor asked for it directly ("no YOU go for it") during the 2026-09-15 quick refresh.

**What was decided and built:**
- **Direction #1 (a delivery channel)** — judged already solved by architecture: `grace-quick-refresh`'s move to on-demand, Start-Here-first reporting (culminating in the 2026-09-12 retirement of the fixed weekly auto-run) already gets flagged items in front of Connor the same session, which this very item's own path through this run demonstrates.
- **Direction #2 (an approval-pending nudge)** — built as [[Workflows/pending-drafts-check.py]]: scans the vault for `tags: [..., draft, ...]` files outside `/Archive` untouched ≥5 days. Detection-only, same split as `query-messages.py`/`resolve-phone.py`. Wired into the standalone sweep as new [[Workflows/Open-Actions-Tracker]] Step 3.6, which runs on every `grace-quick-refresh` (Phase 3).
- **Direction #3 (trigger-liveness checking on On Hold items)** — left out of scope, no forcing deadline.

**First run's catch:** 8 hits. 2 were sent but left mistagged `draft` (fixed in place: `2026-07-24-Boot-Camp-Team-Signup-Draft`, `2026-07-19-Boot-Camp-Vision-Lunch-Recap-Text-Draft`). 3 are dead (event cancelled or already happened) and belong in `/Archive` — surfaced to Connor rather than archived unilaterally. 2 are correctly held on a known, already-tracked trigger (JeanPaul Timeline Draft; Volunteer Signup Email Draft) — left alone. 1 was genuinely live and urgent: [[Events/2026-09-16-Boot-Camp-Fall-Relaunch/2026-07-28-Boot-Camp-Table-Outreach-Text]], a send-ready leader text drafted 48 days ago and never sent, supporting a relaunch happening the next day — minted as [[Archive/Actions/Connor - Send the Boot Camp table-outreach text to leaders]] and surfaced directly in the run's report.

**Touches:** [[Workflows/pending-drafts-check.py]] (new) · [[Workflows/Open-Actions-Tracker]] (new Step 3.6) · [[Workflows/grace-quick-refresh]] (Phase 3 step list).
