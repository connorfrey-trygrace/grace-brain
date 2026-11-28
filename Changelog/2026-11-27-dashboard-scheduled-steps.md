# 2026-11-27 — Dashboard: scheduled steps count as waiting

**Why:** Connor: "if my next task is a scheduled thing (like the 12/13 bible lab announcement), list the next thing that I can do now, or count that scheduled thing as a waiting on."

**Change:** `Workflows/dashboard.py` reads each live to-do's open checkboxes. A checkbox tagged `📅 YYYY-MM-DD` (future) is a scheduled occasion. Next action = first open checkbox without a future 📅 (shown in Dashboard.md as "next:" and in the artifact via a new `next` field in items.json; the artifact page shows `next` in place of the title). If every open step is scheduled, the item counts as waiting on "Sun 12/13 (scheduled)" and the date strip labels it "scheduled:". Artifact page edit: one `str_replace` in `files/index.html`.

**Tagged:** [[Trackers/Actions/Connor - Promote the January Bible teaching from the 12-13 morning stage]] (📅 2026-12-13). Convention noted in [[Workflows/grace-quick-refresh]] Phase 3a.
