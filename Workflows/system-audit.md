# Workflow: System Audit (Second-Brain Health Check)

Keeps the vault and the AI deployment internally consistent so drift doesn't accumulate. Two modes:

- **Light** — runs weekly, folded into [[Workflows/weekly-synthesis]]. Fast, mostly mechanical. Auto-fixes Tier-1 issues, flags the rest, stays silent when clean.
- **Deep** — runs on explicit request (or if the light check keeps surfacing the same unresolved issue). Produces a standalone `System-Audit-YYYY-MM-DD.md` at the vault root, like the 2026-06-15 baseline.

## Guiding principle
The point is to keep the system lean, not to generate work. **Watch for accretion** — rules, trackers, and note types multiplying faster than they're used. Flag over-engineering as readily as you flag gaps. Silence is a valid, good result.

## Tier policy (applies to anything the check finds)
Follow the maintenance tiers in [[CLAUDE.md]]:
- **Tier 1 (typos, clarity, stale tracker rows, broken links, refreshing an index)** — fix directly, note it in the report, add a changelog entry to the affected file.
- **Tier 2 (new rule/field, changed threshold, relabeling)** — propose with a draft; don't apply without Connor.
- **Tier 3 (new workflow file, cross-workflow restructuring, the Project Instructions panel)** — propose only.
- If Connor declines a proposal, record it so it isn't re-proposed.

## Light check (weekly)
Run these quickly; report only anomalies (name the specific file/line/item — generic notes add noise):

1. **Instruction-surface consistency** — does the Project Instructions panel still match `/CLAUDE.md`? Do CLAUDE.md's FOLDERS and JOBS still match the actual folders and workflows present? (The panel can't be edited from here — flag for Connor.)
2. **Broken wikilinks** — scan `.md` files for `[[links]]` whose target file is missing (ignore illustrative placeholders like `[[link]]`, `[[file]]`). Fix or flag.
3. **Filename ↔ frontmatter drift** — event-note filenames must match their `date`; flag any mismatch (rename is ask-first).
4. **Vocabulary drift** — tracker section names and status values match their workflows' defined sets (e.g. Open Actions = Active / In Progress / Stale / Completed).
5. **Tracker freshness** — `/Trackers/Events.md` lists every live event note (+ planners); no event marked settled that's actually pending.
6. **Schema adherence** — recently processed transcripts have the required frontmatter fields; `date` reflects the meeting date, not the processing date.
7. **Name consistency** — same person spelled the same way across transcripts/contacts (watch transcription variants).
8. **Orphans & accretion** — new note types or trackers with no governing workflow; workflows or rules that no longer earn their keep.
9. **Watcher check** (added 2026-07-16, advisory-board audit; re-scoped 2026-07-24, and again 2026-09-16 after `grace-weekly-refresh` was retired) — the watchdog duties now live in `weekly-synthesis` itself (see [[Workflows/weekly-synthesis]] § System health check), which is also the job running this light check. That is circular by construction, so the check has to be the one thing this job can verify about itself plus one thing it can verify about everything else:
   - **Receipt check:** confirm last Friday's `/Synthesis/Weekly YYYY-MM-DD.md` note exists. A missing note is the signature of a run that didn't fire — the 2026-09-11 gap was found this way, three days late, by accident.
   - **Heartbeat:** `list_scheduled_tasks` — confirm every Grace job's `lastRunAt` is within one full cycle and matches [[Trackers/Automation]]'s rows. (A job whose first scheduled fire hasn't occurred yet has no `lastRunAt`; that's expected, check `nextRunAt` instead.)

   Because this check cannot catch its own job dying, the durable backstop is the receipt itself: **if `/Synthesis/` has no note for a given Friday, that week's watchdog did not run** — that is the signal to check, and it's visible to Connor without any tooling.

Output: a short **## System Health Check** subsection appended to the weekly synthesis note. If nothing actionable: "System health: no issues this week."

## Deep check (on request)
Run the full light list plus: read every workflow end-to-end for internal contradictions; verify changelog discipline; check `/Contacts` for stale/duplicate entries and credential exposure; review whether the tier/maintenance rules are being followed; assess overall complexity vs. usage. Write the standalone dated audit doc with prioritized, tiered, drafted changes and a clear "needs Connor" list.

## Changelog

History lives in [[Changelog/_history/system-audit-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
