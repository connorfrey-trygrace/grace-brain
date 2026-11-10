---
name: "🤖 Connor: Investigate suspected missed m365-to-obsidian-sync run (7/15 ~8 AM slot)"
status: completed
owner: "Connor"
resolved: 2026-07-21
source: "[[Workflows/m365-to-obsidian-sync]] Run Log health check, 2026-07-17 daily-stale-sweep"
source_line: 531
---

# 🤖 Connor: Investigate suspected missed m365-to-obsidian-sync run (7/15 ~8 AM slot)

- **Source**: [[Workflows/m365-to-obsidian-sync]] Run Log health check, 2026-07-17 daily-stale-sweep
- **Resolved**: 2026-07-21 — **Connor confirmed closed.** Run Log showed only 2 of 3 expected 7/15 entries (no ~8 AM entry), same silent-death-before-logging pattern as 7/8/7/12/7/16, with the same self-healing next-window-absorbs-the-gap logic. Connor closed the investigation 2026-07-21 without requesting the Outlook spot-check.
- **Notes**: none
- **Blocked by**: none (was none)
