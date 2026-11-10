Maintain `/Trackers/Actions/` — one note per action item — as the single source of truth for action items across all transcripts, with `/Trackers/Open Actions.base` as the aggregated view over that folder.

**Migrated 2026-07-21** from a single `/Trackers/Open Actions.md` file (heading blocks inside status sections) to one note per action (frontmatter properties + a Base for views). See ## Changelog for what changed and why. All logic below (priority rubric, escalation windows, flagging, on-hold/waiting-on/closure-candidate rules) is unchanged from the prior version — only the storage mechanism and the mechanics of each step changed.

## Modes

This workflow runs in two modes:
- **Full update** (default, triggered after synthesis on a new transcript): Run Steps 1, 2, 2.5, 3, 3.5, 4.
- **Standalone sweep** (triggered by the weekly safety-net task, the on-demand quick-refresh routine, or explicit request without a new transcript): Run Step 2.5 (Completion & confirmation sweep), Step 3 (Neglect/flag sweep), Step 3.5 (Re-prioritization sweep), and Step 4 (Report). Skip Steps 1-2 since there's no new transcript to process.

When triggering, the caller specifies the mode. If not specified, assume full update if a transcript is referenced, otherwise standalone.

**Standalone-sweep side duties (run by the weekly `grace-weekly-refresh` task, not the on-demand quick-refresh, and not part of full updates):** alongside the sweep itself, that task also runs (a) the **Run Log health check** defined in [[Workflows/m365-to-obsidian-sync]] § Run Log health check, and (b) a **scheduler heartbeat**: one `list_scheduled_tasks` call comparing each Grace task's `lastRunAt` against its cadence per [[Trackers/Automation]], flagging any job overdue by more than one full cycle as an Active note in `/Trackers/Actions/` (same flagged-item pattern as the health check; search for an existing flag on the same job before adding one; ignore non-Grace and expired-temporary tasks). See [[Trackers/Automation]] for the current schedule of both the weekly safety net and the on-demand quick refresh.

## Storage model

Each action is its own note in `/Trackers/Actions/`, filename `{Owner} - {short action description}.md`. Frontmatter carries the queryable fields; the note body keeps the same human-readable bulleted-metadata format the old tracker used (still authoritative — if a frontmatter field and the body ever disagree, the body wins, since it's what a human actually wrote/reasoned through). `/Trackers/Open Actions.base` provides table views equivalent to the old sections — Closure Candidates, Active, In Progress, Waiting On, On Hold, Flagged/Needs Review, By Project, Completed, All — filtered on the `status` property. **There is no physical "moving" of items between buckets anymore** — changing an item's status is a one-line frontmatter edit (`status: active` → `status: waiting-on`), and the Base view picks it up automatically. Sort order within a view (flagged-first, then priority, then timing — see ## Sort order) is configured in the Base's view definition, not enforced by manual reordering.

### Item schema (frontmatter)

```
---
status: active | in-progress | waiting-on | on-hold | closure-candidate | completed
priority: P1 | P2 | P3
owner: "{Owner}"
added: YYYY-MM-DD
deadline: "YYYY-MM-DD, 'Implied {context}', or 'Unstated'"
needs_by: "YYYY-MM-DD (latest start) or omitted"
last_mentioned: "YYYY-MM-DD"
resolved: YYYY-MM-DD                      # Completed items only
flagged: "YYYY-MM-DD — reason: ..."       # omit unless currently flagged
waiting_on: "{party} since YYYY-MM-DD — what's awaited"   # Waiting On items only
chase_by: "YYYY-MM-DD HH:MM ET — what dies if it passes"    # short-fuse items only (see ### Waiting On)
on_hold_since: "YYYY-MM-DD — trigger: ..."                 # On Hold items only
source: "[[link to originating transcript]] or email/calendar citation"
blocked_by: "[[Trackers/Actions/{other item's filename}]]" # real wikilink where resolvable, else the plain description
blocks: "[[Trackers/Actions/{other item's filename}]]"     # same
projects:
  - "{cross-cutting theme, e.g. Sunday Night Launch, World Cup}"
---
```

`blocked_by`/`blocks` should be real wikilinks whenever the referenced item is itself tracked in `/Trackers/Actions/` — this is new since the migration (the old tracker used plain-text descriptions because heading-anchor links were fragile; individual notes make the link stable). Only fall back to plain text when the reference is to something outside the tracker (e.g. "Chandler Moore rescheduling" — a real-world trigger, not an action item).

### Item body

Directly under the frontmatter, an H1 with the original heading text (owner + action, emoji optional), then the same bulleted fields the old schema used — **Priority**, **Source**, **Added**, **Deadline**, **Needs-by**, **Status** (prose narrative — this is where the actual reasoning/history lives, same as before), **Last mentioned**, **Notes**, **Blocked by**, **Blocks**, **⚠️ Flagged**, **⏳ Waiting on**, **On hold since**, **Resolved**. Not every field applies to every status — Completed items in particular are often looser (just Source/Resolved/Notes), consistent with how the pre-migration tracker treated historical items. When in doubt, prefer writing a complete prose **Status**/**Resolved**/**Notes** line over forcing data into frontmatter that doesn't fit — frontmatter is the index, the body is the record.

## Sort order

Within the Active and In Progress Base views, items are ordered **flagged-first, then Priority, then timing** (configured in the view's sort rules, but the *logic* Connor should expect is):
0. **⚠️ Flagged items first** — anything carrying a `flagged` property sorts above even P1. Neglect is meant to be the loudest thing on the list.
1. **Priority band** — among unflagged items, P1 at the top, then P2, then P3.
2. **Timing within a band** — within a single priority band, order by how early the action can or must be performed (earliest first).

Priority is the primary key among unflagged items, on purpose: an item with a near deadline but low priority (e.g., the Planning Center workflow, which Connor flagged low) stays in the P3 band rather than floating to the top on timing alone. See ## Priority for how to assign the band.

## Priority

Every Active / In Progress note carries a **priority** of **P1**, **P2**, or **P3**. Priority is a function of **two factors scored separately** — not a loose blend of four:

**Factor 1 — Importance (intrinsic).** How much rides on it, *including whether it sits on the critical path*. An item is **high-importance** if it is keystone / make-or-break for an event, OR it **blocks one or more other open actions** (see the `blocks` field). Minor assists that nothing depends on are low-importance. Importance does not fade just because the deadline is far off.

**Factor 2 — Time pressure.** How soon it must be **started**, not just finished. Judge against the item's lead time: a task due Sept 20 that needs four weeks of runway becomes time-pressing in late August, not the day before. Capture this with an optional **needs_by** date (the latest it can start and still land on time); fall back to the raw **deadline** when none is set.

**Band = the more severe of the two reads:**
- **P1 — Critical / now.** On the critical path this week, inside its P1 escalation window (below), or explicitly flagged top by a stakeholder. Keep this band small so it stays meaningful.
- **P2 — Important.** High importance — keystone **or blocks other work** — even with a long lead. This is the **critical-path floor**: an item that blocks another open action never sits below P2 once it is actionable. Also P2 for anything inside its P2 escalation window.
- **P3 — Low / deferred.** Reserved for items that are **both** low-importance **and** not time-pressing. **Long lead time alone does not make something P3** — only the combination of low importance and no time pressure does.

**Tension rule.** When importance and time pressure disagree, **importance sets the floor and time pressure can only raise the band, never lower it.** A high-impact item with a far deadline is at least P2; it is not demoted to P3 for being early.

**Stakeholder override.** An explicit call from **Connor, John, or Derek** overrides the mechanical read in either direction. If Connor says "low priority," it's P3 even with a near deadline (the Planning Center workflow is the canonical case). Record the override in the item's **Status** (body) or **Notes** with who set it; it stands until that stakeholder revisits it.

**Escalation windows** (applied on every sweep — see Step 3.5), measured off **needs_by** when present, else **deadline**:
- → **P2** when within ~3 weeks.
- → **P1** when within ~1 week, or on the critical path this week.

Escalation and the critical-path floor only ever **raise** a band; they never auto-lower one.

## Status values and their entry/exit criteria

### On Hold — entry and exit criteria

`status: on-hold`. An item belongs here, not Active, when **both** hold:
- It has a real, still-valid origin (passes the Step 1 source-validity gate) and is **not** complete or superseded; and
- There is **nothing for the owner to do right now** because it is either (a) locked to a confirmed future date (e.g., the van orientation confirmed for 6/28 — the scheduling is done; the session itself is the only remaining action), or (b) waiting on an external trigger outside the owner's control (e.g., the Chandler Moore concert being rescheduled before a sound-tech search can resume).

On Hold is **not** for items that are merely low-priority, far off, or un-filed — those stay Active with the appropriate band. A long lead time alone does not qualify; there must be no actionable step until the date/trigger. Set `on_hold_since` with the reason and the trigger.

**Exit:** flip `status` back to `active` (re-banding per ## Priority) only when its parking condition actually ends — for a **date-locked** item, on the **day of** the confirmed date (not earlier); for an **external-trigger** item, when the trigger clears. Move to `status: completed` if it resolves while parked. On Hold items are **exempt from the Step 3 stale sweep and the Step 3.5 escalation sweep** while parked; the only sweep that touches them is the date/trigger re-activation check below.

### Waiting On — entry and exit criteria

`status: waiting-on`. An item belongs here, not Active, when the ball is currently in **someone else's** court (Connor has done his part and is awaiting their response) **and** Connor can chase them if they go quiet.

**Entry:** flip an Active item's `status` to `waiting-on` once Connor's next step is done and the next move is the other party's. Set `waiting_on` naming the party and the "since" date.

**Exit — two paths:**
- **They respond / the ball returns to Connor:** flip `status` back to `active` (re-band per ## Priority).
- **They go quiet past the neglect threshold (Step 3):** flip `status` back to `active` with a note like "awaited {party} {N} days, no response — follow up." Don't also add a flag — the note already makes the neglect visible.

#### Short-fuse carve-out — when NOT to park an item in Waiting On

Waiting On's only exit-on-silence mechanism is the **7-day** quiet threshold in Step 3. That is the wrong instrument for an item whose whole remaining window is hours or a couple of days: parking it removes it from the Active view at exactly the moment it is live, and the sweep that would rescue it fires days after the opportunity is gone.

**Rule.** Before flipping an item to `waiting-on`, compute its **remaining window** — the earliest of `needs_by`, `deadline`, or an explicit window named by the awaited party in their own reply (e.g. *"I can do today before 2 or tomorrow before noon"*). **If the remaining window is shorter than 7 days, do NOT flip it. Keep `status: active`** and instead:
- set **`chase_by`** to the moment the current option dies, with what dies — e.g. `chase_by: "2026-08-10 13:00 ET — Jennifer's today-before-2 window closes; only tomorrow-before-noon left"`;
- record in the body that the ball is the other party's, naming them and the time it went out (the Waiting On *fact* is still worth writing down — it's only the status flip that's wrong here);
- state the fallback channel in the body, because the point of a chase-by is that Connor does something different when it passes, not that he waits harder. Per memory, **Connor works remotely — the escalation channel is text, then a call, never an in-person nudge.**

**Set `chase_by` on short-fuse items regardless of status.** It is not exclusive to this carve-out: any Active item where a specific clock (not a deadline, a *clock*) governs the next move can carry one.

**Exit.** Clear `chase_by` when the awaited party responds, when the window it names has passed and the item has been re-planned around the next one (set a new `chase_by` if there is one), or when the item completes.

Unlike On Hold, Waiting On is **not** exempt from the Step 3 neglect sweep or Step 3.5 escalation.

### Flagging — entry and exit criteria

Neglect does **not** change `status`. The item stays exactly where it is (active or in-progress) and gets a `flagged` property set, which the Base's sort rule pushes to the top of its view (above even P1 — see ## Sort order).

**Entry.** Per Step 3, when an item with `status: active` or `status: in-progress` has gone >7 days without a newer `last_mentioned`, or its `deadline` has passed, set `flagged: "YYYY-MM-DD — reason: {no follow-up in N days | past deadline by N days}"`. Do **not** change `status`.

**Exit — three paths:**
- **Completion evidence turns up** (Step 2.5, run before flagging and again on every subsequent sweep): flip to `status: completed`; clear `flagged`.
- **Connor reactivates/updates it** (new information, a decision to keep chasing, etc.): clear `flagged`. Simply mentioning or updating the item is enough — flags don't require a special "unflag" command.
- **Connor cancels/drops it:** flip to `status: completed` with a `resolved` date and a note that it was cancelled.

**A flagged item blocking another item is still a live block** — the same "don't mark the downstream item neglected while its blocker is legitimately open" logic applies regardless of whether the blocker itself is flagged.

### Closure Candidates — entry and exit

`status: closure-candidate`. A Closure Candidate is a pointer, not really a status change to the underlying item's substance — it flags an active/in-progress/waiting-on/on-hold item that an automated sync believes is **complete** but is **not** authorized to close on its own (the text sync never closes items — it can only suggest, see [[Workflows/text-message-sync]] Step 5; the email sync auto-closes only clear completions, see [[Workflows/m365-to-obsidian-sync]]).

**Entry.** A sync (or a manual pass) sets `status: closure-candidate` on the note and appends to **Notes** the evidence (source + date) and what to verify before closing. Don't duplicate — if a note already carries a closure-candidate flag, append the new evidence to its Notes instead of creating anything new.

**Exit — Connor's call:**
- **Confirm** → `status: completed`, add `resolved` + a Notes line citing the evidence, clear any `blocked_by` references to this item on other notes (surfacing anything newly unblocked).
- **Dismiss** → revert `status` to whatever it was before (active/in-progress/waiting-on/on-hold). Optionally append a dated Notes line explaining why it wasn't done.

**Sweeps.** On every standalone sweep, re-list open candidates (`status: closure-candidate`) in the report so they don't sit unseen. A candidate is **never** auto-confirmed by the passage of time.

## Item creation and update procedure (run after synthesis, or on explicit request)

### Step 1: Add new items

**This duplicate-check is mandatory for every path that adds an item, not just post-transcript full updates.** It applies identically when [[Workflows/text-message-sync]] Step 5 or [[Workflows/m365-to-obsidian-sync]] adds an item from a text or email. Search `/Trackers/Actions/` (all statuses, including completed) for a substantively identical item — same owner + same essential action, judged by substance not exact wording — before creating a new note.

For each new action item (from a transcript, text, or email):
- If a substantively identical note already exists anywhere in `/Trackers/Actions/`, update its `last_mentioned` (and Notes, if there's new detail) instead of creating a duplicate note.
- Otherwise, create a new note in `/Trackers/Actions/` with `status: active` and full frontmatter, including a **priority** band (see ## Priority).

**Priority assignment checklist (run before assigning any band):**
1. Was this item directly assigned by Connor, John, or Derek? If yes → **P1** floor, unless the assignor explicitly said otherwise. Record the override in the body's Priority line.
2. Does this item block one or more other open actions? If yes → **P2** floor minimum.
3. Is the needs-by or deadline within ~1 week? If yes → **P1**.
4. Is the needs-by or deadline within ~3 weeks? If yes → **P2** floor.
5. After applying all floors, assign the highest band triggered.

**Source validity gate (Traceability rule — mirrors [[Workflows/Transcript-Synthesis]] Step 2).** Before creating any note, check its `source`:
- The `source` must point to a **transcript** (or external evidence: email/calendar) where the action was actually committed. A `source` that points only to an **event note or another action note is self-referential and invalid** — it means the action has no real origin.
- If an item arrives with only a self-referential source, do NOT create it as an assigned action. Either trace it to the transcript that justifies it, or — if it's a derived idea no one committed to — record it `[inferred]` in the description with what it was derived from, or push it back to the event note's Open Questions.
- Never promote a derived/suggested idea into an unqualified assigned action.

### Step 2: Update existing items based on the new transcript

Read the new transcript body. For each note with `status: active` or `status: in-progress`:
- If the new transcript mentions the item or its substance, update `last_mentioned`. If it was flagged, clear the flag — a mention is itself evidence the item isn't neglected, whether or not the underlying task has moved forward.
- If progress is mentioned but not completion, set `status: in-progress`.
- If completion is indicated (done, sent, spoke with, confirmed), set `status: completed` and add a `resolved` date.
- If the item is superseded or canceled, set `status: completed` with a note about what replaced it.
- When flipping a note to completed, search all other notes' `blocked_by` for a reference to this one. If found, surface these in your report as newly unblocked: "Items now unblocked by completion of {item}: {list}" and clear their `blocked_by`.

Be honest about confidence. If you're unsure whether something counts as completion, leave the item's status where it is and surface the uncertainty in your report.

### Step 2.5: Completion & confirmation sweep (source-agnostic)

Completion evidence is NOT limited to transcripts. Actions are frequently resolved by email or calendar — and the email→Obsidian sync often writes that evidence straight into a note's own **Status**/**Notes** without ever changing its `status` property. This step catches those so resolved items don't linger (and don't later get wrongly flagged).

For each note with `status: active` or `status: in-progress`, check for a resolution signal from any available source:
- **The note's own Status/Notes already describe the action as done.** Treat as completion any language such as: "scheduled", "confirmed", "submitted", "sent", "accepted the invite", "complete", "done", "works for me", or an explicit future-but-locked date/time for a "schedule X / set up X meeting" action. This is a pure-text check — no connector needed.
- **Calendar (if accessible):** for any "schedule / set up / hold a meeting" item, a created or accepted event matching the people + topic means the *scheduling* action is complete. (The meeting still occurring later does not keep the scheduling action open — note the meeting date in the Resolved line instead.)
- **Email (if accessible):** a sent email confirming the action ("I submitted…", "sent over…", "confirmed for…"), or an inbound reply confirming the other party has fully delivered ("that's everything I have", "nothing further to send").

When a resolution signal is found:
- Set `status: completed` with a `resolved` date citing the evidence (and source: status note / calendar event / email).
- Search other notes' `blocked_by` for this item; surface those as newly unblocked (per Step 2) and clear their `blocked_by`.

Be conservative: a vague or one-sided mention is not completion. If the signal is ambiguous, leave the note's status in place and set `status: closure-candidate` instead (per ### Closure Candidates — entry and exit) — and surface it in the report — rather than auto-closing.

### Step 3: Neglect (flag) sweep

**On Hold items are exempt from this sweep.** Leave them; the Step 3.5 re-activation check handles them instead.

**Short-fuse items are swept first, on the clock, not the calendar.** For each note with `status: active` or `status: in-progress` carrying a **`chase_by`** whose moment has **passed**, flag it immediately — `flagged: "YYYY-MM-DD — reason: chase-by passed ({what it named}) — the window it was waiting on is gone"` — regardless of `last_mentioned` age or the 7-day threshold, and surface it at the top of the Step 4 report with the fallback channel the body names. A short-fuse item is the one case where the sweep can be *too slow by days*, so it is checked before anything else. If `chase_by` has **not** passed, leave the item entirely alone this sweep — do not flag it on `last_mentioned` age; a live short fuse is by definition not neglected.

**Waiting On items ARE swept.** For each note with `status: waiting-on`, measure the wait off its `waiting_on` "since" date. If the awaited party has been quiet **>7 days**, set `status: active`, re-band per ## Priority, and add a note like "awaited {party} {N} days, no response — follow up." Surface the move in the report. If under threshold, leave it.

For each note with `status: active` or `status: in-progress` where `last_mentioned` is >7 days before today, OR where `deadline` has passed without completion:
- BEFORE flagging, re-run the Step 2.5 check. If the note's own Status/Notes (or calendar/email evidence) already indicate completion, set `status: completed` instead — do not flag it.
- Also BEFORE flagging, check `blocked_by`. If the blocking item is still active/in-progress (not completed), do NOT flag — it's legitimately waiting on the dependency.
- Otherwise, set `flagged: "YYYY-MM-DD — reason: {no follow-up in N days | past deadline by N days}"`. Do not change `status`.

### Step 3.5: Re-prioritization (escalation) sweep

Runs on every update — full and standalone.

**On Hold re-activation check (run first).** For each note with `status: on-hold`, check whether its parking condition has ended. For a **date-locked** item, re-activate **only on the day of** the confirmed date. For an **external-trigger** item, re-activate when the trigger has cleared. On re-activation, set `status: active`, drop `on_hold_since`, and band per ## Priority. Otherwise leave it parked.

**Active → On Hold eligibility check (run second).** The check above only catches the reverse direction (parked items waking up); it does nothing for Active items that have quietly *become* On Hold-eligible mid-sweep. For each note with `status: active` or `status: in-progress`, check whether the do-now stated in its own **Status**/**Notes** has already been satisfied — cross-reference any agenda, event, or calendar note it names, not just the item's own text — leaving nothing further to do until either (a) a confirmed future date/meeting occurs, or (b) an external trigger outside the owner's control clears. This is the same bar as ### On Hold — entry and exit criteria; both conditions there must hold, not just one.
- **Signal to look for:** the item's Notes describe a prep step ("raised it," "added to the agenda," "asked X to put it on the calendar") and a linked note (an Agendas entry, an Events planner, a calendar hit) confirms that step actually happened, and the substantive next move is someone else's during a meeting/date that's already locked.
- **If found:** flip `status: on-hold`, set `on_hold_since` with the trigger and the re-activation condition (date-of or trigger-clears), and add a body line citing the cross-referenced evidence.
- **Be conservative — this is not a demotion tool.** A stale `last_mentioned` alone is not evidence; that's the Step 3 neglect case, not this one. If there is *any* live action the owner could still take right now (ask someone, decide something, draft something, follow up), it stays Active — do not park an item just because it's been quiet or because a meeting is coming up. When in doubt, leave it Active and surface the ambiguity in the Step 4 report rather than parking it.

For each note with `status: active` or `status: in-progress`, recompute its band per ## Priority:
- **Critical-path floor:** if `blocks` is not empty and the item is itself actionable (not `blocked_by` an item that's still open), its band is at least **P2**.
- **Escalation windows:** measuring against `needs_by` if set, else `deadline`, raise to **P2** within ~3 weeks and **P1** within ~1 week (or critical-path-this-week).
- These only ever **raise** a band. Never auto-lower: a stakeholder override or a higher importance read stands until a stakeholder revisits it.
- When a `blocks`/`blocked_by` relationship changes (e.g., a blocker just completed in Step 2/2.5), recompute both ends.

Be conservative on lowering: if the mechanical read suggests a band should drop, leave it and surface it in the report rather than auto-demoting — a human (or stakeholder) confirms downgrades.

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
- 2026-08-10: Added a **short-fuse carve-out** to the Waiting On criteria (new `#### Short-fuse carve-out` subsection), a new **`chase_by`** frontmatter field, a clock-based check at the head of Step 3, and a matching Step 4 report line. **The gap:** Waiting On's only exit-on-silence mechanism is a 7-day quiet threshold, so an item whose remaining window is *hours* gets parked out of the Active view at the moment it matters and is rescued days too late. An item is now kept Active with a `chase_by` when its remaining window — `needs_by`, `deadline`, or **a window the awaited party named in their own reply** — is shorter than 7 days; a passed `chase_by` flags immediately regardless of `last_mentioned` age, and a live one exempts the item from age-based flagging. Tier 2 (new field + entry-criteria carve-out + sweep rule). Trigger: Connor, 2026-08-10 — the 11:57 quick refresh hit the case live on [[Archive/Actions/Connor - Schedule the Kay + Jennifer Planning Center setup sync]] (Jennifer offered "today before 2 or tomorrow before noon", Connor relayed to Kay at 11:36, ~2 hours of runway), the run left it Active against the letter of the rule and surfaced the gap, and Connor said to build it in. **Not changed: `/Trackers/Open Actions.base`** — short-fuse items stay Active and flag through the existing flagged-first sort, so no view definition needed editing; a `chase_by` column on the Active view would surface the clock without a flag, worth adding if Connor wants it.
- 2026-07-21 (4): Added an **Active → On Hold eligibility check** to Step 3.5, run second (after the existing On Hold re-activation check). Previously Step 3.5 only caught the reverse direction — parked items waking up — so an Active item whose stated do-now had quietly been satisfied (nothing left but a confirmed future date/external trigger) had no rule surfacing it; it had to be caught by manually cross-referencing linked notes. New check: for each Active/In Progress item, cross-reference any agenda/event/calendar note its Notes cite to see if the prep step described has actually happened, and if so — and if the On Hold entry criteria are otherwise met — park it. Explicitly conservative (a stale `last_mentioned` alone doesn't qualify; that's Step 3's job). Tier 2 (new sub-step, no schema change). Trigger: Connor asked for a manual On Hold audit of the 20 live Active items; found one real case — [[Archive/Actions/Brian - Confirm Sunday night AVL plan; loop in on security]] had its only do-now ("add lighting to the 7/22 Seth-call agenda") already done per the linked Agendas note, with nothing left until that call — reclassified to On Hold, and Connor asked for the gap to be closed so it's caught automatically going forward.
- 2026-07-21 (3): **Migrated from a single `/Trackers/Open Actions.md` file to one note per action** in `/Trackers/Actions/`, with `/Trackers/Open Actions.base` providing the aggregated views (Closure Candidates, Active, In Progress, Waiting On, On Hold, Flagged/Needs Review, By Project, Completed, All), mirroring the pattern already in use for [[Events/2026-07-29-Boot-Camp/Boot-Camp-Leaders-Roster]]. All 107 items (20 Active, 1 In Progress, 11 On Hold, 75 Completed) migrated, including full history — Connor chose consistency over leaving Completed behind. `Blocked by`/`Blocks` are now real wikilinks between notes where resolvable (only one reference in the whole set didn't resolve — "Chandler Moore rescheduling," a real-world trigger, correctly left as plain text). Rewrote every "section" reference in this workflow as a `status` property; rewrote the item schema as frontmatter + body; the underlying priority rubric, escalation windows, flagging, and on-hold/waiting-on/closure-candidate criteria are **unchanged in substance** — only the storage mechanism and step mechanics changed. Rewrote all 43 heading-anchor cross-links and 127 whole-file links across the vault (Workflows, Agendas, Events, People, Synthesis, CLAUDE.md) to point at the new notes/Base; fixed 3 pre-existing stale links found during the sweep (unrelated to this migration — they'd gone stale from earlier heading renames). The original file is preserved at [[Archive/Open Actions (pre-Bases migration, archived 2026-07-21)]]. Tier 3 (new storage model + full procedure rewrite). Trigger: Connor's request — the single-file model made "moving" an item between sections a heading-block cut/paste, made heading text fragile (had to stay verbatim forever for anchor links to survive), and gave no way to filter across projects/themes. Bases fixes all three.
- 2026-07-21 (2): Tightened the Step 1 duplicate-check so it's mandatory for **every** path that adds an item — text-sync ([[Workflows/text-message-sync]] Step 5) and email-sync ([[Workflows/m365-to-obsidian-sync]]), not just post-transcript full updates — and widened the check scope from Active-only to the whole tracker. Trigger: Connor noticed recurring duplicates in the live tracker; the clearest live case (two near-identical "missed m365 sync run" items for adjacent time slots, 7/15 and 7/16) had already been manually merged/closed the same day. Tier 2 (procedure tightening, no schema change).
- 2026-07-21: **Retired the standalone Stale section.** Neglected items no longer move to a separate bucket — they stay in Active/In Progress and get a `**⚠️ Flagged**` line instead (new schema field), which sorts them to the top of their section, above P1 (new ## Sort order rule 0). Renamed Step 3 "Stale sweep" → "Neglect (flag) sweep"; updated Steps 2/2.5/3.5/4 and the item schema accordingly; added "### Flagging — entry and exit criteria". Migrated all 7 live Stale items into Active with ⚠️ Flagged lines. Tier 2 (structural change — removes a section, adds a field). Trigger: Connor — the Stale bucket was "a catch-all he had to remember to separately check"; flagging in place surfaces neglect on the list Connor already works from daily, instead of a bucket he has to remember exists.
- 2026-07-03: Added a plain checkbox line (`- [ ]` / `- [x]` on Completed) under every item heading, restating the heading text — purely additive so Tasks-plugin/Dataview can index and check off items without any schema rewrite. Headings, bulleted metadata, and all heading-anchor cross-links (e.g. `[[Trackers/Open Actions#...]]`) are unchanged. Explicitly rejected a full checkbox-line migration (collapsing each item onto one Tasks-syntax line): items carry paragraph-length Notes and a dozen metadata fields Tasks has no field for, and converting headings to task lines would break every existing anchor link into this tracker. Migrated all 81 existing items in the live tracker. Tier 2 (additive schema field). Trigger: Connor installed the Tasks and Dataview community plugins and wanted to use them. **Superseded 2026-07-21** — the checkbox-line concern this rejected is moot now; each item has its own note.
- 2026-06-03: Initial creation — procedure for maintaining /Trackers/Open Actions.md as single source of truth for action items across all transcripts, tier 1, trigger: Connor's request
- 2026-06-03: Added "## Modes" section — distinguishes full update (Steps 1-4, post-synthesis) from standalone stale sweep (Steps 3-4 only, no transcript). Tier 2. Trigger: Connor's scheduling setup.
- 2026-06-10: Added "## Sort order" section — Active items must be ordered by how early the action can/must be performed, earliest first. Tier 2. Trigger: Connor's explicit instruction.
- 2026-06-15: Added **Priority** field (P1/P2/P3) to the item schema and a new "## Priority" section defining the band rubric. Tier 2. Trigger: Connor's request.
- 2026-06-15: Added Step 2.5 "Completion & confirmation sweep (source-agnostic)". Tier 2. Trigger: Connor — leadership check-in was scheduled but stayed Active because completion was only ever detected from transcripts.
- 2026-06-17: Added a **Source validity gate** to Step 1. Tier 2 (new gate). Trigger: Connor — the "Shadow Jennifer on a captain session" action entered the tracker with a self-referential event-note source and no real origin; archived.
- 2026-06-21: Added a **Waiting On** section/status and an **On Hold** section/status with their entry/exit criteria. Tier 2. Trigger: Connor's request.
- 2026-06-30: Added explicit **Priority assignment checklist** to Step 1. Tier 2. Trigger: Connor — comms request was added at P2 despite being directly assigned by Derek.
- 2026-06-16: Made the Priority rubric two-factor and self-escalating (importance + time pressure scored separately, critical-path floor, Needs-by field, Blocks field, escalation windows, tension rule, Step 3.5). Tier 2. Trigger: Connor's request.
- 2026-07-16: Documented the sweep task's **side duties** — the m365 Run Log health check and a scheduler heartbeat, plus a daily-including-weekends cadence with an event-week-only weekend gate. Tier 2. Trigger: 2026-07-16 advisory-board audit (Finding 1), approved by Connor. **Superseded 2026-07-21** — see [[Trackers/Automation]] for the current weekly-safety-net + on-demand quick-refresh cadence.
