# Workflow: Note History Splitting (the companion-log convention)

**The rule, in one line: a note that is read on every run must not carry its own append-only history.**

This is vault-wide. It is not a new idea — the vault had already invented it three separate times, by hand, each time after the same failure. This file makes it a convention with a tool instead of a habit re-derived under pressure.

| date | what was split | out of | why |
|---|---|---|---|
| 2026-08-11 | `<Event>-Log.md` | event plan note | Launch.md was **93 KB, 78% history**; a sync re-read all of it to append one line |
| 2026-08-12 | `/Logs/<job>-run-log.md` | workflow file | procedure files are read **in full every run**; the log is never read |
| 2026-08-12 | `/Changelog/<date>-<slug>.md` | workflow files + CLAUDE.md | same reason; see [[Changelog/README]] |
| 2026-08-17 | `/Trackers/Action-Logs/<note>-Log.md` | action notes | the last class still violating the rule — Connor's call, this run |
| 2026-09-16 | `/Changelog/_history/Automation-changelog.md`, `/Changelog/_history/Events-changelog.md` | `Trackers/Automation.md`, `Trackers/Events.md` | 2026-09-15 deep audit (item F): both are read on every relevant check yet carried a growing inline `## Changelog` — the exact rule this file exists to enforce. Neither has the action-note's interleaved-fields problem (both had a clean, undecorated `## Changelog` heading with nothing live below it), so this was a manual move-to-`/Changelog/_history/` per the CLAUDE.md changelog precedent, not a `split-note-log.py` run — that script's classifier is scoped to action notes and event logs, not this pattern. |

## Why it matters (the actual cost)

Every sync — text, email, sweep — appends one or two lines to an action note. To append, it reads the whole file. A 21 KB note costs 21 KB of context to add 400 bytes. `actions-index.py` exists for exactly this reason at the *folder* level; this convention is the same fix at the *note* level. The `OVERSIZED NOTES` section of the index is the alarm; this workflow is the response.

## What splits, and what deliberately does not

**Split** — notes read on every run that accumulate dated history:

- `/Trackers/Actions/*.md` → `/Trackers/Action-Logs/<same name>-Log.md`
- `/Events/<event>/<plan note>.md` → `<same name>-Log.md`, beside it

**Do NOT split** — being large is not the trigger; *carrying history you re-read for nothing* is:

- **`/Contacts/Phone-Index.md` (28 KB), `/People/Good Noodles.md` (18 KB), `/Events/…/4th-Service-Volunteer-Signups.md` (33 KB)** — data caches, rosters and inventories. Their bulk **is** current state. Splitting them would move live data out of the note that is supposed to hold it. (`/Trackers/Automation.md` was listed here too until 2026-09-16 — re-inspection found its bulk had become a long prose changelog, not current-state data; see the table above. Its live tables — Active/Non-Grace scheduled tasks, Required mounts, Operating note — are still exactly this kind of data cache and still don't split.)
- **`/Synthesis/Weekly *.md`** — these *are* the history. There is nothing to move out.
- **`/Workflows/*.md`** — already split (run logs → `/Logs`, changelogs → `/Changelog`). What remains is procedure, and procedure is read in full on purpose.
- **`/Events/2026-09-20-…-Launch.md` (51 KB)** — checked 2026-08-17 and **it is not a candidate**: its residual `## 🗒️ Status update history` section is only **1.7 KB**. The other 49 KB is live plan content — logistics tables, run-of-show, open questions, action items. The 8/11 split already did its job. **A big event note is not automatically a split candidate; measure before assuming.**

## How to split

```
python3 "Workflows/split-note-log.py" --scan                  # candidates vault-wide
python3 "Workflows/split-note-log.py" --dry-run "<note.md>"   # show the plan first
python3 "Workflows/split-note-log.py" "<note.md>"             # write it
```

**Do not do this by hand.** The dated history in an action note is *interleaved* with live structural bullets — `- **Blocked by**:`, `- **Status**:`, `- **Chase-by rationale**:` sit *after* dated entries, not before them — so any "move everything below the last field" approach silently eats dependency edges and status. The classifier in the script exists for that one reason; a human doing it fast will get it wrong on exactly the notes that matter most (the big ones). **Kept current 2026-08-22:** when the value-carrying body bullets were replaced by `- **Priority rationale**:` / `- **Status history**:` ([[Workflows/Open-Actions-Reference]] § The body explains fields, never restates them), those names were added to the classifier's structural list — a renamed live field that isn't listed gets swept into the log as if it were history.

**The script keeps the 2 newest dated entries in the live note. That number is load-bearing, not taste:** `actions-index.py evidence()` emits the last 2 dated lines so a sweep can clear most candidates without opening the body at all. Keep fewer and you break the cheap path the split exists to create.

## Where action logs live, and why not beside the note

Action logs go in **`/Trackers/Action-Logs/`**, a sibling folder — *not* alongside the note the way event logs do.

The reason is [[Trackers/Open Actions]]`.base`: its global filter is `file.inFolder("Trackers/Actions")`, and its **`All` and `By Project` views carry no status filter**. Any file dropped in that folder becomes a blank row in the two views Connor reads most. Excluding logs with a Bases filter (`type != "log"`) would be tidier — but a wrong filter expression blanks *every* view over 130 notes, and Bases expressions cannot be tested from outside Obsidian. A sibling folder is correct by construction: no filter to get wrong, no `actions-index.py` change (its glob is `Trackers/Actions/*.md`), nothing to test. **Revisit only if the filter is ever verified in-app.**

Event logs stay beside their plan note — there is no Base over `/Events`, so the constraint doesn't exist there.

## Ordering divergence, stated on purpose

Event `-Log` files put **newest at the top**. Action `-Log` files are **oldest-first, append at the bottom**. This is deliberate: every writer of an action note already appends chronologically at the bottom, and flipping the order would guarantee mis-ordered appends by anyone following the existing habit. The split pattern is what is being mirrored, not the sort order.

## Standing duties

- **The sweep already owns detection.** `actions-index.py` prints `OVERSIZED NOTES` (>15 KB, live notes only) on every full run. When it names a note, split it — don't note it and move on, which is what happened on 2026-08-17 when the Kay note surfaced at 21 KB.
- **After splitting, the live note still owns current state.** Anything that changes status, a date, a dependency, or the do-now gets folded into the fields and bullets — never left only in the log.
- **Never read a `-Log` on a normal run.** Same standing rule as `/Logs` and `/Changelog`. Read one only when auditing or reconstructing how a decision was reached.
- **Never delete history to shrink a note.** The fix is always a move.
