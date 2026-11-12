---
type: changelog
date: 2026-11-11
tier: 2
touches: ["[[Workflows/grace-quick-refresh]]", "[[Trackers/Automation]]"]
trigger: "Connor"
---
# Quick refresh now triages the inbox for replies owed

The Phase 1 email subagent also scans the last 7 days of Inbox vs. Sent Items, drops threads Connor already answered, and returns the ones where a person is waiting on him. They appear in the report's Start Here as "Replies owed," with drafts offered on request. Report-only by Connor's choice: nothing in Outlook is moved, flagged, or sent (the M365 connector is search-only, and driving OWA through Chrome has deleted mail before). Lookback is fixed at 7 days, independent of the sync marker, because the sync window is too short to see a thread that's been sitting since Monday.
