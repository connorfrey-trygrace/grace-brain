---
type: changelog
date: 2026-09-09
tier: 2
touches: ["[[Workflows/text-message-sync]]"]
trigger: "Connor, 2026-09-09 — caught a hallucinated attribution in the quick-refresh report: \"I'm the one who texted Jeff, not vice versa - that is a concerning hallucination.\""
---
# Text-scan findings now require a rowid on every attribution claim, verified before being written down

## What happened

During the 2026-09-09 quick refresh, the Phase 1 text-scan subagent reported that Jeff Brady had texted Connor asking to touch base about that night's Boot Camp leaders meeting. The scan's own output for that row read `[193103] chat225 +12024650816 ME 2026-09-09 11:55 :: '...'` — `ME` means Connor sent it. The subagent's prose inverted the direction: three earlier rows in the same finding fit a pattern ("people separately checking in with Connor about tonight"), and this row got folded into that pattern instead of read on its own terms. The parent agent then wrote the inverted claim into `/Trackers/Actions/Connor - Line up who receives tonight's 9-9 Boot Camp dinner delivery.md` and reported it to Connor as fact. Nothing in the pipeline checked it — the retrieval was correct and unambiguous; the summarization silently flipped a fact, and it survived until Connor caught it from personal knowledge.

Re-running `query-messages.py verify` on the cited rowid confirmed the correction in under a minute — the fix was never expensive, it just never ran.

## Why the existing rules did not prevent it

This file's Sky-exclusion and clock-marker fixes both establish the same lesson (see [[Changelog/2026-08-28-messages-exclusion-enforced-in-code]], [[Changelog/2026-08-21-clock-enforced-in-code]]): a prose reminder to "be careful" or "double-check" only ever covers the last failure mode discovered, not the next one. This is that lesson applied to a third surface — not chat.db access, not timestamps, but attribution of who-said-what in a summarized finding. `query-messages.py verify` already existed for exactly this ("let me just check that myself" needs a guarded path) but nothing required anyone to actually call it before a directional claim was committed to a permanent note.

## What changed

[[Workflows/text-message-sync]] gained a new **Step 4.5**, sitting between filtering for relevance and folding findings into trackers:

- Any finding describing who **initiated, asked, offered, confirmed, or committed** to something must cite its rowid(s) inline, next to the claim — not only in a trailing per-finding `[Source: ...]` line.
- Direction gets stated as the scan literally shows it (`ME`/`THEM`) before being translated into names, rather than composing the sentence first and backfilling direction from the narrative already built.
- Before such a claim is written into a tracker note or reported to Connor as fact, whoever is about to commit it — subagent or parent — runs `query-messages.py verify --rowids <N>` and confirms the row matches the claim.

Content/topic summaries ("Callie asked about a billing code") are explicitly exempted — this applies only to claims about who did what to whom, which is both the class summarization is most likely to invert and the class Connor is most likely to act on directly (whose court the ball is in).

## Files

- `Workflows/text-message-sync.md` — new § Step 4.5
- `Trackers/Actions/Connor - Line up who receives tonight's 9-9 Boot Camp dinner delivery.md` — corrected in place, rowid cited
