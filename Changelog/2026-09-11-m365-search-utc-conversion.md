---
name: 2026-09-11-m365-search-utc-conversion
---

# m365 email sync: outlook_email_search interprets bare timestamps as UTC, not ET

**What happened:** During the 15:07 ET quick-refresh's email-sync leg, the subagent passed this run's ET-labeled window (`"2026-09-11 13:45"` → `"2026-09-11 15:06"`) literally to `outlook_email_search`'s `afterDateTime`/`beforeDateTime`. The tool returned 4 emails from ~10:03–10:51 AM ET — mail from **before** the intended window, not after. Cross-checked with `date -u` vs `TZ=America/New_York date`, then independently verified by the parent session: a query for `afterDateTime: "2026-09-11 15:00"` / `beforeDateTime: "2026-09-11 16:00"` (bare, no zone marker) returned an email whose actual `receivedDateTime` was `2026-09-11T15:33:15Z` — i.e. the tool read `15:00`–`16:00` as UTC, not ET.

**Why it doesn't silently lose mail permanently:** the m365 marker only ever records a window-end; the next run computes its start from that same marker and applies the same (buggy) conversion, so the drift is internally consistent — each run's real coverage is consistently offset ~4h stale (during EDT) versus what the marker claims, not gapped. Recent mail just surfaces about 4 hours later than it otherwise would, once a later run's "now" catches up past it.

**Fix:** [[Workflows/m365-to-obsidian-sync]] §Source & window now instructs converting the ET window bound to UTC (`Z` suffix) before calling `outlook_email_search`, rather than passing the ET clock string directly.

**Not yet done:** no audit of how many past runs passed literal ET strings vs. already handled this correctly — the fix is forward-looking. If a past miss turns out to matter for a specific item, it would surface via the item's own later mention, not from this note.
