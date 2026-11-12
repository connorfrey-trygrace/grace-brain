# Workflow: Grace Quick Refresh (on-demand)

The on-demand counterpart to `grace-weekly-refresh` (see [[Trackers/Automation]]). Run this whenever Connor asks — "run my quick refresh," "time to work," "catch me up," "scan my texts and email," or similar — because he's about to sit down and do Grace work and wants current trackers before he starts.

**Why this exists (2026-07-21):** replaces the prior fixed 3x-daily email / 1x-daily text cadence, which Connor found "sometimes less than I need and very often more than I need" and still required a manual kick-off anyway. `grace-weekly-refresh` was the once-a-week safety net so nothing went silently stale between asks — **retired as an automatic schedule 2026-09-12** (Connor's call: he runs refreshes manually now instead). This routine is therefore the only thing keeping the trackers current; there is no unattended fallback underneath it any more. Full rationale in [[Workflows/grace-quick-refresh-reference]] (not read on a normal run).

## What it runs

Five phases (0–4). **Phase 1's two jobs run concurrently** — changed 2026-08-10; they had been serialized for no reason other than list order.

### Phase 0 — process new transcripts (runs first, sequential)

Scan `/Transcripts/` for any note still tagged `unprocessed`. For each, run speaker-identification then synthesis per [[Workflows/speaker-identification]] and [[Workflows/transcript-synthesis]] — rename to a titled filename + repoint wikilinks, fill frontmatter (summary, action items, tags, `processed`, `processed_date`, `people:`), update /People and any matching /Events note, and register new action items in `/Trackers/Actions/`. **Nothing else in the vault promotes `unprocessed` → `processed`** — the transcribe pipeline only creates the `unprocessed` file, and weekly-synthesis merely *consumes* already-processed ones. So if this phase doesn't run, transcripts sit indefinitely (exactly what happened to three of them, 7/22–7/30, until 2026-08-10).

**Speaker-confidence gate (the one place this can corrupt the record):** only auto-process a transcript when *every* speaker is high-confidence from in-transcript evidence plus the known roster ([[People/People]] + [[People/Good Noodles]] + the meeting's expected attendees). If any speaker is genuinely ambiguous, do **not** rename or synthesize that transcript:
- **On-demand (this routine — Connor present):** surface the speaker-ID table for the ambiguous transcript and process it on his confirmation; process the unambiguous ones without asking.
- **Autonomous (`grace-weekly-refresh` — Connor absent):** process the unambiguous transcripts and leave each ambiguous one `unprocessed`, listed in the report under **"needs speaker confirmation."** Never guess a speaker in an unattended run.

Sequential (not parallel with anything) — synthesis writes to the same `/Trackers/Actions/` and `/Events` notes the later phases touch — and it runs **before** Phase 1 so any items synthesis mints are in place before the Phase 3 sweep indexes the folder. No `unprocessed` transcripts → no-op, one line in the Run Log.

### Phase 1 — pull and analyze, concurrently (no writes)

**First, before the two subagents: pull the calendar.** One `outlook_calendar_search` call, next ~3 weeks, and write [[Trackers/Calendar-Window]] per the format documented in that file's header. Cheap (one call, ~2 KB) and it is the input everything downstream needs to stop guessing.

> **This is a phase step, not a rule, because a rule saying "check the calendar first" had already been written three times and still didn't stop a fabricated meeting from reaching a report** (2026-08-20 incident in reference). Fetching the fact removes the inference gap a fourth rule can't.
>
> **Exclude the daily self-blocks** (`Morning Availability`, `Afternoon Availability`, `Daily FTJ Conflict`) — Connor uses them to shape availability, they have no attendees. `calendar-window.py` drops them again by subject as a second line of defence.
>
> **Never assert an occasion this file does not contain.** Before writing any sentence of the form *"raise it at X," "bring it to X," "wait for X"* — in a note or in the report — query it: `python3 "Workflows/calendar-window.py" --who "<Name>" --before <date>`. `unknown` means the person could not be resolved to an address and is **not** the same as `none`.

**Then the attendance gate** (added 2026-11-11): `python3 "Workflows/attendance-update.py" stale`. Exit 0 → skip. Exit 1 → pull the missing Sunday(s) from Rock per [[Workflows/attendance-pull]] (Chrome; needs Connor's Rock sign-in). Writes only [[Trackers/Attendance-Data.csv]] + [[Trackers/Attendance]], which no other phase touches, so it can run beside the subagents.

Then run these two as **parallel subagents**. They share no inputs: the text scan reads `chat.db` off its own `## Last scan` marker, the email sync reads Outlook off its own `## Last successful run` marker, and neither reads the other's output. All the expensive work — decode, phone resolution, relevance filtering — is here.

1. **Text scan** — [[Workflows/text-message-sync]] Steps 1–4, incremental off its `## Last scan` marker. ⛔ **`chat.db` is read only through `Workflows/query-messages.py`** — run `python3 "Workflows/query-messages.py" self-test` first and **stop the phase on a non-zero exit**, then `probe` / `scan`. This binds the parent agent too: **any double-check of the subagent's output goes through `verify`, never a hand-written query** — that is exactly how the 2026-08-28 exclusion breach happened. See [[Changelog/2026-08-28-messages-exclusion-enforced-in-code]].
2. **Email sync** — [[Workflows/m365-to-obsidian-sync]] through its capture/resolve stages, incremental off its `## Last successful run` marker (30-min overlap buffer). Outlook only, never Gmail; both Inbox and Sent Items. **Plus inbox triage** (below), in the same subagent.

Each returns a **findings list**, and neither writes to the vault yet.

#### Inbox triage (inside the email subagent — read-only, writes nothing)

Added 2026-11-11. Answers one question: **which inbox threads are waiting on a reply from Connor?** The sync's window is too short for this (a thread from Monday is still unanswered on Thursday), so triage uses its own fixed lookback and is **not** tied to the marker.

1. **Pull:** Inbox, last **7 days** (one `outlook_email_search`, no `order`), and Sent Items, same 7 days (`folderName: "Sent Items"`). Pass UTC bounds (`...Z`) — same conversion rule as the sync.
2. **Drop as answered:** any thread where Sent Items has a message in the same conversation (subject minus `RE:`/`FW:`, same counterpart) dated **after** the latest inbound one.
3. **Classify what's left** — return only `needs-reply`:
   - **needs-reply** — a person (not a system) asks Connor something or needs a decision/confirmation from him, and he is on **To** (not only CC).
   - **skip** — newsletters, notifications, calendar accept/decline receipts, automated mail (Rock, PCO, ClickUp, vendors' no-reply), CC-only FYIs, and threads where Connor's answer is already "done" per a closed action note. Rock mail still goes through the sync's routing rules as before — triage just doesn't list it.
4. **Return per needs-reply thread:** sender, subject, received date, one-line ask, and the matching `/Trackers/Actions/` note if one exists (`actions-index.py --titles`). **Never fetch full bodies for skipped mail** — previews decide skip.

Triage creates no action notes and touches no markers. A needs-reply thread that carries a dated commitment is already handled by the sync's own rules; triage only surfaces it.

> **Why analysis is parallel but writing is not:** both jobs fold findings into the *same* notes in `/Trackers/Actions/` and the same [[Events]] notes. Two agents editing one note concurrently loses one of the two edits silently — the exact failure this system has no way to detect, since neither run reports an error. Reading is safe to overlap; writing is not.

### Phase 2 — apply writes, sequentially

Apply **email findings first, then text findings** — order matters. The email sync may auto-close a clearly-completed item; the text sync only ever proposes closure candidates. Running email first means the text pass sees the already-closed state and won't raise a closure candidate against an item that's already resolved. Each job's own write rules still govern (text sync Steps 5–6 and 8; email sync's routing, guardrails, and marker update).

Both markers (`## Last scan`, `## Last successful run`) and both Run Log entries in `/Logs` are written in this phase, not Phase 1 — a job that dies mid-analysis must not leave its marker advanced.

> ⛔ **Never type a timestamp. `Workflows/stamp.py` writes all six of them** (added 2026-08-21):
> ```
> python3 "Workflows/stamp.py" mark --m365 --window-end "<end of this run's email search window, ET>"
> python3 "Workflows/stamp.py" mark --text-scan <highest ROWID>
> python3 "Workflows/stamp.py" log --m365 "<line body>"      # and --text, --refresh
> ```
> The execution shell — container and Mac VM alike — reports **UTC**, so a bare `date` reads ~4h ahead and labelling it "ET" corrupts the marker. `ZoneInfo("America/New_York")` ignores the shell entirely, which is why anything a script stamps has always been correct and only hand-typed values have ever broken. `stamp.py` also refuses to move `last_rowid` backwards.
>
> **Then close the phase with the gate — it is not advisory:**
> ```
> python3 "Workflows/clock-check.py"
> ```
> It compares every stamp against its file's real **mtime** and exits non-zero on any that claims to have been written later than it was — checking mtime rather than "is the stamp in the future" catches a UTC-shift defect the future-check missed (incident in reference). **A non-zero exit ends Phase 2** — correct the stamp with `stamp.py` and re-run before Phase 3. Do not honour a bad marker as a window.

### Phase 3 — sweep

3. **Open Actions sweep** — [[Workflows/Open-Actions-Tracker]] in standalone sweep mode (Step 0, then 2.5, 3, 3.5, 3.6, 4) against `/Trackers/Actions/`. Genuinely gated on Phase 2: it must see both jobs' writes, and Step 0's index is built *after* them or it indexes stale frontmatter. **Step 3.6** (added 2026-09-15) runs `pending-drafts-check.py` over the whole vault, not just `/Trackers/Actions/` — it catches held drafts (leader texts, invite drafts) going stale outside the Actions folder entirely, which is a different failure class than a neglected action item.

**Step 0's index now answers "when's the moment?" for every waiting-on item** (added 2026-08-20). Each one carries `next w/ <person>: <date>` computed from [[Trackers/Calendar-Window]], and a new list — **WAITING-ON WITH NO SHARED OCCASION** — names the items where there is no meeting to raise the wait at before its own date. Use it: an item in that list must **not** get a note line pointing at a meeting, and if the wait genuinely has to end, the channel is **text, then call** (see [[connor-works-remotely]] — Connor works remotely; "in person," "in the room" and "live" are the same error in different words). An item *not* in the list has a real occasion, and naming its date is the useful thing to tell him.

### Phase 4 — Agent Hub visit (Notion)

After the sweep, do Grace Claude's Agent Hub visit: read **Hub Protocol**, then **Start here: Grace Claude** in Connor's Agent Hub in Notion, and follow them (Agent Mail → Connor changed → text-message check → sync Grace Tasks from the vault → prioritize). Use the Notion connector; if it isn't available in the session, use Claude in Chrome.

- **Connector shortcuts (skip discovery):** Grace Tasks = `collection://4684fe37-3892-4bdf-84eb-0f9c523fd357` (read it through saved views in view mode or `fetch` only — **never SQL or `rows` queries**: they draw on a shared hourly quota and overuse breaks Connor's dashboard. Start with the "Connor changed (check first)" view, `view://40d12cb6-3a8b-81dc-8969-000c655b11e9`). Every row you edit also gets `date:Agent synced:start` = now (ET offset, `is_datetime` 1) in the **same** update, or the formula flags your own edit as Connor's.

- **Gated on Phase 3** — the Notion list mirrors the vault, so it must see this run's writes.
- **The text-message check reuses Phase 1's text findings** for Grace tasks; don't re-scan `chat.db`. Its extra job is the cross-list part: compare the same window's texts against the Personal and St Onge lists and send one Agent Mail FYI per owner. The Skylar 1:1 exclusion still holds and is still enforced by `query-messages.py`.
- **Connor's Hub edits are decisions** — mirror them into the vault notes per Start here, after Phase 2's writes, so a refresh never overwrites them.

The same visit, minus the text check and plus the email sync, also runs daily at 5 AM ET as a cloud routine (see [[Trackers/Automation]] → Cloud routines). Both share the email sync's `## Last successful run` marker, so neither re-processes the other's mail.

## What it deliberately skips

The m365 Run Log health check, the scheduler heartbeat, and the frontmatter/body **drift check** (`actions-index.py --drift`) do **not** run here — they audit the automation system itself, not Connor's actual data, and only need to happen once a week. They're `grace-weekly-refresh`-only duties. Running this on-demand routine several times in a day should not produce repetitive "scheduler looks healthy" noise.

## Timing (measure it, don't estimate it)

Run `date '+%s'` **at the top of Phase 0**, again at **each phase boundary**, and **a fifth time after the report is written** — five stamps, they cost nothing, and skipping the fifth hides real cost (report/verification has outweighed Phase 3 before). After Phase 3, append one line to [[Logs/refresh-run-log]] in the format documented there: total, per-phase minutes, what came in (transcripts / emails / messages), what went out (notes touched, KB), plus `report Xm` and `wrote N KB` (bytes actually **added**, not file size — a 27 KB note with a one-line append is ~200 bytes of real cost, not 27 KB). Each sync additionally carries its own `elapsed Xm` on its own Run Log line. If a stamp was missed, write `unmeasured` rather than a guess.

**Token usage, alongside elapsed time.** At the same fifth-stamp moment, run:
```
python3 "Workflows/usage-report.py" --session-id <this session's uuid> --since <phase-0 stamp> --until <final stamp>
```
Read the session id off your own scratchpad path — never guess it, never ask Connor for it. Fold the printed line straight into the refresh-run-log entry (`tokens ... | peak context ...`). Its per-model context-window table is a best-effort guess that self-corrects when a run disproves it — never a reason to skip logging.

**Why any of this exists:** Connor once asked why a refresh took ~30 minutes and nothing in the vault recorded elapsed time — file mtimes can't distinguish thinking from reading, or see anything a phase did without writing. Full history in reference.

## Report

**Connor runs this because he is about to sit down and do Grace work.** So the report is a **work queue first and a sync log second** — he needs to know what to pick up, not what the sync did. Two parts, strictly in this order.

### Part 1 — Start here (always first, never skipped)

After Phase 3, run:

```
python3 "Workflows/actions-index.py" --brief
```

⚠️ **`--brief` is a triage view, not the work queue. It is one of two inputs, and it is the smaller one.** It returns only what is *date-urgent* — chase-by passed, deadline/needs_by reached, **within 14 days** (`HORIZON_DAYS`), open closure candidates, unparked, flagged — and it caps each group. **The queue itself is every `active`/`in-progress` item Connor owns that is not `blocked_by` an open item**, which the full `actions-index.py` output already lists; `--brief` then tells you which of those are on a clock. **Build Part 1 from the full list and use `--brief` to order it** — building it from `--brief` alone once told Connor he had nothing to do while 22 real active items sat in the folder (incident in reference).

**Three rules for this part, and the first one is a gate the other two run behind:**

- ⭐ **Only list items with a Connor-side next physical action that is available TODAY. If there is nothing for him to do today, do not raise it — at all, in any section.** A `needs_by` or `deadline` firing on a `waiting-on` item is **not work**; the only Connor-side action a `waiting-on` item can have is a chase, and if there is no chase to make it does not belong in Start Here. It is still in the vault and still in the full sweep view, which is the inventory. **Start Here is a work queue,** not a fact dump.

  **A near deadline is not the test, an available action is.** Attending a commitment is not work; preparing for it is, and only if the prep is due now. Before listing anything, ask *what does he physically do about this in the next hour?* — no answer means it does not go in. `--brief`'s "Next 14 days" section is a **candidate list, not the answer** — it's computed off dates, and dates can't tell a due task from a date on the calendar; filter it by hand. Same for held items — an on-hold item doesn't get raised early because its release date is close.

  **Enforced in code, not left to judgment:** `actions-index.py --brief` suppresses `waiting-on` items that carry no live `chase_by`. **The corollary the guard can't enforce for you: never write a `chase_by` against someone who has already committed to reporting back.** A manufactured chase defeats the suppression at the source — this is a church, and a colleague saying "I'll let you know" is a person keeping their word, not an open ticket. Three worked incidents behind this rule (a manufactured chase, an attendance-vs-prep mixup, the brief-alone miss above) in reference.

- **Name the next physical action, not the item title,** wherever the note makes one obvious — "text JeanPaul the call-time list" beats "Send JeanPaul the Sunday-night services general timeline." Connor is choosing what to do in the next hour; the title is a label, not an instruction.
- **Don't pad it to look thorough.** If `--brief` returns nothing urgent, say so in one line and move on. A short queue is a real result, and inflating it trains him to skim past the section that matters most.
- **Replies owed** (from inbox triage) — a reply is a physical action available today, so it belongs here. One line each: *Reply to <Sender> — <the ask>* (received date). If the thread maps to an action note already in the queue, fold it into that line instead of listing it twice. Oldest first. None → omit the group, no "inbox clear" line.
  - **Offer drafts, don't write them unasked.** End the group with one line offering to draft any of them. On his pick, draft per [[Reference/Connor-Communication-Style]] in chat for approval — never save to Outlook or send without his explicit yes. Volunteer asks follow the "we, not I" rule.

### Part 2 — What changed this run

Then, and more briefly: Agent Hub mail answered and Connor's Hub changes applied; transcripts processed this run (titled links) and any left `unprocessed` pending speaker confirmation; new findings from texts/email folded into trackers (with links), anything newly flagged or re-banded in `/Trackers/Actions/`, new closure candidates added this run, unresolved phone numbers, and any contradiction needing Connor's call.

Everything else — counts, windows scanned, "the sync looks healthy" — belongs in the Run Log under `/Logs`, not in this report.

## Relationship to `grace-weekly-refresh`

Both run the same phases 0–3 (process new transcripts → text scan ∥ email sync → apply writes → Open Actions sweep). `grace-weekly-refresh` additionally runs the two watchdog duties (Run Log health check, scheduler heartbeat) plus the drift check — but **it no longer fires automatically** (retired 2026-09-12; see [[Trackers/Automation]]). The one behavioral difference in Phase 0: this on-demand routine can ask Connor to confirm an ambiguous speaker inline, whereas [[Workflows/grace-weekly-refresh]]'s unattended framing defers ambiguous transcripts and flags them instead of guessing — relevant now only if Connor explicitly asks for that file's procedure rather than this one. **There is no scheduled safety net under this routine any more** — the watchdog duties and the drift check only happen when Connor asks for them.

## Changelog

History lives in [[Changelog/_history/grace-quick-refresh-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
