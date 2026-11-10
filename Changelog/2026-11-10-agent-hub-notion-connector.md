# 2026-11-10 — Agent Hub visit: Notion connector shortcuts

**Changed:** [[Workflows/grace-quick-refresh]] Phase 4 now names the Grace Tasks data source and the "Connor changed" view, and says to set `Agent synced` in the same update as any edit.

**Why:** Connor asked that Hub visits use the Notion connector instead of Chrome (it connected this session). Chrome visits ran 7–9 min, mostly UI clicking; the date picker's per-row UTC/EST timezone also made `Agent synced` easy to set wrong, which flags the agent's own edit as a Connor change. Through the connector it's a single property write.

**Follow-up (same day):** Phase 4 shortcut now says views/fetch only, never SQL or `rows` queries — matching the 5am routine's own safety rule (shared hourly quota). Connor attached the Notion connector to the 5am routine; [[Trackers/Automation]] updated.
