---
type: changelog
date: 2026-08-12
tier: 2
touches: ["[[Workflows/m365-to-obsidian-sync]]", "[[Logs/m365-sync-run-log]]"]
trigger: "grace-quick-refresh, 2026-08-12 17:56 ET run"
---
# The m365 sync must query Sent Items with an explicit `folderName` and never with a bare `order`

Passing `order` to `outlook_email_search` without `folderName` silently scopes the search to Inbox. The 2026-08-12 12:24 ET run logged `inbox 0, sent 0` and asserted Sent Items was empty; Connor had in fact sent *"Counting Tech"* (9:38 AM ET) and *"Faith For Everyday Life schedule"* (10:44 AM ET) hours earlier, and both were only recovered by the 17:56 ET run because its window reached back past them. That same 12:24 log line had already diagnosed the defect for the all-folders leg and prescribed omitting `order` — but never applied it to the Sent leg, which is where it was dropping content, so the defect was documented and still live.

Fix: § Source & window now states the rule for both legs — Sent runs as `folderName: "Sent Items"`, the all-folders leg omits `order`. Whether the earlier `sent 0` windows (12:24 on 8/12, 13:44 on 8/11) need a backfill audit is Connor's call, tracked at [[Archive/Actions/Connor - Fix the m365 sync Sent Items scoping defect (bare order param)]].
