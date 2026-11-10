---
date: 2026-08-17
files:
  - "[[CLAUDE.md]]"
  - "[[Workflows/note-history-splitting]]"
  - "[[Workflows/split-note-log.py]]"
  - "[[Workflows/Open-Actions-Tracker]]"
  - "[[Workflows/event-planning-note]]"
  - "[[Workflows/actions-index.py]]"
type: convention
---

# Companion-log convention made universal + `/Trackers/Action-Logs/`

**What changed.** The pattern the vault had invented three times by hand is now a stated rule in [[CLAUDE.md]], a workflow ([[Workflows/note-history-splitting]]), and a tool (`Workflows/split-note-log.py`). Connor's call, this run: *"make it universal to mirror this structure across the whole vault."*

**The rule:** a note that is read on every run must not carry its own append-only history.

Prior instances, all hand-rolled: the 2026-08-11 event-note split (`<Event>-Log.md`, after Launch.md hit 93 KB / 78% history), and the 2026-08-12 workflow splits (run logs → `/Logs`, changelogs → `/Changelog`). Action notes were the one class still violating it — surfaced this run when the Kay note reached 21 KB and the report recommended a split rather than doing one.

**Applied to 4 action notes.** 69 KB → 22 KB live, 47 KB moved to logs. `OVERSIZED NOTES` is now empty for the first time.

| note | before | live after |
|---|---|---|
| Connor - Get Kay to create the Sunday Night service type + Rock↔PCO sync tags | 21 KB | **5.7 KB** |
| Connor - Build a reliable Sunday night core / second leader | 17 KB | 11 KB |
| Connor - Draft the Sunday night multi-week experimentation game plan | 15 KB | **5.2 KB** |
| Connor - Discuss the Sunday night feedback form with Kay and Derek | 15 KB | **5.7 KB** |

**Three decisions worth recording, because each rejected a tidier option:**

1. **Action logs live in `/Trackers/Action-Logs/`, not beside the note.** [[Trackers/Open Actions]]`.base` filters globally on `file.inFolder("Trackers/Actions")` and its `All` and `By Project` views carry **no status filter** — a log dropped in that folder becomes a blank row in the two views Connor reads most. A Bases exclusion (`type != "log"`) is tidier, but **a wrong filter expression blanks every view over 130 notes and cannot be tested from outside Obsidian.** The sibling folder is correct by construction: no filter, no `actions-index.py` change (its glob is `Trackers/Actions/*.md`), nothing to test. Event logs still sit beside their plan note — there is no Base over `/Events`.

2. **A script, not a procedure step.** Dated history in an action note is **interleaved** with live structural bullets — `- **Blocked by**:` and `- **Chase-by rationale**:` sit *after* dated entries in the Kay note — so the obvious hand method ("move everything below the fields") silently eats dependency edges from exactly the largest, most-linked notes. The classifier is the entire value of the file.

3. **Keep the 2 newest entries in the live note.** Not taste: `actions-index.py evidence()` emits the last 2 dated lines so a sweep can clear most candidates without opening the body at all. Keeping fewer breaks the cheap path the split exists to create.

**What deliberately does NOT split, and why the scan stayed narrow.** Being large is not the trigger; re-reading history for nothing is. Excluded: Phone-Index, Good Noodles, Automation.md and the volunteer-signups table (their bulk *is* current state), the Synthesis weeklies (they *are* the history), and the workflow files (already split; what remains is procedure, read in full on purpose).

⭐ **The 51 KB Launch note was checked and rejected as a candidate** — its residual `## 🗒️ Status update history` is only **1.7 KB**; the other 49 KB is live plan content. The 8/11 split already worked. **Recorded because the intuition "it's huge, split it" was wrong here, and the measurement is what caught it.**
