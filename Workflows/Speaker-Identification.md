Procedure for identifying speakers in transcripts before synthesis.

## Step 1: Analyze for clues

Read the transcript body. Look for:
- Names mentioned ("Thanks, John", "as Sarah said...")
- Roles referenced ("as the pastor...", "our finance person...")
- Self-identifications ("Hi, this is Connor...")
- Topics tied to specific people based on context

## Step 1.5: Cross-reference vault sources (when body clues aren't enough)

If Step 1's clues don't clearly resolve every speaker, check these sources in order — cheapest and most local first, escalating only as needed:

1. **`/People/*.md`** — small folder; each note is a curated hub stating role, duties and aliases. Grep for keywords surfaced in Step 1 (a task, a distinctive phrase, a name mentioned). Often decisive on its own.
2. **`/Trackers/Calendar-Window.md`** — cross-check the transcript's date/time against known scheduled meetings and attendees. Run `python3 "Workflows/calendar-window.py" --check` first (free — reads the cache, no API call). **If the window's `generated` date is before the transcript's own `date`, refresh live** (one Outlook calendar search over the ~3-week window) before trusting the file — a cache generated the day before won't contain a meeting added same-day. Also refresh if `--check` reports past its own staleness threshold. If the live refresh fails (connector disconnected), fall back to the stale cache with a noted caveat rather than blocking identification on it. When a run is processing more than one unprocessed transcript, refresh once for the run, not once per transcript. **Coverage is partial** — not every real meeting lives on Connor's Outlook calendar (some are informal/ad hoc or live on a colleague's calendar instead); a hit is strong evidence, but absence is not evidence the meeting didn't happen.
3. **`/Trackers/Actions/`** — grep (not a full read) for distinctive phrases, roles, or dates from the transcript. The folder is large, but grep itself is cheap and only matched files get read in full. Often the single most decisive source when someone is assigned a specific, dated task matching the transcript's content.
4. **Prior `/Transcripts`** — grep for matching names, topics, or phrasing, only if still ambiguous after the above.
5. **Live connectors (Outlook calendar/email search)** — last resort, since each is an external round-trip that can return large, unfiltered results. (This is separate from the targeted Calendar-Window refresh in step 2, which is scoped and cheap.)

## Step 2: Handle merged transcripts (edge case)

If the transcript contains a "--- Part 2 (recording resumed after pause) ---" divider, treat each side as a SEPARATE identification puzzle. The diarization for Part 1 and Part 2 was independent — Speaker A in Part 1 is not necessarily Speaker A in Part 2. Identify each part's speakers separately, then unify by real-world identity at the end.

## Step 3: Present findings as a table

| Section | Label | Best guess | Confidence | Evidence |
|---|---|---|---|---|
| — | A | Connor | High | Self-identified at 0:42 |
| — | B | Pastor John | Medium | Referenced as "Pastor" by Speaker C |
| — | C | Unknown 1 | — | No name or role found |

- For merged transcripts, "Section" is "Part 1" or "Part 2". For single-recording transcripts, use "—".
- For unidentified speakers, use "Unknown 1", "Unknown 2", etc. with unique numbers across the transcript.
- **Pre-verify spellings in Outlook before presenting** (per Step 5's Outlook check) so the names in the table are already correctly spelled, not raw audio guesses — Connor is confirming identity, not proofreading the transcriber.

## Step 4: Wait for confirmation

Ask the user to confirm or correct each row. Do NOT proceed until they respond.

## Step 5: Rename throughout

Once confirmed:
- Update the YAML "speakers" list with real names, deduplicated
- **Name format:** use full name (First Last) on first identification. If only a first name is known, use that consistently. Match the spelling already used in /Contacts and prior transcripts so the same person isn't recorded as both "Jennifer" and "Jennifer Claffey." Watch for transcription variants of one person (e.g. a recording may render the audio lead as "John Paul," but the real spelling is "Jean Paul") and normalize to the real spelling.
- **Verify every spelling against the canonical staff directory (authoritative).** Before finalizing a name, confirm its spelling.
    - **First-line source — the Grace _Office_ Dropbox folder**, connected as a Cowork folder at **`/Users/connorfrey/Library/CloudStorage/Dropbox/Office/`** (in bash it appears under the session mount, e.g. `…/mnt/Office/`): **`Grace Org Chart.pdf`** (full names + titles; reads directly) and **`Staff Contact List.xlsx`** (names + emails/phones). The xlsx is Dropbox cloud-synced — if a bash command errors on it, it's cloud-only, so use the **Read tool** (downloads on demand) or have Connor make it available offline; the org chart PDF reads directly regardless. This is the **primary** authority: official, local, and connector-independent.
    - **Second-line — Outlook** (only if a name isn't in the Office directory): there's no contacts API, so use `outlook_email_search` (`sender`/`recipient`/`query`) or `outlook_calendar_search` (`attendee`/`query`); the email **display name + address** (@trygrace.org) is canonical. Note the Outlook connector can be disconnected and need reconnecting.
    - **Spelling precedence: Office staff directory > Outlook directory > /Contacts > prior transcripts > the audio transcript** (audio is least reliable — e.g. "Steve Koy" → **Steve Coy**, "John Paul" → **Jean Paul**). Preserve deliberate normalizations recorded in memory/`/Contacts`. If a source reveals a correction, also fix `/Contacts/Vendors` so the vault stays consistent. (Calendar/email are Outlook, not Google — see [[CLAUDE.md]].)
- Find-and-replace EVERY occurrence of "Speaker A", "Speaker B", etc. in the body with the confirmed names
- For merged transcripts, Part 1 and Part 2 may rename to different names for the same label

## Step 6: Report completion

Provide:
- File(s) processed
- Final speaker list
- Any speakers that remain "Unknown" (will need manual identification later)

## Changelog

History lives in [[Changelog/_history/Speaker-Identification-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
