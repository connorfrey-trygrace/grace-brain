---
name: "🗓️ Connor: Build the Sunday night roster in Planning Center Online (PCO)"
status: completed
resolved: 2026-08-28
priority: P1
owner: "Connor"
added: 2026-06-21
deadline: 2026-09-20
needs_by: 2026-08-30
last_mentioned: "2026-08-28"
source: "[[Transcripts/2026-06-16 16.41 ROC Orientation with Kay — Event Registration & Comms Walkthrough]]; [[Transcripts/2026-07-07 09.58 Planning Center Training with Jennifer — Sunday Night Service Setup]]"
blocks:
  - "[[Trackers/Actions/Connor - Confirm Sunday night custodian (default Alex)]]"
  - "[[Trackers/Actions/Connor - Recruit Sunday night greeters (20s–30s pool)]]"
  - "[[Trackers/Actions/Connor - Recruit Sunday night usher crew (lean; CJ willing)]]"
projects:
  - "Sunday Night Launch"
source_line: 197
---

# 🗓️ Connor: Build the Sunday night roster in Planning Center Online (PCO)

- **Priority rationale**: reactivated from On Hold; currently Blocked by the Rock service-type item, so the critical-path P2 floor is suspended until that clears (then it floors to P2). **Linchpin** — most Sunday-night recruitment gates behind this.
- **Source**: [[Transcripts/2026-06-16 16.41 ROC Orientation with Kay — Event Registration & Comms Walkthrough]]; [[Transcripts/2026-07-07 09.58 Planning Center Training with Jennifer — Sunday Night Service Setup]]
- **Needs-by rationale**: roster scheduled before launch (estimate)
- **Status**: **Completed 2026-08-28 (Connor).** The 21 signups are loaded into their `SNL` Rock groups, the sync push ran, PCO teams are set as tag teams and members auto-populate — verified live on 8/28. The post-8/30-lunch pass for anyone who signs up at the lunch is **not** held here; it rides on [[Archive/Actions/Connor - Message the Sunday-night volunteers to sign up for shifts in PCO]].
- **Notes**: As individual roles get staffed, they land here. **Gates:** greeters, ushers, custodian, host (and, downstream of greeters, name tags). Does **NOT** gate worship team, second leader, or lights (PCO-independent per Connor 6/21). **2026-07-21: the old blocked-by-a-Stale-item ambiguity is resolved by retiring the Stale section** — its blocker ([[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]]) is Active (flagged, restored from the old Stale bucket 2026-07-21), so per Step 3 this item is legitimately blocked and should not itself be flagged regardless of how long "Last mentioned" ages — that's now unambiguous since a flagged blocker is still an open, non-Completed item.
- **Blocks**: [[Trackers/Actions/Connor - Confirm Sunday night custodian (default Alex)]] · [[Trackers/Actions/Connor - Recruit Sunday night greeters (20s–30s pool)]] · [[Trackers/Actions/Connor - Recruit Sunday night usher crew (lean; CJ willing)]] · and, one link further down, [[Trackers/Actions/Connor - Set up weekly name-tag station for Sunday night]] (gated on greeters)
- **2026-08-04 (quick refresh sweep) — bidirectional link repaired, no status change.** Four notes named this item in their `blocked_by`, but this note carried no `blocks` field at all, so the dependency was invisible from the linchpin end and from any Base query over `blocks`. The **Gates:** line in Notes had the information in prose since 6/21; it is now structured. Band left at **P3** deliberately: the critical-path P2 floor stays suspended while this item is itself blocked by the Kay/Rock item, per ## Priority. It floors to P2 the moment that clears — and needs-by 2026-08-30 puts it inside the ~3-week P2 escalation window in about four days regardless, so expect it to move at the next sweep.

- **2026-08-06 (Connor) — the blocker is being actively worked for the first time since 7/07.** Connor is scheduling a three-way Kay + Jennifer Planning Center setup sync for early next week ([[Archive/Actions/Connor - Schedule the Kay + Jennifer Planning Center setup sync]], deadline 8/14), in which Kay would create the Rock service type and sync tags live. This item stays blocked, but the chain is moving.
    - **What to have ready so the roster can be built the moment the Rock side exists:** there are now **22 registrants** on [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] with stated serving areas — 9 Greeter/Welcome, 5 Tech/Slides, 5 Usher, 5 Setup, 2 MC/Host. That is the roster's content, already collected. ⚠️ **But five of the 22 rows are blank across all five substantive columns** because they arrived as email notifications only; the **Rock instance 542 re-pull** has been recommended in four consecutive sync reports and still has no owner. **Do the re-pull before the sync meeting** — otherwise the session hands you a working service type and an incomplete list to load into it.
- **Blocked by**: none — cleared 2026-08-24

- **2026-08-10 (quick refresh sweep) — escalated P3 → P2 by the Step 3.5 escalation window.** `needs_by` is **2026-08-30**, now **20 days out**, i.e. inside the ~3-week P2 band. Independently, this item **blocks three others** (custodian, greeters, ushers) which are all parked On Hold waiting on exactly this roster — the critical-path floor would put it at P2 the moment it becomes actionable. It is currently `blocked_by` [[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]], which is itself blocked by [[Archive/Actions/Connor - Schedule the Kay + Jennifer Planning Center setup sync]] — **whose needs_by is today**. That is a three-deep chain with four parked items behind it and 41 days to launch; the chain's front end is the thing to move.

- **2026-08-11 (Phase 0 transcript synthesis) — still blocked, but now under an explicit hold, not an inferred one. No band change.** Source: [[Transcripts/2026-08-11 11.54 Sunday Night Service Rock Setup — SNL Groups Created, PCO Tags Blocked]]
    - Jennifer Claffey said it outright in the 8/11 session: **do not bulk-load until the Rock→PCO sync is confirmed working** — *"otherwise we're going to have to figure out a way to redo all this."* Connor: *"Yeah, good call."* Previously this note inferred the block from the blocker's state; it is now a stated instruction from the person who owns the PCO side.
    - **The blocker's character changed and that matters for planning.** [[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]] is no longer waiting on Kay's calendar — the Rock groups exist. It is waiting on **Planning Center vendor support** (Jennifer's 12:15 PM Zoom, Wed 8/12) and possibly on **Melissa at Rock** after that. Connor cannot accelerate either. The chain is shorter but the front end is now outside Grace.
    - **What Connor CAN do while blocked, and should:** the **Rock instance 542 re-pull** for the five blank rows on [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] — recommended in **five** consecutive sync reports now and still unowned. It did not come up in the 8/11 meeting. If the sync clears on 8/12, the roster load is gated on having a complete list; doing the re-pull now converts dead waiting time into readiness. `needs_by` **2026-08-30**.

- **2026-08-11 (later) — the readiness gap this note named is closed.** The **Rock instance 542 re-pull is done** (Connor's request, ~1:30 PM ET): all 21 registrants now have complete serving-area / frequency / morning-team / age data on [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]]. The 8/06 warning above — *"otherwise the session hands you a working service type and an incomplete list to load into it"* — no longer applies. **When the Rock↔PCO sync clears, the list is loadable the same day.** Still `blocked_by` the sync; nothing else.
    - Count correction to carry forward: the roster is **21, not 22** — Sumay Lu is no longer in Rock.

### 2026-08-12 (email)
- 12:44 PM · Jennifer: PCO tags created; Rock↔PCO sync still broken
- **Still blocked, and specifically on the sync — not on the tags.** The tag/service-type half of [[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]] is done; the sync that would carry the 21 registrants into PCO is not. Jennifer's own hold from 8/11 (*do not bulk-load until the sync is confirmed working*) therefore still stands. No status or band change.
[Source: Email, Jennifer Claffey → Connor (cc Kay Carter-Corker), "PCO set up", 2026-08-12 12:44 PM ET]

### 2026-08-17 15:11 ET (quick refresh, email) — still blocked; the Sync v2 maintenance did not clear it
- Kay Carter-Corker, replying to Connor: *"Not yet. We are still trying to figure out why it is not working."* The Rock↔PCO sync is **broken 41 days** and Jennifer's explicit 8/11 no-bulk-load hold stands, now re-confirmed at source.
- **21 registrants remain loadable the same day the sync clears** — the readiness gap closed 8/11 and nothing here reopens it. No status or band change; `blocked_by` unchanged.
[Source: Email, Kay Carter-Corker → Connor + Jennifer Claffey, 2026-08-17 3:11 PM ET]

### 2026-08-24 (standalone sweep)
- → priority: P2 → P1 — 6 days to needs_by 2026-08-30, inside the escalation window. Timing only; the importance read is unchanged.

### 2026-08-24 (transcript synthesis) — 🟢 **UNBLOCKED after 48 days.**
- Sync verified working live; [[Archive/Actions/Connor - Get Kay to create the Sunday Night service type + Rock↔Planning Center sync tags]] → completed
- 21 registrants on [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] are loadable now; the 8/11 readiness gap stays closed
- Rock `SNL AVL` → `SNL Audio`, new `SNL Slide` child group; Audio + Slide tags created in PCO
- PCO markers were verified on **SNL Audio, SNL Greeter, SNL Captain** only; the other six SNL groups were not checked. A marker is a Rock **group attribute** and Connor's permission level cannot set it.
- ✅ **Connor's call, 2026-08-24: load anyway.** *"Markers don't matter for me yet — I am going to plow forward and if there are problems, we'll figure that out."* **Settled — do not re-raise unverified markers as a blocker on this item.** The symptom to watch for after a sync is a group whose people don't appear in PCO; that is what goes to Kay, and only then.
- → blocked_by: cleared. Band **P1** unchanged (needs_by 2026-08-30, 6 days).
- Still parked behind this note, deliberately: greeters, ushers, custodian, name tags — the gate was the sync, but the roster itself is not built yet.
[Source: [[Transcripts/2026-08-24 18.15 Sunday Night Rock–PCO Working Session — Sync Confirmed, Tag Teams Adopted]]]

### 2026-08-28 (transcript synthesis) — 🟢 the mechanism works end to end; only signups remain
- Root cause of tags-without-team-members found: the **PCO tag team had never been pointed at its tag**. Kay set the associations live; membership populated immediately
- Not the new teams and not the sync — Jennifer hit the same wall converting a Sunday-morning team as a test
- Greeter positions all key off one `greeter` tag (intended); SNL AVL keys `audio` and `slides` separately
- Direction rule: start in Rock for anyone without a profile and let Rock create the PCO profile; PCO→Rock is fine only for someone who already has one
- Connor: *"Other than getting volunteers to sign up, yes"* — it does what he needs. Remaining here: one final pass that everyone needed is loaded, repeated after the Sun 8/30 lunch
- → no field changed; band P1 and needs_by 2026-08-30 stand
[Source: [[Transcripts/2026-08-28 10.35 Rock–PCO Tag Teams Resolved — Sunday Night Attendance Metrics]]]

### 2026-08-28 (email)
- Jonathan Mazurkiewicz added to Rock `SNL Audio` 8/27 at JeanPaul Tauler's request — first volunteer sourced by a team lead, not the form
- Jennifer: tag synced, team membership did not (tag team had no association set); she added him manually
- Connor: "I set it back to tagged team and it worked. Just had to give the new guy the right tag."
- same missing step Kay fixed vault-wide on 8/28 — a worked example, not a new problem
- rostered on [[People/Good Noodles]]
[Source: Email thread, Jennifer Claffey → Connor + Kay Carter-Corker, "RE: PCO/ROCK", 2026-08-27]

### 2026-08-28 (Connor) — closed
- Connor: roster is built. Rock groups loaded, sync push run, PCO tag teams populating
- → status: active → completed; resolved: 2026-08-28
- unblocks 4 on-hold items whose `blocked_by` pointed here: custodian, greeters, ushers, name-tag station. `blocked_by` cleared on each; **status left `on-hold`** — their own parking conditions are separate and were not re-judged
- the recurring "is everyone loaded" pass lives on [[Archive/Actions/Connor - Message the Sunday-night volunteers to sign up for shifts in PCO]], not here

### 2026-08-28 (Connor asked for a bucket check)
- worksheet built: [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-SNL-Group-Load-Check]] — expected membership of every SNL group, name by name, against the 8/26 load
- **2 of 8 form areas loaded** (Greeter 15, Usher 9). Setup 10 · Breakdown 10 · Slide 6 · Host 3 · Band 4 = **43 memberships outstanding**
- 3 registrants (Joe Lu, Lihong Lu, Mara Marin) have no area at all → [[Trackers/Actions/Connor - Follow up with the 4th-service volunteer signups on role placement]]
- 1 fake test record (Trixie Fake-Carter-Corker) to remove from SNL Greeter before any volunteer sees a schedule
- caveat recorded: the load state is the 2026-08-26 Group Viewer read, not a live Rock read

### 2026-08-28 (Connor authorised the load; done in Rock)
- **31 memberships created**: SNL-Set-up +10, SNL-Break-down +12, SNL-Slide +6, SNL-Host +3. Read back and verified
- **SNL-Band untouched** — Connor: not his call, info for Seth Addison
- Joe Lu + Lihong Lu placed on **Break-down**, not Set-up (Connor); Aila Lu stays Teardown-only
- Mara Marin left unplaced — no reply to Connor's 8/20 email, and her stated interest is worship
- ⚠️ 6 data problems found, none fixed: Trixie Fake-Carter-Corker in 3 groups, Betty Rock Cloud in Slide, **LaurenNichole Wertz duplicated as two person records both in Greeter**, Vacca doubled in Slide, Jennifer Claffey inactive in Host, Lihong Lu recorded as "Lu Lu"
- next: sync push, then point each new PCO tag team at its tag — it does not happen by itself
- detail: [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-SNL-Group-Load-Check]]

### 2026-08-28 (cleanup, done in Rock)
- fakes removed: Trixie Fake-Carter-Corker out of Greeter/Slide/Host, Betty Rock Cloud out of Slide — 4 membership rows, no person records touched
- Jennifer Claffey removed from SNL-Host (1 row); Vacca's duplicate rows left as instructed
- "Lu Lu" was **not a duplicate** — one record with NickName "Lu"; corrected to **Lihong Lu**
- ⏳ **Wertz merge is a REQUEST, not done** — Connor's Rock account lacks merge rights, so it filed to the data integrity team with a note naming 26541 as the keeper. Both records are still in SNL-Greeter until Kay or Jennifer processes it
- restore data for every deleted row is recorded on [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-SNL-Group-Load-Check]]
