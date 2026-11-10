# Workflow: Boot Camp Attendance

Weekly tally of Boot Camp (Wed night men's small groups) attendance from the table leaders' replies in the **Boot Camp leaders group text** (chat2557). Tracker: [[Events/2026-09-16-Boot-Camp-Fall-Relaunch/2026-09-16-Boot-Camp-Attendance]].

Run when Connor asks ("log boot camp attendance"), or fold into [[Workflows/grace-quick-refresh]] Phase 1 whenever the text scan shows new chat2557 messages.

## Steps

1. Read the tracker's `last_synced_rowid`. Scan through the sanctioned path only: `python3 "Workflows/query-messages.py" scan --since-rowid <N>`, then filter to `chat2557`.
2. Find Connor's weekly ask ("share your attendance numbers") and the replies after it, until the next week's ask.
3. Resolve each sender with `python3 "Workflows/resolve-phone.py"` — the sender identifies which table is reporting.
4. Normalize to **total at the table, leaders included**. "X + us 2" / "+ 2 leaders" → add. "N total" → as-is. Bare "N guys" → record N, add an ⚠️ line noting it could exclude leaders. Never guess past that.
5. Fill the by-table column and the weekly total row (tables reported, total, range if ⚠️ rows exist). New table → new row. Table missing a report → leave blank, don't carry last week's number.
6. Update `last_synced_rowid`. Report to Connor: week total, tables not yet reported, any ⚠️.
7. Refresh the dashboard (https://claude.ai/artifact/SH567LJnJmxqxFsnM6WdGS): rebuild its CSV (`week,date,table,count`, one row per reporting table, counts as in the By-table grid), upload it as an asset to that artifact, then `update` the `datasets/attendance` doc's `source.url` and `updated`. Leave unreported tables out — no zero rows.
