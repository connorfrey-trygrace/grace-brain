---
date: 2026-08-14
tier: 1
trigger: weekly-synthesis light system audit (broken-wikilink check)
---

# Fixed two broken `[[People/...]]` links in live files

The light system audit found two live files still linking peripheral volunteers to standalone `People/` notes that don't exist. The vault convention for Good Noodles roster members is the piped form `[[People/Good Noodles|Name]]` (e.g. `[[People/Good Noodles|Sumay Lu]]`). Repointed both to match:

- `Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups.md` — `[[People/Sean Liesegang|Sean Liesegang]]` → `[[People/Good Noodles|Sean Liesegang]]`
- `Trackers/Actions/Connor - Capture observations + photos on the 711 NYC recon trip (for the Sunday Night launch).md` — `[[People/Emily Horneffer|Emily Horneffer]]` → `[[People/Good Noodles|Emily Horneffer]]`

Note: the 2026-08-09 System Health Check reported these two links as "no longer appear in any live file." That was inaccurate — both persisted in the piped `[[People/Name|Name]]` form, which the prior scan missed. Both are now genuinely resolved. Sean and Emily are both present as rows in `People/Good Noodles.md`.

Tier 1 (broken link fix).
