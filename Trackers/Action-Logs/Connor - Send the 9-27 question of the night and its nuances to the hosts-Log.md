---
type: log
source_note: "[[Archive/Actions/Connor - Send the 9-27 question of the night and its nuances to the hosts]]"
tags: [log]
---

# Connor - Send the 9-27 question of the night and its nuances to the hosts — History Log

Append-only history, split out of [[Archive/Actions/Connor - Send the 9-27 question of the night and its nuances to the hosts]] on **2026-09-22** so the live note stays cheap to read on every run (it was 41 KB, and every sync that appended one line read all of it). Same pattern as the 2026-08-11 event-note split.

**This file is not read during a normal run** — only when auditing or reconstructing how a decision was reached. Entries are **oldest-first**; append new history at the bottom. *(This is a deliberate divergence from the newest-first event `-Log` files: action notes have always been appended chronologically at the bottom, and flipping the order would guarantee mis-ordered appends by any writer following the habit.)*

---

### 2026-09-21 (quick refresh, text) — ✅ bullet 1 done; two bullets left, both still due today
- Connor → hosts group, **12:48 PM ET**: 9/27 announces the Inspira partnership from the stage; **QOTN before the message, with movie-theater popcorn**; **peer discussion in the Lobby after the message**, prompts on the screens, **Brandon Geddes + Simba Kanjanda developing the prompts**; theme **"What Shapes You," John 15:1–11**; QOTN *"How can I hear God when I don't know what his voice sounds like?"*; **Brandon Geddes + Will Gralley hosting.**
- ⚠️ **The nuance list went out as an image attachment, not text.** The hosts have the one-line question; whether they have the eight-variant hearing-from-God list in usable form is unverified, and the vault cannot read the attachment. Worth a glance at whether that image is legible on a phone.
- ❌ Still open, both due today: **write the question into PCO plan 91453887's Q&A → Host item** (it still names no question), and **tell John Slye the host-intro wording** he asked to be in sync on.

### 2026-09-21 (Connor, live session) — ✅ bullet 2 done; bullet 3 drafted, not sent
- **PCO write complete.** Plan 91453887, Q&A → Host item (id `1237916265`) now carries the question. Appended below the existing three lines, matching the plan's terse newline style: `QOTN: "How can I hear God when I don't know what his voice sounds like?"` / `Hosts: Brandon Geddes + Will Gralley` / the nuance line (God's voice vs. your own brain / your psyche / an external source; what God's presence feels like; how to access it) / `John responds — 10 min max` / `Popcorn handed out during`. Written through Claude in Chrome (Services API is read-only) and **verified afterward via `services_plan_items`**, not off the screen.
- The nuance line is the half John specifically asked for: *"you equip the host of the night to understand the nuances underneath that bucket."* It is now in the run of show as well as in the hosts' text thread, which closes the gap left by the nuance list having gone out as an image attachment.
- **Bullet 3 (tell John the host-intro wording) is drafted, not sent** — [[Events/2026-09-20-Sunday-Night-Service/2026-09-27-Connor-Host-Intro-Draft]]. Awaiting Connor's review.
- ⚠️ **Still open and NOT done here: the 9/27 plan's ordering.** Q&A still sits after Message in plan 91453887 (seq 14 Message → 15 Q&A), and peer discussion is not marked as moving to the Lobby. That is [[Archive/Actions/Connor - Add peer-discussion prompts to the 9-27 closing Host item]] + [[Archive/Actions/Michael Vacca - Correct stale week-1 theme and scripture in the 9-27 PCO plan]], to be done in one pass.

### 2026-09-21 (Connor, correction) — PCO rewritten: confidence monitor notes are host speech, carried forward from 9/20
- **Connor's correction:** *"the confidence monitor notes are only for things the hosts have to say, not for the whole game plan... We don't want to lose anything that the hosts said this weekend, just changing the topic (new qotn/scripture/theme)."*
- My earlier write put the production plan into the Q&A Host item (hosts' names, "John responds — 10 min max", popcorn). That is planner content, not host speech. Removed.
- Root cause was bigger than my one edit: **all four Host items in plan 91453887 were abbreviated stubs** of the 9/20 blocks (`Welcome!\nEvening service\nTheme:...`), not carried-forward copies. Whoever set up the 9/27 plan re-summarized instead of porting. Rewrote all four from plan 91130954 (9/20), verbatim, topic swapped only. Verified via `services_plan_items`.

| seq | item | topic swap applied |
|---|---|---|
| 2 | Host Welcome | "first ever Sun night svc" → "week 2"; Main Q → "What shapes you?" |
| 13 | Host (transition) | scripture → John 15:1-11; "New series" → "Series" (week 2, no longer new) |
| 16 | Host (Q&A) | QOTN → "How can I hear God when I don't / know what his voice sounds like?"; slide → 9.27.26 |
| 18 | Host (peer discussion) | slide → 9.27.26. Otherwise untouched. |

- **Format now recorded as a standing rule** — see the agent memory `confidence-monitor-notes-format`: opens `Confidence Monitor Notes:`, lines wrap at **~37 chars** (hand-wrap long quotes so they fit the monitor), terse cues with `svc`/`w/`/`wk`/`Qs` abbreviations, `->` for sub-steps, CAPS for hard cues, trailing `Slide (Vacca):` path block.
- ⚠️ **Two carried-forward lines will be wrong once the plan is re-ordered.** seq 16 still says `Curiosity about the message` / `Top Qs from last wk` — written for 9/20 when Q&A followed the message. On 9/27 the QOTN moves *before* it. And seq 18 says `Invite ~10 min peer discussion` with no Lobby. Both are correct as carried-forward-verbatim per Connor's instruction; both need a second pass when the re-order happens. Not changed here.

### 2026-09-21 (Connor, live session) — Inspira notes added; Connor re-ordered the plan himself
- Connor re-ordered plan 91453887 and added a new item; asked for a double-check plus the Inspira notes.
- **Connor's edits, verified:** Q&A moved **before** Message (seq 15-16 Q&A/Host, seq 17 Message) — matches the call (QOTN → John's 10-min response → message). New item seq 13 **"Inspira Announcement Con/Sky"** (id `1239653470`, 2:00) in the Host Transition block. seq 14 renamed **"Host Will/Brandon"**, 2:00. seq 2 reworded ("Theme tonight" replaces "Main Q tonight"). seq 19 lines reordered — FEEDBACK FORM + Football now above the discussion invite.
- **Inspira block written** into seq 13: thank Seth / thank the room / 10/4 news (end early, walk down, YP night, registration coming) / the 14-upvote YP question quoted / Connor's answer (*"this is it — Sunday night IS the investment"*) / hand off to Brandon + Will. Ends `Slide (Vacca): TBD - 10/4 Inspira` — no Inspira slide exists yet and the path was **not** invented. Verified via `services_plan_items`.
- ⚠️ **The YP answer is in PCO ahead of John's sign-off.** [[Events/2026-09-20-Sunday-Night-Service/2026-09-27-Connor-Host-Intro-Draft]] asks John whether *"Sunday night is the investment"* overstates his position; that text is still unsent. If John softens it, seq 13 changes with it.
- **Resolved by the re-order:** seq 16's carried-forward `Curiosity about the message` now reads correctly — it precedes the message rather than following it.
- **Still open after this pass:** (a) **no communion item** though John said *"It's communion this week"*; (b) **no scripture slide** for John 15:1-11 (9/20 carried a full-text one, seq 11); (c) seq 19 still says `Invite ~10 min peer discussion` with **no Lobby** though Connor's 12:48 text moved it there; (d) seq 16 and 19 both `0:00` so the plan total does not reflect John's 10-min QOTN cap.

### 2026-09-21 (Connor, live session) — communion + scripture slide + Lobby added; "YP" corrected
- **"YP" was wrong and is fixed.** Connor: *"What is YP??"* — the abbreviation sat inside a **quote the host reads aloud**, where the format's `svc`/`wk`/`Qs` shorthand does not apply. seq 13 now reads `"Young professionals had 1 event / this year, 10+ in 2023 - what will / leadership do?"`. **Rule: abbreviate cue lines, never spoken lines.** Added to the `confidence-monitor-notes-format` memory.
- **Lobby added** to seq 19: `HEAD TO THE LOBBY for it`, placed under the discussion invite, CAPS to match `FEEDBACK FORM`. Connor's own line ordering preserved.
- **Scripture slide created** — `Scripture Slide: John 15:1-11 (NIV)`, item `1239657909`. Full text, verse-numbered, fetched verbatim from Bible Gateway 2026-09-21 and carrying the same translation caveat the 9/20 slide has (NIV not confirmed as Grace's standard — verify with Michael Vacca).
- **Communion created** — header `1239658435` + item `1239658594`. Content is **not invented**: the mechanic comes from [[Trackers/Actions/Connor - Plan Sunday night communion logistics]] (both distributions — greeters at the two door points on the way in, ushers on a raised hand mid-service, *"nobody has to get up"*, slide 13 `NOBODY MISSES COMMUNION`). That note also confirms **9/27 is Communion week** per John Slye's series brief (Week 3, VINE, John 15:1-11) — which independently corroborates the scripture.
- ⛔ **All three new items are sitting at the END of the plan (seq 20-22) and need dragging into position.** PCO's reorder is drag-only; synthetic drags did not engage its sortable library, and there is no context menu, Detail-tab position field, or API write path. Target: **Scripture Slide → immediately before `Message` (seq 17); Communion header + item → between `Message` and `Peer Discussion`.** Content is correct and verified; only placement is outstanding, and it is a manual drag for Connor.
- **Still open:** seq 16 and 19 are both `0:00`, so the plan total (25:00) does not reflect John's 10-min QOTN cap. Communion has no named leader (`TBD - who leads it from stage`). No Inspira slide exists (`Slide (Vacca): TBD - 10/4 Inspira`).

### 2026-09-21 (Connor, correction) — NIV confirmed; caveat removed from both slides
- Connor: *"the NIV is confirmed - not a question for Vacca."* The "verify with Michael Vacca" caveat came from a 2026-09-15 run that could only infer NIV from one matching quote (Luke 18:8, Aug 30 AM plan). It is settled.
- **Both slides corrected**, verified via `services_plan_items`: 9/27 item `1239657909` and **9/20 item `1237963407`** (the original source of the inference — it carried the same false caveat). Both now read `[Full text for slides - NIV, Grace's standard translation. Wording verified verbatim against Bible Gateway <date>]`. **Wording verification stays** — that check is transcription accuracy, not translation choice.
- Recorded as a standing fact in the agent memory `grace-bible-translation` so no future run re-opens it. The historical reasoning in [[Archive/Actions/Connor - Write host bullets for launch night and put them in Planning Center]] was left alone — it was true when written.
- **Connor's drags landed.** Scripture Slide seq 15 (after Host Will/Brandon, before Q&A); Communion header + item seq 19-20 (after Message, before Peer Discussion). Placement is done.
- ⚠️ **One line to check in the Communion item (`1239658594`).** Connor trimmed it; the mid-service line now reads `-> mid-service: raise a hand and a- nobody gets up`. The **usher** is gone from it ("raise a hand and an usher brings it"), and the usher is the role that mechanic assigns — per [[Trackers/Actions/Connor - Plan Sunday night communion logistics]], ushers had no communion duty anywhere in the vault before 2026-08-22. Reads like a slipped edit rather than a deliberate trim. Not corrected — it is Connor's edit to make.

### 2026-09-21 (Connor, correction) — PCO holds stage content only; logistics + verification stripped out
- Connor: *"Communion logistics don't need to live in PCO - neither does scripture verification. Michael can trust it is correct, you report those things to me, not PCO."*
- **Three items cleaned, verified via `services_plan_items`:**
  - `1239657909` (9/27 scripture slide) — bracket removed; carries John 15:1-11 and nothing else.
  - `1237963407` (9/20 scripture slide) — same, John 14:15-31.
  - `1239658594` (Communion item) — description cleared. The header + item still mark the moment in the order; the mechanic does not ride along.
- **The logistics still live where they belong** — [[Trackers/Actions/Connor - Plan Sunday night communion logistics]] holds the both-distributions mechanic (greeters at the two door points on the way in, **ushers** on a raised hand mid-service, *"nobody has to get up"*), and slide 13 of the Formation Lunch deck states `NOBODY MISSES COMMUNION` publicly. Nothing was lost by taking it out of PCO.
- Recorded as a standing rule in the agent memory `pco-carries-stage-content-only`: **host speech, order, lengths and slide cues go in PCO; logistics, TBD markers and my own verification notes get reported to Connor.** The verification itself still happens — only the record of it moves.

### 2026-09-22 (Connor, live session) — communion note added; **Inspira slide built** (the communion one was a misread)
- **PCO Communion item (`1239658594`)** now carries Connor's instruction verbatim: `Slide (Vacca): add the communion slide from the morning`. Verified via `services_plan_items`. Communion leader is settled — see [[Trackers/Actions/Connor - Plan Sunday night communion logistics]]; the pastor preaching always leads it, so 9/27 is John Slye.
- **I misread "can you make one?" as a communion slide and built that first. Connor: *"we don't need a communion slide, we need an inspira slide."*** The 10/4 Inspira slide is the one that did not exist — the Inspira item has read `Slide (Vacca): TBD - 10/4 Inspira` since it was created.
- **Built:** `Events/2026-09-20-Sunday-Night-Service/Discussion-Slides/9.27.26 - Inspira 10-4.png`, 1920×1080, house style (ink field, white Lato Light, auto-fit, **no chrome**). Reads: *Next Sunday, October 4 / we walk down to Inspira together / right after the service. / Young professionals night, 7:30.*
- **New renderer:** `Workflows/statement-slide-build.py` — a statement slide is any slide that is just words on the field (announcement, instruction, promo). It **imports** `discussion-slide-build.py` rather than copying it, so the template, brand colors, fonts and auto-fit have exactly one definition and cannot drift. One fix over the discussion renderer: each line is a `nowrap` block, not a `<br>`, because `<br>` lets the browser add a second unwanted break that the auto-fit loop accepts as fitting.
- ⛔ **The slide is deliberately one line short.** No registration link or QR, because **two surfaces are live** — Callie's Eventbrite and Connor's Partiful — and [[Archive/Actions/Callie Taylor - Build the 10-4 Inspira Eventbrite page with Maggie]] records that nobody has said which is canonical. No price either: `$10` is on file as the **venue's normal night**, not as what Grace attendees pay. Both are Connor's calls; add the call-to-action line and re-run once settled.
- **Unused:** the communion slide + JSON (`9.27.26 - Communion.*`) are still in `Discussion-Slides/`. Not archived — awaiting Connor's word.

### 2026-09-22 (Connor, correction) — promo rebuilt with energy; the real hook was buried in an August transcript
- Connor on the first Inspira slide: *"That slide is SOOOO boring. This should not be the same style as a QOTN slide, this should amp people up."* Correct, and the reason is structural: the QOTN slide is **deliberately quiet** because the room is being asked to think; a promo is selling a night to people who have not decided to come. **The no-chrome rule in [[Workflows/peer-discussion-slide]] is scoped to the discussion set and does not govern promos.**
- **The content problem was worse than the design problem.** My first version said "we walk down to Inspira" because that is all the 9/21 notes say. Searching further turned up what the night actually *is*: **Inspira Dance — Sunday-night country swing, $10 a head** ([[Transcripts/2026-08-30 13.10 Sunday Night Formation Lunch — Team Assembled, Captain Roles Unfilled]], Skylar Frey; she **priced it up from the $7 Inspira offered** so the rate would not have to rise later), and *"dancing upstairs rather than a bar"* ([[Transcripts/2026-07-30 19.08 Post-NYC Sunday Night Structure Call — Connect-Time Experiments]]).
  - ⚠️ **This also retracts my 2026-09-21 caution that `$10` was "the venue's normal night, not what Grace attendees pay."** It is Grace's own set rate. I had read only the action notes, not the August transcripts.
- **New renderer:** `Workflows/promo-slide-build.py`. Palette straight from [[Reference/Grace-Brand-Guideline]] — Active Blue `#2F97A0`, Stable Blue `#1C3B6B`, Cinder `#ABABAB`, Cloud `#E3E3E3`; Lato Black display. Reuses the discussion renderer's Chrome call and escaper rather than copying them.
- ⛔ **Still no registration link or QR** — Callie's Eventbrite and Connor's Partiful are both live and nobody has said which is canonical ([[Archive/Actions/Callie Taylor - Build the 10-4 Inspira Eventbrite page with Maggie]]). That is the one thing keeping the slide from final.
- **Also caught pre-render:** a draft of the JSON claimed *"Lesson, then open dancing"* and *"no partner and no experience needed — they teach you."* Neither is anywhere in the vault. Removed; the correction is recorded in the JSON's own `_source`.

### 2026-09-22 (Connor, correction) — copy cut to 14 words; Partiful is the registration surface
- Connor: *"SOOO much text. Refer to the partiful please."* Cut the standfirst paragraph and the four-caption fact row outright; the slide now carries hook, venue, date, way in, price. Rule written into the renderer's own docstring so it does not creep back.
- **Registration surface settled: Partiful.** This closes the split flagged on 2026-09-21 — [[Archive/Actions/Callie Taylor - Build the 10-4 Inspira Eventbrite page with Maggie]] should be reconciled, since Callie is building an **Eventbrite** and has a 9/23 session with Maggie for it. **Two surfaces still exist in the trackers even though the slide now points at one.** Connor's call whether Callie's Eventbrite is cancelled, or kept for a different audience.
- ⚠️ **The QR encodes the bare event URL, not the link Connor pasted.** He supplied `https://partiful.com/e/KUB4Es5wEdR15GEdMfI1?c=GWnijqVg`; the QR drops `?c=GWnijqVg`. Reason: the same tracker records that Connor *"created a Partiful event and sent cohost links to this group"*, so a `c=` token may carry cohost rights — and a QR on an auditorium screen is a public broadcast to a few hundred people. The bare URL reaches the same event page. **If the token is only invite attribution, say so and it goes back in.**
- **QR verified by decode, not by eye:** `cv2.QRCodeDetector` run against the finished 1920×1080 PNG returns `https://partiful.com/e/KUB4Es5wEdR15GEdMfI1`. A 4-module quiet zone is baked into the symbol (`border=4`) because the white card alone gave ~2.4 modules, under spec and unreliable on a projected screen.
- New dependency for the renderer: `segno` (pure-python QR, installed `--user`). `opencv-python-headless` is verification-only, not needed to build.

### 2026-09-22 (Connor, live session) — Partiful cover added, and the page corrected four facts on the slide
- Read the Partiful event page directly (browser; `og:description` + `og:image`). **The page is a better source than the vault for this event, and it disagreed with the slide in four places:**
  | Slide said | Partiful says |
  |---|---|
  | "Country Swing" | event's own name is **Young Adults Country Night** |
  | "Young Professionals" | **Young Adults** — *"young adults from churches across the DMV"*, i.e. multi-church, not Grace-only |
  | nothing about a lesson | **"7:30pm: Beginner country swing lesson, no partner needed"** · 8–9:30pm social dancing |
  | "$10 at the door" | **"For discounted entry, sign up with the code GCC26 online"** → `https://momence.com/l/Z4h2l9DE` |
- 😐 **The lesson line I invented on 2026-09-21 and then cut for being unsourced turns out to be true.** Cutting it was still right — it was a guess at the time. It is now on the slide *with* a source.
- ⛔ **PRICE IS OFF THE SLIDE AND NEEDS CONNOR.** Three-way conflict: the vault says **$10 a head** (Skylar, 8/30 formation lunch, priced up from Inspira's $7); the event page says **discounted entry with code GCC26 on Momence**. Printing "$10 at the door" would actively push the room to the more expensive path. Left blank rather than wrong.
- ⚠️ **A third registration surface is now in play** — **Momence** (the actual ticketing) alongside **Partiful** (RSVP) and **Callie's Eventbrite** (still being built, session with Maggie was 9/23). The slide's QR points at Partiful per Connor; the Partiful page itself carries the Momence link, so scan → RSVP → tickets is coherent. **Callie's Eventbrite is the odd one out and she may be building something already superseded.**
- Photo: Partiful cover saved as `inspira-partiful-cover.jpg`. Full bleed, Stable Blue `mix-blend-mode:color` at .28 to pull the warm club lighting toward the brand without flattening it to a duotone, plus a left-heavy scrim so type stays legible. QR re-verified by decode after the rebuild.

### 2026-09-22 (Connor, live session) — slide final: QR → Momence, $5 with code GCC26
- Connor: *"point it here - Grace folks cost $5"* → `https://momence.com/Inspira-Dance/Young-Adults-Country-Night/144119258`. QR repointed from Partiful to **Momence** (the ticketing surface). Decoded off the finished PNG to confirm.
- **Loaded the Momence page before trusting it** — a QR on an auditorium screen is not a place to guess. It confirms *Young Adults Country Night · Sun, October 4, 2026 · 7:30 PM · 2 hours · Ballston Quarter* and **"For $5 entry, sign up with the code GCC26!"**
- **The $5 is conditional on the code**, which is why the slide reads `$5 / with code GCC26` rather than `$5` alone — a bare $5 would misprice the night for anyone who books without it.
- **Subhead changed to `Inspira Dance · Ballston Quarter`.** It read *"Upstairs at Inspira Dance"* (from the 7/30 transcript's *"dancing upstairs rather than a bar"*); Momence gives the location as Ballston Quarter, and for a promo the neighbourhood is worth more to a stranger than the floor of the building.
- **Supersedes the $10 figure** from Skylar's 8/30 formation-lunch report for this night. [[Trackers/Actions/Connor - Plan Sunday night communion logistics]] untouched; the $10/$7 history stays where it is as the record of the standing weekly rate.
- ⚠️ **Three surfaces still exist and only one is now pointed at.** Momence = tickets (the QR). Partiful = RSVP (Connor's, still live). **Callie's Eventbrite = still being built** — her Maggie session was 9/23. She may be building a fourth surface nobody will use. Unresolved, and it is a person's time.

### 2026-09-22 (Connor, live session) — running order added to the slide
- Connor: *"I like 7:30 Beginner lesson and 8:30 social dancing."* Added as a two-row running order under the subhead — times in Active Blue, labels in Cloud Gray. It also does objection-killing work: *no partner needed* now sits on the face of the slide rather than in a footnote.
- ⚠️ **Rendered `8:00`, not `8:30` — flagged to Connor, not silently overridden.** Both sources say 8:00: Partiful's description reads *"8-9:30pm: Social Dancing"*, and Momence lists *7:30 PM · 2 hours* (= 7:30–9:30). A 8:30 on a screen sends people in half an hour after the dancing starts, which is the expensive direction to be wrong in. One-word change if 8:30 is right.
- QR re-verified by decode after the re-render: still the Momence URL.

### 2026-09-22 (Connor, live session) — photo blurred, times returned to the footer
- Connor: *"can you make the background image a little fuzzier? I also think the times being at the bottom worked betted."* Both applied.
- **Blur** is `photo_blur` in the JSON (default 7px), paired with `transform:scale(1.06)` so the blur does not feather the frame edge. Rationale written into the renderer: the photo is **atmosphere, not information** — sharp faces compete with the headline and pull the eye into the crowd instead of the words.
- **Times moved into the footer row**, between the QR and the price, at reduced size (42px/36px vs 48px/42px in the mid-slide version). "SCAN TO SIGN UP" became a small caption **under** the QR to free the middle slot. The mid-slide position had pushed the hero and subhead up and left a dead band across the middle; the footer reads as one band of practical detail.
- QR re-verified by decode after the re-render: still the Momence URL.
- **Slide is final pending one answer:** 8:00 vs Connor's 8:30 for social dancing (both sources say 8:00).

### 2026-09-22 (Connor, live session) — footer reordered; "Scan to sign up" dropped
- Connor: *"remove the 'scan to sign up' and swap the $5 marker with the times."* Footer is now **QR · $5 with code GCC26 · [right rail] times**. The caption is gone — a QR next to a price needs no instruction.
- Schedule rows are **flush right**, not column-aligned on the time. Against the frame edge a ragged right edge reads as a mistake; a ragged left does not.
- QR re-verified by decode: still the Momence URL.
- **Copy total is now 20 words** including the date badge. Still the one open question: **8:00 vs 8:30** for social dancing.

### 2026-09-22 (Connor, live session) — bubble added; QR rebuilt toward Heather's style, and the guideline gap surfaced
- **Bubble:** the times now sit in a rounded panel (Active Blue hairline, dark translucent fill, backdrop blur). The footer holds three unlike things — a code, a price, a running order — and containing the times stops them reading as a caption hanging off the price.
- **QR rebuilt** in Grace colors with round dot modules, drawn from segno's module matrix (segno only emits squares). Stable Blue `#1C3B6B` carries the data; Active Blue is the eye centres only, because Active Blue is ~2.9:1 on white and a scanner wants more.
- ⛔ **The finder-pattern corners had to stay square, and that is measured.** Rounding them (`rx=1.6`) made the symbol **undecodable at every size tested**, standalone at 800px included; the identical symbol with square eyes and round data dots decodes. Isolated it with a four-way test (squares / all-dots / dots+square-eyes / dots+round-eyes). Heather's style calls for shaped corners — matching that needs her spec and a real phone test, not a guess that silently stops working.
- ⚠️ **Answering Connor's actual question: no, this does not follow Heather's QR guidelines, and it cannot.** See the re-opened [[Trackers/Actions/Heather Noble - Email Connor the updated brand-guidelines document]] — the document never arrived; what was sent on 9/15 was the same Summer 2019 book, which contains no QR guidance at all (verified against the PDF's text layer).

### 2026-09-22 (Connor, live session) — QR rebuilt to Grace's real house style
- Emulated from Heather's own artifacts (see [[Trackers/Actions/Heather Noble - Email Connor the updated brand-guidelines document]]): **dot modules in Stable Blue, rounded-square eyes with a solid circular centre, and the teal Active Blue disc carrying the white Grace `g`**. Error correction raised to **H** because the badge occludes modules.
- The `g` was extracted from `Archive/2026-07-19-World-Cup/grace-logo-dark.png` (the full wordmark), cropped to the first glyph and inverted to white, saved as `Workflows/assets/brand/grace-g-white.png` so the renderer has a reusable brand asset.
- ⚠️ **Verification note — the earlier "rounded eyes don't scan" finding was an artifact of my decoder, not of the design.** OpenCV's strict `QRCodeDetector` rejects rounded eyes; it would also reject **Heather's own working QR**, which is rounded. Installed `opencv-contrib` and re-verified with the **WeChat detector**, which is far more tolerant and much closer to a phone camera: it decodes the finished slide to the Momence URL. **The strict detector still returns empty, and that is expected for this style — it is not evidence of a broken code.**
- **Still worth one real phone scan before Sunday.** Two decoders disagree by design; a camera is the only ground truth, and this is the first QR Grace will project rather than print.

### 2026-09-22 (Connor, live session) — QR promoted to half the slide
- Connor: *"put the qr on the right half of the page - it should be almost as big as possible."* New `layout: "qr-right"` in the renderer: **840px QR card** filling the right half, everything else stacked down the left.
- The **date badge was dropped** — no room beside an 840px card, and the date reads perfectly well as a line (`Sunday, October 4 · 7:30 PM`). The times bubble and the price moved into the left stack.
- Heather's two reference signs are now vaulted at [[Reference/Brand-QR-Examples/README]], so the style no longer depends on her email.
- Re-verified after the layout change: **WeChat detector decodes to the Momence URL; strict OpenCV returns empty, as expected for this style.**

### 2026-09-22 (Connor, live session) — communion slide archived
- Connor: *"archive the communion slide."* `9.27.26 - Communion.png` + `.json` moved out of `Discussion-Slides/` to **/Archive**, named to the folder's existing convention (reason + archived date in the filename). Not deleted.
- Supersedes the "Unused / awaiting Connor's word" line logged earlier today. The 9/27 plan reuses **the morning's communion slide** per `Slide (Vacca): add the communion slide from the morning` on PCO item `1239658594`.
- **Kept, deliberately:** `Workflows/statement-slide-build.py`. It was written for that slide, but it is a general renderer for any words-on-the-field slide and shares one template with the discussion renderer. Worth knowing it currently has **no live caller** — the promo renderer supersedes it for promos — so if nothing uses it by the next sweep it is a fair archive candidate itself.

### 2026-09-22 (Connor, live session) — 8:00 confirmed; the John draft is now factually stale
- Connor: *"8:00 is correct. Trust partiful over me."* The slide already carried 8:00; no change needed. Recorded as a standing rule in the agent memory `trust-the-primary-source-over-recollection` — on event details the live page beats recollection, and the right move is to render the sourced value **and name the conflict**, never to silently override or silently obey.
- ⚠️ **[[Events/2026-09-20-Sunday-Night-Service/2026-09-27-Connor-Host-Intro-Draft]] has gone stale since it was written on 9/21**, and it is addressed to the Lead Pastor:
  - says *"a young professionals night"* → the event's own name is **Young Adults Country Night**, and it is *"young adults from churches across the DMV"* — multi-church, not Grace-only
  - says *"Registration's coming this week"* → registration is **live now** on Momence, **$5 with code GCC26**
  - omits the strongest hook entirely — **beginner lesson at 7:30, no partner needed**
- Still unsent, and both of its open questions to John are still open (is *"Sunday night is the investment"* too strong; does the Inspira line belong in the evening as well as the morning).

### 2026-09-22 (Connor, live session) — "not swing" raised, then withdrawn on the primary-source rule
- Connor: *"It's not swing - correct that EVERYWHERE."* → then, on being shown that the Partiful and Momence both read *"Beginner Country Swing Lesson"*: *"if it is on partiful, then that is correct."* **It is country swing.** Canonical entry on [[Trackers/Actions/Connor - Foster the Grace–Inspira relationship (Maggie)]].
- **Nothing in the vault actually needed changing**, and the promo slide was never affected either way — its schedule row names no dance style (`Beginner lesson — no partner needed`). Both stage scripts are back to *beginner country swing lesson*.
- The historical lines in [[Events/2026-09-20-Sunday-Night-Service/2026-08-30-Formation-Lunch-Recap]], the Launch note, the Role-Ask-List and [[Synthesis/Weekly 2026-09-04]] were never touched — correctly, as it turns out.

### 2026-09-22 (Connor, live session) — 9/27 plan timed to a 7:15 finish
- Connor settled the 10/4 conflict — *"7:15 is actually a fine time to end"* — and asked for every segment framed in PCO to hit it, per the 9/21 John call. **Plan 91453887 total: 25:00 → 72:00**, against a 6:00 PM start = **7:12, with 3 minutes of cushion before 7:15.** Deliberate: 9/20 ran **1h40m** against a 50–55 min norm, and a plan that sums exactly to its end time has no room to absorb anything.
- **John's two locked numbers are honoured exactly:** worship **18:00** (*"I'm gonna get Seth to tighten up to 18 minutes"*) and the Q&A block **10:00** (*"a tight 10-minute response max, so the question of the night doesn't go more than 10 minutes"*).

| # | Segment | Was | Now |
|---|---|---|---|
| 2 | Host Welcome | 1:00 | 1:00 |
| 4–11 | **Worship block** | 20:00 | **18:00** |
| 6 | · Space | 1:00 | 0:30 |
| 7 | · Medley 1 | 6:00 | 5:30 |
| 10 | · Invitation Into Exchange | 1:00 | 0:30 |
| 11 | · Medley 2 | 6:00 | 5:30 |
| 13 | Inspira + YP moment (Con/Sky) | 2:00 | 3:00 |
| 14 | Host Will/Brandon | 2:00 | 2:00 |
| 15 | Scripture slide | 0:00 | 1:00 |
| 17 | Q&A — QOTN + John's response + popcorn | 0:00 | **10:00** |
| 23 | **Message — John Slye** (new item) | — | **28:00** |
| 20 | Communion | 0:00 | 7:00 |
| 22 | Send the room to the Lobby | 0:00 | 2:00 |

- **Two numbers are frames, not decisions, and belong to other people:** the **worship split** is Seth Addison's (I took 2:00 out of the two pauses and the two medleys to land on John's 18:00 — he may prefer to take it elsewhere), and **28:00 for the message** is John's. Both are easy to move; the total is what matters.
- ⛔ **`Message — John Slye` (id `1240004492`) sits at the END of the plan and needs one drag** under the `Message` header, between seq 18 and the Communion header. PCO reorders by drag only and synthetic drags do not engage its sortable — same limitation as the 9/21 additions Connor dragged himself.
- ⚠️ **PCO's service time for this plan is still 6:00–7:00 PM** (plan time `226476504`). The frame now runs to 7:12. Worth changing to 7:15 so the block matches the plan — and it likely wants changing on 10/4 and 10/11 too.
- **10/4 needs the same pass and has a harder constraint** — plan `91455422` is still 18 items / 21:00, and that is the night the room has to be walking to Inspira at 7:15.

### 2026-09-22 (Connor, live session) — communion/lobby/message corrected against the morning plan; service time fixed to 7:15
- Connor: *"Communion probably doesnt take 7 minutes - what does it say in the morning Plan? We also dont need to budget for lobby time."* **Checked the morning plan rather than guessing** — Sunday Morning 9/27 (plan `90823259`) has **Communion = 2:30** and **Message: John = 25:00**.
  - Communion **7:00 → 2:30**, matched to the morning.
  - Peer-discussion Host **2:00 → 0:00** — the Lobby time is after the room is dismissed, so it does not belong in the service budget.
  - Message **28:00 → 25:00**, matched to the morning. Same message both services, so the morning's own number is the better source than my estimate.
- **Plan 91453887 total: 72:00 → 62:30.** Against a 6:00 start that lands at **7:02:30 — 12:30 of headroom before 7:15.** Comfortable rather than tight, which is the right side to be on after 9/20's 1h40m.
- **Service time fixed: 6:00–7:00 PM → 6:00–7:15 PM**, and the dialog's *"Update this time in future plans"* checkbox propagated it — verified by API on **all three** future plans (9/27, 10/4 `91455422`, 10/11 `91781260`).
- **Found while checking the morning plan:** `Inspira Dance: Felipe` is **already on the 9/27 morning plan** at seq 13, **0:30**. That corroborates Connor's handoff and gives the morning script a length target — the draft at [[Events/2026-09-20-Sunday-Night-Service/2026-09-27-Connor-Host-Intro-Draft]] runs ~30 seconds spoken, so it fits.
- Connor had already dragged `Message — John Slye` into place under the Message header.

### 2026-09-22 (Connor, live session) — 10/4 lengths framed; structure still needs Connor's drags
- Connor chose **lengths-only on 10/4** (plan `91455422`) rather than rebuilding it from a template. Done and API-verified: worship block **20:00 → 18:00** (Space 0:30, Medley 1 5:30, Invitation 0:30, Medley 2 5:30), **Host Transition 0:00 → 3:00**, **Q&A Host 0:00 → 10:00**, peer-discussion Host left at **0:00**.
- **Added:** `Scripture Slide` (1:00) and `Message — John Slye` (25:00). Plan total **21:00 → 58:00** → ends **6:58**, which leaves a real margin to dismiss and walk to Inspira for 7:30.
- ⛔ **No Communion item added to 10/4, deliberately.** Checked the 10/4 **morning** plan (`91076172`) — it has no communion either. **9/27 is communion week; 10/4 is not.** Adding one would have invented an element.
- ⛔ **Two drags still needed from Connor on 10/4**, because PCO reorders by drag only:
  1. `Q&A` header (+ its Host) above the `Message` header — 10/4 still carries the **old order**, message before Q&A.
  2. `Scripture Slide` and `Message — John Slye` are at the END (seq 19–20) and belong before/under the Message header.
- **The service-type template was left alone** — Connor's call. Future plans will keep being created in the old shape until it is updated, so this same pass will be needed on 10/11 and beyond. Worth revisiting as a one-time fix.

### 2026-09-22 (Connor, live session) — lobby time named on 9/27; plan lands exactly on 7:15
- Connor: *"We actually do need to call lobby time out on 9/27. that can be how we spend the last 12 minutes."* Peer-discussion Host item (`1237916267`) **0:00 → 12:30**. **Plan total 62:30 → 75:00 = exactly 7:15.** Verified by API.
- **This reverses the earlier "don't budget for lobby time" only for 9/27, and the reasoning is better than mine was.** I had left the 12:30 as invisible slack; naming it as the Lobby block means the buffer is *doing something* — and it degrades gracefully, because if the service runs long the optional discussion compresses instead of the service overrunning. The cushion and the content are the same 12:30.
- **10/4 keeps its lobby at 0:00** and ends **6:58** — that night the room leaves for Inspira, so there is no Lobby block to name.
- **Template decision, recorded:** Connor — *"We will change the template when we confirm the new format works."* So the service-type template stays on the old shape deliberately until 9/27 and 10/4 have run. **This answers my flag from earlier; it is a decision, not an oversight.** Revisit after 10/4.
