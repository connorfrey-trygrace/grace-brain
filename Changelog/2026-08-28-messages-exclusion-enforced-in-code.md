---
date: 2026-08-28
area: text-message-sync
---

# The chat.db exclusion moved from prose into the only code path that reaches the data

## What happened

During the 2026-08-28 15:49 ET quick refresh, the Phase 1 text-scan subagent applied the Sky 1:1 exclusion correctly, at SQL level, as the workflow requires. The parent agent then ran **its own verification query** against `chat.db` to check the subagent's decoding — with no exclusion — and decoded **6 messages from the excluded 1:1 thread**. Nothing was recorded in the vault, and the temp copy was deleted; reading it is the breach.

Connor: *"Add a guard to the double check. This should never happen, that is a breach of privacy."*

## Why the existing rule did not prevent it

The exclusion had been prose since the workflow was written, and had **already been strengthened in prose once**, on 2026-08-17, after a probe query returned excluded bodies. That strengthening named the probe: *"this applies to every query against chat.db, including the cheap 'is anything new?' count/probe query."*

It did not name a verification pass, because nobody had failed that way yet. **That is the structural problem with the prose approach: each rule names the last failure.** The 8/28 defect is the same class as the 8/17 one — a query that does not feel like "the scan" — reached by a different route.

## The fix

`Workflows/query-messages.py` is now the only sanctioned reader of `chat.db`. Four subcommands — `probe`, `scan`, `verify`, `self-test` — and **no subcommand that accepts arbitrary SQL**. The exclusion list lives in one constant and is applied by every path before a body is decoded. `verify` exists specifically so that *"let me just check that myself"* has a guarded path to take, since that is the move that caused this.

`self-test` measures the guard rather than asserting it: it reports how many messages exist in the excluded thread versus how many come back through the guard, and it checks the opposite failure too.

## The bug the self-test caught immediately

The first version excluded **89 chats instead of 1**. It put the handle match in the `WHERE` and the "is this a 1:1?" count in a `HAVING`, so the count only ever saw the one filtered row and **every group chat containing Sky came back as a 1:1**. That would have silently dropped Grace group threads the workflow explicitly puts in scope.

**Over-exclusion is data loss, not a safe direction to err in** — and it is invisible, because a scan that returns fewer messages looks like a quiet week. The self-test now checks both directions and both were verified on real data: 1 thread excluded, 26,727 messages in it, 0 returned; group chat 9 (which includes the excluded handle) still in scope.

## Files

- new: `Workflows/query-messages.py`
- `Workflows/text-message-sync.md` — § Exclusions rewritten to point at the script; the two prose paragraphs it replaces are described, not restored
- `Workflows/grace-quick-refresh.md` — Phase 1 text scan runs `self-test` first
