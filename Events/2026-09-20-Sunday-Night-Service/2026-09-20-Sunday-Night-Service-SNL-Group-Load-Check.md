---
title: "SNL Rock Group Load Check — every signup vs every bucket"
date: 2026-08-28
purpose: "Answer 'is everyone who responded to the survey in the proper bucket?' — the expected membership of each SNL Rock group, against what the vault last recorded as actually loaded."
event: "[[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Launch]]"
source: "[[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]], Rock instance 542, re-pulled 2026-08-17; load state from the 2026-08-26 Group Viewer verification"
tags: [sunday-night-service, rock, pco, verification]
---

# SNL Rock Group Load Check

> **2026-10-18:** Eric Wright removed from SNL-Greeter, Usher, Set-up, Break-down (archived) at Connor's request — counts below are as of 8/28.

## ✅ 2026-08-28 — LOADED. 31 memberships created; every group but Band is populated.

Done directly in Rock over the authenticated session (REST `POST /api/GroupMembers`, role **Member #54**, status **Active**), then read back. **SNL-Band was deliberately not touched** — Connor: *"That's not my call to make, just info for Seth if he needs it."*

| SNL group | Rock GroupId | Members now | Added this pass |
|---|---:|---:|---:|
| SNL-Greeter | 96947 | 18 | — (loaded 8/26) |
| SNL-Usher | 96948 | 9 | — (loaded 8/26) |
| **SNL-Set-up** | 96949 | **10** | **+10** |
| **SNL-Break-down** | 96950 | **12** | **+12** |
| **SNL-Slide** | 97396 | 10 | **+6** |
| **SNL-Host** | 96955 | 5 | **+3** |
| SNL-Band | 96952 | 1 (Seth Addison) | **0 — Seth's call** |
| SNL-Captain / SNL-AUDIO / SNL-Events | 96946 / 96951 / 96954 | untouched | 0 |

**SNL-Set-up (10)** — Steven Bader · Brandon Geddes · Liz Goodiel · Sean Liesegang · Omayra Martinez · Renae Mittelmeier · Sarah Payne · Michael Thompson · Sarai Wilburn · Eric Wright

**SNL-Break-down (12)** — the 10 who checked Teardown (Bader · Goodiel · Liesegang · Aila Lu · Mittelmeier · Nayiga · Erik Shaw · Thompson · Wilburn · Wright) **plus Joe Lu and Lihong Lu**, placed here by Connor 2026-08-28: *"keep her on tear down — add the rest of the family to tear down, not setup."* Aila stays on Teardown only.

**SNL-Slide (+6)** — Brandon Geddes · Aj Norton · Sarah Payne · CJ Sidener · Michael Thompson · Sarai Wilburn

**SNL-Host (+3)** — Felipe Gomez Trujillo · Jen Porter · CJ Sidener

**Mara Marin: deliberately left with no group.** Connor's instruction was to place her from her email reply if one existed. **There is none.** Connor emailed her 2026-08-20 (*"Sunday Night Service - worship, and where you might fit"*), recommended **ushering** — *"Please let me know if that sounds like a fit for you"* — and she never answered. Her stated interest is **worship**, which is the one team not being loaded. So she stays blank, and the dangling ask is his 8/20 question.

---

## ⚠️ Six data problems found while loading. None were fixed — all need a human.

Nothing here was deleted or altered; these are reads.

1. **`Trixie Fake-Carter-Corker` (person 11846) is a fake test record sitting in THREE groups** — SNL-Greeter, SNL-Slide and SNL-Host. She will sync to all three PCO teams and appear on real schedules. **Remove before any volunteer sees a roster.**
2. **`Betty Rock Cloud` (person 13504) is in SNL-Slide** — a Rock sample/system record, same problem, one group.
3. **LaurenNichole Wertz exists twice as a person** — **26541** (record status 3) and **34819** (status 5), same email `LaNicholeHome@gmail.com`, **and both are in SNL-Greeter.** That is a duplicate person record, not just a duplicate membership. It is the merge case Jennifer Claffey described from the PCO-first outage. Merging is a Kay/Jennifer job.
4. **Michael Vacca has two memberships in SNL-Slide** — one **Member**, one **Leader** (both person 23999). Probably intended as Leader only; the duplicate row is noise on a scheduled team.
5. **Jennifer Claffey sits in SNL-Host with status Inactive (0).** Left exactly as found.
6. **Lihong Lu is in Rock as `Lu Lu` (person 34378)** — the signup form says Lihong Lu, `lihong.l.mcphail@gmail.com`. Correct name, wrong record label. Also: **Brandon Geddes (17499) shares his email with `Thalyta Salimo` (33223)** — a household record sharing an address, worth knowing before anything emails by person record.

---

## Next, in order

1. **Ask for a Rock→PCO sync push**, then **confirm each newly populated PCO tag team is pointed at its tag** — Set-up, Break-down, Slide, Host. This does not happen by itself (Kay's 2026-08-28 rule); the tags will write and the team membership will not.
2. **Pull Trixie and Betty Rock Cloud** before the volunteer message goes out.
3. Send the sign-up message → [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Volunteer-Signup-Email-Draft]].
4. Second loading pass after the Sun 8/30 lunch, per Connor's own sequencing.
5. **Frequency is still nowhere in Rock** — five said *every week*, nine said *not sure*, and group membership treats them identically. It only shows up when shifts get filled.

---

## Appendix — the state this file was written to check (2026-08-28, pre-load)

Kept because the "before" is what makes the load auditable. Greeter and Usher were loaded 8/26; **Set-up and Break-down were empty; Slide held only test records plus Vacca; Host held only Jennifer Claffey (inactive) and Trixie.** Source for the expected membership: [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]], Rock instance 542, re-pulled 2026-08-17 — 24 registrations / 25 registrants, 21 live people after Sumay Lu dropped out.

Scope rule applied, per Connor 8/26: **everyone who checked the box**, including those already on Sunday-morning teams (Sidener, Wertz, Wilburn, Gomez Trujillo, Porter).

---

## 🔧 2026-08-28 cleanup — restore data, written BEFORE anything was removed

Connor authorised: remove the fakes, remove Jennifer as Host, merge the two Wertz profiles, merge Lu Lu with Lihong, leave Vacca as is.

### Rows removed — exactly how to put each one back

Only **GroupMember** rows were deleted. **No person record was deleted.** Each row can be recreated with `POST /api/GroupMembers {GroupId, PersonId, GroupRoleId:54, GroupMemberStatus:<n>}`.

| Was | Group | GroupId | PersonId | Old row | Role | Status |
|---|---|---:|---:|---|---:|---:|
| Trixie Fake-Carter-Corker | SNL-Greeter | 96947 | 11846 | gm213940 | Member (54) | 1 |
| Trixie Fake-Carter-Corker | SNL-Slide | 97396 | 11846 | gm215027 | Member (54) | 1 |
| Trixie Fake-Carter-Corker | SNL-Host | 96955 | 11846 | gm215029 | Member (54) | 1 |
| Betty Rock Cloud | SNL-Slide | 97396 | 13504 | gm215010 | Member (54) | 1 |
| Jennifer Claffey | SNL-Host | 96955 | 993 | gm215050 | Member (54) | **0 (was already Inactive)** |

**Left alone as instructed:** Michael Vacca's duplicate Member + Leader rows in SNL-Slide (person 23999). **Skylar Frey stays in SNL-Greeter** — she is a real person and Connor's test volunteer from 8/11, not a fake record; not removed and not raised as one.

### ⛔ "Merge Lu Lu with Lihong" — there is nothing to merge

**There is only one record.** Person **34378** has `FirstName = "Lihong"` and `NickName = "Lu"`, so Rock renders her as *"Lu Lu"*. No second Lihong record exists — a search on `NickName eq 'Lihong'` returns nothing, and `LastName eq 'Lu'` returns eleven people, only one of whom is her.

So this was **a one-field data-entry error, not a duplicate**: the signup form put her surname in the nickname slot. Fixed by setting `NickName` to *Lihong*. Nothing was merged, and no record was destroyed. Family 93199 (the McPhail/Lu household — Joe 32645, Lihong 34378, Sumay 34379, Aila 34380) is untouched.

### LaurenNichole Wertz — a genuine duplicate, and the direction is not a coin flip

| | **26541 — keep** | **34819 — merge away** |
|---|---|---|
| Created | 2025-01-29 | **2026-08-16 11:28** — the minute she registered at the high tops |
| Record status | 3 (Active) | 5 (Pending) |
| Group memberships | **25** | 6 |
| Attendance records | **26** | **0** |
| Person alias | 26550 | 34828 |
| Family | 97032 | 97032 — *the same family, so the household currently holds two copies of her* |

**26541 is the real record**; 34819 is the thin shell the 8/16 signup created. Merging the other way would throw away 26 attendance records and a year of group history.

⭐ **And this is a systemic finding, not a one-off.** The duplicate was created **by the 4th-service signup form** for someone who was already in Rock. Two of the other three 8/16–8/17 high-top registrants are also long-standing attendees, so the same thing may have happened to them. Worth one look before the next platform push.

### ✅ Cleanup executed 2026-08-28 — result

| Asked | Done | Note |
|---|---|---|
| Remove the fakes | ✅ | Trixie Fake-Carter-Corker out of Greeter, Slide and Host; Betty Rock Cloud out of Slide. **4 GroupMember rows deleted, 0 person records touched** — both people still exist in Rock. |
| Remove Jennifer as Host | ✅ | 1 row deleted (she was already Inactive). Jennifer Claffey's person record untouched. |
| Leave Vacca as is | ✅ | Both his Member and Leader rows in SNL-Slide are intact. |
| Merge Lu Lu with Lihong | ✅ **but it was not a merge** | One record only. `NickName` was *"Lu"*; set to *"Lihong"*. She now reads **Lihong Lu**. Nothing merged, nothing destroyed. |
| Merge the two Wertz profiles | ✅ **done 2026-08-28 by Kay Carter-Corker** | Connor's account lacks merge rights, so it filed as a request to the data integrity team (keep 26541, merge 34819 in). Kay processed it that afternoon and reports no remaining LaurenNichole duplicates in Rock or PCO. SNL-Greeter has not been re-read since. |

**Final state — every SNL group**

| Group | n | Members |
|---|---:|---|
| SNL-Set-up | 10 | Bader · Geddes · Goodiel · Liesegang · Martinez · Mittelmeier · Payne · Thompson · Wilburn · Wright |
| SNL-Break-down | 12 | Bader · Goodiel · Liesegang · Aila Lu · **Lihong Lu** · Joe Lu · Mittelmeier · Nayiga · Shaw · Thompson · Wilburn · Wright |
| SNL-Slide | 8 | Geddes · Norton · Payne · Sidener · Thompson · Wilburn · Vacca (Member + Leader) |
| SNL-Host | 3 | Gomez Trujillo · Porter · Sidener |
| SNL-Greeter | 17 → re-read | the 15 signups + Skylar Frey + the duplicate Wertz row; the 8/28 merge should have collapsed it, not verified |
| SNL-Usher | 9 | Bader · Martinez · Nayiga · Osarumwense · Payne · Sidener · Thompson · Wilburn · Wright |
| SNL-Band | 1 | Seth Addison — untouched, Seth's call |
| SNL-Captain / AUDIO / Events | — | untouched |

**Clean: zero test records anywhere in the SNL family.**

⚠️ **One thing to watch on the next push.** The Wertz duplicate was created **by the signup form itself**, for a person already in Rock. That is a property of the form, not a one-off, and the merge needs someone with rights every time it happens. Worth one question to Kay about whether the form can match on email before creating a person. Kay, 8/28: she regularly reviews and merges Rock duplicates — a cleanup cadence, not form-level prevention, so the question is still unasked.

## 2026-08-28 — PCO side verified

Rock → PCO sync confirmed landed. All 9 `Sunday Night` (service type 1804248) teams are Tag Teams with their tag attached at position level: Set Up 10, Breakdown 12, Host 3, Audio/Visual 9 (Audio + Slide), Greeters 16 across 4 positions, Captain 3, Ushers 9, Events **0**, Band 1.

- **Evening Events is wired but empty** — the tag `Events (Evening Volunteers)` is on the position and nobody carries it. Rock group 96954 was never loaded.
- **Greeters: 16 in PCO vs 17 in Rock** as of 8/28. The merge cleared that evening; re-read Rock 96947 and PCO Evening Greeters (7460439) to settle it.
- **Team membership is not a schedule.** On the 9/20 plan itself only the Usher position is filled (CJ Sidener, confirmed 8/28). Still needed: Greeters 10, Audio/Visual 2, Band 1, Captain 1, Events 1.

Team ids for future runs: Band 7460437, Audio/Visual 7460438, Greeters 7460439, Ushers 7460440, Captain 7460441, Events 7460442, Set Up 7460443, Breakdown 7460444, Host 7460445. Plan 9/20 = 91130954.

## 🔧 2026-10-25 — SNL-Host trimmed (restore data written before removal)

At Connor's request, Felipe Gomez Trujillo, Jen Porter and CJ Sidener are coming off **SNL-Host (96955)**. Only GroupMember rows are deleted; person records are not touched. To restore one: `POST /api/GroupMembers {GroupId:96955, PersonId, GroupRoleId:54, GroupMemberStatus:1}`.

| Was | PersonId | Old row | Role | Status | Added |
|---|---:|---|---:|---:|---|
| Felipe Gomez Trujillo | 26071 | gm215077 | Member (54) | 1 | 2026-08-28 |
| Jen Porter | 4151 | gm215078 | Member (54) | 1 | 2026-08-28 |
| CJ Sidener | 15640 | gm215079 | Member (54) | 1 | 2026-08-28 |

**Result:** all 3 DELETEs returned 204. SNL-Host now has **7 members**, all Active: Brandon Geddes · Emily Horneffer · Simba Kanjanda · Sean Liesegang · Liz Goodiel · Connor Frey · Skylar Frey. Their PCO tag and Evening Connection team membership drop off on the next Rock→PCO sync.
