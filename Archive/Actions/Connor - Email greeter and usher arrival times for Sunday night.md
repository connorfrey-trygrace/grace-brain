---
name: "✉️ Connor: Email greeter and usher arrival times for Sunday night"
status: completed
priority: P1
owner: "Connor"
added: 2026-09-20
deadline: 2026-09-27
needs_by: 2026-09-26
chase_by: none
last_mentioned: "2026-09-25"
resolved: 2026-09-25
source: "Text, greeter thread, 2026-09-20 10:49 AM ET"
projects:
  - "Sunday Night Launch"
people:
  - "[[People/Connor Frey]]"
---

# ✉️ Connor: Email greeter and usher arrival times for Sunday night

- [x] Email all Evening Greeters + Ushers (not Skylar): thanks for 9/20, still need volunteers for 9/27, October sign-ups open.
- [x] **Sat 9/26**: send arrival-time reminder (5:20 call for 5:30 huddle, 6:00 service — no doors time) to the scheduled 9/27 greeters/ushers only.

- **Priority rationale**: P1 — the service is tonight and PCO is not reminding them.
- **Source**: Connor asked the greeter thread whether PCO sends automated reminders; Liz Goodiel: they don't think so. Connor: "I'll shoot one out shortly."
- **Status**: ✅ Completed 2026-09-25 — automated in PCO: "Volunteer Arrival" 5:20–6:00 PM Other Time on every future plan, Greeters + Ushers, reminder 1 day before (10:00 AM). No manual Saturday email needed.
- **Notes**: the underlying gap — PCO scheduling reminders not reaching the evening volunteer team — is broader than tonight and worth its own item if it recurs.
- **Blocked by**: none · **Blocks**: nothing named

### 2026-09-21 (quick refresh, sweep, Step 2.5) — 🟡 closure candidate: the 9/20 instance is moot either way
- The action was "send arrival times **for tonight's 6 PM service**." That service has happened. Whether or not the email went out, there is nothing left to do about 9/20.
- ⚠️ **But the gap this note itself predicted has now recurred.** Its own Notes say: *"the underlying gap — PCO scheduling reminders not reaching the evening volunteer team — is broader than tonight and worth its own item if it recurs."* Greeters are confirmed for **9/27 and 10/11** (Michael Thompson accepted both) and PCO still does not remind them.
- **Not minted unilaterally** — turning this into a standing weekly task is a shape change, not a sweep decision. Surfaced for Connor: make it recurring, or accept ad-hoc.

### 2026-09-22 (Connor, chat) — reopened for 9/27
- Connor: "This matters for 9/27. We need to ask for more volunteer sign ups"
- → status: closure-candidate → active; deadline 2026-09-20 → 2026-09-27

### 2026-09-23 (Connor, chat) — shape changed
- No split: one email to everyone on both lists — thanks for 9/20, need volunteers 9/27, October sign-ups open
- Time reminder to scheduled folks held until Sat 9/26

### 2026-09-23 (sent via PCO) — team email
- PCO "Email These People" from Evening Greeters team, + Sarai Wilburn, Steven Bader (Ushers-only); Skylar removed → **20 recipients**
- Subject "Thank you + Sunday night volunteers": thanks for 9/20, still need volunteers 9/27 (sign up in PCO or reply), October sign-ups open
- Remaining: Sat 9/26 time reminder to scheduled folks only

### 2026-09-23 (Connor, chat) — reminder times
- 5:20 call for a 5:30 huddle; 6:00 service; leave doors out

### 2026-09-23 (Connor, chat) — reminder wording locked
- Subject: "Sunday 9/27: please arrive at 5:20 PM"
- Body: "Thanks so much for serving this Sunday night! Please come at 5:20 PM in time for our volunteer huddle at 5:30. The service starts at 6:00. — Connor"
- Send Sat 9/26 via PCO plan 91453887 team email, scheduled greeters/ushers only (not Skylar)

### 2026-09-23 (Connor, chat) — 9/27 roster cleaned
- Removed 4 people who were scheduled by a copy of the 9/20 roster on 9/15 and never notified: Sarah Payne, Cameron Waggener, Michael Thompson (Hall), Victoria Nayiga
- 9/27 greeters now: Renae Mittelmeier, Michael Thompson (Auditorium Doors), Liz Goodiel, LaurenNichole Wertz, Shannon Coen. Ushers: CJ Sidener only (Sean Liesegang declined)
- The Sat reminder goes to this list

### 2026-09-23 (email) — PCO confirmations
- 12:39 PM · Shannon Coen confirmed 9/27 Hall
- 1:33 PM · Hannah Hagen confirmed 10/4 Front Doors
[Source: Planning Center notification emails, 2026-09-23]

### 2026-09-23 (email) — Renae asked
- 5:23 PM · Renae Mittelmeier asked her 9/27 arrival time
- 5:36 PM · Connor: 5:20 call for 5:30 huddle; automated reminder Saturday. Renae: "Thanks!"
[Source: Email thread "Re: Thank you + Sunday night volunteers", 2026-09-23]

### 2026-09-24 (email + PCO check) — Cameron Waggener back on 9/27
- 6:54 PM · New PCO record for Cameron Waggener, 9/27 Hall, created and confirmed at once (created after the 9/23 removal). He signed up again; this isn't the stale copy.
- Checked plan 91453887 on 9/25. Sat reminder list: Renae Mittelmeier, Michael Thompson, Liz Goodiel, LaurenNichole Wertz, Shannon Coen, **Cameron Waggener**; usher CJ Sidener
[Source: PCO notification email 2026-09-24 6:59 PM ET; PCO plan 91453887 roster, read 2026-09-25]

### 2026-09-25 (Connor, chat) — can PCO automate it? (API check)
- Plans 91453887 / 91455422 / 91781260: reminders_disabled = false, but **0 rehearsal/other times** — only the 6:00 service time exists
- So any PCO reminder can only say 6:00, never 5:20
- Fix: add an "Other" plan time (5:20 call / 5:30 huddle) assigned to Evening Greeters + Ushers, on each plan + the template
- Not exposed by the API: the service type's Scheduling → Reminders setting (days before). Liz's "don't think so" suggests it's off

### 2026-09-25 (Connor, chat) — set shift times by position
- Jennifer's method, 8/11 Rock setup session: per-position shift times under the plan's Other Times, so the PCO reminder carries service time + shift time ([[Transcripts/2026-08-11 11.54 Sunday Night Service Rock Setup — SNL Groups Created, PCO Tags Blocked]] ~10:25)
- Evening plans have none set — why the reminder only ever says 6:00

### 2026-09-25 (Connor, chat) — go-ahead to set shift times
- Connor: "Fix it, yes please" — blocked: PCO web unreachable from the built-in browser, Chrome extension disconnected, MCP is read-only

### 2026-09-25 (Connor, live session) — automated in PCO
- Root cause: every team on the service time was set to "No Reminder" — PCO never sent any
- Added Other Time "Volunteer Arrival" 5:20–6:00 PM, Evening Greeters + Evening Ushers, reminder 1 day before (Sat 10:00 AM), "Create this time in future plans" on
- API-verified: all 12 future plans (9/27 → 12/13) now carry 1 other time
- Other evening teams (A/V, Band, Captain, etc.) still have No Reminder on the service time — untouched
