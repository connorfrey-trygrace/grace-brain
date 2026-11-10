---
date: 2026-08-31
area: Open-Actions-Tracker / actions-index.py
---

# `--brief` now suppresses items blocked by an open item, and the frontmatter that should have said so

## What happened

The 2026-08-31 08:21 ET quick refresh's `--brief` led Start Here with:

```
## [!] Overdue or due today (4)
  P1  Connor - Message the Sunday-night volunteers to sign up for shifts in PCO  <- needs_by 2026-08-30 — latest start
```

That send has been **held since 2026-08-29** on [[Trackers/Actions/Kay Carter-Corker - Turn on Rock's automatic Planning Center welcome email]]: a volunteer who has never logged in cannot set a Planning Center password until the welcome email reaches them, and cannot reach the signups until they have. Sending the ask first points people at a door they cannot open. There is no Connor-side action, and Kay is a colleague, not a ticket queue ([[Changelog/_history/…|church-not-a-corporation]]).

## Two defects, one line

**1. The hold was written into the body only.** The 8/29 entry set `blocked_by` in prose and in the `- **Blocked by**:` bullet. The frontmatter had no `blocked_by` field at all, so `actions-index.py` — which reads frontmatter — never saw it. The sweep view did not print `blocked`, and Step 3's own "check `blocked_by` before flagging" gate had nothing to check. Fixed: the field is now in frontmatter.

**2. `brief()` never read `blocked_by` in the first place.** [[Workflows/Open-Actions-Tracker]] defines the queue as *"every `active`/`in-progress` item Connor owns that is not `blocked_by` an open item"*, and the sweep view has printed a `blocked` marker since 2026-08-18. `brief()` filtered on `waiting-on`-without-`chase_by` and on status, and on nothing else. So even after defect 1 was fixed, `--brief` still printed the item under **Overdue or due today**.

Fixing only the frontmatter would have left the second defect invisible until the next note held it the same way — the pattern [[Changelog/2026-08-28-messages-exclusion-enforced-in-code]] and [[Changelog/2026-08-21-clock-enforced-in-code]] both close by moving the rule into the code.

## The fix

`open_blockers(n, status_by_file)` resolves each `[[wikilink]]` in `blocked_by` to a note in `/Trackers/Actions/` and returns the ones whose status is still open (`active`, `in-progress`, `waiting-on`, `on-hold`, `closure-candidate`). `brief()` skips any item with a non-empty result. The sweep view is unchanged — it is the inventory and still shows everything, marked `blocked`.

**It fails open, deliberately.** A blocker string that resolves to no note suppresses nothing. Over-suppression silently removes real work from the only view Connor reads first; under-suppression costs one line he can strike. Same reasoning as the `query-messages.py` self-test measuring over-exclusion as well as under-exclusion.

## Measured, both directions (2026-08-31)

All four notes in the folder carrying a `blocked_by` value:

| note | blocker's status | suppressed? |
|---|---|---|
| Connor - Message the Sunday-night volunteers to sign up for shifts in PCO | Kay's welcome email — **active** | yes |
| Derek Adye - Make the 9-13 morning QR push from stage | Connor/Heather QR destination — **waiting-on** | yes |
| Connor - Set up weekly name-tag station for Sunday night | greeters — **on-hold** | yes (already out: status `on-hold`) |
| Connor - Follow up with the 4th-service volunteer signups on role placement | Kay's Sunday Night group — **completed** | **no** — the negative control |

`--brief` Overdue 4 → 3, Next-14-days 17 → 16. The sweep view still lists 57 live items.
