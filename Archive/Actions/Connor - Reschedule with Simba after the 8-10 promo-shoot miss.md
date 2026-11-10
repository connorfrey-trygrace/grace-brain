---
name: "🔁 Connor: Reschedule with Simba after the 8/10 promo-shoot miss"
status: completed
priority: P2
owner: "Connor"
resolved: 2026-08-17
added: 2026-08-11
deadline: 2026-08-16
last_mentioned: "2026-08-17"
source: "Text from Simba Kanjanda, 2026-08-10"
projects:
  - "Sunday Night Launch"
---

# 🔁 Connor: Reschedule with Simba after the 8/10 promo-shoot miss

- [ ] Reschedule with Simba after the 8/10 promo-shoot miss
- **Priority rationale**: **and this is a deliberate deviation from the mechanical read, recorded rather than applied silently.** [[Workflows/Open-Actions-Reference]] § Priority's escalation window (deadline within ~1 week → P1) would put this at P1 off the 8/16 date. Not doing that, for two reasons: (a) **the 8/16 date is derived by this sync, not stated by anyone** (see Deadline below) — escalating a band off a date the system invented itself is circular; and (b) importance is genuinely low, because Heather Noble already made Simba **upside rather than a dependency** (*"If Simba or Skylar can come, we can do a take with them as well"*, 8/06). The main asset is shot. **Connor or a sweep should feel free to raise this to P1 or drop it to P3 — the band is the least confident thing on this note.**
- **Source**: Text from **Simba Kanjanda** (267-858-2454), **2026-08-10**. He missed the 5:30 PM shoot — **5:31 PM**: *"Still in Rockville"* / *"I can be there in like an hour"*; Connor, **5:32 PM**: *"I hope I'm not here that long lol we can catch up another time"*. Simba's later message in the same thread — **"We can find another time this week ?"** — is the **unanswered last word in the thread.**
- **Status**: **Completed 2026-08-17** — Connor: *"Reschedule with Simba done."* The relational half repaired itself in the 8/15 thread; the production half is moot — the main promo asset was already shot ([[Archive/Actions/Connor - Shoot the Sunday Night promo video with Simba for Heather's campaign]] completed), so no pickup take is owed.
- **Notes**: Simba's reliability profile is worth carrying into the reschedule: he **answers texts within hours and ignores call requests** (the 8/06 12:18 PM ask for a phone call went unanswered; the 2:29 PM text plan got a yes by 8:20 PM), and he lives far enough out — **Rockville** — that a 5:30 PM after-work call time in Ashburn was optimistic in the first place, which is new information this thread produced. **Any rescheduled slot should account for travel from Rockville, not just for "after work."** If the pickup take happens, Heather's alternate crew dates were **Tue/Thu/Fri, normal business hours only** (8/06) — strictly worse for a full-time-employed volunteer, so a genuinely new evening slot would have to be negotiated, not picked off that list.
- **Blocked by**: [[Archive/Actions/Connor - Shoot the Sunday Night promo video with Simba for Heather's campaign]] — for the *production* half only (whether a second take is authorized). **The relational half — replying to Simba — is blocked by nothing and should not wait on it.**
- **Blocks**: none
- **Deadline rationale**: [derived] Simba's own \"another time this week\"; no explicit date was named by anyone · **[derived], and labelled as such on purpose.** Simba said *"this week"*; nobody named a date. **So the [[Workflows/text-message-sync]] Step 5 named-deadline rule does not strictly compel a separate note here** — that rule fires on an *explicit* commitment tied to a specific day ("I'll send X on Monday", "meeting Thursday at 3"), and "this week" is not that. **This note is a judgement call, and the judgement is that the unanswered-last-word property is what justifies it, not the date.** A vague deadline buried in the parent item's Notes is exactly the invisibility the Step 5 rule exists to prevent, and the parent is now a `closure-candidate` — an open thread parked inside an item awaiting closure is the worst place for it. If Connor disagrees, the right fix is to fold this back into the parent, not to re-date it.

- **2026-08-11 (Open Actions sweep, Step 3.5) — considered the mechanical P2 → P1 escalation and did NOT apply it. Recorded so the next sweep doesn't re-litigate it, and so Connor can overrule in one line.**
    - `python3 "Workflows/actions-index.py"` proposes **P2 → P1 (5 days to deadline 2026-08-16)**. Declined for the reason this note already argues in its own § Priority line: **the 8/16 date was derived by the sync that created this item, not stated by Simba or anyone else** — Simba said *"this week."* Escalating a band off a date the system invented itself is circular, and § Priority's escalation windows are meant to measure real commitments. Importance is also genuinely low on the production half: Heather Noble made Simba **upside, not a dependency** (*"If Simba or Skylar can come, we can do a take with them as well"*, 8/06), and the main asset is already shot.
    - **This is the one open band question on the board, and it is Connor's call.** The note invited it explicitly (*"the band is the least confident thing on this note"*). Raise it to P1 if the relational half matters more than the derived date suggests; drop it to P3 if the pickup take is off the table.
    - **What the sweep is *not* saying is that nothing is urgent here.** The **relational half is blocked by nothing** and has been Connor's move since **8/10 evening** — Simba's *"We can find another time this week ?"* is still the unanswered last word, now ~41 hours old, from a volunteer who confirmed twice and drove in from Rockville. No `chase_by` was set because no party named a clock; the decaying thing is goodwill, not a window. A real answer either way ("let me get a date from marketing" / "we got what we needed, let's just catch up") costs one text.
    - **Block left in place:** `blocked_by` still points at [[Archive/Actions/Connor - Shoot the Sunday Night promo video with Simba for Heather's campaign]], which is a `closure-candidate` — **believed complete but not closed**, so it is still an open blocker for the *production* half only, per § Closure Candidates. Recompute both ends if Connor confirms that candidate.

- **2026-08-11 (text sync) — 🟡 CLOSURE CANDIDATE. The property this item exists to protect is gone.**
    - This note is explicit that its justification is *"the unanswered-last-word property… not the date."* Simba's *"We can find another time this week?"* (8/10 5:32 PM ET) sat unanswered; Connor replied **8/11 10:55 AM ET** (~17 hours), Simba responded warmly, and the thread ends **11:59 AM ET** with *"I have 😂 / You're good."* Goodwill intact, nothing hanging.
    - **What's still not settled:** **no reschedule date was set, and the pickup take was never explicitly ruled out** — not to Simba, and not to Heather Noble. *"We got all the filming done yesterday"* strongly implies the pickup is off, but no one said so. This note's own guidance: *"drop it to P3 if the pickup take is off the table."*
    - **Connor's call:** close it outright, or hold at **P3** pending one line to Heather confirming no pickup is needed. Note `blocked_by` points at [[Archive/Actions/Connor - Shoot the Sunday Night promo video with Simba for Heather's campaign]], also a closure candidate — resolve the pair together. [Source: Texts, chat 141, 2026-08-11 10:55–11:59 ET]

- **2026-08-11 (transcript synthesis) — ⛓️‍💥 UNBLOCKED, and the case for doing it at all just got weaker. Status left as `closure-candidate` — Connor's call.** Source: [[Transcripts/2026-08-11 16.38 Connor–Derek Weekly Sync — Feedback Form Scoped & Catering Boundaries]]
    - `blocked_by` **cleared**: [[Archive/Actions/Connor - Shoot the Sunday Night promo video with Simba for Heather's campaign]] is now **completed**, confirmed first-person by Connor.
    - **The shoot did not come up short.** Two finished videos exist — Connor + Will Gralley (immediate) and Connor + Skylar Frey (6–8 weeks out). Heather Noble's campaign has what it needs, and **Connor described the outcome to Derek without once raising a pickup take or a reshoot.** Simba's absence was reported as a fact, not a gap.
    - **So the open question is not "when do we reshoot" — it is "is there anything to reshoot for."** If the answer is no, this closes outright; if Connor wants Simba on camera for relational reasons (he is a Boot Camp leader and a volunteer-recruiting contact), that is a *different* item with a different justification, and it should be written as one rather than inherited from a production need that no longer exists.
    - Per memory, the channel to Heather/Simba is **text, then a call** — Connor works remotely.

## 2026-08-15 (text sync) — the relationship half repaired itself. The production half did not. **Do not close on this.**

Simba volunteered unprompted in the high-tops group chat (8/15 12:55: *"I can help after 11:30 service if you still need people"*), Connor "Loved" it and replied directly (13:06: *"Simba I'll meet you right as the prayer team and new to Grace are mentioned"*). **They are back in contact with a shared Sunday plan** — which softens this note's core concern that Simba asked a direct question and got no answer.

- **⚠️ It does not answer the question that was actually left hanging.** Simba's unanswered last word was *"We can find another time this week ?"* — about the **promo pickup take**. Nothing in the 8/12→8/17 window touches a reshoot. **The production ask is still unanswered; only the awkwardness is gone.**
- Stays `closure-candidate`. If Connor closes it, close it on the honest ground — *Heather made Simba upside, the main asset is shot, no pickup is needed* — not on "we talked."

## 2026-08-17 — CONFIRMED COMPLETE by Connor. Closure candidate -> completed.
Connor, 2026-08-17: **"Reschedule with Simba done."** This resolves the pair the 8/11 entry asked to be resolved together — the production half ([[Archive/Actions/Connor - Shoot the Sunday Night promo video with Simba for Heather's campaign]]) was already completed and `blocked_by` cleared. `resolved: 2026-08-17`. [Source: Connor, 2026-08-17]
