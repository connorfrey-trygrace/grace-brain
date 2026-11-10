---
date: 2026-08-17
file: "[[Workflows/text-message-sync]]"
type: defect-fix
---

# chat.db WAL under-read — `immutable=1` silently drops the newest messages

**What changed:** [[Workflows/text-message-sync]] § Source & access, step 2. The rule *"Open read-only, do not copy — `sqlite3.connect("file:<path>?immutable=1", uri=True)`"* is retired and replaced with: copy `chat.db` + `chat.db-wal` + `chat.db-shm` to a temp dir and open the copy **without** `immutable=1`.

**Why.** `immutable=1` is a promise to SQLite that the file cannot change, so SQLite skips the write-ahead log. Everything Messages.app has committed to `chat.db-wal` but not yet checkpointed into `chat.db` is therefore **invisible** — and on an incremental scan whose window ends *now*, the un-checkpointed tail is precisely the set of messages the scan exists to catch. The failure is silent: the query succeeds, returns rows, and reports a max ROWID that looks like the end of the window.

**Measured, same database, same instant (2026-08-17 quick refresh):**

| open | max ROWID | rows |
|---|---|---|
| `immutable=1` on the live file | 191673 | 191,544 |
| copy incl. `-wal`/`-shm`, no `immutable` | **191676** | **191,547** |

**3 messages invisible — and both of that run's substantive findings were among them:** Brian Sulc's security confirmation for the 9/20 launch (ROWID 191674/191675) and Connor's callback ask to Michael Vacca on question screening (191676). A scan that missed them would have left the Launch note's Security row at 🟡 pending and the Vacca item reading *"the ask itself is still unmade"* — both wrong, with nothing anywhere to indicate it.

**The original justification wasn't false, it was answering the wrong question.** The 2026-08-12 measurement (copy 2.38s vs immutable open 0.01s) is real; today's copy of a ~350 MB DB took ~5s. **Correctness is not tradeable against 5 seconds.** The "copying risks the database Messages is actively writing" concern is also backwards: copying is the *safe* operation — it is opening the live DB read-write that would be risky, and that is still forbidden.

**Prior history.** The same symptom was reported on the 2026-08-17 14:57 `grace-weekly-refresh` run, which found John Slye's 2:50 PM message missing from its own window, correctly diagnosed the cause, and closed with *"Not changed unilaterally."* That was the second occurrence. Per the standing rule that a **repeat failure gets code and a measurement, not an edit to procedure prose**, this run measured it directly rather than re-arguing it, and the fix landed on the measurement.

**Copy all three files.** A `-wal` without its `-shm` may fail to replay.
