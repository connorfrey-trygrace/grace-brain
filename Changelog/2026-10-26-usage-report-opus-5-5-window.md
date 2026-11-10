# 2026-10-26 — usage-report.py: context window for claude-opus-5-5

On the 10/26 quick refresh, a single turn peaked at 245k tokens. claude-opus-5-5 wasn't in `CONTEXT_WINDOWS`, so it fell to the 200k default and the script reported 123%. Added `claude-opus-5-5: 1_000_000`. This is the same corrected-guess tier as sonnet-5, not a documented value.
