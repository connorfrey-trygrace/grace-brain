---
name: "🛠️ Connor: Fix the m365 sync Sent Items scoping defect (bare order param)"
status: completed
resolved: 2026-09-11
priority: P2
owner: "Connor"
added: 2026-08-12
deadline: none
last_mentioned: "2026-09-11"
source: "[[Logs/m365-sync-run-log]] 2026-08-12 12:24 ET line; confirmed by the 2026-08-12 17:56 ET run"
projects:
  - "Vault system"
---

# 🛠️ Connor: Fix the m365 sync Sent Items scoping defect (bare order param)

- [ ] Decide whether the earlier `sent 0` nulls need a backfill audit. The workflow-text half of the fix is already applied (see Status).

- **Priority rationale**: data-integrity: it silently drops Connor's own sent commitments, which the workflow itself calls *"often the most actionable"* class of email. Nothing is blocked on it.
- **The defect**: passing `order` to `outlook_email_search` **without** a `folderName` silently scopes the search to **Inbox**. A Sent-Items leg run that way returns `sent 0` and is indistinguishable from a real null.
- **What it cost, concretely**: the **2026-08-12 12:24 ET** run logged `inbox 0, sent 0` and asserted Sent Items was empty. It was not — Connor's *"Counting Tech"* (9:38 AM ET) and *"Faith For Everyday Life schedule"* (10:44 AM ET) were both already sent. Both were only caught by the 17:56 ET run, whose window reached back past them.
- **Twice-documented, once-applied**: that same 12:24 line diagnosed the defect for the **Inbox/all-folders** leg and prescribed *"omit `order` when running the all-folders leg"* — but never applied the same reasoning to the **Sent** leg, which is where it was actually doing damage. A fix documented for one leg and not the other reads as fixed.
- **Status**: **Completed 2026-09-11 — closed, not audited.** The workflow-text fix (2026-08-12: Sent leg always passes `folderName: "Sent Items"`, no leg passes a bare `order`) has now held across every run checked since, including an independent subagent on 2026-09-11 with no memory of the incident that followed the documented instructions correctly unprompted. Connor's call: accept the loss on the two historical `sent 0` nulls (2026-08-11 13:44, 2026-08-12 12:24) rather than audit them. Recorded in [[Changelog/2026-08-12-m365-sent-items-scoping-fix]].
- **Blocked by**: none

### 2026-08-20 (standalone sweep)
- flagged: quiet 8 days, no blocker
- **The code/workflow half is done and held up in practice** — this run's email pass explicitly queried Sent Items with `folderName` and no bare `order`, and returned **5 sent items** where the broken runs returned `sent 0`
- next physical action: **Connor's one-word call — audit the earlier `sent 0` runs, or accept the loss and close this.** That decision is the only thing keeping it open

### 2026-08-28 (quick refresh) — measured, not reasoned: the workaround holds
- this run's email pass queried Sent Items with an explicit `folderName: "Sent Items"` and **no** `order` param. Control: the same query across 8/27+ returned **6** messages; the 10:41–15:52 window returned **0**
- so the zero was a real null, not the scoping defect swallowing results. The documented workaround works
- ⚠️ this is evidence the **workaround** is sound, not that the underlying `order`-param defect is fixed. Item stays open; flag reason ("no follow-up in 8 days") is no longer true
- → `flagged` cleared, no other field changed

### 2026-08-28 (weekly synthesis, light audit) — flag-clear correction
- the 8/28 clear wrote `flagged: none`, but YAML parses `none` as a truthy string, so the actions index kept showing this note FLAGGED. Normalized to `flagged: ""` to match the vault convention and actually clear the flag. No other field changed

### 2026-09-08 (quick refresh, sweep, Step 3) — flagged
- → flagged: no follow-up in 11 days; the order-param defect itself and the backfill-audit decision are both still open

### 2026-09-11 (Connor, live session) — closed
- Connor: close it if the bug won't recur. Today's independent email-sync subagent (no memory of this item) used `folderName: "Sent Items"` and no bare `order` correctly, per this run's own findings report — the fix is holding on its own, not just when someone remembers to check.
- → status: active → completed, resolved 2026-09-11 (accept the loss on the two historical nulls); `flagged` cleared.
