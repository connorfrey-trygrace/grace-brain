Procedure for synthesizing transcripts tagged "unprocessed".

## Prerequisites

Speaker identification must be complete first. If the transcript still has generic "Speaker A/B/C..." labels, run /Workflows/speaker-identification.md before this workflow.

**Name spelling:** every person named in synthesis output (summary, action items, title, event-note and tracker updates) must use the **canonical-directory spelling** — including people who are only *mentioned*, not speakers. Audio transcription is unreliable for names. **First check the Grace _Office_ Dropbox staff directory**, connected as a Cowork folder at `/Users/connorfrey/Library/CloudStorage/Dropbox/Office/` (`Grace Org Chart.pdf` + `Staff Contact List.xlsx`); use Outlook only as a fallback when a name isn't in that directory. Full procedure + precedence in /Workflows/Speaker-Identification Step 5: **Office staff directory > Outlook > /Contacts > prior transcripts > audio.**

## Step 1: Identify scope

Find all transcripts in /Transcripts with the "unprocessed" tag. Process them one at a time.

## Step 2: For each transcript, generate three artifacts

### Summary (3-5 sentences)

Capture substance, not process. Include:
- What was decided (specific outcomes, not "discussed X")
- Key topics covered with the actual content
- Notable dollar figures, dates, named people, named places
- The thread/arc of the conversation

When the meeting includes a time-sensitive risk or commitment (named deadline, urgent uncovered need, single point of failure on an upcoming event), lead the summary with it rather than burying it at the end.

AVOID:
- Generic phrases like "the team discussed various topics"
- Just listing what was said in order
- Editorializing or interpretation beyond what's in the source

### Action items

Format: `"Owner: Action [by Deadline]"`
- Use real names (post-speaker-identification), spelled per the **canonical staff directory** (see Prerequisites — Office staff directory first, then Outlook) — applies to the owner *and* any other person named in the action
- Omit `by Deadline` if not stated
- Use `"Owner: Unknown"` if genuinely unclear
- Only include EXPLICIT commitments — not implied next steps or possibilities

**Traceability rule (applies to EVERY action item, wherever it is recorded — transcript frontmatter, event notes (Step 5), and the tracker (Step 9)):**

Each action item must be backed by one of two things, and never anything in between:

1. **A direct source** — a specific commitment in the transcript. The item is traceable to a line/speaker (e.g., "X said they'd do Y"). This is the default and the only kind that may be written as an assigned, unqualified action.
2. **An explicit `inferred` tag** — if the item is a *good idea you derived* (from a stakeholder's reasoning, an open question, or a pattern) but **no one actually committed to it**, you may still record it, but it MUST be marked. Prefix it `[inferred]` and state what it was derived from, e.g. `"[inferred] Connor: Shadow a captain session — derived from John's captain-systematization remark + the open greeter-profile question; not a stated commitment."`

Hard prohibitions:
- **Never write a derived/suggested action as if it were an assigned commitment.** If you can't point to where it was committed, it is `[inferred]` or it is not an action item.
- **A self-referential source is not a source.** An action whose only provenance is the event note or tracker it lives in has no real origin — either find the transcript that justifies it or mark it `[inferred]`.
- When in doubt, prefer leaving it as an Open Question (Step 5 / Step 8) over minting an action.

### Topic tags (3-5)

Specific to content. Use kebab-case.
- GOOD: `vendor-selection`, `easter-2027`, `audio-equipment`, `volunteer-coordination`
- BAD: `discussion`, `meeting`, `general`, `important`

## Step 3: Generate a descriptive title

Write a short, human-readable title for the meeting that describes what it was about. This title is used in BOTH the `title` frontmatter field AND the filename (see Step 3.5).

Format: `[Context] — [What happened or what was decided]`

Examples:
- `Connor Shadow Day — Service Operations Orientation`
- `World Cup Watch Party Planning Meeting`
- `Connor Onboarding — Full Planning Meeting`

Rules:
- Prefer noun phrases over gerunds when the meeting had a clear outcome
- Use " — " (space-dash-space) as separator if there's a context/topic split
- Keep it under 10 words
- Avoid characters macOS forbids in filenames: `:` and `/` (em dash `—`, en dash `–`, and `&` are fine and already used in existing filenames)

## Step 3.5: Rename the transcript file to include the title

The transcribe script writes each transcript as a bare timestamp: `YYYY-MM-DD HH.MM.md` (e.g. `2026-06-16 10.03.md`). Synthesis must rename it to append the title, matching the convention used by every processed transcript:

`YYYY-MM-DD HH.MM {Title}.md`  →  e.g. `2026-06-16 10.03 Sunday Night Service — Launch Vision & Operations Planning.md`

- KEEP the existing `YYYY-MM-DD HH.MM` prefix exactly; just append a space and the title. (Some older transcripts have a date-only prefix with no time — preserve whatever prefix is already there.)
- This is a rename/move, not a delete — it does not require the usual "ask before destructive" confirmation.
- **⚠️ Rename FIRST, then write the frontmatter.** `device_bash` cannot delete (`Operation not permitted`), so the natural write-new-then-remove-old pattern strands a duplicate. `os.rename`/`mv` is the only move available, and if you write the titled file first and rename onto it afterwards, the rename **clobbers the frontmatter you just wrote** with the raw original. Order: `mv old → new`, then rewrite `new` in place. (This failure has now occurred twice — 2026-08-11 and 2026-08-17.)
- **Update every wikilink that points at the old bare-timestamp name.** Obsidian links resolve by filename, so a link like `[[Transcripts/2026-06-16 10.03]]` breaks on rename. Search the vault (`/Trackers`, `/Events`, `/Synthesis`, `/Agendas`, other transcripts) for the bare-timestamp link and repoint it to the full new name. When you create NEW links to a just-processed transcript (Steps 5, 9), use the full titled filename from the start.

## Step 4: Update YAML frontmatter

- Set `title` to the generated title
- Set `summary` to the generated summary
- Set `action_items` to the generated list
- Add the new topic tags to the existing `tags` list (don't replace existing tags)
- Change `"unprocessed"` tag to `"processed"`
- Set `processed_date` to today's date (YYYY-MM-DD)
- Add a `people:` array mapping each speaker to `[[People/<Name>]]` (plus `[[People/Good Noodles]]` if peripheral folks appear), per [[Workflows/people-notes]]. Then update the relevant person notes' Meetings sections and the Good Noodles roster, and run the promotion check.

## Step 5: Update relevant event planning notes

After updating the transcript frontmatter, check whether the meeting contains information that should update an existing event planning note in /Events/.

Signs that an event note needs updating:
- The transcript's `event` tag matches an event in /Events/
- Decisions were made that supersede what's currently in the event note (venue, timing, budget, catering, AV, registration, etc.)
- New action items were assigned that aren't yet in the event note
- Open questions in the event note were answered

If an event note needs updating:
- Update the relevant sections (logistics, food, AV, action items, open questions, notes)
- Add/extend the event note's `participants:` frontmatter array with anyone newly involved (`[[People/<Name>]]`), per [[Workflows/people-notes]]
- Add a source reference to the transcript in the Notes section
- Do NOT wholesale replace content — preserve history and context already in the note
- **Action items added here obey the Step 2 Traceability rule.** This is where untraceable actions tend to creep in: it is tempting to convert a stakeholder's reasoning or an open question into a to-do. Don't — unless someone committed to it. If it's your own derivation, either mark it `[inferred]` or (better) leave it in the note's **Open Questions** section rather than its Action Items. An action item whose source would just be this event note is not traceable.

If no event note exists yet but the transcript is clearly scoped to a specific named event, check whether one should be created per /Workflows/event-planning-note.md.

## Step 6: Do NOT modify the body

Only frontmatter changes during synthesis.

## Step 7: Report

For each transcript processed:
- File name
- Number of action items extracted
- Any uncertainties (e.g., action items with "Unknown" owners, ambiguous decisions)
## Step 8: Observations (when warranted)

After processing transcripts, scan the vault for:

- **Stale action items**: Open items from transcripts older than 2 weeks that haven't appeared in newer transcripts. Flag with file reference: "Action 'Brian to confirm budget' from 2026-05-15 — no mention in subsequent meetings."
- **Cross-meeting threads**: If a topic in the new transcript was also discussed in a prior one, link them: "This Easter 2027 budget discussion continues from 2026-05-15 — different conclusion reached."
- **Workflow gaps**: Note anything that took guesswork or improvisation. Propose a workflow file if a pattern is emerging.
- **Open questions**: Things mentioned but not concluded. "Catering options" was raised but no decision made.

Output as an "## Observations" section in your report. If you have nothing actionable, write "No observations this round." Don't manufacture observations to fill space.
## Step 9: Update the open-actions tracker

After synthesis is complete, follow the procedure in /Workflows/open-actions-tracker.md to update `/Trackers/Open Actions.md` with new and existing action items. Include the tracker update report as part of your overall response.

## Step 10: Re-transcription check

Before finalizing, check whether any just-processed transcript covers a source file already present in another processed transcript (single-file or merged). Signs of a re-transcription:

- Same `source_file` value appears in two different `.md` files in /Transcripts or /Archive
- The new transcript's `date` field is later than the existing processed one (indicating it was re-generated)
- Speaker count differs between the two versions (re-transcription may detect more speakers)

If a re-transcription is found:
- Process it normally (it may have improved diarization — e.g., more speakers detected)
- Note the overlap explicitly in your report: which source file, which two transcripts cover it, how they differ
- Do NOT delete or archive the re-transcription without asking

## Changelog

History lives in [[Changelog/_history/Transcript-Synthesis-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
