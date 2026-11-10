---
name: pco-flow-check
description: Check a Sunday Night PCO plan has every pillar and that items sit under the right header, and reorder blocks when asked. Use when Connor says "check the flow", "is the plan in order", "fix the order", or before the Wednesday-night handoff to Vacca.
disable-model-invocation: true
---

Pull the plan: `services_plan_items`, service type 1804248, `title, sequence, item_type, length`. Default plan = next Sunday.

**Pillars, always present:** Welcome, Host Transition (Announcements), Message, QOTN (the Q&A header), Peer Discussion — plus Worship. **The order is in flux.** Don't enforce one. Ask Connor for this week's order, or take the plan's current order as the baseline and only report gaps.

**Rules:**
- The scripture slide is always a part of the Message section. Flag it anywhere else.
- Flag blank or "New Item" rows, a missing pillar, and a Peer Discussion item with no slide pointer.
- **Never edit, rename or delete anything in Worship or Message.** Moving a whole block is the only change allowed, and only when Connor asked for it.

**Reorder (verified 2026-09-30, Connor allows PCO writes):** from a logged-in `services.planningcenteronline.com` tab, POST to `https://api.planningcenteronline.com/services/v2/service_types/1804248/plans/<plan>/item_reorder` with header `X-CSRF-Token` (from `meta[name=csrf-token]`) and body `{"data":{"type":"PlanItemReorder","attributes":{"sequence":[<every item id, in the new order>]}}}`. Returns 204. Send every id; moving a header means moving its items with it. `sequence` can't be set on a single item (422).

After any move: re-pull, confirm item count and that no title or description changed, then close the tab. Report one line per pillar and the moves made.
