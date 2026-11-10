# Project Migration Guide — Grace Event Coordinator Second Brain

Purpose: move this project off the empty `~/Documents/Vaults/Obsidian Vault 1` anchor folder onto a new project anchored on the Dropbox vault, without losing scheduled tasks, context, or memory.

Created during migration on 2026-06-25. **This `_Migration/` folder is temporary — remove it (move to /Archive) once the migration is verified.**

---

## What carries over automatically (no action needed)

- **Vault content** — CLAUDE.md, /Workflows, /Trackers, /Events, /Synthesis, /Agendas, /Contacts, /Archive, /Raw From Grace, /Transcripts. All live in *this* Dropbox vault, so they're present the moment the new project mounts this folder.
- **Scheduled tasks (all 6)** — stored at the user level (`~/Claude/Scheduled/`), not inside the project. They keep firing regardless of the project move. **Do NOT recreate them — that would double them up.** Inventory below for verification only.

## What must be redone manually (no tools exist for these)

1. Create a new project anchored on the **Dropbox vault**: `~/Library/CloudStorage/Dropbox/Vaults/Obsidian Vault 1`
2. Add context folders: **Office** (`~/Library/CloudStorage/Dropbox/Office`) and **Messages** (`~/Library/Messages`).
   - Do NOT add the empty `~/Documents/Vaults/Obsidian Vault 1`.
3. Paste the project **Instructions** (verbatim text below).

## What Claude rebuilds programmatically (from inside the new project)

- **Memory** — 16 files. Source (old space): `~/Library/Application Support/Claude/local-agent-mode-sessions/02c16a78-7791-40ca-8084-777229f3181f/af639598-a375-45b2-b935-4e37aac411b4/spaces/f3196d58-f9f7-4cc8-804e-2c48ee561641/memory/`. Backup copy: `_Migration/memory-backup.md` (this folder).

---

## Project Instructions (paste verbatim)

```
You manage a transcript-synthesis and event-coordination second brain in this Obsidian vault. The authoritative spec is /CLAUDE.md in the vault — always follow it. Before any task, check /Workflows for an applicable procedure and follow it if one exists. Be direct, structured, low-fluff. Report what you did and found, not what you're about to do. Never delete files (move to /Archive); never modify /Raw From Grace; ask before merging, archiving, or destructive changes.
```

---

## Scheduled task inventory (verify all 6 still present — do NOT recreate)

| Task ID | Schedule | Cron |
|---|---|---|
| weekly-synthesis | Fri 4:09 PM | `0 16 * * 5` |
| daily-stale-sweep | Mon–Fri 5:32 PM | `30 17 * * 1-5` |
| m365-to-obsidian-sync | 8am/12pm/4pm daily | `0 8,12,16 * * *` |
| daily-finance-scan | 6:04 AM daily | `0 6 * * *` |
| event-checklist-autocopy | 7:02 AM daily | `0 7 * * *` |
| grace-text-scan-hourly | hourly | `0 * * * *` |

Note: `daily-finance-scan` targets a *different* vault (`~/Claude/Projects/Personal Finance`, via Gmail/Google Calendar) — it is not Grace-specific and just appears in the same global task list.

Verification check for `grace-text-scan-hourly`: it needs the **Messages** folder mounted at run time to read `chat.db`. Confirm it ran successfully after migration (check `lastRunAt`).

---

## Post-migration steps (Claude, in new project)

1. Rebuild the 16 memory files into the new project's memory dir + regenerate MEMORY.md.
2. `list_scheduled_tasks` → confirm all 6 present and `lastRunAt` is recent.
3. Spot-check vault content is readable (CLAUDE.md, /Trackers/Open Actions.md).
4. Report. Then archive the old project (last).
