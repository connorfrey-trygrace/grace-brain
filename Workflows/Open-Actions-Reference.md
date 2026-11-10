---
type: workflow
---
# Open Actions — Reference

Schema, field authority, sort order, priority bands and status entry/exit criteria for `/Trackers/Actions/`. Split out of [[Workflows/Open-Actions-Tracker]] on **2026-08-12**.

**Read this only when a specific decision needs it** — a priority band change, a status flip, a closure call, a field conflict. It is not part of the standard read for a sweep.

---

## Storage model

Each action is its own note in `/Trackers/Actions/`, filename `{Owner} - {short action description}.md`. Frontmatter carries the queryable fields; the note body keeps the same human-readable bulleted-metadata format the old tracker used (still authoritative for **reasoning** — see ### Field authority immediately below, which replaced the old blanket "the body always wins" rule on 2026-08-10). `/Trackers/Open Actions.base` provides table views equivalent to the old sections — Closure Candidates, Active, In Progress, Waiting On, On Hold, Flagged/Needs Review, By Project, Completed, All — filtered on the `status` property. **There is no physical "moving" of items between buckets anymore** — changing an item's status is a one-line frontmatter edit (`status: active` → `status: waiting-on`), and the Base view picks it up automatically. Sort order within a view (flagged-first, then priority, then timing — see ## Sort order) is configured in the Base's view definition, not enforced by manual reordering.

### Field authority

**Frontmatter wins for the machine-maintained fields. The body wins for reasoning.** Specifically:

- **Frontmatter is authoritative** for `status`, `priority`, `deadline`, `needs_by`, `chase_by`, `last_mentioned`, `flagged`, `waiting_on`, `on_hold_since`, `blocked_by`/`blocks`. These are what the syncs and sweeps actually maintain, and what [[Trackers/Open Actions.base]] filters and sorts on.
- **The body is authoritative** for the prose **Status** narrative, **Notes**, and any history or rationale. On any question of *why* an item is where it is, the body wins — that is what a human actually wrote.

**Why this replaced "the body always wins" (measured 2026-08-10):** a full comparison across all 132 notes found **44 fields where frontmatter and body disagree**, and in every directional case **the frontmatter was the fresher value** — syncs update `last_mentioned` and escalate `priority` in frontmatter but left the body's bulleted `- **Last mentioned**:` / `- **Priority**:` lines carrying the original text. Under the old rule, a sweep that read bodies would have *rewound* escalated bands (P1 → P2) and *reverted* last-mentioned dates — quietly undoing its own prior work.

### The body explains fields, never restates them

**Field-authority was a rule about who wins a disagreement. It did not stop the disagreements, so the duplication itself is now gone.** As of **2026-08-22** no note body carries a bullet holding a frontmatter *value*. Where the body had reasoning, the bullet was renamed and the literal dropped:

| gone | replaced by |
|---|---|
| `- **Priority**: P2 — <why>` | `- **Priority rationale**: <why>` |
| `- **Deadline**: 2026-09-20 — <why>` | `- **Deadline rationale**: <why>` |
| `- **Needs-by**: 2026-09-06 — <why>` | `- **Needs-by rationale**: <why>` |
| `- **Last mentioned**: <date>` | deleted — pure duplication, no reasoning to keep |
| `- **Added**: <date>` | deleted, or `- **Status history**:` where it carried move history |
| `- **On hold**: …` / `- **Waiting on**: …` | `- **Status history**: …` |

**Never write one of these bullets again**, in any path — a new note, a sync appending a line, a hand edit. `actions-index.py` prints a `REDUNDANT BODY FIELDS` block in **every** mode if one reappears, and Step 0 is not optional, so a reintroduced bullet surfaces on the next sweep.

**The prose `- **Status**:` bullet stays** — it is narrative, not a value, and it is guarded by its own `STATUS CONTRADICTIONS` check. So do `- **Blocked by**:` / `- **Blocks**:`, which carry wikilinked dependency edges the split tooling reads; those are a known, deliberate exception.

### Item schema (frontmatter)

```
---
status: active | in-progress | waiting-on | on-hold | closure-candidate | completed | merged
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

Directly under the frontmatter, an H1 with the original heading text (owner + action, emoji optional), then the checkbox line, then bulleted fields. **Since 2026-08-22 the body carries only what frontmatter cannot**: **Priority rationale**, **Source**, **Deadline rationale**, **Needs-by rationale**, **Status** (prose narrative — where the reasoning and history live), **Status history**, **Notes**, **Blocked by**, **Blocks**. The value-carrying bullets — Priority, Added, Deadline, Needs-by, Last mentioned, Flagged, Waiting on, On hold, Resolved — **are frontmatter only**; see § The body explains fields, never restates them. Not every field applies to every status — Completed items in particular are often looser (just Source/Resolved/Notes), consistent with how the pre-migration tracker treated historical items. When in doubt, prefer writing a complete prose **Status**/**Resolved**/**Notes** line over forcing data into frontmatter that doesn't fit — frontmatter is the index, the body is the record.

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

### Merged — a terminal status, not a live one

`status: merged`, with a `merged_into` frontmatter pointer to the note it was folded into. Used when two action notes turn out to describe the same underlying ask and Connor consolidates them rather than closing one as a duplicate — the merged-away note stays on disk (never delete) but its status says it's no longer independently actionable.

**Entry.** Set `status: merged` + `merged_into: "[[Trackers/Actions/{surviving note}]]"` at the point of consolidation; leave the note live in `/Trackers/Actions/` rather than archiving it, so the merge is visible in context (Connor's 2026-08-17 call — see [[Trackers/Action-Logs]] for the Jennifer Claffey precedent).

**Views.** `merged` has no dedicated Open Actions.base view and is intentionally excluded from every status-filtered one (Active, Waiting On, On Hold, Flagged, Completed) — a merged note is no longer any of those. It remains visible in **All** and **By Project**, which carry no status filter.

**Exit.** None — merged is terminal, like completed. If the merge turns out to be wrong, revert `status` to whatever it was before and remove `merged_into`.
