# Weekly Synthesis
Procedure for generating the weekly cross-meeting synthesis. Triggered every Friday afternoon via schedule, or on explicit request.
## Output location
/Synthesis/Weekly YYYY-MM-DD.md where the date is the Friday it runs. Create /Synthesis/ if it doesn't exist.
## Step 1: Identify scope
Find all transcripts in /Transcripts/ that:
- Have the "processed" tag
- Were processed within the past 7 days — use the `processed_date` frontmatter field as the primary source; fall back to file modification time only if `processed_date` is absent
If no transcripts qualify, still produce the synthesis — cover only the aging report and cross-event progress, and note in the executive summary that no new transcripts were processed this week.
## Step 2: Read source materials
For each in-scope transcript, read the YAML frontmatter (summary, action_items, speakers, event, tags). Read the body only when needed for deeper context — frontmatter is usually sufficient.
Also read the Open Actions tracker for aging info and cross-references — since the 2026-07-21 migration this is the per-action notes in /Trackers/Actions/ (aggregated by the views in /Trackers/Open Actions.base), not the retired single /Trackers/Open Actions.md file (archived).
## Step 3: Generate the synthesis with these sections
### Header
- Title: "Weekly Synthesis — {Friday's date}"
- Period covered: {previous Friday}-{this Friday}
- Transcripts included: count and list with `[[file]]` links
### Executive summary (3-5 sentences)
Lead with what was most consequential this week — biggest decision, biggest risk surfaced, or biggest progress made. Same quality bar as transcript summaries: specific people, decisions, dollars, dates.
### Themes & patterns
What recurred across multiple meetings? What tensions or contradictions appeared? What's trending?
Quality bar: each theme must reference at least 2 transcripts with file links. Single-meeting topics don't qualify as themes.
### Decisions made + open questions
- Decisions made: concrete outcomes with file links
- Open questions: raised but unresolved, with file links
### Action items aging report
From the /Trackers/Actions/ notes (views in /Trackers/Open Actions.base):
- New items added this week (count + brief list) — `added` within the period
- Items moved to Completed this week (count + brief list) — `status: completed` with `resolved` within the period
- Items currently flagged for review (count + full list with the `flagged` reason) — the "Flagged / Needs Review" view; this is the post-migration equivalent of the old "Stale" list
- Items In Progress (count + brief status) — `status: in-progress`
### Cross-event progress
Group by event tag. For each event referenced this week:
- Brief status
- What progressed
- What's blocking
- Time-sensitive concerns
Quality bar: only include events actually discussed this week, not every event in the system.
### Observations
Same proactive pattern as transcript synthesis. Surface only when actionable:
- Workflow gaps revealed this week
- Cross-system insights
- Suggested follow-ups
- Proposed workflow changes (per Tier 2/3 in maintenance rules)
If nothing actionable: "No observations this week."
### System health check
Three duties, appended here as one short subsection. **This job is the system's only scheduled watchdog** — the duties in 2 and 3 moved here on 2026-09-16, when `grace-weekly-refresh` (which used to carry them) was retired. If this run skips them, nothing else catches the gap.

1. **Light system audit** — per [[Workflows/system-audit]]. Auto-fix Tier-1 issues (note them); flag Tier-2/3 for Connor. Keep it lean: a consistency sweep, not a second report.
2. **m365 Run Log health check** — per [[Workflows/m365-run-log-health-check]], against [[Logs/m365-sync-run-log]].
3. **Scheduler heartbeat** — `list_scheduled_tasks`, comparing each task's `lastRunAt` against its cadence *and* against [[Trackers/Automation]]'s rows. Flag any job overdue by more than one full cycle, and any live-scheduler/inventory mismatch, as a flagged Active note per [[Workflows/Open-Actions-Tracker]]. Check for an existing flag on the same job first. Note the two-store split documented in [[Trackers/Automation]]: `~/.claude/scheduled-tasks/` is visible to this tool, `~/Claude/Scheduled/` is not and is out of scope — its absence from the listing is not a defect.

If all three are clean: "System health: no issues this week." **Always write the line** — an explicit clean result and a silent failure must not look the same.
## Step 4: Write to file
Save to /Synthesis/Weekly YYYY-MM-DD.md with YAML frontmatter:
- date: YYYY-MM-DD (Friday)
- period_start: YYYY-MM-DD (previous Friday)
- period_end: YYYY-MM-DD (this Friday)
- transcripts_count: N
- tags: [synthesis, weekly]
## Step 5: Report
After writing:
- File created (with link)
- N transcripts synthesized
- Brief preview of executive summary
- Observations needing Connor's attention
- System health check result (issues found + anything auto-fixed or flagged for Connor)
## Source of truth
Meeting summaries come exclusively from processed transcripts in /Transcripts/. Do NOT use calendar events, email, or any other source as a substitute. If no transcripts qualify for the week, follow the fallback in Step 1 (produce aging report + cross-event progress only; note absence of transcripts in the executive summary).

## Changelog

History lives in [[Changelog/_history/weekly-synthesis-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
