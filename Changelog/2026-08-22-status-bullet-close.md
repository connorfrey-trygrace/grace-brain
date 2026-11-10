---
type: changelog
date: 2026-08-22
tier: 2
touches: ["[[Workflows/actions-index.py]]", "[[Workflows/Open-Actions-Tracker]]", "[[Workflows/Open-Actions-Transcript-Steps]]"]
trigger: "Connor, 2026-08-22 — asked for the 17 status contradictions swept and the closure procedure fixed so it stops recurring"
---
# Closing an item now includes rewriting its Status bullet — and the contradiction check runs in every sweep, not just the weekly one

**The defect.** Setting `status: completed` in frontmatter and appending a dated closing entry leaves the note's prose `- **Status**:` bullet untouched at the top of the file. The next reader — human or sync — meets *"Active — nobody has been asked"* on an item that closed days earlier. Connor first called this class out on **2026-08-10** (*"should have been caught"*). By **2026-08-22** it had recurred **17 times**.

**Measured, not assumed.** All 17 were audited individually against their closing evidence before anything was rewritten. **Frontmatter was correct in all 17** — every one had a real close (a Connor confirmation, an email reply, a live-session decision), so the prose bullet was the loser in each case. That is a finding, not a default: the check is deliberately two-sided, because a body reading "Completed" under an `active` field is the same defect in the other direction.

Two of the 17 were closed on something other than delivery, and the rewritten bullets now say so rather than reading as wins: the **event-comms timing rules** were *cancelled by the owner who opened them*, and the **Boot Camp new-believer headcount** was *dismissed, not delivered* (Connor: "nice to have").

## Why the fix is code first, procedure second

The detection already existed — `actions-index.py --drift` has flagged status contradictions since 2026-08-10. It never fired in practice because **`--drift` only runs as a `grace-weekly-refresh` side duty**, so a contradiction created on a Tuesday sat unseen until the following Monday, if the Mac was awake for it.

`status_contradictions()` is now a module-level function called from **both** `--drift` and the **default index output**, so it prints in the `## STATUS CONTRADICTIONS` block on every Step 0 — and Step 0 is not optional in either mode. Verified by a 7-case unit test over the detector (fires on completed-over-Active, active-over-Completed, completed-over-Waiting; silent on correct closes, dismissals phrased as "Closed — cancelled", live waiting-on notes, and notes with no Status bullet). The full sweep output is otherwise unchanged.

**The procedure half:** a new `## Closing an item` section in [[Workflows/Open-Actions-Tracker]] makes the Status-bullet rewrite part of the close on *every* path — Step 2, Step 2.5, live-session confirmations, the text sync and the email sync — with the pointer repeated inline at Step 2.5 and in [[Workflows/Open-Actions-Transcript-Steps]] Step 2, which are the two places the omission actually happened.

The index catching it afterward is a backstop. The fix is closing the item properly.

## One thing deliberately left alone

[[Archive/Actions/Connor - Identify Sunday night hostMC (boot camp alumni pool)]] carries `resolved: 2026-08-30` — a **future** date, set on purpose on 2026-08-18 because Connor closed it on the 8/30 lunch being the confirmation. Left as-is and now stated in its Status bullet, but worth knowing that nothing distinguishes a deliberate forward-dated `resolved` from a typo, and no check looks for one.
