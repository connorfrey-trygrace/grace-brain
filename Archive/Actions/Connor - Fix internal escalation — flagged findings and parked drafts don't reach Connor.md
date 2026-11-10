---
name: "📣 Connor: Fix internal escalation — flagged findings and parked drafts don't reach Connor"
status: completed
priority: P3
owner: "Connor"
added: 2026-07-28
deadline: none
needs_by: none
last_mentioned: "2026-09-15"
resolved: 2026-09-15
source: "2026-07-28 — split out of [[Archive/Actions/Connor - Confirm standard timing rules for event communications (attendeevolunteer reminders, registration follow-ups)]] after Connor corrected its scope; diagnosed from the cancelled [[Events/2026-07-29-Boot-Camp/2026-07-29-Boot-Camp-Summer-Camp]]"
projects:
  - "Vault System"
---

# 📣 Connor: Fix internal escalation — flagged findings and parked drafts don't reach Connor

- **Priority rationale**: a real system gap with no deadline and no event riding on it. Banded low deliberately; **Connor should kill this item if he'd rather not carry a meta-task**, since nothing external breaks if it never gets done. Raising the band only makes sense if a second event dies the same way.
- **Scope — and what it deliberately excludes.** This is about **internal** escalation: how the vault, the scheduled jobs, and drafts-awaiting-approval get Connor's attention. It is **not** about outbound event comms timing — that's [[Archive/Actions/Connor - Confirm standard timing rules for event communications (attendeevolunteer reminders, registration follow-ups)]], which Connor clarified on 2026-07-28 covers *when to communicate with people about events* and nothing else. The two were briefly conflated in that item's notes; they are now separate on purpose. Don't merge them again.
- **Source**: Split out 2026-07-28 after Connor corrected the scope creep. Diagnosed from the [[Events/2026-07-29-Boot-Camp/2026-07-29-Boot-Camp-Summer-Camp]] cancellation.
- **Status**: Completed 2026-09-15 — see the closing entry below.
- **The evidence.** The Boot Camp Summer Camp died at T-1 with every safeguard working correctly:
    - `event-checklist-autocopy` built the Day-Of Planner on time at T-7 (7/22), and that planner accurately named every missing input — venue, start time, food lead, Rock registration, comms — with dates assigned to 7/23–7/27. **It was never opened.**
    - The invite + Rock event-request draft was correctly held pending Connor's clearance per the standing never-auto-submit rule. It waited **33 days (6/25 → 7/28)**. Nothing ever prompted the clearance decision. The rule worked; the follow-through had no owner.
    - The stale sweep flagged the umbrella item on **7/28** — one day out. Early enough to be an obituary, not a reminder.
    - Separately and on the same day, two items were found parked 37 days each on a trigger that had become permanently unreachable ([[Archive/Actions/Connor - Boot camp relaunch]], [[Archive/Actions/Connor - Identify Sunday night hostMC (boot camp alumni pool)]]) — the same class of failure: correct information sitting in a file nobody was reading.
- **The problem in one line**: a finding that lands as a line in a vault note Connor isn't reading that day is indistinguishable from no finding at all. The system's detection is good; its delivery is nonexistent.
- **Notes** — three candidate directions, none decided:
    1. **A delivery channel for flagged items.** The weekly refresh and sweeps already produce run reports; nothing carries them to Connor. Options include folding a short "needs your attention" section into the existing morning brief, or a push (text/email) gated to genuinely urgent flags only, so it doesn't become noise Connor learns to ignore.
    2. **An approval-pending nudge.** Drafts held awaiting Connor's clearance currently have no expiry and no reminder. A rule like "any `status: NOT SUBMITTED` draft older than N days surfaces as a flagged item" would have caught the invite around 7/2 instead of never. This is the single highest-value piece and the cheapest to build.
    3. **Trigger-liveness checking on On Hold items.** The sweep asks "has the trigger cleared?" and never "is the trigger still alive?" — see [[Workflows/Open-Actions-Tracker]]. Cancelling an item should also surface its `blocked_by` dependents for re-keying in the same pass (done manually on 7/28).

- **⚠️ Flagged 2026-08-06 (Open Actions sweep, Step 3)** — reason: no follow-up in 9 days (last mentioned 2026-07-28); still a problem statement with no design. **This sweep produced fresh evidence for it, which is either useful or ironic depending on your mood:** (a) the **Rock instance 542 re-pull** has been recommended in [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] on 7/27, 7/28, 8/03 and again today — **four sync reports, no owner, no action item, five incomplete rows**; and (b) the **8/03 reactivation of [[Trackers/Actions/Connor - Design new-guy table-routing system for Boot Camp]]** was made unattended with an explicit "confirm or reverse this" request that has now gone unanswered through two sweeps. Both are findings that reached a report and stopped there — the precise failure this item names.
- **Blocked by**: none

- **2026-08-11 — the 542 re-pull resolved, and how it resolved is the clearest evidence this item will ever get.** It was recommended in **six consecutive sync reports** (7/27, 7/28, 8/03, 8/06, 8/10, 8/11) across [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] and four action notes. It never had an owner, never became an item, and blocked placement for five volunteers for **14 days**. It was resolved the moment **Connor read a report and said "go do it"** — and the work took about **five minutes**.
    - **The failure was not effort, priority, or difficulty. It was routing.** Every ingredient was in the vault: the instance ID, the admin URL, the list of blank rows, and a live browser session. What was missing was any mechanism that converts *"recommended in a report"* into *"assigned to someone."*
    - **Concrete design input for this item:** a finding repeated in N consecutive reports should be **auto-minted as an action item with an owner**, not restated. Repetition is currently the system's only escalation move, and repetition is exactly what a human skims past. Suggested rule: **third consecutive appearance → create the item.** That would have opened this on 8/03 and saved eight days.
- **2026-08-12 (standalone sweep) — flag cleared.** Superseded by the **2026-08-11** entry above (the 542 re-pull resolution), which is real new information about this item's subject matter; per [[Workflows/Open-Actions-Reference]] § Flagging, an update clears the flag. ⚠️ **Still no work started on the fix itself** — the 8/11 entry is evidence *for* the problem, not a step toward solving it. Expect this to re-flag ~8/19 unless something is actually built.

### 2026-08-20 (standalone sweep)
- flagged: quiet 9 days, no blocker, no dates
- ⚠️ **This run added a sixth data point to its own case:** the `resolve-phone.py` PHANTOM defect was a *silent* wrong answer that only surfaced because a number happened to be in the roster already. The pattern this item names is not just findings failing to reach Connor — it is findings the system was confident about being wrong. See [[Changelog/2026-08-20-resolve-phone-wal-phantom-fix]]
- next physical action: **decide the one channel** flagged findings should land in (nothing else on this item is buildable until that's picked)

### 2026-09-15 (Connor: "no YOU go for it") — both open decisions closed
- **Direction #1 (a delivery channel) — decided: it's already been solved by architecture, not by picking a channel.** This item's own evidence (7/28) is from when the sweep ran on a fixed weekly cadence. Since then `grace-quick-refresh` moved to on-demand, Start-Here-first reporting (2026-08-10 → 2026-09-12 retirement of the weekly auto-run) — flagged/urgent items now surface as a work queue at the top of every refresh Connor runs, not buried in a report he may not open. This session is itself the evidence: item #7 in this run's Start Here queue *was* this note, flagged and surfaced, same session it got acted on.
- **Direction #2 (approval-pending nudge) — built.** New script [[Workflows/pending-drafts-check.py]]: finds any `tags: [..., draft, ...]` file outside `/Archive` untouched ≥5 days, detection-only (same split as `query-messages.py`/`resolve-phone.py` — it never writes). Wired into the standalone sweep as [[Workflows/Open-Actions-Tracker]] Step 3.6, which now runs on every `grace-quick-refresh`.
- **First run found exactly the failure this item describes, live, on the first try — the day before a real event.** 8 hits; triage: **2 sent-but-mistagged** (fixed the tag on the spot: `2026-07-24-Boot-Camp-Team-Signup-Draft`, `2026-07-19-Boot-Camp-Vision-Lunch-Recap-Text-Draft`), **3 dead and belonging in `/Archive`** (Summer Camp Invite-Draft — event cancelled; Leaders'-Vision-Lunch Invite-Draft and the NYC Trip Connect draft — both events already happened by other means; surfaced to Connor to confirm before archiving, not archived unilaterally), **2 correctly held on a known, already-tracked trigger** (JeanPaul Timeline Draft, Volunteer Signup Email Draft — the system working as designed, left alone), and **1 genuinely live and urgent**: [[Events/2026-09-16-Boot-Camp-Fall-Relaunch/2026-07-28-Boot-Camp-Table-Outreach-Text]] — a fully workshopped, "send-ready — awaiting Connor" leader text, drafted 48 days ago, never sent, re-pinging a team-pick ask that sat at 1 of ~21 replies — with the Fall Relaunch it supports happening **tomorrow, 2026-09-16**. Surfaced to Connor directly in this run's report rather than left for the next sweep.
- **Direction #3 (trigger-liveness checking on On Hold items) — deliberately out of scope, not pursued.** No deadline forced a decision on it and it's a distinct mechanism from the two built here; left as a candidate for its own item if it's ever picked up.
- → status: active → completed. Closed by explicit instruction, not by the passage of time.
[Source: Connor, chat, 2026-09-15]
