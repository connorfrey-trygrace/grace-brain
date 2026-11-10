---
name: "✂️ Connor: Build question-list pruning into the AhaSlides system"
status: active
priority: P3
owner: "Connor"
added: 2026-08-31
deadline: none
last_mentioned: "2026-09-25"
source: "[[Transcripts/2026-08-30 13.10 Sunday Night Formation Lunch — Team Assembled, Captain Roles Unfilled]]"
projects:
  - "Sunday Night Launch"
people:
  - "[[People/Connor Frey]]"
  - "[[People/Callie Taylor]]"
flagged: "2026-10-13 — reason: no follow-up in 18 days"
---
# ✂️ Connor: Build question-list pruning into the AhaSlides system

- [ ] Work out how the question queue gets pruned or bucketed periodically, so a late submitter can still compete with an early question sitting on a pile of up-votes.

- **Priority rationale**: Connor accepted it in the room, which is a P1 floor — **overridden to P3 because he framed the problem himself as a 40-weeks-in one** (*"instead of keeping all of the questions for all 40 weeks after we're 40 weeks in"*). Nothing about launch depends on it. Raise the band the first time a stale question tops the board.
- **Source**: [[Transcripts/2026-08-30 13.10 Sunday Night Formation Lunch — Team Assembled, Captain Roles Unfilled]]
- **Deadline rationale**: none stated. Do not derive one from launch night — this problem does not exist until several weeks of submissions have accumulated.
- **Status**: Active — accepted as a real gap, no mechanism designed.

### The problem, as Callie Taylor put it
*"If there's 10 really good questions the first week and they all get 40 upvotes, someone who has a question the second week is much less likely to have that question near the top."* Her earlier version: unanswered questions *"build up pretty quickly"* — is there a system where a question that has sat for a few weeks comes off?

**Connor had no plan and said so** — *"No, I don't have a plan for that"* — then landed on the shape: **bucket by topic and start a new list periodically.** *"Okay, these are questions about this parable. These are questions about Noah's Ark… so bucketing them so that people can be competitive. Just pruning it sporadically is a good idea. So we should probably work that into the system."*

### The same problem from the other end — Sean Liesegang
*"Is there a way as you're reading through the questions to synthesise them? Because a lot of them may be connected in some way of the same topic. If you can create an umbrella question and then have those questions underneath them. If you're someone who's maybe new to the church and you put this question in and you keep upvoting it and it just seems like no one's answering it, I feel like that could send you away."*

**This produced a real clarification of how the question of the night is chosen**, which belongs in the launch note as much as here — Connor: *"I don't think the question of the night every week will just be the number one question from the previous week. It'll be the number one question and anything below that that is related to that top question… It's not like we can only answer one question per week. There's just gonna have to be a focus."*

⚠️ **Simba Kanjanda's suggestion, unaddressed:** *"You can use AI for that."* It got a laugh from John (*"some people love AI, some people think AI is the devil"*) and no answer. Grouping and de-duplicating an up-voted question queue is exactly the shape of problem Connor already solves this way elsewhere.

- **Related**: [[Trackers/Actions/Connor - Pay for the AhaSlides Pro plan + build the mock question rank]] — the tool this would live in.
- **Blocked by**: none

### 2026-09-09 (quick refresh, sweep, Step 3) — first sweep read; not flagged
- Window gate: Connor's own framing (problem doesn't exist until several weeks of submissions accumulate) means there is no Connor-side action available today. 10 days quiet is not neglect on an item whose action window hasn't opened.
- No hard trigger date to park it on-hold against, so left `active`; re-check once launch-week submissions start piling up.

### 2026-09-11 (Connor, live session) — Sean's synthesis/persistence idea accepted, folded into this workflow
- Connor: Sean Liesegang's idea (persisting/synthesizing questions across weeks — see [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Role-Ask-List]] row 2, and Connor's own 9/2 "Dream team" reply, rowid 192664) is being folded into this pruning mechanism, not tracked as a separate open ask to Sean.
- No status/priority change — still window-gated to launch-week submissions.

### 2026-09-21 (quick refresh, sweep, Step 3) — ⭐ the window this was gated on has now opened
- This item has been parked on a stated condition: *"re-check once launch-week submissions start piling up"* / *"window-gated to launch-week submissions."* **The launch happened 9/20 with 149 attendees and a live question board** — the submissions now exist.
- Corroborating, from Connor himself: his 9/20 6:55 PM note-to-self (Outlook, subject *"One off questions"*) reads **"How do we close the loop on those questions??"** — which is this problem, in his words, the night the window opened. [Source: Outlook, Connor → self, 2026-09-20 6:55 PM ET]
- Also live: the debrief's decision to cut to **one question per night** ([[Transcripts/2026-09-21 11.36 Sunday Night Launch Debrief — One Question & Time Signposting]]) makes pruning *more* load-bearing, not less — fewer slots against the same inflow.
- **Not re-banded unilaterally** (it carries no date, so the escalation windows don't apply). Left `active` at P3 with the gate noted as cleared. If Connor wants it to compete for attention it needs a date.

### 2026-09-24 (text) — Keegan Lange: embedding + clustering approach
- 9:38 PM · Keegan (unprompted): embed questions with all-MiniLM-L6-v2, cluster with KNN, visualize. Caveat from him: gives statistical similarity, not theme labels; may struggle with nuanced faith questions. Concrete version of Simba's "use AI" suggestion above.
- Connor loved it and sent an image (unreadable); Keegan: "That looks really nice!"
[Source: Text, Keegan Lange → Connor, 2026-09-24 9:38 PM ET – 2026-09-25, rowids 194205, 194235–194238]

### 2026-10-13 (quick refresh, sweep, Step 3)
- Flagged: no follow-up in 18 days
