---
type: changelog
date: 2026-08-12
tier: 2
touches: ["[[Trackers/Actions]]","[[Archive/Actions]]"]
trigger: "Connor"
---
# 94 completed action notes moved to /Archive/Actions; 174 wikilinks repointed

`/Trackers/Actions/` held 139 notes, **94 of them `status: completed`** (230 KB) — the folder only ever grew. Moved to `/Archive/Actions/` (nothing deleted), 127 link instances repointed across 35 live files plus 47 inside Archive itself. Live folder: 139 → 45 notes, 880 KB → 392 KB. Dangling-link check clean.

Note this was **hygiene, not a speed fix** — `actions-index.py` read all 139 in 47 ms. The gain is that sweeps, greps and the Bases views stop ranging over dead items.
