# 2026-11-13 — Grace Outlook calendar synced into Notion's Grace Calendar table

**What changed:** new procedure [[Workflows/grace-calendar-sync]]. Every run that can reach Outlook copies the next 14 days of Grace events into Notion's **Grace Calendar** (`collection://41812cb6-3a8b-8134-ad1d-000bafb14bc1`). It upserts by Outlook ID, ticks Cancelled instead of deleting, skips the Availability/FTJ self-blocks, and sets an Agent synced heartbeat on the next upcoming event.

Wired into:
- [[Workflows/grace-quick-refresh]] Phase 1, reusing its calendar pull
- Notion "Start here: Grace Claude" → Your things → Calendar, which the 5 AM cloud routine follows
- `agent-hub-visit-local` Step 2b (pre-change prompt copy in the session scratchpad)

The morning FYI's "Grace calendar, next 14 days" section now carries one line, "Synced HH:MM" or "Grace calendar unavailable", instead of the event list added earlier the same day ([[Changelog/2026-11-13-grace-calendar-in-morning-fyi]]).

**Why:** Agent Mail MSG-28 from Personal Claude. Connor is retiring the M365 connector from My Day too, so My Day and the planner need Grace events as data. Connor approved it in chat on 2026-11-13.

**First sync:** 2026-11-13 ~10 PM ET, 6 rows (11/13 John call → 11/23 Bi-weekly Sync).

**Location rule:** Zoom/Teams URLs are written as `Zoom`/`Teams`, because the meeting links carry passwords and the table feeds dashboards.
