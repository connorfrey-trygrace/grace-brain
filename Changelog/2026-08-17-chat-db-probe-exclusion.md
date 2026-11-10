---
type: changelog
date: 2026-08-17
tier: 2
touches: ["[[Workflows/text-message-sync]]"]
trigger: "Excluded-thread bodies returned by a pre-scan probe query"
---
# The chat.db exclusion filter binds every query, including the cheap probe

## What happened

The 16:49 quick refresh ran a "is anything new since the marker?" probe against `chat.db` before deciding whether a full Phase 1 text pass was worth spawning — 13 minutes after the prior run, the expected answer was zero. The probe selected `ROWID, date, is_from_me, handle, substr(text,...)` for all rows above the marker. It did **not** carry the Sky 1:1 exclusion filter.

Two new messages existed. Both were in the excluded thread. Their bodies came back.

## Why the rule did not catch it

The Exclusions section says the filter is enforced "at the SQL level ... so their message bodies are never returned," and says it is applied "before any decode." Both statements describe **the scan**. The probe is not the scan — it runs *before* the decision to scan, produces no findings, and writes nothing, so it reads as out of scope. It is not out of scope: it is a SQL query against `chat.db` that returns message text, which is the exact thing the exclusion exists to prevent.

The short-window case makes it worse rather than better. On a 2-message window the excluded thread was not a minority of the result set that a later relevance filter would drop — it was 100% of it.

## The change

Added to [[Workflows/text-message-sync]] § Exclusions: the filter binds every query against `chat.db`, probe included. Filter at SQL level, or select no `text` column at all — a probe only needs a count and a max ROWID, so the cheapest correct form of it never touches `text`.

## What was not done

Nothing from the excluded thread was surfaced, quoted, recorded in a tracker, or carried into the run report. The marker still advanced to 191678 — the rows were scanned, and leaving the marker behind would only guarantee they are read again.
