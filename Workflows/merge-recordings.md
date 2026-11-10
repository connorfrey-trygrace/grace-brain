# Workflow: Merge Split Recordings

Procedure for combining two or more transcripts that are really **one meeting** recorded as separate files (e.g., recording stopped and resumed, or a clip plus the full session). This is Job #4 in [[CLAUDE.md]].

## When to use
- Two transcripts cover the same meeting, split by a pause or a stop/restart.
- A short "clip" and a longer "full" recording overlap the same conversation.
- Connor explicitly asks to merge named files.

## Hard rule: ASK FIRST
Merging archives the source transcripts, which is a destructive-ish change. **Confirm with Connor before merging** — which files, and the intended merged title. Do not merge unprompted just because two transcripts look related.

## Step 1: Confirm the pieces belong together
Verify the files are the same meeting, not two meetings on the same day. Check `date`, `source_file`, speakers, and opening/closing context. If genuinely unsure, ask rather than merge.

## Step 2: Build the merged transcript
- Create one new transcript file. Title per [[Workflows/Transcript-Synthesis]] Step 3.
- **Body:** concatenate the parts in chronological order. Insert a divider between independently-diarized segments:
  `--- Part 2 (recording resumed after pause) ---`
  Diarization is independent per part — "Speaker A" in Part 1 is **not** necessarily "Speaker A" in Part 2. Keep the parts visually separated so [[Workflows/Speaker-Identification]] can treat each as its own puzzle.
- **`source_file`:** list **every** original filename as a YAML list, so re-transcription detection and the `transcribe-pending` script can see all sources:
  ```yaml
  source_file:
    - "Meeting ...A.mp4"
    - "Meeting ...B.mp4"
  ```
- **`duration_minutes`:** sum of the parts.
- **`speakers`:** union of all parts, deduplicated by real-world identity (after speaker ID).
- Carry `tags` (keep `unprocessed` until synthesis runs) and `event`.

## Step 3: Run speaker identification, then synthesis
Run [[Workflows/Speaker-Identification]] on the merged file (handling each Part separately), then [[Workflows/Transcript-Synthesis]] as normal.

## Step 4: Archive the originals (never delete)
Move each original source transcript to `/Archive` (and `/Archive/Events` for event notes if relevant). Never delete. The merged file is now the live record.

## Step 5: Guard against re-transcription
Because originals are archived rather than deleted, the transcription pipeline can re-process the same audio later. Two safeguards:
- The `transcribe-pending` script scans `/Archive` and handles the YAML-list `source_file` format so already-merged audio isn't re-transcribed (see memory note on the `~/.zshrc` fix).
- [[Workflows/Transcript-Synthesis]] Step 10 (re-transcription check) catches any that slip through.

## Step 6: Report
- The merged file (with link) and the originals archived
- Final speaker list and any remaining "Unknown" speakers
- Any overlap or contradiction between the parts worth noting

## Changelog

History lives in [[Changelog/_history/merge-recordings-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
