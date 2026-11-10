---
type: workflow
---
# M365 Sync — Run Log Health Check

A weekly-only duty of [[Workflows/grace-weekly-refresh]] (§ Weekly-only duties). Split out of [[Workflows/m365-to-obsidian-sync]] on **2026-09-09** — `grace-quick-refresh`'s email-sync subagent read that file in full on every on-demand run, including this section it never uses, since only the weekly job runs this check.

**Not part of a normal (quick-refresh) read.** `grace-weekly-refresh` reads this file directly when it runs its weekly-only duties; nothing else should open it.

---

The Run Log ([[Logs/m365-sync-run-log]]) only helps if someone actually looks at it. Rather than relying on Connor to notice a gap, `grace-weekly-refresh` (Mon 6:00 AM, see [[Trackers/Automation]]) checks it as a side duty alongside its Open Actions sweep, and turns a suspected gap into a visible, trackable item instead of a thing you'd only catch by reading a log no one reads.

**⚠️ Recalibrated 2026-07-27 for the weekly + on-demand cadence.** This check was written against the retired 8 AM / 12 PM / 4 PM schedule and counted entries *per calendar day*, expecting 3. Since 2026-07-21 the sync runs **weekly (Mon, via this task) plus on-demand (`grace-quick-refresh`)** — so most calendar days are *correctly* empty, and the old rules would have flagged a gap every single week. Both the per-day count and the ~20-hour staleness threshold are gone.

**Procedure:**
1. Read **[[Logs/m365-sync-run-log]]**. Take the **most recent entry's timestamp** (America/New_York).
2. **Primary check — did the weekly floor hold?** If the most recent entry is **more than 8 days old**, flag a **suspected missed run**. Eight days = one weekly cycle plus a day of slack, so a single late Monday doesn't false-positive but a skipped Monday does. On-demand runs are a bonus, never a substitute — their presence doesn't excuse a missing weekly entry, and their absence is not a fault.
3. **Event-week tightening.** If any /Events planning note's `date` is ≤3 days out, tighten the threshold to **4 days**. In an ordinary week a late catch-up costs nothing (the marker self-heals, zero data loss, per 7/15); in event week a delay can convert to a real-world miss — e.g. a registration or a volunteer cancellation arriving the morning of the event. Detection tightens exactly when delay is expensive.
4. **Secondary check — errored runs.** If the two most recent entries both carry `ERROR:` and the marker was not advanced, flag it regardless of age: the job is firing but failing, which the age check alone won't catch.
5. If nothing is flagged, do nothing further — this is not a report-every-week mechanism; it matches the refresh's "report only if something changed" behavior.
6. If something is flagged: check whether an **Active** item already exists in `/Trackers/Actions/` (visible in the Active view of [[Trackers/Open Actions.base]]) covering the same or an overlapping date range (search for "suspected missed m365-to-obsidian-sync run"). If so, just add a dated note to it instead of duplicating. If not, create a new note `/Trackers/Actions/Connor - Investigate suspected missed m365-to-obsidian-sync run(s).md`:

   ```
   ---
   status: active
   priority: P2
   owner: "Connor"
   added: {date of this sweep}
   deadline: "Unstated"
   last_mentioned: "{date of this sweep}"
   source: "[[Workflows/m365-to-obsidian-sync]] Run Log health check, {date of this sweep}"
   ---

   # Connor: Investigate suspected missed m365-to-obsidian-sync run(s)

   - **Priority rationale**: data-integrity risk; a missed run can silently drop registrations or commitments (per the 7/8 and 7/12 precedent), but nothing else is blocked on it
   - **Source**: [[Workflows/m365-to-obsidian-sync]] Run Log health check, {date of this sweep}
   - **Status**: Open — Run Log shows {N} of {3 or expected} entries for {the flagged date(s)} (or: most recent entry is {timestamp}, {H} hours old). Suspected missed run around {window}. To verify: manually search Outlook Inbox + Sent Items across that window and cross-check against the trackers it would have touched — same method as the 2026-07-13 full-history audit.
   - **Notes**: none
   - **Blocked by**: none
   - **Blocks**: none
   ```

6. Report the flag (if any) alongside `grace-weekly-refresh`'s normal output. Resolving the item (confirming a real gap and backfilling, or dismissing a false alarm) is manual — this check only surfaces the suspicion, it never backfills on its own.

**Note on threshold:** under the old 3x-daily schedule the worst-case normal gap was overnight (~16h), so a flat time threshold couldn't distinguish "quiet night" from "missed slot" and a per-day count was needed. Under the weekly cadence the opposite is true: the expected gap *is* a week, so a flat threshold is now the right instrument and per-day counting is meaningless. The trade-off is coarser detection — a missed weekly run can go up to 8 days unnoticed, versus ~1 day before. That's the accepted cost of the cadence change (see [[Trackers/Automation]] § Operating note), mitigated by the fact that the marker-based window self-heals: a skipped run loses no email, it only delays processing.

## Changelog

History lives in [[Changelog/_history/m365-to-obsidian-sync-changelog]] (this section's prior history was part of that file before the 2026-09-09 split); new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
