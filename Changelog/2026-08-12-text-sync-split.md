---
type: changelog
date: 2026-08-12
tier: 2
touches: ["[[Workflows/text-message-sync]]", "[[Workflows/text-message-sync-reference]]"]
trigger: "Connor"
---
# text-message-sync split into run procedure + reference

After the Open Actions split it was the largest procedure file read on every run at 21.1 KB — bigger than the Open Actions core. Two sections were 40% of it and neither was operational: `## Source & access` (1.9 KB, mostly the history of three wrong mount paths) and `## Step 3: Resolve contacts to names` + Step 3.5 (8.2 KB, mostly the source-authority spec behind a script that already implements it).

Both moved to **[[Workflows/text-message-sync-reference]]** (10.7 KB, read only when a mount fails in a new way or a resolution is contested). The run procedure keeps a three-line operational version of each: glob the mount and verify `chat.db` inside it, open with `file:…?immutable=1` rather than copying (measured 2.38s → 0.01s), never touch `Attachments`; and for resolution, run `resolve-phone.py` and act on its three verdicts.

**21.1 KB → 14.0 KB.** Exclusions, privacy rules, Steps 1–2 and 4–8, the `## Last scan` marker and the Run Log pointer all stay in the run procedure untouched.
