---
type: changelog
date: 2026-11-12
tier: 2
touches: ["[[Workflows/actions-index.py]]", "[[Workflows/grace-quick-refresh]]", "[[Workflows/text-message-sync]]", "[[Workflows/m365-to-obsidian-sync]]", "[[Workflows/Open-Actions-Tracker]]"]
trigger: "Connor"
---
# Off-calendar calls get a `meeting:` field and always lead Start Here

The 11/12 quick refresh omitted John Slye's Fri 11/13 call (agreed by text, 3 PM proposed and unconfirmed): the item was `waiting-on`, so `--brief` suppressed it, and the call wasn't on Outlook, so Calendar-Window and `next w/` pointed at the 11/17 All Staff. Fix in code: new `meeting:` frontmatter field; `actions-index.py --brief` prints an **[@] Conversations** section (next 3 days, any live status, bypasses the waiting-on suppression), backstopped by a scan of `waiting_on` text for near M/D dates; `next w/` prefers the field when it comes first. Syncs now set the field whenever a call is agreed or proposed; the refresh report lists every [@] row first.
