---
type: workflow
---
# M365 → Obsidian Sync — Reference

Incident write-ups behind the corrected/hardened rules in [[Workflows/m365-to-obsidian-sync]]. Split out **2026-09-09** so the main procedure file stays cheap to read on every run.

**Not part of the standard read for a sync.** The main file carries the operational rule; come here when the reasoning behind one is genuinely in question.

---

## Sent Items scoping defect (2026-08-12)

The rule (main file, § Source & window): query Sent Items with an explicit `folderName: "Sent Items"`, and never pass a bare `order` without `folderName`.

Why: passing `order` to `outlook_email_search` **without** `folderName` silently scopes the search to Inbox, so the Sent leg returns a `sent 0` that is indistinguishable from a real null. That is how Connor's 8/12 9:38 and 10:44 ET sent mail was missed by the 12:24 run — the sync reported a clean zero-finding run when two of his own commitments never got scanned. See [[Changelog/2026-08-12-m365-sent-items-scoping-fix]].

## The 30-minute overlap buffer (added 2026-07-15)

The rule (main file, § Source & window): window = (last successful run − 30 min) → now.

Why: an email can arrive *inside* a run's window but not yet be returned by Outlook search — there's a lag of minutes between delivery and the message becoming searchable/indexed. Without a buffer, that run advances the marker past the email's timestamp, and the *next* run's window starts exactly where the marker left off — so the email falls into a dead zone between two windows and is **permanently skipped by both**. This is what dropped Derek's 7/14 Staff Mtg Recap: arrived 12:17 PM ET, ~17 min before the 12:34 marker, caught by neither the 12:34 nor the 4 PM run; found only because Connor asked.

Starting each window 30 min *before* the marker re-scans that lag zone every run. This is safe because of the dedup guardrail (main file, Guardrails §2): before adding anything, confirm the target note doesn't already reflect the email, and skip if it does. Overlap therefore costs a few redundant reads, never a duplicate entry.

## Marker semantics: window-end, not completion time (changed 2026-09-04, Connor's call)

The rule (main file, § Update the marker): call `stamp.py mark --m365 --window-end "YYYY-MM-DD HH:MM"` with the actual scanned-through timestamp, not the moment the command runs.

Why: § Source & window already treats the marker as "the point mail has been scanned through" — but until this change, `stamp.py mark --m365` always wrote the run's *completion* time. Those coincide only when analysis and writing happen at the same instant; `grace-quick-refresh` splits them into Phase 1 (analysis) and Phase 2 (writing), so a run that takes 5-10 minutes to fold findings into trackers was quietly donating that gap to the next window's 30-minute overlap buffer, shrinking the real safety margin every time. See [[Archive/Actions/Connor - Decide whether the m365 sync marker should record scan-window end instead of run-completion time]] for the defect history (a 2h25m dead zone opened 2026-08-25) and [[Changelog/2026-09-04-m365-marker-window-end]]. `stamp.py` still refuses a missing `--window-end` outright — it falls back to completion time with a printed warning — so an un-updated caller degrades loudly rather than crashing.

## Registration routing rules that have expired

The World Cup Final Viewing Party and 7/19 Vision Setting Lunch registration-routing rules expired 2026-07-19 and were retired into the changelog on 2026-07-20 — see [[Changelog/_history/m365-to-obsidian-sync-changelog]] for their last-active text if another rule needs to be modeled on them.
