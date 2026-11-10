---
type: workflow
---
# Text Message Sync — Reference

Mount access detail, contact-resolution source authority, and the watchlist rules. Split out of [[Workflows/text-message-sync]] on **2026-08-12**.

**Not part of the standard read for a scan.** The run procedure carries the operational three-line version of each; come here when a mount fails in a new way or a resolution is genuinely contested.

---

## Source & access

- The source is the macOS Messages database, `chat.db`, inside the mounted `~/Library/Messages` folder. Messages writes live to `chat.db` plus its `-wal` / `-shm` sidecars.
- **Mount path (bash) — GLOB FOR IT. Do not hardcode the tail.** The mount name is **account-name-prefixed and is not stable**; both the `/sessions/<session>/` prefix *and* the `mnt/...Library--Messages/` tail vary between sessions and machines. **Procedure:** run `ls -d /sessions/*/mnt/*Library--Messages*`, then **verify `chat.db` actually exists inside the match** before proceeding. Existence of `chat.db` in the directory is the only reliable test — never the directory's name. ⚠️ **A `System--Library--Messages` match is the WRONG one:** it exposes `/System/Library/Messages` (app resources only — `PlugIns`, `iMessageApps`, `iMessageBalloons`, `iMessageEffects`) and contains **no `chat.db`**. Measured 2026-08-11: the glob returned exactly two matches — `mnt/connorfrey--Library--Messages/` (has `chat.db`) and `mnt/System--Library--Messages/` (does not). **Never hardcode a `/sessions/...` path and never treat a mount name as stable** — this section was wrong three times for doing so (2026-07-24, 2026-08-04, 2026-08-10/11); detail in [[Changelog/_history/text-message-sync-changelog]].
- The mount may require **Full Disk Access** for the Claude app (System Settings → Privacy & Security → Full Disk Access). If a scan reads as empty or permission-denied, that's the first thing to check.
- **Never open the live database in read/write mode.** Copy `chat.db` + `chat.db-wal` + `chat.db-shm` to a temp dir first, then open the copy. This avoids corrupting or locking the database Messages is actively using. ⚠️ **Do not open with `file:chat.db?immutable=1`** — see "The immutable=1 defect" below; that shortcut is retired.
- **Never touch the `Attachments` subfolder.** It can be many GB of photos/video and is out of scope. Read `chat.db` only.

## The immutable=1 defect (corrected 2026-08-17)

The prior rule here was "open read-only, do not copy," using SQLite's `immutable=1` URI flag, justified on speed (2.38s vs 0.01s to open). That was a silent under-read and is retired. `immutable=1` tells SQLite the file cannot change, so it **skips the write-ahead log entirely** — every message Messages.app has committed to `chat.db-wal` but not yet checkpointed into `chat.db` is invisible. On a window whose newest messages are minutes old, that is exactly the messages a fresh scan exists to catch.

**Measured 2026-08-17, same DB, same instant:** `immutable=1` → max ROWID **191673**, 191544 rows. WAL-replayed copy → max ROWID **191676**, 191547 rows. **3 messages missing, 2 of them the substantive findings of that run** (a security confirmation and a callback ask). The defect was first reported 2026-08-17 14:57 on the same symptom and left unfixed; this is the measurement that closed it.

The speed argument was never wrong, it was answering the wrong question — the copy is ~5s for a ~350 MB DB, and correctness is not tradeable against 5 seconds. Copy all three files; a `-wal` without its `-shm` may not replay.

## Note-to-self double-recording, worked example

The rule (main file, Step 3.9): collapse (timestamp, text) duplicates from the `973-699-0180` self-thread; don't report them as findings or re-sends. Why the duplicates happen, and what one looked like: Alexis Hendrickson's 8/19 Sour Patch Kid voice memo. ROWIDs **191824/191825** landed with NULL text (16:44 ET) and **191893/191894** carried the same 2,049-byte transcription at the same stamp. The 2026-08-21 11:58 run logged this as *"Duplicate surfacing, no write"* with no explanation. The explanation: Connor had pasted the transcription to himself so it would be readable, and the self-thread recorded it twice. Nothing was wrong, and the content was the point.

## Attribution-direction incident (2026-09-09)

The rule (main file, Step 4.5): cite the rowid inline next to any who-did-what-to-whom claim, state `ME`/`THEM` before translating to names, and verify before writing it down as fact. Why it's a checkable requirement and not a reminder: a quick-refresh subagent scanned 45 messages and reported, in prose, that Jeff Brady had texted Connor asking to touch base. The scan's own output for that row read `[193103] chat225 +12024650816 ME 2026-09-09 11:55 :: '...'` — `ME` means Connor sent it. The direction was unambiguous in the data and inverted in the sentence describing it: three earlier rows in the same finding fit a pattern ("people reaching out to Connor about tonight"), and the last row got folded into that pattern instead of read on its own terms. The retrieval was correct; the summarization silently flipped a fact. The parent agent then wrote the inverted claim into a permanent tracker note and reported it to Connor as fact, and it survived until Connor caught it from personal knowledge. See [[Changelog/2026-09-09-text-scan-attribution-verification]].

This is the same class of lesson as the exclusion-guard incident below: a prose reminder to "double-check attribution" would have been a third prose rule of exactly the kind that had already failed twice elsewhere in this file. The fix is a checkable requirement, not a virtue.

## Exclusion-guard incident (2026-08-28) and its self-test

The rule (main file, Exclusions section) lived here as prose from the start, and was strengthened in prose on 2026-08-17 after a probe query returned excluded bodies — *"this applies to every query, including the cheap probe."* On **2026-08-28 it failed again**, in the one place neither paragraph named: the refresh's subagent filtered correctly at SQL level, and then the parent agent ran **its own verification query to double-check the subagent** with no exclusion, and decoded 6 messages from the 1:1. Nothing was recorded — reading is the breach. A third prose rule would have been the third prose rule. Same lesson as [[Changelog/2026-08-21-clock-enforced-in-code]]: put it where omitting it is not an option. See [[Changelog/2026-08-28-messages-exclusion-enforced-in-code]].

⚠️ **The guard can fail in two directions and `self-test` measures both.** Its first version excluded 89 chats instead of 1 — every group thread containing the excluded person — because the 1:1 test counted only the matching handle row. Over-exclusion is data loss, not a safe direction to err in: it would have silently dropped Grace group threads this file explicitly puts in scope.


## Step 3: Resolve contacts to names

> 🛑 **Run the script. Do not hand-roll a grep.**
> ```
> python3 "Workflows/resolve-phone.py" 434-996-6618 "(704) 956-4975" ...
> python3 "Workflows/resolve-phone.py" --audit     # vCard health check
> ```
> [[Workflows/resolve-phone.py]] checks every source below in authority order and is the **only** approved resolution method. It exists because grepping for a number as formatted in the Phone-Index silently missed **18% of vCard entries** (format blindness — `(434) 996-6618` never matches a search for `434-996-6618`) and, worse, **34% of TEL lines are malformed** in a way that makes naive last-10-digit extraction return a *confidently wrong* number. That combination hid Jake Lindo, Logan Aldridge, and Tyler Dressler for weeks, and defeated the 2026-07-17 `phone:`-property fix entirely. Full measurements in [[Contacts/Phone-Index]]'s 2026-07-28 changelog.
>
> The script never invents a name: it reports `phone:`-property notes, the Phone-Index **Confirmed** table, the Office list, and the vCard as identifications, and anything else as a **mention only**. A number appearing in a sync's own run notes is not an identification.

Map phone numbers / emails to real names so threads are identifiable. Sources, in authority order (all of these are what the script checks — the list is the spec, the script is the implementation):

- [[Contacts/Phone-Index.md]] — number→name cache; **check this first** (fastest, covers non-staff like cohort members/volunteers identified in prior scans).
- **Any `*.vcf` in `Contacts/`** (newest by mtime wins; macOS auto-names the export e.g. `Connor Frey and 614 others.vcf`) — an exported vCard of Connor's macOS Contacts (~625 numbers as of 2026-06-25). Parse for `TEL` ↔ `FN` matches on last 10 digits. Optional and may be stale; Connor re-exports periodically. The live Contacts DB can't be mounted (macOS protects `Library/Application Support`), so the export is the substitute. **Note:** the contact's card name is used verbatim (e.g. "Seth-Worship Addison"); normalize to the canonical Office spelling when writing to trackers.
- `Dropbox/Office/` Grace Org Chart.pdf + Staff Contact List.xlsx (canonical name authority — wins on any conflict with the index/export).
- [[Contacts/Vendors.md]] for vendor numbers.
- **Any vault note with a `phone:` frontmatter property** — e.g. the Boot Camp leader notes under `Events/2026-07-29-Boot-Camp/Leaders/`. Search the vault for the last 10 digits (grep, digits-only normalization) before declaring a number unknown. Added 2026-07-17 after the **second** miss of this kind: Kirk Salvary (7/6) and Brandon Brys (7/3→7/17) both sat on the watchlist for days while their numbers were already recorded in roster/leader notes this list didn't cover.
- Memory: confirmed Grace staff contacts; spelling rules (e.g. "Jean Paul" not "John Paul", "Steve Coy" not "Koy").
- **Rock** (`trygrace.rockcloud.com`) — **person-search by Phone**: switch the top-nav search selector from Name to **Phone**, or go straight to `/Person/Search/phone/?SearchTerm={10 digits}`. There is no Rock connector; do this in **Claude in Chrome** on Connor's Mac (see memory). ⚠️ **`resolve-phone.py` cannot reach this source — it is a manual step, and it is the LAST one, run only on numbers the script returns UNRESOLVED.** Added 2026-08-10 because it covers a class every other source structurally cannot: **Grace visitors and attendees, who are not in Connor's own contacts and so can never appear in the vCard.** 202-294-5417 sat unresolved for 14 days and 3 null passes; Rock identified him in one lookup as **Nathan Wilkens**, a Visitor with an open "Contact our Volunteer Coordinator" connection request — i.e. exactly the person a cold Sunday-night recruitment text would be going to. When Rock resolves a number, also capture the **person ID, connection status, campus, and any open connection request**, since those are the context the text alone never carries.

**When a scan newly resolves a number** (via export, Office list, or Connor confirming it), append it to the **Confirmed** table in [[Contacts/Phone-Index.md]] (additive: date + how confirmed) so the next run resolves it automatically. Mark inferred/unconfirmed matches as such — don't promote a guess to Confirmed.

**Before adding any number to the watchlist, verify it is a real handle and record where it came from.** `resolve-phone.py` now checks every queried number against `chat.db`'s `handle` table and labels one that isn't there **⚠️ PHANTOM — no such handle in chat.db**. A phantom is not an unidentified texter; it is a typo made by an earlier run. **Never add a phantom to the watchlist, and never re-resolve one** — go find the run that introduced it, correct the digits against the actual handle, and retro-tie its messages to the right person. Watchlist rows must cite the **chat id (and rowid where known)** the handle came from, so provenance is checkable later without re-deriving it. (Trigger: `571-344-1742` was carried from 2026-07-10 to 2026-08-10 and survived **ten** re-resolution passes; chat.db has no such handle — the real one was `+17033441742`, Liz Goodiel, and a run mis-transcribed the area code, most likely off the 571-3xx handles sharing that same NYC-trip group chat. Every pass correctly reported it absent from every source, which was true and useless.)

**If a number still can't be resolved** — and it is confirmed real, and Rock has been checked — do two things: (a) keep the raw handle and surface it in the run report — an unknown number texting Grace logistics is itself worth surfacing; and (b) **add it to the "Unconfirmed / inferred" section of [[Contacts/Phone-Index.md]]** (number + thread/context + date first seen). That section is a standing **re-resolution watchlist**, not a dead end (see the re-resolution pass below). This matters because scans are incremental: once a handle is flagged unknown, no later run revisits that message, so without a watchlist a number stays unknown forever — even after Connor adds the contact. (Exactly what happened 6/25–6/26: Brandon Geddes / Simba Kanjanda were flagged unknown because the vCard export (mtime 6/25 21:45) post-dated the scan that hit them; Connor's later export could resolve them, but nothing re-ran resolution, so the seeding-completion they evidenced went unconnected.)


### Step 3.5: Re-resolution pass (run at the START of every scan, before Step 4)

Re-check every number in the Phone-Index **"Unconfirmed / inferred"** watchlist by passing the whole watchlist to `resolve-phone.py` in one call — that is the entire pass, and it takes seconds. **Act on the three verdicts it now returns:** a **name** → promote and retro-tie (below); **⚠️ PHANTOM** → do not re-resolve, correct or drop it per Step 3; **UNRESOLVED** on a real handle → this is the only case that survives to the next run, and it is the case to try **Rock** on (Step 3's last source) before leaving it parked.

**Don't re-run this pass against a frozen input.** If the newest `*.vcf` mtime is unchanged since the last run *and* no new source has appeared, the vCard half of the pass cannot produce a different answer — say so in one clause and move on. Ten consecutive null passes were run between 2026-07-19 and 2026-08-10 against an export frozen at 2026-06-25; a single re-export on 2026-08-10 cleared two of four within seconds. **Surface an export ask whenever the newest export is >30 days old** — that is the action, not another null pass. (Historically this step was done by eye and by grep, which is why it produced three false "unknown" verdicts on contacts that were already in the vault.) Sources checked: vCard export + Office list + Vendors + `phone:`-property notes + Phone-Index Confirmed + memory. **Trigger especially when the newest `*.vcf` mtime is newer than this workflow's last run** — that means Connor re-exported contacts and previously-unknown numbers may now resolve. For each that now resolves: move it to the **Confirmed** table (date + how confirmed), drop it from the watchlist, and **retro-tie it to any tracker item or note where its earlier (unknown-flagged) messages belong** (additively — and record a closure candidate if that retro-tie now evidences a completed item). Leave still-unknown numbers on the watchlist for the next run.

