# Text Sync — Activation Pending

**Status:** Set up, not yet live. Needs a fresh conversation to go active.

## What's done
- `~/Library/Messages` mounted to the project.
- Workflow written: [[Workflows/text-message-sync]] (on-demand scan → fold into trackers; additive only).
- Sky's 1:1 thread excluded at the query level (handle `9087980030`); group chats in scope.

## Why it's not live yet
This session's sandbox was initialized **before** the Messages folder was mounted, so my tools can't see `chat.db` in this conversation. New mounts only register in a **new session**.

## To activate
1. Start a **new conversation** in this project.
2. Say: **"scan my texts for Grace stuff."**
3. First run = full-history pass; Sky's private thread is skipped automatically.

## If the scan comes back empty
macOS is blocking `chat.db` — grant the **Claude app Full Disk Access** (System Settings → Privacy & Security → Full Disk Access), then rerun.

## Optional later
Register Messages as a source/job in `CLAUDE.md` once a scan or two has run cleanly (currently workflow-only, by choice).
