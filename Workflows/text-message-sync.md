# Workflow: Text Message Sync

Procedure for scanning Connor's text messages (iMessage/SMS) for Grace-relevant content and folding the findings into the existing trackers. **Runs as Phase 1 of [[Workflows/grace-quick-refresh]] (on-demand, whenever Connor sits down to work) and of [[Workflows/grace-weekly-refresh]] (Mon 6 AM, the weekly floor)**, and can also be run standalone any time Connor asks (e.g. "scan my texts"). ⚠️ **The old fixed daily 8:00 AM `grace-text-scan` task was retired 2026-07-21** — see [[Trackers/Automation]] for the live inventory; this line said otherwise until 2026-08-12. Every run is **incremental** — it processes only messages newer than the `## Last scan` marker, so nothing is scanned twice. **Discretion in automated runs:** only clearly-safe additive findings are folded into trackers automatically; sensitive/personnel content and any contradictions are *surfaced in the run report for Connor to decide*, never auto-written.

This exists because Grace staff and vendors text important logistics, decisions, and asks about as often as they email — so texts are a real source alongside [[CLAUDE.md]] transcripts, not a substitute for them.

**Reference material** — mount-failure history, resolution source authority, watchlist rules, and the incident write-ups behind the corrected/enforced rules below (WAL replay, attribution direction, the exclusion guard) — lives in [[Workflows/text-message-sync-reference]]. Do not read it speculatively.

## Source & access

Three lines are the whole operational rule; the reasoning, the failure history and the privacy caveats are in [[Workflows/text-message-sync-reference]].

1. **Glob for the mount, never hardcode it:** `ls -d /sessions/*/mnt/*Library--Messages*`, then confirm `chat.db` exists inside the match. A `System--Library--Messages` hit is the wrong one — it has no `chat.db`. This has been wrong three times for naming a literal path.
2. **Copy `chat.db` + `chat.db-wal` + `chat.db-shm` together to a temp dir, then open the copy WITHOUT `immutable=1`.** Copy all three files — a `-wal` without its `-shm` may not replay — and never open the live DB read-write. ⚠️ **`immutable=1` is retired, do not reintroduce it:** it makes SQLite skip the write-ahead log entirely, silently dropping the newest un-checkpointed messages — exactly the ones a fresh scan exists to catch. Measurement that caught it, and why the copy's ~5s cost isn't worth trading against correctness, in reference.
3. **Never touch the `Attachments` subfolder.** Many GB of photos/video, out of scope.

If a scan reads empty or permission-denied, check Full Disk Access for the Claude app first.

## Privacy & discretion

The mount exposes *all* of Connor's texts, not just Grace ones. Two standing rules:

- Only surface and record **Grace-relevant** content. Personal/unrelated messages are read past, never quoted, never written anywhere.
- Some Grace texts are shared in confidence. Anything folded into a Dropbox-synced tracker should be logistics/decisions/asks — not sensitive personal disclosures. When in doubt, surface it to Connor in chat and let him decide rather than writing it down.

## Exclusions (hard skip — applied before any decode)

Some threads are **never** to be read, decoded, or surfaced. This is not a "read then ignore" — excluded content is never seen.

> ⛔ **`chat.db` is never opened directly. Every read goes through `Workflows/query-messages.py`, which carries the exclusion in the only code path that reaches the data.**
> ```
> python3 "Workflows/query-messages.py" self-test              # run first; non-zero exit stops the scan
> python3 "Workflows/query-messages.py" probe --since-rowid N  # "is anything new?" — no text columns
> python3 "Workflows/query-messages.py" scan  --since-rowid N  # the real pass
> python3 "Workflows/query-messages.py" verify --rowids A,B    # double-checks go through here TOO
> ```
> **"Every read" includes the ones that do not feel like the scan** — the cheap probe, a spot check, and above all **a verification pass over someone else's work**. There is no subcommand that takes arbitrary SQL, deliberately.
>
> **Why this is enforced in code, not prose (2026-08-28):** a prose-only version of this rule failed twice, including once when a parent agent ran its own unfiltered verification query over a subagent's correctly-filtered work. Put it where omitting it is not an option. Incident write-up, and the self-test check that catches over-exclusion (dropping whole group threads) as well as under-exclusion, in reference.

Excluded contacts:
- **Sky** — handle: `9087980030`. Exclude the **1:1 / direct thread only**. Match on the last 10 digits (handles in `chat.db` may be stored as `+19087980030`, `9087980030`, etc.).

Scope of the Sky exclusion:
- **Direct (1:1) thread with Sky → never read, decode, or surface.** Enforced at the SQL level.
- **Group chats that include Sky → OK to scan.** Per Connor, only the private 1:1 messages are off-limits; group threads (including any with Grace people) are in scope and processed normally.

## Step 1: Determine scan window (incremental)

Read the **## Last scan** section at the bottom of this file for the last-synced `ROWID` and date. Scan only messages with a higher `ROWID` (i.e. new since last run). If there is no recorded marker (first run), scan full history per Connor's standing choice.

## Step 2: Extract and decode

- Query `message` joined to `handle` and `chat` for: `ROWID`, contact handle (phone/email), `is_from_me`, `date` (Apple epoch — convert: nanoseconds since 2001-01-01), `text`, and `attributedBody`.
- **Timezone — convert to Connor's local Eastern time before reporting.** `date` is stored in **UTC**. A naive epoch→datetime gives UTC, which is **4h ahead of EDT (5h ahead of EST)** — so an 8:43 AM ET text renders as 12:43 without conversion. Always convert UTC → `America/New_York` (DST-aware) so text times line up with meeting-recording filenames (which are already local) and with Connor's recollection. (Caught 2026-06-25: a morning text mislabeled as midday made it look like it came *after* a call it actually prompted.)
- On recent macOS the `text` column is often NULL and the message body lives in `attributedBody` (an NSAttributedString typedstream blob). Decode it to recover the text.
- If a message body can't be cleanly decoded, **flag it as garbled — do not guess at the content.** Note the contact and timestamp so Connor can check the thread himself.

## Step 3: Resolve contacts to names

> 🛑 **Run the script. Do not hand-roll a grep.**
> ```
> python3 "Workflows/resolve-phone.py" 434-996-6618 "(704) 956-4975" ...
> python3 "Workflows/resolve-phone.py" --audit     # vCard health check
> ```

[[Workflows/resolve-phone.py]] is the **only** approved resolution method. It checks every source in authority order and never invents a name — it returns a name, `⚠️ PHANTOM` (not a real handle), or `UNRESOLVED`.

- **A name** → use it.
- **`UNRESOLVED` on a real handle** → check Rock by phone (`trygrace.rockcloud.com`, search selector Name → **Phone**). Still nothing: keep the raw handle in the run report and add it to the Phone-Index watchlist.
- **`⚠️ PHANTOM`** → do not re-resolve; correct or drop it.
- **Newly resolved** → append to the **Confirmed** table in [[Contacts/Phone-Index]] with the date and how it was confirmed, and retro-tie it to any item its earlier unknown-flagged messages belong to.

The source authority order, the watchlist rules and why grep fails here are in [[Workflows/text-message-sync-reference]] § Resolution sources. Read it only when a resolution is genuinely contested.

### Step 3.5: Re-resolution pass (start of every scan)

Pass the whole Phone-Index watchlist to `resolve-phone.py` in one call — that is the entire pass, and it takes seconds.

**Skip it when the input is frozen.** If the newest `*.vcf` mtime is unchanged since the last run and no new source has appeared, the vCard half cannot return a different answer — say so in one clause and move on. **If the newest export is >30 days old, surface an export ask** — that is the action, not another null pass.

## Step 3.9: Connor's note-to-self thread — a source, not noise (added 2026-08-21)

**`973-699-0180` is Connor's own line** ([[Contacts/Phone-Index]] line 31, "self"). The thread with that handle is where he **deliberately pastes content he wants readable and searchable** — voice-memo transcriptions, summaries, notes off a call. Treat it as a **high-signal capture inbox**, not as chatter, and read it before concluding a detail exists only in media the sync cannot open.

**It structurally double-records every message.** A self-thread stores each message twice — one row `is_from_me=1`, one `is_from_me=0` — so a single paste produces two identical rows at the same timestamp, and an empty-then-decodable pair can produce four. **Collapse them by (timestamp, text); do not report the copies as a finding, and do not treat a repeat as a re-send.** Worked example (Alexis Hendrickson's 8/19 Sour Patch Kid voice memo, ROWIDs 191824/191825 + 191893/191894) in reference.

## Step 4: Filter for Grace-relevant content

A message qualifies if it references any of:

- A known Grace person (staff/vendor/volunteer) discussing church matters
- An event by name or its logistics (World Cup party, Rend Collective concert, Sunday-night service, etc.)
- A decision, commitment, deadline, date, time, or location tied to Grace work
- An action item — something Connor (or someone else) needs to do
- A vendor/credential/cost detail

Casual or unrelated personal messages do not qualify. **Do not fabricate** relevance or content — if it isn't clearly in the message, it doesn't go in.

## Step 4.5: Attribution discipline — every directional claim carries its rowid, and gets verified before it's written down

**Why this is a checkable requirement, not a reminder (2026-09-09):** summarization has already silently inverted a `ME`/`THEM` direction once, and the inverted claim reached a permanent tracker note as fact before Connor caught it from personal knowledge — nothing in the pipeline would have caught it otherwise. Full incident in reference. The fix:

- **Any finding describing who initiated, asked, offered, confirmed, or committed to something must cite the rowid(s) it's based on**, inline, next to the claim — not only in a trailing `[Source: ...]` line covering the whole finding. A claim about who-did-what-to-whom with no rowid attached is not a usable finding; it goes back to the scan output before it goes anywhere else.
- **State direction as the scan literally shows it** (`ME` / `THEM`) when drafting the claim, then translate to names — don't compose the sentence first and backfill the direction from the narrative you've already built. If the sentence and the `ME`/`THEM` tag don't obviously agree, stop and re-read the row.
- **Before any such claim is written into a tracker note (or reported to Connor as fact), run `python3 "Workflows/query-messages.py" verify --rowids <N>` on the cited rowid(s) and confirm the row matches the claim.** This applies whether the writer is the subagent itself or the parent agent consuming the subagent's report — whoever commits the claim to a permanent record is the one who verifies it. Content/topic summaries ("Callie asked about a billing code") don't need this; claims about who initiated or offered something do, because that's exactly the class of claim summarization is most likely to invert and Connor is most likely to act on directly (whose court the ball is in).

## Step 5: Fold into trackers (additive only)

Per Connor's standing choice, findings go into the existing trackers — **not** a separate text-log note.

- **Action items** → create (or update) a note in `/Trackers/Actions/` per [[Workflows/Open-Actions-Tracker]]'s item schema (frontmatter: status, priority, owner, added, deadline, etc.; body carries only what frontmatter cannot — Priority rationale, Source, Deadline rationale, Needs-by rationale, Status, Notes, Blocked by; **never a bullet restating a frontmatter value** (no `- **Priority**:`, `- **Added**:`, `- **Deadline**:`, `- **Last mentioned**:`), per [[Workflows/Open-Actions-Reference]] § The body explains fields, never restates them). For **Source**, cite the text: `Text from {Name}, {YYYY-MM-DD}` (there is no transcript file to link).
- **Event details** (dates, logistics, vendor info) → the relevant [[Events]] note.
  - **Status-update history goes to the event's `-Log.md` companion, not the plan note** (e.g. [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Launch-Log]]). Only changes to the *live plan* — owners, dates, scope, open questions — are folded into the plan note itself. Convention added 2026-08-11; see [[Workflows/event-planning-note]].
- **Additive rule:** only add or append. Never subtract, overwrite, or "correct" existing tracker content based on a text — if a text contradicts the tracker, surface the conflict to Connor, don't silently resolve it. (See memory: push notes additively.)
- **Entry format is mandatory: terse timestamped lines — see [[Workflows/Open-Actions-Tracker]] § Entry format.** One line per event, no verbatim quotes, no analysis; judgment goes in the run report, not the note.
- If a finding would duplicate an item already tracked, append a dated line to the existing note's body and bump its `last_mentioned`, rather than creating a second note. Check **every note in `/Trackers/Actions/`**, not just active ones — do this with `python3 "Workflows/actions-index.py" --titles` (one status+filename line per note, ~12 KB) rather than reading the folder; open a body only when a title looks like a plausible duplicate (added 2026-08-10) — per [[Workflows/Open-Actions-Transcript-Steps]] Step 1, this is the same mandatory cross-check that applies to every path that adds an item (added 2026-07-21 after two near-duplicate m365-sync-investigation items slipped through).
- **A finding with its own named deadline is never note-only.** If a text contains an explicit commitment tied to a specific day/date ("I'll send X on Monday", "meeting Thursday at 3"), give it its own new note in `/Trackers/Actions/` with `status: active` — even when it's clearly a sub-step of a broader item already being tracked. Cross-reference the parent item with a `blocked_by`/`blocks` wikilink or a one-line pointer; don't bury the dated commitment inside the parent's Notes field, where it has no deadline field of its own and won't surface until the whole entry is re-read. (Trigger: Connor asked whether a Monday-follow-up commitment had become its own open action — it hadn't, it was folded into a long Notes blob on a broader On Hold item and was effectively invisible.)
- **A call or meeting agreed or proposed off-calendar sets `meeting:` on the item** (`YYYY-MM-DD HH:MM`, or a bare date if no time yet) — even when the item is `waiting-on` and even when the time is only proposed. Texts and email set up calls Outlook never sees, so without the field the conversation is invisible to [[Trackers/Calendar-Window]], the `next w/` column and Start Here. `actions-index.py --brief` lists every `meeting:` in the next 3 days under **[@] Conversations**; a waiting-on item whose `waiting_on` names a near date but has no field shows there with "set it." Added 2026-11-12 after John Slye's 11/13 call (agreed by text) was missing from the report the day before — [[Changelog/2026-11-12-off-calendar-meetings]].
- **Never change status to completed on your own.** When a text appears to COMPLETE an existing item, append the confirming text as a dated note (additive) AND record it as a **closure candidate**: set `status: closure-candidate` on the target note and append the evidence + what-to-verify to its Notes, and also surface it in the run report. This is what makes the candidate visible in the Closure Candidates view of [[Trackers/Open Actions.base]] even after the run report scrolls away — Connor said he can't read every sync's output. Connor decides whether to close (confirm/dismiss). See [[Workflows/Open-Actions-Reference]] → ### Closure Candidates — entry and exit. (A text can confirm one part of an item while a hidden sub-blocker remains open — see the 2026-06-24 Sunday-welcome-rep case, where the Derek confirmation arrived but the kids-coverage sub-question was separate.)

## Step 6: Ask before anything non-additive

Folding new items in is routine and needs no confirmation. **Ask first** before: merging or rewriting an existing tracker entry, archiving anything, or recording a finding that looks sensitive/confidential.

## Step 7: Report

In chat, report:
- Scan window (date range / ROWID range) and message count scanned
- Grace-relevant findings, grouped by person or event, each with the text source (name + date)
- What was folded into which tracker (with links)
- Any garbled/undecodable messages flagged (contact + timestamp)
- Any unresolved phone numbers flagged
- **Closure candidates** — tracked items a new text appears to complete (item name + evidence + what to verify), for Connor to confirm before they're closed. These are **also recorded as `status: closure-candidate`** on the target note (visible in the Closure Candidates view of [[Trackers/Open Actions.base]]) so they persist beyond this report (not just listed here).
- Any contradictions with existing tracker content that need Connor's call

## Step 8: Update the marker

Update the **## Last scan** marker below with the highest `ROWID` scanned and the run date, so the next run is incremental. Then **append a one-line entry to ## Run Log** (format defined there) — every run, even zero-finding or errored. The run *report* (Step 7) carries the detail; the log line only needs the counts.

## Rejected: the minimum-window guard (2026-08-12, Connor's call — do not re-propose)

Three run-log lines (8/11 13:44, 8/11 13:46, 8/12 12:27) proposed skipping this phase when `max(ROWID) - last_rowid` is tiny and the last run was recent, on the grounds that full fixed overhead for a 2-message window is waste. **Connor declined it. Stop suggesting it** — the cost observation is real but it is not worth building, and re-raising it every quiet run is itself noise. If a future run notices the same waste, say nothing.

## Source of truth

Findings come exclusively from `chat.db`. Do not blend in email, calendar, or transcript content during a text scan — those are separate jobs. If a text references a meeting, note the reference; don't pull the meeting's content from another source.

## Last scan

- last_rowid: 198499
- last_run: 2026-11-13

> ⛔ **This marker is written by `python3 "Workflows/stamp.py" mark --text-scan <rowid>`, never by hand** — the shell reports UTC, `ZoneInfo` does not. Verified every run by `Workflows/clock-check.py`, which compares the stamp against the file's real mtime. Retired the prose guard that stood here 8/17–8/21 and did not prevent the 8/21 recurrence: [[Changelog/2026-08-21-clock-enforced-in-code]].

(Marker only. Per-run detail lives in **## Run Log** below — one line per run. The rich pre-2026-07-16 entries are archived verbatim at [[Archive/text-scan-run-history-2026-06-24-to-2026-07-16]].)

## Run Log

**Entries live in [[Logs/text-message-sync-run-log]]** — split out of this file on 2026-08-10 because this procedure file is read in full on every run and the log is not. Every run appends **one line** there (success, zero-finding, or caught-error alike); the line format and the ~90-entry housekeeping cap are documented at the top of that file. **Do not append entries here.** **Every line carries an `elapsed Xm` field**: stamp `date '+%s'` when the job starts and again before writing the line, and report whole minutes (`<1m` if under). Added 2026-08-11 — Connor asked why a refresh took ~30 minutes and nothing anywhere recorded elapsed time, so the answer had to be reconstructed from file mtimes.

## Changelog

History lives in [[Changelog/_history/text-message-sync-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
