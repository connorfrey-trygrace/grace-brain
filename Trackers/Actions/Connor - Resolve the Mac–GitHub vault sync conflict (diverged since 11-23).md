---
name: "🤖 Connor: Resolve the Mac–GitHub vault sync conflict (diverged since 11-23)"
status: active
priority: P1
owner: "Connor"
added: 2026-11-27
deadline: none
needs_by: none
last_mentioned: "2026-11-27"
flagged: "2026-11-27 — reason: scheduler heartbeat — cloud 5am routine output not reaching the Mac vault; vault-git-sync merge conflict every run since 2026-11-23"
source: "[[Workflows/weekly-synthesis]] scheduler heartbeat, 2026-11-27"
projects: []
people:
  - "[[People/Connor Frey]]"
blocked_by: []
blocks: []
---
# 🤖 Connor: Resolve the Mac–GitHub vault sync conflict (diverged since 11-23)

- [ ] Merge `origin/main` into the Mac vault by hand (resolve the 9 conflicting files), push, then merge or discard the three orphaned `cloud/` branches.

- **Status**: Open. The Mac vault and GitHub `main` have diverged. Local `main` is 21 commits ahead and 3 behind `origin/main` (merge base: "Mac auto-sync: 19 file(s)", 11/23 04:54). `Workflows/vault-git-sync.sh` hits a merge conflict on every run and aborts, so nothing has synced either way since 11/23. Latest entries in `~/Library/Logs/grace-brain-sync.log`: "CONFLICT with GitHub, merge aborted" (11/26 12:26 → 11/27 16:01, every run).
- **Conflicting files (9)**:
  - `Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Launch-Log.md`
  - `Logs/m365-sync-run-log.md`
  - `People/Good Noodles.md`
  - `Trackers/Actions/Connor - Invite Naomi Shoger (YP connect card) to Sunday Night.md`
  - `Trackers/Actions/Connor - Submit Sunday Night QR landing-page comms request every Tuesday.md`
  - `Trackers/Actions/Connor - Submit the 4 curiosity-dinner comms requests once Kay sends links.md`
  - `Trackers/Actions/Connor - Tell John Slye Emily Horneffer is off the Sunday Night core team.md`
  - `Trackers/Actions/Connor - Work out a Friendsgiving plug for Sunday Night.md`
  - `Workflows/m365-to-obsidian-sync.md`
- **Also unmerged**: cloud runs that hit conflicts pushed to `origin/cloud/2026-11-22-5am`, `cloud/2026-11-25-5am` and `cloud/2026-11-26-5am`. None of them is in `main`.
- **Effect**:
  - The cloud 5am routine (`trig_01FRTcmfLV86McxXg5h2Q16e`) fires daily and reports success (runs 11/22–11/27 all present), but none of its email folds since 11/21 reach the Mac vault. Example: GitHub closed "Tell John Slye Emily is off the core team" on 11/27; it's still active on the Mac.
  - The m365 `## Last successful run` marker now differs between the copies. The Mac's quick refresh and the cloud run will re-scan overlapping windows, which risks duplicate lines once merged.
  - The cloud run reads a 4-day-stale vault (it can't see Mac edits since 11/23).
- **Priority rationale**: silent data drift between the two writers. It grows with every run (2 cloud + several Mac commits a day) and gets harder to merge.
- **Notes**: `vault-git-sync.sh` is correctly refusing to auto-resolve (by design). This job did not attempt the merge: resolving conflicts is ask-first.
- **Blocked by**: none · **Blocks**: trusting any cloud-run output
