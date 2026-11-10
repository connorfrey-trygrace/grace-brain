---
name: "🎫 Jennifer Claffey: Planning Center support Zoom — PCO tag creation + Rock↔PCO sync root cause"
status: merged
priority: P1
owner: "Jennifer Claffey"
merged_into: "[[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]]"
added: 2026-08-11
deadline: 2026-08-12
needs_by: 2026-08-12 13:00
last_mentioned: "2026-08-17"
source: "[[Transcripts/2026-08-11 11.54 Sunday Night Service Rock Setup — SNL Groups Created, PCO Tags Blocked]]"
blocks:
  - "[[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]]"
projects:
  - "Sunday Night Launch"
---

# 🎫 Jennifer Claffey: Planning Center support Zoom — PCO tag creation + Rock↔PCO sync root cause

- [ ] Jennifer Claffey — 12:15 PM Zoom with Planning Center support, Wed 2026-08-12
- **Priority rationale**: it is not Connor's to do, but it is the single front end of the entire Sunday-night volunteer chain, and it has a fixed one-hour window.
- **Source**: [[Transcripts/2026-08-11 11.54 Sunday Night Service Rock Setup — SNL Groups Created, PCO Tags Blocked]]
- **Status history**: **Deadline**: 2026-08-12 (the call) · **Needs-by**: 2026-08-12 13:00 ET
- **Status**: **Closure candidate as of 2026-08-12** — she reported back at 12:44 PM (see the 8/12 entry below): the PCO half is built, the Rock↔PCO sync half is not. Opened as: Waiting on Jennifer. She filed a Planning Center support ticket and booked the Zoom because two things broke and she thinks they are one thing.
- **The three questions on the call:**
    1. **How do you create a PCO tag now?** The in-app help changed — it now directs her to a "groups page" in Planning Center that she cannot find (*"never seen a groups page in Planning Center, can't find one"*).
    2. **Which of the two ways to build a new service type is better?** She knows there are two and is explicitly unsure of the difference — *"I really am not sure I have a grasp on the differences between the 2… let me just find out the best way to do it."* This is why she declined to build it live on 8/11 despite having ~14 minutes spare.
    3. **Is the PCO tag change what broke Rock→PCO sync?** Her hypothesis: *"Planning Center has changed the way they do tags, and Rock's still doing the tags the old way, and that's why none of the tags are working right now."*
- **If the answer is no (PCO didn't cause it):** she hands the problem back to **Kay Carter-Corker**, who works it with **Melissa at Rock**. That path has a vendor timeline Connor cannot compress.
- **Connor's involvement:** he offered to join; Jennifer declined (*"I think it would be better to save your time to share everything once we learn it"*). He will be **available by text** during the hour. ⚠️ **Single-source-of-truth risk, which Connor himself named as his reason for wanting in.** Worth asking for the **ticket number** and a short written summary rather than a verbal report-back — the launch date depends on this answer and only one person will hear it.
- **Blocks**: [[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]] → and behind that, the PCO roster and four parked volunteer items.
- **Notes**: The sync has been broken since **2026-07-07** (Jennifer deleted a linked profile) and was assumed repaired for 35 days. It was not — confirmed live on 8/11 when her two 8/10 Rock additions failed to appear in PCO.
- **Deadline rationale**: the call itself
- **Needs-by rationale**: everything on the Sunday-night volunteer chain is parked behind this hour
- **Chase-by rationale**: if no report-back by end of Wednesday, text Jennifer; the 8/15 needs_by on the service-type item is three days later

### 2026-08-12 (email)
- 12:44 PM · Jennifer reports the PCO half done; the rock/pco glitch still unfixed
- → status: waiting-on → closure-candidate
- → chase_by cleared — the 2026-08-12 17:00 clock was met; she reported at 12:44
- **Closure evidence**: email Jennifer Claffey → Connor (cc Kay Carter-Corker), *"PCO set up"*, 2026-08-12 12:44 PM ET — majority of the Sunday Night Plan set up in PCO, all tags created; she offered another Zoom once the glitch is fixed.
- **Verify before closing**: only the PCO half landed. The **Rock↔PCO sync is still open** — no ticket number, no root cause, no date for the follow-up Zoom. Confirm only if this item is read as the PCO-tag half alone; otherwise dismiss and it stays waiting on the sync answer.

## 2026-08-17 — closure candidate DISMISSED by Connor. Reverted to `waiting-on`.
Connor, 2026-08-17: **"PCO zoom, pending PCO rock update from Jen or Kay."** The call itself happened, but the thing this item exists to produce — the PCO/Rock outcome — has not landed, so it is not complete. Status reverted from `closure-candidate` to **`waiting-on`**, `waiting_on` set to **Jennifer Claffey or Kay Carter-Corker**.

- **No date set.** Connor named none and no external event anchors one — `deadline` and `needs_by` are left at their historical 2026-08-12 values (the call date) rather than re-derived into a chase this system would have invented.
- **`blocks` stands:** [[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]] is still downstream of this, which is consistent — that item's `chase_by` fired today, and chasing Kay *is* chasing this update. The two are one conversation.
[Source: Connor, 2026-08-17]

### 2026-08-17 15:11 ET (quick refresh, email) — the update Connor was waiting on **partially landed, and it is negative**
- Kay Carter-Corker → Connor + **Jennifer Claffey** (cc matters here — Jennifer is the other half of this note's `waiting_on`): *"Not yet. We are still trying to figure out why it is not working."*
- This is the *"pending PCO rock update from Jen or Kay"* Connor named when he dismissed the closure candidate. **It arrived, from Kay, and it says the Rock↔PCO sync is still broken after Sync v2.** The outcome this item exists to produce still has not landed.
- → `status: waiting-on` **unchanged. Not a closure candidate** — an answer is not the outcome.
- Still outstanding from this call, 5 days on: **the ticket number**, a root cause, and a date for the follow-up Zoom Jennifer offered *"as soon as we have that fixed."*
[Source: Email, Kay Carter-Corker → Connor + Jennifer Claffey, 2026-08-17 3:11 PM ET]


## 2026-08-17 — MERGED into the Kay item. Not closed, not cancelled — the same item, tracked once.
Connor: *"Jennifer's and Kay's items are the same. This is for the PCO foundation for the night service, waiting on a bug fix."*

- Live record moves to **[[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]]**. Read that note, not this one.
- `status: waiting-on` → **`merged`** so it drops out of the Active/Waiting-On views without being archived or deleted. Nothing here is superseded — the three call questions, Jennifer's tag-change hypothesis, and the 8/12 outcome all remain valid history.
- **The ticket-number ask recorded above is retired.** Connor, same session: *"no ticket number, just trust."* Church staff doing their best, not a vendor under SLA. Do not resurface it.
- Archiving this file is Connor's call and has not been done.
[Source: Connor, 2026-08-17 live session]
