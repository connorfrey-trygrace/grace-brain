---
type: workflow
---
# Open Actions — Steps 1–2 (transcript mode only)

Split out of [[Workflows/Open-Actions-Tracker]] on **2026-08-12**. **Only read in full-update mode** (after synthesis on a new transcript). A standalone sweep never runs these steps.

Run after Step 0 and before Step 2.5; both are documented in [[Workflows/Open-Actions-Tracker]]. Field definitions are in [[Workflows/Open-Actions-Reference]].

---

### Step 1: Add new items

**This duplicate-check is mandatory for every path that adds an item, not just post-transcript full updates.** It applies identically when [[Workflows/text-message-sync]] Step 5 or [[Workflows/m365-to-obsidian-sync]] adds an item from a text or email. Search `/Trackers/Actions/` (all statuses, including completed) for a substantively identical item — same owner + same essential action, judged by substance not exact wording — before creating a new note.

For each new action item (from a transcript, text, or email):
- If a substantively identical note already exists anywhere in `/Trackers/Actions/`, update its `last_mentioned` (and Notes, if there's new detail) instead of creating a duplicate note.
- Otherwise, create a new note in `/Trackers/Actions/` with `status: active` and full frontmatter, including a **priority** band (see ## Priority).

**Priority assignment checklist (run before assigning any band):**
1. Was this item directly assigned by Connor, John, or Derek? If yes → **P1** floor, unless the assignor explicitly said otherwise. Record the override in the body's `- **Priority rationale**:` line — the rationale, never the band literal (see [[Workflows/Open-Actions-Reference]] § The body explains fields, never restates them).
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
- If completion is indicated (done, sent, spoke with, confirmed), set `status: completed`, add a `resolved` date, **and rewrite the note's `- **Status**:` bullet to match** — see [[Workflows/Open-Actions-Tracker]] § Closing an item. Half a close is how 17 notes ended up reading "Active" under a `completed` field.
- If the item is superseded or canceled, set `status: completed` with a note about what replaced it.
- When flipping a note to completed, search all other notes' `blocked_by` for a reference to this one. If found, surface these in your report as newly unblocked: "Items now unblocked by completion of {item}: {list}" and clear their `blocked_by`.

Be honest about confidence. If you're unsure whether something counts as completion, leave the item's status where it is and surface the uncertainty in your report.
