Maintain `/Trackers/Actions/` — one note per action item — as the single source of truth for action items across all transcripts, with `/Trackers/Open Actions.base` as the aggregated view over that folder.

**Migrated 2026-07-21** from a single `/Trackers/Open Actions.md` file (heading blocks inside status sections) to one note per action (frontmatter properties + a Base for views). See ## Changelog for what changed and why. All logic below (priority rubric, escalation windows, flagging, on-hold/waiting-on/closure-candidate rules) is unchanged from the prior version — only the storage mechanism and the mechanics of each step changed.

## Where the rest of this workflow lives

Split **2026-08-12** — this file was 32 KB and read in full on every run, but a standalone sweep executes only Steps 0, 2.5, 3, 3.5 and 4. **Read only what the run needs:**

| You need | Read |
|---|---|
| The sweep itself (Steps 0, 2.5, 3, 3.5, 4) | this file |
| Adding/updating items from a new transcript (Steps 1–2) | [[Workflows/Open-Actions-Transcript-Steps]] |
| Schema, field authority, sort order, priority bands, status entry/exit criteria, short-fuse carve-out | [[Workflows/Open-Actions-Reference]] |

**Do not read the reference file speculatively.** Read it when a specific decision needs it — a band change, a status flip, a closure call — not at the top of a run.

## Modes

This workflow runs in two modes:
- **Full update** (default, triggered after synthesis on a new transcript): Run Steps 0, 1, 2, 2.5, 3, 3.5, 4.
- **Standalone sweep** (triggered by the weekly safety-net task, the on-demand quick-refresh routine, or explicit request without a new transcript): Run Step 0 (Build the index), Step 2.5 (Completion & confirmation sweep), Step 3 (Neglect/flag sweep), Step 3.5 (Re-prioritization sweep), and Step 4 (Report). Skip Steps 1-2 since there's no new transcript to process.

**Step 0 is not optional in either mode** — every later step keys off its output, and skipping it means reading the whole folder again.

When triggering, the caller specifies the mode. If not specified, assume full update if a transcript is referenced, otherwise standalone.

**Standalone-sweep side duties (run by the weekly `grace-weekly-refresh` task, not the on-demand quick-refresh, and not part of full updates):** alongside the sweep itself, that task also runs (a) the **Run Log health check** defined in [[Workflows/m365-run-log-health-check]], (b) the **frontmatter/body drift check** — `python3 "Workflows/actions-index.py" --drift`, added 2026-08-10; and (c) a **scheduler heartbeat**: one `list_scheduled_tasks` call comparing each Grace task's `lastRunAt` against its cadence per [[Trackers/Automation]], flagging any job overdue by more than one full cycle as an Active note in `/Trackers/Actions/` (same flagged-item pattern as the health check; search for an existing flag on the same job before adding one; ignore non-Grace and expired-temporary tasks). See [[Trackers/Automation]] for the current schedule of both the weekly safety net and the on-demand quick refresh.

**How to act on the drift check (added 2026-08-10).** It returns two things, and they are not the same severity:
- **STATUS CONTRADICTIONS** — frontmatter says `completed` while the body's prose **Status** still reads Active/Open/On Hold, or the reverse. **Treat every one of these as a real finding**: open the note, decide which is true, correct the loser, and surface it in the run report. This class is how three genuinely-closed items (the Michele Smith check, the NYC card reconciliation, the Unshaken inquiry) sat looking open for weeks — Connor's read on 2026-08-10 was that they "should have been caught."
- **`REDUNDANT BODY FIELDS`** — a body bullet restating a frontmatter *value* (`- **Priority**: P2 …`, `- **Last mentioned**: …`). **This used to be a value comparison and is now a presence check**, because comparing values only catches the ones that have already drifted — 47 had by 2026-08-22, when the duplication was removed vault-wide. Any hit is a bullet that should not exist: rename it to `- **<Field> rationale**:` and drop the literal, or delete it if it held no reasoning. Full convention: [[Workflows/Open-Actions-Reference]] § The body explains fields, never restates them.

## Note size — split history out, never let it accumulate

Action notes are read in full by every sync that appends a line to them. **Dated history therefore lives in `/Trackers/Action-Logs/<note name>-Log.md`, not in the note.** `actions-index.py` flags any live note over 15 KB under `OVERSIZED NOTES`; when it names one, split it in that run rather than recording the observation and moving on:

```
python3 "Workflows/split-note-log.py" --dry-run "<path>"   # review, then drop --dry-run
```

**Never split by hand** — `- **Blocked by**:`, `- **Status**:` and the rationale bullets are interleaved *between* dated entries, so any "move everything below the fields" approach silently drops dependency edges. Full convention, and the list of notes that deliberately do NOT split: [[Workflows/note-history-splitting]].

The 2 newest dated entries stay in the live note by design — `evidence()` emits the last 2 dated lines so a sweep can clear most candidates without opening the body.

## Entry format — terse timestamped lines, not narrative

**This is a hard format, not a preference.** Every dated entry a sync writes into an action note, event note or event log uses it.

```markdown
### 2026-08-06 (text)
- 12:18 PM · Simba asks for a call
- 2:04 PM · Simba delays
- 2:29 PM · Connor unavailable; asks Simba to attend Mon 8/10 video shoot
- → status: active → waiting-on (Simba)
```

Rules:

- **One line per event.** `H:MM AM/PM · who + what`, target ≤12 words. Drop the timestamp only when the source has no time (email digests, transcripts) — then just `- <who> <what>`.
- **No verbatim quotes** unless the quote *is* the content (a number, a date, a name, an exact commitment). The transcript and the email are the record; the note is the index to them.
- **No interpretation, no advocacy, no ⭐/⚠️ essays.** If a finding needs judgment — a contradiction, a risk, a recommendation — it goes in the **run report to Connor**, not into the note. A note is a status ledger.
- **A `→` line only when a field actually changed** (`status`, `priority`, `deadline`, `needs_by`, `chase_by`, `waiting_on`, `meeting`). One line, `→ field: old → new`. The reason, if it isn't obvious, is a clause on the same line — not a paragraph.
- **Never restate what a prior entry already says.** If nothing moved, write nothing and bump `last_mentioned`.
- **Superseded content is deleted, not struck through.** When a claim turns out wrong or an item resolves, remove the dead text and state what is true now. `~~strikethrough~~` leaves the wrong version on the page, doubles the bytes every future run reads, and makes the note read as an argument with itself. Never delete a *file* (move it to /Archive) — this rule is about dead lines inside a live note.

**Why:** entries had grown to essays — one bullet in a single action note measured **4,966 bytes**. Wall-clock on a refresh tracks tokens *generated*, so entry length is the single largest controllable cost in a run, and long entries make the note harder to scan, not easier. Connor, 2026-08-12: *"The exact texts do not need to be included, just the status of the ask and the changes by date."*

## Closing an item — the Status bullet is part of the close

**Setting `status: completed` in frontmatter is half a close. The note's prose `- **Status**:` bullet is the other half, and it is not optional.** Rewrite it in the same edit, to what is true now: `- **Status**: **Completed YYYY-MM-DD** — <the evidence, one clause>.` Where the item was dismissed rather than delivered, say so (`**Closed YYYY-MM-DD — dismissed, not delivered**`); a close on a promise rather than a completed act says that too.

This applies to **every** path that closes an item — Step 2, Step 2.5, a live-session confirmation, [[Workflows/text-message-sync]] and [[Workflows/m365-to-obsidian-sync]] alike. It also applies to any other field the bullet contradicts: superseded prose is **deleted and replaced**, never left standing under a corrected field (see ## Entry format).

**Why it is a hard rule.** The closing entry is appended to the bottom of the note, and the stale Status bullet stays at the top — so the next reader, human or sync, meets *"Active — nobody has been asked"* on an item that closed five days ago. Between 2026-08-10, when Connor first said this class *"should have been caught,"* and 2026-08-22, **17 notes** accumulated that contradiction, because the check that catches it (`--drift`) only ran in the weekly refresh. It now runs in the default index output too, so Step 0 surfaces it in every mode — but the index catching it after the fact is a backstop, not the fix. The fix is closing the item properly.

## Item creation and update procedure (run after synthesis, or on explicit request)

### Step 0: Build the index (run first, every mode)

```
python3 "Workflows/actions-index.py"            # sweep view: live items + computed candidate lists
python3 "Workflows/actions-index.py" --titles   # every note, "status | filename" — for dedup cross-checks
```

Run from the vault root. This is the **only** full pass over `/Trackers/Actions/` that a sweep should make. It emits ~8 KB instead of the ~430 KB the folder now holds, and it does the date arithmetic — chase-by, 7-day neglect, escalation windows, on-hold trigger dates — so later steps don't have to.

**Then read note bodies ONLY for the files the index names in its candidate lists.** A live item that appears in none of them needs no body read this run. (Added 2026-08-10: reading all 132 bodies every sweep was the single largest cost in the refresh, and ~70% of it was `completed` items that no step acts on.)

**`REDUNDANT BODY FIELDS` (added 2026-08-22)** — any body bullet restating a frontmatter value. Fix it in the run that surfaces it; it is a two-second rename, and leaving it is how 47 accumulated.

**`STATUS CONTRADICTIONS` (added 2026-08-22)** — the index now prints, in **every** mode, any note whose frontmatter `status` disagrees with its prose **Status** bullet. Treat each as a real finding: open it, decide which side is true, correct the loser, and surface it in Step 4. Do not batch-trust the frontmatter — the point of the check is that either side can be the wrong one.

**`OVERSIZED NOTES` (added 2026-08-11)** — the index also flags **live** notes over 15 KB (`BLOAT_KB` at the top of the script). These are not work items and don't belong in the work queue; report them in Step 4 and fix by moving the note's dated history into a companion `-Log.md`, the same pattern as the 2026-08-11 event-note split — **never by deleting content**. Completed notes are exempt, so old history doesn't nag.

**`COMPLETED, UN-ARCHIVED` (added 2026-09-16, the standing rule after the 2026-08-12 sweep fully recurred)** — the index flags any `completed` note whose `resolved` date is more than `ARCHIVE_DAYS` (14) in the past and still sitting in the live `/Trackers/Actions/` folder. **This is the rule the 2026-08-12 one-time cleanup should have been.** Fix it in the run that surfaces it, the same way as OVERSIZED NOTES: move each named note to `/Archive/Actions/`, repoint its inbound wikilinks (grep the vault for `[[Trackers/Actions/<name>]]` first), and log the count in that run's changelog entry — see [[Changelog/2026-08-12-archive-completed-actions]] for the exact method and what "done" looks like. Never delete. If the list is long enough that a full sweep can't clear it in one pass, archive what you can and say so in Step 4 rather than skipping the section.

Two things the index deliberately does **not** decide, because they need a human read:
- Whether an **undated external trigger** on an On Hold item is still alive (the known dead-trigger gap). The index lists only date-locked releases.
- Whether a completion signal is real. It surfaces candidates; Step 2.5 judges them.

### Step 2.5: Completion & confirmation sweep (source-agnostic)

Completion evidence is NOT limited to transcripts. Actions are frequently resolved by email or calendar — and the email→Obsidian sync often writes that evidence straight into a note's own **Status**/**Notes** without ever changing its `status` property. This step catches those so resolved items don't linger (and don't later get wrongly flagged).

Work from **Step 0's index**: the `OPEN CLOSURE CANDIDATES` list plus any item the current run touched. Open bodies only for those. For each note with `status: active` or `status: in-progress` so identified, check for a resolution signal from any available source:
- **The note's own Status/Notes already describe the action as done.** Treat as completion any language such as: "scheduled", "confirmed", "submitted", "sent", "accepted the invite", "complete", "done", "works for me", or an explicit future-but-locked date/time for a "schedule X / set up X meeting" action. This is a pure-text check — no connector needed.
- **Calendar (if accessible):** for any "schedule / set up / hold a meeting" item, a created or accepted event matching the people + topic means the *scheduling* action is complete. (The meeting still occurring later does not keep the scheduling action open — note the meeting date in the Resolved line instead.)
- **Email (if accessible):** a sent email confirming the action ("I submitted…", "sent over…", "confirmed for…"), or an inbound reply confirming the other party has fully delivered ("that's everything I have", "nothing further to send").

When a resolution signal is found:
- Set `status: completed` with a `resolved` date citing the evidence (and source: status note / calendar event / email).
- **Rewrite the note's `- **Status**:` bullet in the same edit** — see ## Closing an item. A frontmatter close over a body that still reads "Active" is the single most common defect in this folder.
- Search other notes' `blocked_by` for this item; surface those as newly unblocked (per Step 2) and clear their `blocked_by`.

Be conservative: a vague or one-sided mention is not completion. If the signal is ambiguous, leave the note's status in place and set `status: closure-candidate` instead (per ### Closure Candidates — entry and exit) — and surface it in the report — rather than auto-closing.

### Step 3: Neglect (flag) sweep

**On Hold items are exempt from this sweep.** Leave them; the Step 3.5 re-activation check handles them instead.

**Short-fuse items are swept first, on the clock, not the calendar.** For each note with `status: active` or `status: in-progress` carrying a **`chase_by`** whose moment has **passed**, flag it immediately — `flagged: "YYYY-MM-DD — reason: chase-by passed ({what it named}) — the window it was waiting on is gone"` — regardless of `last_mentioned` age or the 7-day threshold, and surface it at the top of the Step 4 report with the fallback channel the body names. A short-fuse item is the one case where the sweep can be *too slow by days*, so it is checked before anything else. If `chase_by` has **not** passed, leave the item entirely alone this sweep — do not flag it on `last_mentioned` age; a live short fuse is by definition not neglected.

**Waiting On items ARE swept.** For each note with `status: waiting-on`, measure the wait off its `waiting_on` "since" date. If the awaited party has been quiet **>7 days**, set `status: active`, re-band per ## Priority, and add a note like "awaited {party} {N} days, no response — follow up." Surface the move in the report. If under threshold, leave it.

Step 0's index has already computed this — its `CHASE-BY PASSED` and `NEGLECT CANDIDATES` lists name exactly the notes that qualify. Open those bodies; don't re-scan the folder. For each note the index names (`status: active` or `in-progress`, `last_mentioned` >7 days before today, OR `deadline` passed without completion):
- BEFORE flagging, re-run the Step 2.5 check. If the note's own Status/Notes (or calendar/email evidence) already indicate completion, set `status: completed` instead — do not flag it.
- Also BEFORE flagging, check `blocked_by`. If the blocking item is still active/in-progress (not completed), do NOT flag — it's legitimately waiting on the dependency.
- Also BEFORE flagging, apply the **owner gate** (no-action-no-raise). If `owner` is not Connor *and* the note body names no concrete Connor-side next action, do NOT flag — a flag means *Connor* has neglected something, and it is never raised against another person's item. If Connor is genuinely awaiting a deliverable from that owner, set `status: waiting-on` with `waiting_on` (that party, "since" = today) instead; otherwise leave it untouched.
- Also BEFORE flagging, apply the **window gate**. If the note's action window has not opened yet — it states a future start date or date range before which nothing can be done — do NOT flag. Park it `status: on-hold` with that date as the re-activation trigger (Step 3.5 releases it on the day of). A live future window is not neglect.
- Otherwise, set `flagged: "YYYY-MM-DD — reason: {no follow-up in N days | past deadline by N days}"`. Do not change `status`.

### Step 3.5: Re-prioritization (escalation) sweep

Runs on every update — full and standalone.

**On Hold re-activation check (run first).** For each note with `status: on-hold`, check whether its parking condition has ended. For a **date-locked** item, re-activate **only on the day of** the confirmed date. For an **external-trigger** item, re-activate when the trigger has cleared. On re-activation, set `status: active`, drop `on_hold_since`, and band per ## Priority. Otherwise leave it parked.

**Active → On Hold eligibility check (run second).** The check above only catches the reverse direction (parked items waking up); it does nothing for Active items that have quietly *become* On Hold-eligible mid-sweep. For each note with `status: active` or `status: in-progress`, check whether the do-now stated in its own **Status**/**Notes** has already been satisfied — cross-reference any agenda, event, or calendar note it names, not just the item's own text — leaving nothing further to do until either (a) a confirmed future date/meeting occurs, or (b) an external trigger outside the owner's control clears. This is the same bar as ### On Hold — entry and exit criteria; both conditions there must hold, not just one.
- **Signal to look for:** the item's Notes describe a prep step ("raised it," "added to the agenda," "asked X to put it on the calendar") and a linked note (an Agendas entry, an Events planner, a calendar hit) confirms that step actually happened, and the substantive next move is someone else's during a meeting/date that's already locked.
- **If found:** flip `status: on-hold`, set `on_hold_since` with the trigger and the re-activation condition (date-of or trigger-clears), and add a body line citing the cross-referenced evidence.
- **Be conservative — this is not a demotion tool.** A stale `last_mentioned` alone is not evidence; that's the Step 3 neglect case, not this one. If there is *any* live action the owner could still take right now (ask someone, decide something, draft something, follow up), it stays Active — do not park an item just because it's been quiet or because a meeting is coming up. When in doubt, leave it Active and surface the ambiguity in the Step 4 report rather than parking it.

Step 0's index lists the mechanical candidates under `ESCALATION CANDIDATES` (it applies the windows below and never proposes a downgrade). Confirm each against the note body, then apply. The critical-path floor still needs a body read, since `blocks` semantics depend on whether the blocker is genuinely open. For each candidate, recompute its band per ## Priority:
- **Critical-path floor:** if `blocks` is not empty and the item is itself actionable (not `blocked_by` an item that's still open), its band is at least **P2**.
- **Escalation windows:** measuring against `needs_by` if set, else `deadline`, raise to **P2** within ~3 weeks and **P1** within ~1 week (or critical-path-this-week).
- These only ever **raise** a band. Never auto-lower: a stakeholder override or a higher importance read stands until a stakeholder revisits it.
- When a `blocks`/`blocked_by` relationship changes (e.g., a blocker just completed in Step 2/2.5), recompute both ends.

Be conservative on lowering: if the mechanical read suggests a band should drop, leave it and surface it in the report rather than auto-demoting — a human (or stakeholder) confirms downgrades.

### Step 3.6: Pending-drafts check

Added 2026-09-15, per [[Archive/Actions/Connor - Fix internal escalation — flagged findings and parked drafts don't reach Connor]]. Run:

```
python3 "Workflows/pending-drafts-check.py"
```

It finds every `tags: [..., draft, ...]` file outside `/Archive` whose mtime is ≥5 days old — i.e. a held draft nobody has touched in at least 5 days — and reports it. Detection only; it never writes. This is the class of failure that killed the 2026-07-29 Boot Camp Summer Camp: a correctly-drafted, correctly-held item that nobody ever re-surfaced.

For each hit, open it and sort into exactly one of three buckets — do not just relist the raw output:
- **Genuinely still pending, and live** (e.g. a send-ready leader text nobody has cleared) → surface it in the Step 4 / Start Here report as a real Connor-side action **today**, not a routine finding. This is the one bucket the whole check exists for.
- **Deliberately held on a known trigger, already tracked** (its own body names the trigger and points to an owning Actions item) → leave it. This is the system working as designed, not a gap — don't re-flag what's already correctly parked.
- **Actually resolved** (sent, event already happened, event cancelled) but never re-tagged/archived → this is a housekeeping miss, not a live gap. Drop the stale `draft` tag (`sent`, or whatever's true) if resolution is unambiguous from the file's own content; if resolution requires judgment (e.g. whether to archive the whole file), ask Connor once per batch rather than per file.

### Step 4: Report

After updating, report:
- N items added (with brief descriptions)
- N items moved to in-progress
- N items completed (note which were auto-resolved by the Step 2.5 completion sweep and the evidence source)
- N items now unblocked by those completions
- N items flagged (with reason) and N unflagged
- N items moved to / from on-hold (with the date or trigger — note which direction: newly parked by the Active → On Hold eligibility check vs. reactivated)
- N items moved to / from waiting-on (who is awaited; and any bounced back to active for going quiet >7 days)
- N short-fuse items carrying a live `chase_by` (name the moment and what dies), and N whose `chase_by` has passed and were flagged — these lead the report, ahead of everything else
- N items re-banded by Step 3.5 (old → new band, reason)
- N closure candidates added / confirmed / dismissed (re-list the open ones)
- Any uncertainties where you held off on changing status or band — surface these for human judgment

## Changelog

History lives in [[Changelog/_history/Open-Actions-Tracker-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
