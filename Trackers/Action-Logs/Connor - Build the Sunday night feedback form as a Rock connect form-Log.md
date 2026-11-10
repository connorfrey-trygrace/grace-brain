---
type: log
source_note: "[[Archive/Actions/Connor - Build the Sunday night feedback form as a Rock connect form]]"
tags: [log]
---

# Connor - Build the Sunday night feedback form as a Rock connect form — History Log

Append-only history, split out of [[Archive/Actions/Connor - Build the Sunday night feedback form as a Rock connect form]] on **2026-08-31** so the live note stays cheap to read on every run (it was 15 KB, and every sync that appended one line read all of it). Same pattern as the 2026-08-11 event-note split.

**This file is not read during a normal run** — only when auditing or reconstructing how a decision was reached. Entries are **oldest-first**; append new history at the bottom. *(This is a deliberate divergence from the newest-first event `-Log` files: action notes have always been appended chronologically at the bottom, and flipping the order would guarantee mis-ordered appends by any writer following the habit.)*

---

## 2026-08-12 (correction) — vacation dates re-checked against Outlook; `needs_by` re-derived.

Outlook is authoritative: `Connor Vacation` entries are **7/10–7/11, 7/31–8/02, 8/07–8/09, 9/04–9/07 and 9/11–9/12**. Connor confirmed 2026-08-12.

- **`needs_by` 2026-08-19 → 2026-09-03.** Same re-derivation: 9/03 is the last working day before the 9/04–9/07 block, and 9/11–9/12 is also out. If the build slips past Labor Day weekend it lands in launch week.
- **Priority unchanged at P2.** The band never depended on the vacation date; it rests on Connor's own “third of three” ranking against a P1 self-assignment floor.

- **2026-08-12 (transcript synthesis)** — one addition accepted: **tag Grace's social handles at the bottom of the form.** Came out of John's ask to start reading the handles from the stage at Sunday night — the form is the second surface for the same thing. [Source: [[Transcripts/2026-08-12 16.49 Connor–John Connect-Plan Call — Q&A Locked & Tables Pulled]]]

### 2026-08-18 (transcript synthesis) — ⭐ DESIGN REVERSED: contact info goes on the form, at the END, plus a new-person flag.
- Derek Adye's data point: Grace's church-wide surveys ask for name, address, cell and email at the **bottom** and still return **~95% completion** — momentum from the quick questions first, *"you're invested at that point."* Grace also tested making them optional and it *"didn't change much of anything."*
- His second argument is follow-up: anonymous feedback that is negative or unusually useful cannot be chased, *"because you literally don't know who said it."*
- Connor: *"that is a much more elegant solution than mine… it's 2 birds with one stone, because then we've done the connect."* He will add a way for respondents to **indicate they are new**, and filter on whether a name has appeared in prior submissions. Form is already ~6–7 questions.
- **This makes the feedback form the Sunday-night top of funnel** — Connor's words — and answers the question Kay Carter-Corker put to Derek that morning, which Connor had no answer for in the room.
- → design: anonymous-by-default → contact fields at end + new-person flag (Connor's call, not final)
- ⚠️ **Not locked.** Derek explicitly left it: *"if your gut's still telling you… let me make this fully anonymous, 100%, dude, I respect and stand by that."* Connor framed it as a **two-way door** and can strip the fields later.
- Follow-through lives on [[Archive/Actions/Connor - Put the feedback form + usher attendance link on the Monday Rock-PCO agenda with Jennifer Claffey and Kay Carter-Corker]]; the back end is [[Archive/Actions/Derek Adye + Kay Carter-Corker - Separate Sunday-night new-person intake from the Sunday-morning automated path]].
[Source: [[Transcripts/2026-08-18 17.09 Connor–Derek Weekly Sync — Feedback Form Becomes the Sunday Night Funnel]]]

### 2026-08-19 (Connor, live session + email) — **Google Form cancelled. Two birds, one stone.**
- Connor: *"We canceled the google form in favor of the rock form - two birds one stone."* The 8/18 two-instruments conflict is settled by merging, not by choosing sides.
- 2:25 PM · Connor → Kay: sent intro text + **7 questions** to sit above the contact fields. Q3 (*"Did you have a real conversation with someone you didn't already know?"*) marked *"this is the number we care about most."*
- → status: active → waiting-on (Kay builds it). `needs_by: 2026-09-03` unchanged — the questions have to be live before the first Sunday night.
- **Consequence worth naming:** feedback is no longer anonymous-optional. Every response now arrives attached to a contact record in the Sunday Night group, which is the trade Connor took to get one list instead of two.
[Source: Sent mail, Connor → Kay Carter-Corker, "Re: Sunday Night Services connect card", 2026-08-19 2:25 PM ET]

### 2026-08-20 (email sync) — questions are LIVE; storage solved (Rock report 219); two new open threads
- 8/19 5:25 PM ET · **Kay → Connor (cc Derek): "Done!"** The 7 questions are on the card. Live link: `trygrace.org/sundaynightserviceconnectcard`. → the 8/19 `waiting_on` (build the questions) is **satisfied and cleared.**
- 8/19 8:36 PM ET · Connor → Kay + Derek, two asks:
    - (a) **Q2 answer scale changed from 1-5 to labeled options** — *Not for me / Not my favorite / It was fine / Really enjoyed it / Loved it.* **Still outstanding** — Kay's 8/20 reply does not address it.
    - (b) **"Derek, can I get your feedback on the questions themselves???"** — unanswered as of this run. Distinct owner, so tracked as a second `waiting_on` inside this item rather than a new note.
- 8/20 11:04 AM ET · **Kay → Connor + Derek: storage solved, credited to Melissa.** Responses land in **Rock report 219** — `trygrace.rockcloud.com/reporting/reports/219` ("Connect Card-Sunday Night Services"). **This is the reporting surface for the weekly Monday pull** and it closes Kay's own open "how do we store these for later review" question.
- ⚠️ **Kay put two test submissions through the live card** (8/19 5:08 and 5:11 PM ET, "Trixie Fake-Carter-Corker", her own email + mobile). **Those records are now sitting in the Sunday Night Service Connect Card Group** — the group Connor is meant to communicate with on Sunday nights. They need deleting or excluding before launch, and that is Kay's to do.
- ⚠️ **The `info@trygrace.org` connect-card notification emails carry only the contact fields - not the 7 answers.** Same defect already documented for instance-542 registration emails: email alone can never populate feedback data. The substance is only in **report 219.** [[Workflows/m365-to-obsidian-sync]] has no routing rule for this new email class - proposed, not written.
[Source: Outlook Inbox + Sent Items, 2026-08-19/20; m365-to-obsidian-sync]

### 2026-08-21 (email sync) — Derek approves the question set; half the 8/19 double-ask closes
- 8/20 3:26 PM ET · **Derek → Kay + Connor, "Re: Sunday Night Services connect card":** *"Awesome! Thanks Kay for talking to Melissa about that and figuring things out. Connor - questions look good!"*
- That answers ask (b) from 8/19 8:36 PM — **feedback on the question set itself.** Read it as covering the seven questions, not the answer scale: he says nothing about ask (a).
- → `waiting_on` Derek clause **cleared.** Kay's Q2 answer-scale relabel (*Not for me / Not my favorite / It was fine / Really enjoyed it / Loved it*) is **still outstanding** — unaddressed in her 8/20 11:04 AM reply and unaddressed by Derek. Status stays `waiting-on` for that one thread.
- No chase written: Kay has been answering same-day on this thread all week.
[Source: Outlook Inbox, Derek Adye → Kay Carter-Corker + Connor Frey, 2026-08-20 15:26 ET; m365-to-obsidian-sync]

### 2026-08-28 (sweep)
- → priority: P2 → P1 (6 days to `needs_by` 2026-09-03; escalation window)
- calendar-window.py: no shared occasion with Kay Carter-Corker before 9/03 — if the answer-scale relabel has to be chased, the channel is text then call
- ⚠️ scope may have moved: on 2026-08-27 Connor told Heather Noble that "Link A," the evening connect/feedback form, is *"ready to go."* The vault records that instrument as Kay's **Rock connect card**, not this Google Form. **Not treated as evidence either way** — surfaced for Connor to say which artifact he meant

### 2026-08-28 (Connor)
- ✅ naming settled, and it was never a real conflict: the Google Form *became* the Rock connect form; the URL merely contains the string "connect card" and it is not a card
- note renamed Google Form → Rock connect form, 11 wikilinks repointed, the superseded "Not Rock" decision bullet deleted
- ✅ resolves the 8/27 Link-A question too — "Link A, evening connect/feedback form, ready to go" in Connor's email to Heather Noble means **this instrument**. No separate Google Form exists or is owed
- priority P1 (set earlier today on the 9/03 `needs_by`) stands
