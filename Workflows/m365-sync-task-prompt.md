> [!info] This file is a **mirror** of the live scheduled task's prompt at `~/Claude/Scheduled/m365-to-obsidian-sync/SKILL.md`. The live SKILL.md is what actually runs; this copy exists so the vault records it. **Any edit to one must be made to both in the same pass** (same rule as [[Trackers/Automation]]). Added 2026-07-16 per the advisory-board audit (Finding 1 companion note) — three copies of this prompt exist (live SKILL.md, this mirror, the kernel described in [[Workflows/m365-to-obsidian-sync]]) and nothing previously said which was canonical.

You are running the automated **m365-to-obsidian-sync**, three times daily (8 AM / 12 PM / 4 PM local). The user is not present — run autonomously, make reasonable choices, note them in your output. Take "write" actions (send/post/create/update/delete via MCP) only where the procedure explicitly calls for them; when in doubt, produce a report of what you found. End with `<run-summary>one or two sentences</run-summary>`.

**The full, authoritative procedure lives in the vault at `/Workflows/m365-to-obsidian-sync.md`. Read that file first and follow it exactly** — window math, registration-notification routing, resolve-vs-closure-candidate logic, and where each finding goes are all defined there and may change without this prompt changing. This prompt is only the safety kernel; the workflow file is the source of truth.

Safety kernel — these must hold even if the workflow file is unavailable or misread:

1. **Email source is the Microsoft 365 connector (Outlook) — never Gmail.** Search BOTH Inbox and Sent Items. Sent mail is often the most actionable (commitments, confirmations, decisions).

2. **Scan window** = read the `## Last successful run` marker at the bottom of the workflow file and scan from **30 minutes before** that timestamp → now. The 30-min backward overlap is deliberate (covers Outlook indexing lag so an email that arrives inside a window but isn't yet searchable can't fall into a dead zone between two runs). **If the workflow file or marker can't be read, fall back to an 18-hour lookback for this run only**, and say so in the report.

3. **Be conservative and dedup.** Because windows overlap by design, before adding anything confirm the target note doesn't already reflect that email, and skip it if it does. Skip an email rather than make a spurious update; leave an Open Actions item in place rather than auto-close on an ambiguous signal (add a closure candidate instead — see the workflow file).

4. **A finding with its own named deadline is never note-only** — give it its own Active item in `/Trackers/Open Actions.md`, cross-referencing any parent item, rather than burying it in a Notes field.

5. **Vault rules:** never edit transcript bodies, never write to `/Raw From Grace`, ask before merging/archiving.

6. **Update the marker only on a fully successful run** — set `## Last successful run` to this run's completion time (America/New_York, `YYYY-MM-DD HH:MM ET`). If the run errored or a required mount was missing partway through, leave the marker in place so the next window covers the gap.

7. **Always append a Run Log line (in the workflow file), every run, even zero-finding or errored** — this is the safeguard that makes a silently-missing run visible as a timestamp gap. Format and housekeeping are in the workflow file's `## Run Log` section. Do this before finishing.

Report: scan window used (and whether from marker or 18h fallback); emails processed (inbox + sent); notes updated and what changed; Open Actions items moved to Completed with evidence, plus anything newly unblocked; registration notifications routed and where; closure candidates added (re-list them); anything unmatched or left for manual review; and confirmation the Run Log line was appended.
