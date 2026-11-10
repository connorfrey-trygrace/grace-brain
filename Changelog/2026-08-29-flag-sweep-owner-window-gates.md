---
type: changelog
date: 2026-08-29
tier: 2
touches: ["[[Workflows/Open-Actions-Tracker]]"]
trigger: "Connor"
---
# Step 3 neglect sweep gains owner + window gates (no-action-no-raise, enforced)

The flag sweep previously flagged any quiet active item after checking only completion and `blocked_by` — nothing about *who owns it* or *whether its action window is open*. Result: items owned by other people (Derek/Heather's marketing/website; John Slye's launch broadcast text) were flagged to Connor as if he'd neglected them, and a not-yet-due item (John's 9/13–9/20 send window) was flagged before there was anything to do. Both violate the standing [[feedback_no_action_no_raise]] rule.

Added two checks before flagging in § Step 3:
- **Owner gate** — if `owner` isn't Connor and the note names no concrete Connor-side next action, don't flag; reclassify to `waiting-on` if Connor is awaiting a deliverable, else leave it. A flag means *Connor* neglected something.
- **Window gate** — if the action window hasn't opened (a stated future start date/range), don't flag; park `on-hold` with that date as the release trigger.

The owner gate alone would have stopped both false flags in the 2026-08-28 weekly synthesis (flagged count went 8 → 6 after clearing them by hand). Trigger: Connor, 2026-08-29 weekly-synthesis follow-up.
