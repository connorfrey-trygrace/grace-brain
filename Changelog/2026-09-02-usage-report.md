---
type: changelog
date: 2026-09-02
tier: 1
touches: ["[[Workflows/grace-quick-refresh]]", "[[Workflows/grace-weekly-refresh]]", "[[Logs/refresh-run-log]]"]
trigger: "Connor"
---
# Token usage now logged per refresh run, alongside elapsed time

Connor asked whether refresh runs are tracked for time and tokens. Elapsed wall-clock already was (`stamp.py log`, added 2026-08-11). Tokens were not — the only place "tokens" appeared anywhere in the vault was a design-rationale aside in [[Workflows/Open-Actions-Tracker]], not an actual logged number.

New: `Workflows/usage-report.py`. Reads the running Claude Code session's own local JSONL transcript (`~/.claude/projects/<slug>/<session-id>.jsonl`) — every assistant turn already carries a full `usage` block (input/output/cache tokens, model, timestamp), so this needed no new setup, no API key, no connector. Given `--session-id`, `--since` and `--until` (the same `date '+%s'` phase-boundary stamps `elapsed Xm` already requires), it prints one line: total tokens for the window, plus the peak single-turn context size as a % of that model's context window (a snapshot, not a sum — the "how full did the conversation get" number).

Wired into Phase 4 of both `grace-quick-refresh` and `grace-weekly-refresh` (including the weekly job's scheduled-task safety-kernel prompt, kept in sync per that file's own rule), folded into the same `refresh-run-log` line `elapsed`/`wrote` already land in. Zero ongoing intervention from Connor — same guarantee as elapsed time, because it's a mandatory step in a procedure the agent already follows every run, not something he has to trigger.

**Scoped down from Connor's first ask, on his own instruction:** no dollar cost, no Anthropic Console/Admin API — just token counts and % of context window, which is fully local. Cost tracking would need an admin-scoped API key (one-time setup, likely Derek's to provision) and was explicitly dropped as out of scope for this pass.

**What it doesn't measure:** only Claude Code sessions on this machine — another device or the raw API is invisible to it. And every number in the script's per-model context-window table is an unverified guess (200k default), not pulled from real docs — this was proven wrong for `claude-sonnet-5` on the very first live run: a single turn in *this* session hit 281k tokens, which a completed API call cannot do if the window really were 200k. The script now self-corrects — when an observed peak exceeds the table, it reports the peak as a floor and flags the table entry as disproved rather than printing a false-precision percentage. Table raised to 1M for `claude-sonnet-5` on the same evidence; still not confirmed against current docs.
