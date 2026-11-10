---
type: changelog
date: 2026-08-12
tier: 2
touches: ["[[Workflows/actions-index.py]]"]
trigger: "Connor"
---
# actions-index.py emits evidence lines per candidate so the sweep stops opening bodies to re-clear known false positives

The index named candidates but not *why*, so Step 3 opened each candidate's full body to decide. It now prints, under each candidate, the relevant `rationale` bullet plus the newest dated entry (≤150 chars each). Most candidates clear or confirm on those two lines; bodies are read only when they don't. Runtime unchanged at ~20–60 ms.
