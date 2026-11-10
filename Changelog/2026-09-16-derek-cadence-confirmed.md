---
type: changelog
date: 2026-09-16
tier: 1
touches: ["[[Workflows/agenda-note]]", "[[Trackers/Automation]]"]
trigger: "Connor, 2026-09-16 — \"We will now be meeting every other week on mondays at 4 rather than weekly on tuesdays at 4\""
---
# Connor–Derek sync cadence confirmed: bi-weekly Mondays 4:00 PM

Closes the question `Trackers/Automation.md` had held open since 2026-09-08, which deliberately refused to re-cron the agenda job on the strength of a calendar-invite acceptance alone ("an invite acceptance is a calendar action, not an explicit confirmation reply"). Connor confirmed the cadence directly. Also confirmed he wants the agenda **in advance** rather than at meeting time, superseding the older preference recorded when the sync was itself at 2 PM.

No re-cron was required — `derek-sync-agenda` gates on the Outlook calendar rather than encoding a cadence, so it already handles bi-weekly correctly and costs one cheap calendar check on off-weeks.

Fixed two stale references in `Workflows/agenda-note.md` that still described the sync as "the Tuesday 4pm Connor–Derek weekly" — the same class of drift that put the old job a day off its own meeting. Also relabelled the agenda's opening recap from "Since last week" to "Since last time": the workflow already correctly scoped it to *the prior meeting of this series* rather than a fixed 7-day window, but on a bi-weekly cadence the old label would have implied dropping half the period.

Note: this records that the cadence is settled *in fact* (recurring invite accepted, confirmed to Claude). It does not record that Connor has sent Derek an explicit reply, which was the original 2026-09-08 caveat.
