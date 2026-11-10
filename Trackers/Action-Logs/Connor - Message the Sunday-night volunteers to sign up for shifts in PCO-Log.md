---
type: log
source_note: "[[Archive/Actions/Connor - Message the Sunday-night volunteers to sign up for shifts in PCO]]"
tags: [log]
---

# Connor - Message the Sunday-night volunteers to sign up for shifts in PCO — History Log

Append-only history, split out of [[Archive/Actions/Connor - Message the Sunday-night volunteers to sign up for shifts in PCO]] on **2026-09-04** so the live note stays cheap to read on every run (it was 16 KB, and every sync that appended one line read all of it). Same pattern as the 2026-08-11 event-note split.

**This file is not read during a normal run** — only when auditing or reconstructing how a decision was reached. Entries are **oldest-first**; append new history at the bottom. *(This is a deliberate divergence from the newest-first event `-Log` files: action notes have always been appended chronologically at the bottom, and flipping the order would guarantee mis-ordered appends by any writer following the habit.)*

---

### 2026-08-28 — created
[Source: [[Transcripts/2026-08-28 10.35 Rock–PCO Tag Teams Resolved — Sunday Night Attendance Metrics]]]

### 2026-08-28 (Connor)
- ⛔ **the "final pass" is not a pass, it is a load.** [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-SNL-Group-Load-Check]]: greeters (15) and ushers (9) are in; **Setup, Breakdown, Slide, Host and Band have never been loaded — 43 memberships across 5 groups**
- ⚠️ **Trixie Fake-Carter-Corker (test record, 8/18) is sitting in SNL Greeter** and will sync to the real PCO greeter team. Pull her before this message goes out
- ⚠️ **3 people have no group at all** — Joe Lu, Lihong Lu, Mara Marin answered only "Not sure." A mass "sign up for shifts" email lands wrong on them; the draft's last paragraph handles it and commits Connor to reaching them individually
- ✅ email drafted; ✅ PCO welcome no longer a blocker (Connor sends manually)
- sequence: pull Trixie → load the 43 → sync push + confirm each tag team → send

### 2026-08-28 (later) — the load is done; two things still gate the send
- all groups except Band are populated (31 memberships added) → [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-SNL-Group-Load-Check]]
- ✅ test records removed 2026-08-28 — Trixie and Betty are out of every SNL group
- ⛔ **still gating: the sync push + pointing each newly populated PCO tag team at its tag** (Set-up, Break-down, Slide, Host). It does not happen by itself
- Mara Marin is not on any team and should not receive the mass "sign up for shifts" message as-is

### 2026-08-28 (quick refresh, email) — a shift is already confirmed on the 9/20 plan
- PCO 12:15 PM ET: CJ Sidener CONFIRMED the Usher (Evening Ushers) position for 9/20 — so a scheduling request for that position has already gone out and been accepted
- ⚠️ that sits against this note's "no volunteer has been asked." **Connor: did you schedule the usher position on the plan directly?** If someone else did, the 8/30 needs_by and the P1 framing need re-judging
- the two stated gates (sync push + pointing each PCO tag team at its tag) are unchanged
[Source: Email, Planning Center → Connor, 2026-08-28 12:15 PM ET]

### 2026-08-28 (verified in Planning Center) — ✅ BOTH GATES ARE CLEARED. Nothing technical is left.
Checked every team on service type `Sunday Night` (1804248) directly, not inferred:

| PCO team | tag pointed at | members |
|---|---|---|
| Evening Set Up | Set Up (Evening Volunteers) | 10 |
| Evening Breakdown | Breakdown (Evening Volunteers) | 12 |
| Evening Host | Host (Evening Volunteers) | 3 |
| Evening Audio/Visual | Audio + Slide (Evening Volunteers) | 9 |
| Evening Greeters | Greeter — on all 4 positions (Auditorium Doors, Front Doors, Garage, Hall) | 16 |
| Evening Captain | Captain (Evening Volunteers) | 3 |
| Evening Ushers | Usher (Evening Volunteers) | 9 |
| Evening Events | Events (Evening Volunteers) | **0** |
| Evening Band | 6 positions | 1 |

- every team is configured as a **Tag Team** and every position carries its tag. The sync push landed and the counts match the Rock groups
- → the "still gating" line from the earlier 8/28 entry is **spent**. The send is unblocked
- ⚠️ **Evening Events: tag linked, nobody carries it.** The Rock Events group (96954) was never loaded — it was not in the 8/28 load, which covered Set-up, Break-down, Slide and Host
- ⚠️ **Greeters reads 16 in PCO against 17 in Rock** — merge cleared 8/28; re-read both counts to close it out
- Band left alone (Seth Addison's call)

### 2026-08-28 (email) — Wertz merge processed
- 6:29 PM · Kay merged the two LaurenNichole Wertz person records; none remain in Rock or PCO
- 6:32 PM · Connor thanked her; no new ask
- proves the **person-record** merge only — the duplicate SNL-Greeter membership row and the 17-Rock/16-PCO greeter counts have not been re-read
[Source: Email, Kay Carter-Corker → Connor (cc Jennifer Claffey), "Merge record request: LaurenNichole", 2026-08-28 6:29 PM ET]

### 2026-08-29 (Connor) — ⛔ HELD. The send waits on Kay's (and Michele's) automated-welcome-email experience.
- **Connor: "Aren't we waiting to hear from Kay and Michele on how their automated emails have worked in the past?"** Yes — and the vault understated it
- **The chain, stated plainly:** a volunteer who has never logged in **cannot set a Planning Center password until the welcome email reaches them**, and cannot reach the signups until they have (Jennifer Claffey, 8/28). Sending the ask first points people at a door they cannot open
- **The escape hatch this note relied on does not exist.** Its 8/28 head line said *"Connor sends the PCO welcome manually."* Verified in-app the same evening: **no PCO People access at all**, and PCO Services offers only `Send Password Reset Email`. Rock's switch is not in his Tools menu either. That correction was written on the Kay note but this note's head was never updated to match — fixed above
- → `blocked_by`: [[Archive/Actions/Kay Carter-Corker - Turn on Rock's automatic Planning Center welcome email]]. `needs_by: 2026-08-30` is spent as a trigger, not met; the binding date is **2026-09-20**
- **Not blocked for everyone** — volunteers who already have PCO logins (e.g. CJ Sidener, Liz Goodiel) could act on the message today. A split send was considered and not taken; recorded so it is not re-proposed as new
- the Michele half is parked separately — Connor is not sending that ask ([[Archive/Actions/Connor - Ask Michele Smith for her Planning Center starter email as a template]], on-hold 2026-08-29). **Michele's relevance here is as the working example Kay copies, not as a correspondent**
[Source: Connor, 2026-08-29]

### 2026-08-31 (quick refresh, sweep) — frontmatter caught up with the 8/29 hold
- the 8/29 entry set `blocked_by` **in the body only**; the frontmatter had no `blocked_by` field, so `actions-index.py` never saw the block and `--brief` listed this as overdue on a passed `needs_by` while the send is held on Kay's switch
- added `blocked_by: Kay Carter-Corker - Turn on Rock's automatic Planning Center welcome email` to frontmatter. No status, band or date changed
- the split send (volunteers who already have PCO logins) stays **not taken**, per 8/29 — not re-proposed here

### 2026-09-02 (transcript synthesis, 9/1 Derek sync) — this is Connor's own top-of-mind concern, and he's naming a path around the Kay block
- Connor, unprompted, named this as what he's most worried about: *"I have not yet reached out to them saying, hey... the signups to be a greeter on September 20th at 6 PM are open now. I haven't done that, which means that no one signed up."* His fear, explicitly: an empty-feeling first week.
- **He's leaning toward self-configuring PCO's native welcome email** rather than waiting on Kay's Rock switch — *"I got an email back from Michelle... it seems mostly native to Planning Center, so that's what I'll do because I don't want to have to rely on folks internally to delay the communication."* This references Michele Smith's 8/30 reply, logged on [[Archive/Actions/Connor - Ask Michele Smith for her Planning Center starter email as a template]].
- ⚠️ **Contradiction worth Connor's attention before he acts on this:** the 8/28 entry on this same note verified in-app that Connor has **no PCO People access** — *"Grace Community Church subscribes to People but your personal user account... doesn't have access"* — and the welcome email is a People-module feature. Michele's answer describes what a **Services**-side default customization can do; it isn't obviously the same switch. If Connor tries the self-serve path and hits the same access wall, the `blocked_by` on Kay's switch is still real, just re-discovered a second way.
- → status, band, `blocked_by` unchanged — Connor named intent, not yet an action taken
[Source: [[Transcripts/2026-09-01 17.30 Connor–Derek Weekly Sync — Leader Asks Sent, Claude Cap Still Open]]]

### 2026-09-02 (Connor) — self-serve path worked; `blocked_by` cleared
- Connor confirmed: Michele's answer was enough to set up his own PCO welcome email — the escape hatch this note originally assumed (8/28) and then retired (8/29) is back, taken a different way
- → `blocked_by` cleared. The technical send-mechanism gate is resolved
- ⚠️ **Worth a quick check before the mass send, not a re-block:** the 8/28 finding that Connor has no PCO **People**-module access was never reconciled with what Michele described (a Services-side default). If his self-configured email is on the Services side, confirm it actually reaches someone who has never logged in before trusting it broadly — that's the one thing this note hasn't verified yet
- **Three data gates, unrelated to the above, still open from 8/28** and not re-checked since: Evening Events team has the tag but 0 members (Rock Events group never loaded); greeter count reads 16 in PCO vs. 17 in Rock (unresolved); Mara Marin, Joe Lu, Lihong Lu are on no team and need individual outreach, not the mass message
[Source: Connor, 2026-09-02]

### 2026-09-02 (Connor, live in Planning Center) — the People access wall is confirmed, not just a risk
- Connor asked for per-position welcome-email templates drafted directly in PCO. Checked live: each team's Automations tab (`added to team → send welcome email`) offers exactly **one** org-wide template and no way to create another without People access. `people.planningcenteronline.com` still refuses Connor's login
- → the 9/1 flag ("if he hits the same wall, that's the finding") is now confirmed. Zero of the 9 evening teams has this automation turned on
- Drafted the 8 position-specific welcome paragraphs as text instead, in [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Volunteer-Signup-Email-Draft]] Draft 3 — ready for either Kay to build as PCO templates, or Connor to send manually per team
[Source: Connor, 2026-09-02; live check at services.planningcenteronline.com and people.planningcenteronline.com]

### 2026-09-02 (Connor, email) — asked for the access directly
- Connor → Jennifer Claffey, cc Kay Carter-Corker, "Planning Center People access": asked to be granted PCO People access so he can build the per-position welcome templates himself
- → no status change; waiting on Jennifer/Kay to grant access before Draft 3 can become live PCO templates
[Source: Email, Connor → Jennifer Claffey (cc Kay Carter-Corker), "Planning Center People access", 2026-09-02]
