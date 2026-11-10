---
name: "🛠️ Connor: Decide whether the m365 sync marker should record scan-window end instead of run-completion time"
status: completed
priority: P3
owner: "Connor"
added: 2026-08-26
deadline: none
last_mentioned: "2026-09-04"
resolved: 2026-09-04
flagged: ""
source: "[[Workflows/grace-quick-refresh]] Phase 1 email sync, 2026-08-26 run; measured against [[Logs/m365-sync-run-log]] 2026-08-25 12:25 ET line"
projects:
  - "Vault system"
---

# 🛠️ Connor: Decide whether the m365 sync marker should record scan-window end instead of run-completion time

- [ ] Decide the fix: **(a)** make `## Last successful run` record the **end of the scan window** rather than the run's completion time (a `stamp.py` change plus a workflow amendment), or **(b)** widen the overlap buffer to cover typical run duration.

- **Priority rationale**: data-integrity, but **measured impact so far is zero** — the one gap this defect has actually opened was scanned explicitly on 2026-08-26 and was empty. Nothing is blocked on it, and the next run's window always covers *some* of the gap. P3 on that evidence; it moves up the first time a real email lands in a dead zone.
- **The defect**: [[Workflows/m365-to-obsidian-sync]] § *Update the marker* says to write **the run's completion timestamp**. § *Source & window* treats the marker as **the point mail has been scanned through**. Those are the same number only when writing is instantaneous. Since [[Workflows/grace-quick-refresh]] separates analysis (Phase 1) from writing (Phase 2), they never are.
- **What it cost, concretely**: the 2026-08-25 run logged `window 08-24 08:00 → 08-25 09:30 ET` but wrote the marker `2026-08-25 12:25 ET`. The next window therefore opened at **11:55 ET** (marker − 30 min), leaving **08-25 09:30 → 11:55 ET — 2h25m — belonging to no window at all.** The 30-minute buffer is far too short to cover it.
- **It recurs on every run**, not occasionally: the 2026-08-24 weekly run took **136 minutes**, so the exposure is routine. This is the same failure family as Derek's 7/14 *Staff Mtg Recap*, which the buffer was added to prevent.
- **Status**: Completed 2026-09-04 — **the 2026-08-26 run scanned the 09:30 → 11:55 ET gap explicitly. 0 inbox, 0 sent. No mail was lost.** The mechanism was wrong until Connor decided option (a) on 2026-09-04; see that entry below for what shipped.
- **Related**: [[Archive/Actions/Connor - Fix the m365 sync Sent Items scoping defect (bare order param)]] — different defect, same file. The three marker changelogs ([[Changelog/2026-08-12-m365-sent-items-scoping-fix]], [[Changelog/2026-08-17-timezone-marker-defect]], [[Changelog/2026-08-21-clock-enforced-in-code]]) all address marker **correctness**; **none addresses marker semantics.**
- **Blocked by**: none · **Blocks**: nothing

### 2026-09-04 (standalone sweep, Step 3) — flagged
- 9 days since last mentioned, no decision made
- → flagged: none → 2026-09-04

### 2026-09-04 (Connor) — decided: (a), built and shipped
- Connor: "Go ahead and fix the m365 sync timing. Less of an issue now that I am working from Claude Code rather than cowork."
- **Built option (a).** `Workflows/stamp.py mark --m365` now takes `--window-end "YYYY-MM-DD HH:MM"` and writes that instead of the run-completion time; the field means what § Source & window always said it meant. Missing `--window-end` falls back to the old completion-time behavior with a printed warning rather than crashing, so a stale caller degrades loudly, not silently.
- Updated [[Workflows/m365-to-obsidian-sync]] § *Update the marker* to call it with `--window-end` and explain why, and [[Workflows/grace-quick-refresh]]'s Phase 2 instructions to match.
- → `status: completed`. [[Changelog/2026-09-04-m365-marker-window-end]]
