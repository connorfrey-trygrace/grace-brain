---
type: changelog
date: 2026-09-16
tier: 2
touches: ["[[Trackers/Automation]]", "[[Events/2026-09-20-Sunday-Night-Service-Launch]]"]
trigger: "Connor — wanted weekly automation supporting the recurring evening service, launching 2026-09-20"
---
# Three Sunday Night readiness jobs deployed, split by lead time

The vault's automation was built around discrete one-off events; `event-checklist-autocopy` was retired 2026-08-29 precisely because Connor's events became recurring *services*. This is the recurring-service replacement.

**Split by lead time, not topic** — Connor's correction to a single Thursday check: *"Thursday is too late for volunteers, and too late for getting things into the slides for Vacca."*
- `snl-week-ahead` (Mon 9:06 AM) — plan runway ≥6 weeks, plus rosters **2–3 Sundays out**, because unfilled slots don't fill in six days.
- `snl-service-prep` (Mon 9:22 AM) — the coming Sunday's content, a day before the Tuesday cut for slides/lyrics.
- `snl-extend-plans` (**ad-hoc, no cron**) — drives PCO in a browser to bulk-create plans, gated on Connor's explicit yes before submitting.

**Scope was cut twice by Connor, both times correctly.** A post-service Monday metrics capture was dropped ("Rock takes care of that"), and a weekly QR re-point was dropped ("only ad hoc — we don't need to refresh the question link in theory"). Both would have been jobs solving nothing.

**Why the write isn't scheduled.** PCO's connector is read-only for Services (no create-plan tool; `pco_unsupported_request` is a telemetry stub), so plan creation needs the browser. Connor approved browser use in a scheduled task but flagged that permissions shouldn't be fully auto. An unattended run would either stall on a permission prompt or write unsupervised into shared church software — so detection is scheduled and the write is staged one click away, with `snl-week-ahead` naming the ad-hoc task when runway runs short.

**Found while building, all on the live 2026-09-20 plan:** QOTN still reads `"[Pending john]"`; neither worship medley has songs attached as PCO records (titles are typed into the description only, so nothing flows to slides); the scripture slide's NIV translation is unverified pending Michael Vacca; 55 unfilled positions against 14 confirmed people. Also `Sunday Night Services` (service type 1814753) is an empty duplicate of `Sunday Night` (1804248) and should be deleted — all three prompts are told to ignore it.

No `/Workflows` file yet, deliberately: the service hasn't run once, so there's no observed procedure to codify. Thin the prompts to pointers at a workflow file after a few real runs show what the checks actually catch.
