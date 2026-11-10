---
type: changelog-history
governs: "[[Workflows/Transcript-Synthesis]]"
tags: [changelog]
---
# Transcript-Synthesis-changelog — changelog (pre-2026-08-12 history)

Split out of the procedure file on **2026-08-12** so procedure text stays cheap to read. **Never read on a normal run.** New changes go in their own dated file under `/Changelog/`, not here.

---

## Changelog
- 2026-06-03: Initial creation — 7-step procedure for synthesizing unprocessed transcripts (summary, action items, tags, observations, tracker update), tier 1, trigger: Connor's request
- 2026-06-03: Added "lead with time-sensitive risk" rule to Step 2 summary guidance — when a meeting contains a named deadline, urgent uncovered need, or single point of failure, lead the summary with it rather than burying it, tier 2, trigger: Connor's request (Chandler Moore framing change)
- 2026-06-03: Added `processed_date: YYYY-MM-DD` to Step 3 frontmatter updates — set to today's date when synthesis completes. Tier 2. Trigger: observation during weekly synthesis run (mtime proxy identified as fragile).
- 2026-06-08: Added Step 8 (Re-transcription check) — transcription function can re-process already-synthesized source files if the originals weren't removed from /Recordings before re-running; this step catches and handles that case. Tier 2. Trigger: observed during June 8 synthesis run (June 2 source files re-transcribed after prior session merged and archived them).
- 2026-06-09: Added Step 3 (title generation) and renumbered subsequent steps — `title` is now a required frontmatter field generated during synthesis. Tier 2. Trigger: Connor's request to add descriptive titles to all transcripts and make it a standard processing step.
- 2026-06-09: Added Step 5 (update relevant event planning notes) — after processing a transcript, check /Events/ for a matching event note and update it with any decisions, resolved questions, or new action items from the meeting. Tier 2. Trigger: Connor's observation that the World Cup event note was stale after the June 9 planning meeting.
- 2026-06-16: Fixed a title/filename contradiction. Step 3 previously said the generated title "is not the filename," but every processed transcript carries its title in the filename. Corrected Step 3 and added **Step 3.5 (rename the transcript file to `YYYY-MM-DD HH.MM {Title}.md` and repoint any wikilinks)**. Tier 1 (corrected a contradiction that left two transcripts as bare timestamps). Trigger: Connor noticed the 2026-06-16 transcripts had no title in their filenames.
- 2026-06-17: Added a **Traceability rule** to Step 2 (Action items) and reinforced it in Step 5 (event-note updates). Every action item — in transcript frontmatter, event notes, or the tracker — must either trace to a direct transcript commitment or be explicitly prefixed `[inferred]` with its derivation; a self-referential source (an action whose only provenance is the note/tracker it lives in) is not valid provenance, and derived ideas default to Open Questions rather than action items. Tier 2 (new rule). Trigger: Connor — the "Shadow Jennifer on a captain session" action was synthesizer-inferred but written as an assigned commitment with a self-referential source; it rang no bell and was archived.
- 2026-06-22: Added an **Outlook name-spelling rule** (Prerequisites + Step 2 Action items) — all names in synthesis output, including people only mentioned, must use the Outlook-verified spelling (audio transcription is unreliable for names); mirrors /Workflows/Speaker-Identification Step 5. Tier 2 (new rule). Trigger: Connor's request, prompted by the "Steve Koy" (audio) vs "Steve Coy" (correct) split.
- 2026-06-22: **Made the Grace _Office_ Dropbox staff directory (`Grace Org Chart.pdf` + `Staff Contact List.xlsx`) the first-line spelling source, with Outlook as fallback** (Prerequisites + Step 2). Tier 2 (changed rule). Trigger: Connor pointed me to the Office folder as the canonical directory.
- 2026-06-23: Recorded the **concrete connected path** for the Office staff directory (`/Users/connorfrey/Library/CloudStorage/Dropbox/Office/`) in Prerequisites, now that the folder is mounted as a Cowork folder. Tier 1 (path). Trigger: Connor connected the Office folder.
