---
name: "🔔 Connor: Confirm standard timing rules for event communications (attendee/volunteer reminders, registration follow-ups)"
status: completed
priority: P2
owner: "Connor"
added: 2026-07-18
deadline: none
needs_by: none
last_mentioned: "2026-08-17"
resolved: 2026-08-17
source: "Connor, 2026-07-18 (direct chat request)"
projects:
  - "Boot Camp"
source_line: 242

---

# 🔔 Connor: Confirm standard timing rules for event communications (attendee/volunteer reminders, registration follow-ups)

- **Priority rationale**: checklist floors P1 (Connor directly assigned this, 2026-07-18 chat request), but banding P2 since this is a system/process-design task with no per-event deadline, not itself a do-now for a single event. *Connor: override to P1 if you want this pinned to Boot Camp Summer Camp's 7/29 date specifically.* **Left at P2 on 2026-07-28** — the 7/29 pin is moot now that the event is cancelled.
- 📌 **Scope, stated plainly (clarified by Connor 2026-07-28, after I got it wrong).** This item is about **when to communicate with people about events** — the outbound timing conventions for attendee reminders, volunteer/crew reminders, and registration checks. **It is not about Connor's internal task tracking**, and not about how the vault or automation gets findings in front of him. Those are a separate concern; do not fold them back in here. See the companion item [[Archive/Actions/Connor - Fix internal escalation — flagged findings and parked drafts don't reach Connor]].
- **2026-07-28 — one in-scope data point from the cancelled Boot Camp Summer Camp.** [[Events/2026-07-29-Boot-Camp/2026-07-29-Boot-Camp-Summer-Camp]] reached T-1 with **no invitations ever sent** to the alumni list. The relevant lesson for *this* item is narrow and real: **there was no standing rule stating how many days before an event a targeted invite has to go out**, so nothing in the process could identify the send as late. A rule of the form "targeted alumni/attendee invite goes out no later than N days before the event date" would have made the lateness a defined fact rather than a judgment call. That's exactly the convention this item exists to set — the event had a 7/29 date from 6/21, so the send window was knowable five weeks ahead.
- **Still the open decision:** the actual timing per comm type — attendee reminder N days out, crew confirm N days out, registration check N days out — for both church-wide pushes and targeted/known-list sends, which plausibly want different windows (the event note itself argued the alumni invite needed "shorter lead time than the World Cup because the list is known"). Once set, encode it in [[Workflows/event-checklist-autocopy]] and log it in [[Trackers/Automation]].
- **Source**: Connor, 2026-07-18 (direct chat request)
- **Needs-by rationale**: n/a
- **Status**: **Closed 2026-08-17 — cancelled by the owner who opened it, not completed.** Connor withdrew it; no timing convention was defined for attendee reminders, volunteer reminders or registration follow-ups.
- **Notes**: Boot Camp Summer Camp is the named example — worth using as the first test case once the rule exists, since it's 11 days out (2026-07-29) and already has an attendee/registration reminder precedent (7/16 leaders group-chat text) to compare a proactive flag against. **2026-07-21 (Connor): raise this at today's Connor–Derek sync** — agenda flag for the `derek-weekly-sync-agenda` draft.

- **⚠️ Flagged 2026-08-06 (Open Actions sweep, Step 3)** — reason: no follow-up in 9 days (last mentioned 2026-07-28). Nothing blocking; deadline Unstated, which is why it keeps sliding. **Two live events would have used it this week if it existed:** the **Mon 8/10 promo shoot** (no reminder went to Simba Kanjanda, who is the one unconfirmed participant — see [[Archive/Actions/Connor - Confirm Simba's attendance for the Mon 8-10 5-30 PM promo shoot]]), and the **Boot Camp table/team sign-up ask**, now on its third manual nudge (7/24 → 7/28 → 8/04) with one reply. Both are exactly the "Connor has to notice and send it himself" failure this item was opened to fix. Cheapest useful version: write down three numbers (attendee reminder N days out, crew confirm N days out, registration check N days out) and stop designing.
- **2026-08-11 (M365 email sync) — the intake path this item lives downstream of is being replaced.** **Derek Adye → AllStaff, "Staff Mtg Recap 8/11/26", 2026-08-11 2:32 PM ET:** *"Callie and Kay… new event request form in Rock."* The route Connor used for the **Mon 8/10 promo shoot** (request via Callie Taylor) has changed. **No status change and nothing owed** — recorded because whatever timing defaults this item eventually settles on will have to live *in* that form to actually fire, rather than in a note Connor has to remember to consult. If the form is being built now, that is the cheap moment to get three numbers into it. [Source: Email — Derek Adye, "Staff Mtg Recap 8/11/26", 2026-08-11 2:32 PM ET]
- **Blocked by**: none
- **Blocks**: none
---
## 🟡 In Progress
- **2026-08-12 (standalone sweep) — flag cleared.** The 2026-08-10 flag ("no follow-up in 13 days") was superseded by the **2026-08-11** entry above; per [[Workflows/Open-Actions-Reference]] § Flagging, a mention or update clears a flag, and `last_mentioned` is now newer than the flag. ⚠️ **Read this as bookkeeping, not progress** — nothing has been decided on the three timing numbers, and the 8/11 entry itself says "no status change and nothing owed." If the Rock event-request form ships without defaults in it, this will re-flag on ~8/19 with the window narrower than it is today.

### 2026-08-17 (transcript) — first real time-of-day data point, and it came from the recipients
- Weekend feedback from the younger Sunday-night volunteers: **daytime texts are harder to respond to than evening texts**
- Connor acted on it immediately — the 8/30 lunch invite is scheduled to send in the evening
- **In scope, and it is a fourth number this item never had:** the rule shape has been *N days out*; this adds *what time of day*, at least for the 20s-30s volunteer cohort
- Still nothing decided on the three N-day numbers. No status or band change

### 2026-08-17 (Connor) — **cancelled by the owner who opened it.** Not completed; withdrawn.
- Connor: *"The comms timing is something that I think I'll just learn with time"*
- Opened 2026-07-18 at his own request; the premise (encode N-day rules so automation fires them) is withdrawn in favor of experiential judgment
- **Nothing replaces it.** No rule will be written into [[Workflows/event-checklist-autocopy]] and none goes into the new Rock event-request form
- **The cost he is accepting, stated once and not re-raised:** this note's own history records two misses the rule would have caught — the Boot Camp Summer Camp alumni invite that was never sent (no rule made the lateness a defined fact) and Simba Kanjanda's un-sent 8/10 promo-shoot reminder
- **One thing did survive it:** the 8/17 finding that evening texts beat daytime texts for the 20s-30s volunteer cohort — a recipient-sourced fact, not a designed rule, and the exact shape of learning he is describing
- → status: active -> completed (cancelled). **Reopen in one word if this was softer than it read.**
