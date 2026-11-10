# Memory Backup — 16 files (captured 2026-06-25)

Faithful copies of the project's memory files for re-import into the new project. Each block below is one file, delimited by `===== FILE: <filename> =====`. Re-create each as a separate `.md` in the new space's memory dir, then rebuild MEMORY.md from the index block.

===== FILE: MEMORY.md =====
# Memory Index

- [Use Google Maps for business lookups](feedback_business_lookups.md) — use Maps via Chrome MCP, not web search, for phone numbers and addresses
- [Room setup/teardown owner](project_room_setup_owner.md) — Connor owns room setup/teardown on all events through ~Dec 2026; pre-fill this, don't leave TBD
- [transcribe-pending fix](project_transcribe_pending_fix.md) — ~/.zshrc:26; fixed to scan Archive + handle YAML list source_file format; prevents re-transcription after merge
- [Grace staff contacts](reference_grace_staff_contacts.md) — confirmed emails (Derek Adye, Brian Parker, Jennifer Claffey, Connor Frey) + unconfirmed contacts (John, Kay Carter-Corker, Comar, etc.)
- [Calendar is Outlook](project_calendar_is_outlook.md) — use Outlook tools for calendar lookups, not Google Calendar
- [Event form submission](feedback_event_form_submission.md) — never auto-submit Comms/Rock event forms; Connor clears first; keep the two consistent
- [Grace platforms](project_grace_platforms.md) — Grace uses BOTH Rock and Planning Center; "Planning Center" ≠ Rock
- [AVL lead is Jean Paul](reference_avl_lead_jean_paul.md) — audio lead spelled "Jean Paul" (J-E-A-N), NOT "John Paul"; don't re-normalize
- [Steve Coy spelling](reference_steve_coy_spelling.md) — worship pastor is "Steve Coy" (C); transcripts render "Koy" — normalize to Coy
- [Decide minor calls yourself](feedback_decide_minor_yourself.md) — act on clear/authoritative answers; only escalate when genuinely unknowable
- [Office staff directory is name authority](reference_office_staff_directory.md) — Dropbox/Office/ Grace Org Chart.pdf + Staff Contact List.xlsx = canonical spelling source
- [Transcript filename titles](feedback_transcript_filename_titles.md) — rename processed transcripts to include the title; repoint wikilinks (Workflow Step 3.5)
- [Push notes additively](feedback_push_notes_additively.md) — proactively sync tracker changes into event/planner notes; only add, never subtract or change
- [Sean Liesegang phone](reference_sean_liesegang.md) — 703-732-6696 = Sean Liesegang, Men's Cohort member / World Cup volunteer
- [Connor's writing voice](reference_connor_writing_voice.md) — clear/structured/action-oriented email style (from Copilot); tuned for business email, adapt for casual/church-facing

===== FILE: feedback_business_lookups.md =====
---
name: feedback_business_lookups
description: "Use Google Maps (via Claude in Chrome) for business contact lookups, not web search"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 34bef227-f8a3-4ce1-bec7-036c6466ebd8
---

Use Google Maps via the Claude in Chrome MCP for phone numbers, addresses, and business details — not web search.

**Why:** Connor finds Google Maps more reliable for this type of current business information.

**How to apply:** Any time a task requires finding a phone number, address, or hours for a local business, use `mcp__Claude_in_Chrome__navigate` to Google Maps instead of WebSearch.

===== FILE: project_room_setup_owner.md =====
---
name: project_room_setup_owner
description: Connor is the default owner for room setup and teardown on all events through December 2026
metadata: 
  node_type: memory
  type: project
  originSessionId: f99e3680-d661-445b-8e69-1569910de9b5
---

Connor is the default owner for room setup and teardown on all Grace events through approximately December 2026 (stated 2026-06-08).

**Why:** Connor told me to assume this for the next 6 months — don't leave room setup/teardown as TBD on new event notes.

**How to apply:** When creating or updating any event planning note, assign "Connor" as the owner in the Room setup / teardown logistics row. No need to ask.

===== FILE: feedback_event_form_submission.md =====
---
name: feedback-event-form-submission
description: Never auto-submit event request forms; Connor reviews/clears first; keep Comms + Rock forms consistent
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 872d4f93-9e95-4f46-8ef8-afad494e6e6f
---

For both event-request forms — Grace Comms Request (ClickUp) and Event Registration Request (Rock) — fill the fields but **never submit without summarizing all values to Connor and getting explicit clearance.** Connor submits or authorizes each submission.

Also prioritize internal consistency between the two forms: title, date, time, location, and event summary/blurb must match across them (Rock's Event Summary is literally meant to mirror the Comms blurb).

**Why:** These are external-facing submissions (comms team + Rock admin Kay Carter-Corker act on them); errors or mismatches create downstream cleanup and confusion.

**How to apply:** Follow [[grace-staff-contacts]] for Kay's address. Defaults: Billing Code 8106 (always confirm), Account "Event Registration". Full procedure in /Workflows/rock-event-request.md.

===== FILE: project_grace_platforms.md =====
---
name: project_grace_platforms
description: Grace uses both Rock and Planning Center as platforms
metadata: 
  node_type: memory
  type: project
  originSessionId: 00c3843e-391c-42da-a858-9f34c970ff67
---

Grace uses BOTH Rock (rockcloud.com — event comms requests via the ClickUp form, registration) AND Planning Center. They are different platforms, not a naming slip. When Connor references "Planning Center," do not assume he means Rock. See [[feedback_event_form_submission]] for the Rock/Comms form handling.

===== FILE: reference_grace_staff_contacts.md =====
---
name: grace-staff-contacts
description: "Grace staff names, emails, and roles — sourced from Outlook calendar attendee data"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5c72608d-95ea-4ec9-a28c-7991c899c676
---

**Domain rule:** All Grace staff emails are **@trygrace.org** — never .com (confirmed by Connor 2026-06-15). Pattern is firstname.lastname@trygrace.org.

Confirmed from Outlook calendar (June 2026):

| Name | Email | Role |
|------|-------|------|
| Connor Frey | connor.frey@trygrace.org | Event Coordinator (Connor = the user) |
| Derek Adye | derek.adye@trygrace.org | Director (marketing/events oversight, occasional preacher) |
| Brian Parker | brian.parker@trygrace.org | AV / Tech |
| Jennifer Claffey | jennifer.claffey@trygrace.org | Event Operations / Sunday Captain |
| Michele Smith | michele.smith@trygrace.org | Finance/admin — handles Capital One credit card account. NOTE: spelled "Michele" (one L); Connor refers to her as "Michelle" |

**Other contacts mentioned in transcripts (email unconfirmed):**
- John Slye — Senior Pastor; john.slye@trygrace.org (confirmed via Outlook 2026-06-15)
- Kay Carter-Corker — kay.cartercorker@trygrace.org (confirmed by Connor 2026-06-15; fits firstname.lastname pattern. Transcripts had variant spellings "kcartercorker@trygrace.com"/".org" — those are wrong) — Volunteer Rock/ROC admin who processes Event Registration Requests; fully retired staff, super flexible
- Matt Komar — Grace facilities/room booking contact; email TBD (confirmed full name 2026-06-10)
- Maria Hernandez — Spanish translation coordinator; 40 translators across 3 services
- Stephanie — Sunday Captain (morning)
- CJ — Usher volunteer willing to work both Sunday morning and Sunday night
- Mary — Usher team lead; will not share Sunday morning volunteers without a separate ask
- Ben Mallott — External sound tech contractor (10+ years); unavailable for Chandler Moore concert

**How to apply:** Pre-fill names and emails when drafting communications, action items, or event notes. Use these to resolve speaker labels when diarization produces generic Speaker A/B/C labels — cross-reference with Outlook calendar attendee lists for meeting-specific confirmation.

===== FILE: project_calendar_is_outlook.md =====
---
name: project-calendar-is-outlook
description: "Connor uses Outlook for both calendar and email — not Google Calendar/Gmail"
metadata: 
  node_type: memory
  type: project
  originSessionId: 73a818a6-cd45-42cf-8fb2-57b251316f58
---

Connor's calendar lives in **Outlook**, not Google Calendar. For any calendar lookup, use the Outlook calendar tools (e.g. outlook_calendar_search). Do NOT use the Google Calendar connector — it returned no events when checked on 2026-06-15 because the data isn't there.

**Email also = Outlook.** Connor confirmed 2026-06-16 that Outlook is always the preferred email platform — draft/search/send via Outlook, never Gmail (despite his personal gmail address). Codified as an EMAIL rule in CLAUDE.md.

**Why:** Calendar confirmed by Connor 2026-06-15 after a gcal lookup came back empty; email confirmed 2026-06-16.
**How to apply:** Default to Outlook for both calendar and email. Also codified as CALENDAR and EMAIL rules in the vault's CLAUDE.md (RULES section).

===== FILE: feedback_transcript_filename_titles.md =====
---
name: transcript-filename-titles
description: "Processed transcripts must be renamed to include the title in the filename, not just frontmatter"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8b3d0ea3-1a83-4035-b366-107482b5f7de
---

When synthesizing a transcript, the descriptive title goes in BOTH the `title` frontmatter field AND the filename. The transcribe script outputs a bare timestamp (`YYYY-MM-DD HH.MM.md`); synthesis must rename it to `YYYY-MM-DD HH.MM {Title}.md` (keep the timestamp prefix, append the title). This matches every existing processed transcript.

**Why:** Connor flagged on 2026-06-16 that the day's processed transcripts had no title in their filenames. The old Transcript-Synthesis Step 3 wrongly said the title "is not the filename."

**How to apply:** Follow /Workflows/Transcript-Synthesis.md Step 3.5 — rename the file AND repoint every wikilink (Obsidian links resolve by filename, so `[[Transcripts/2026-06-16 10.03]]` breaks on rename). When creating new links to a freshly processed transcript, use the full titled filename from the start. Renaming is a move, not a delete — no destructive-change confirmation needed. Related: [[transcribe-pending-fix]].

===== FILE: feedback_push_notes_additively.md =====
---
name: feedback_push_notes_additively
description: "Proactively push updates into event/planner notes when relevant; only add, never subtract or change"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 051e5e63-5b25-4c54-a048-dcf16925ffde
---

When tracker changes have implications for the related event planning/planner notes (e.g. [[Events/2026-09-20-Sunday-Night-Service-Launch]] and its Planner), Connor wants me to proactively push those updates into the event notes — don't just offer.

**Why:** Keeps the roster and Open Questions in the event notes in sync with [[Trackers/Open Actions.md]] without him having to ask each time.

**How to apply:** Only **add** to the event notes (new note lines, annotations, Open Questions). Never **subtract or change** existing content/decisions. Confirmed 2026-06-21.

===== FILE: project_transcribe_pending_fix.md =====
---
name: transcribe-pending-fix
description: "transcribe-pending shell function location, what was fixed, and why it re-transcribed already-processed files"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5c72608d-95ea-4ec9-a28c-7991c899c676
---

`transcribe-pending` is defined in `~/.zshrc` at line 26. It reads from `~/Recordings/` and writes to the Obsidian vault's `/Transcripts/` folder.

**Root cause of duplicate transcriptions, found 2026-06-22 (CORRECTION to the 2026-06-10 note below):** the `vault_dir`/`archive_dir` in `~/.zshrc` were NEVER actually repointed to Dropbox — they still pointed to the empty old `~/Documents/Vaults/Obsidian Vault 1/{Transcripts,Archive}`. So the dedup scan read an empty folder, matched nothing, and re-transcribed the entire backlog on every run (the script writes output to Dropbox via the Python `VAULT_DEFAULT`, so dups landed in Dropbox). Fix: set `vault_dir`/`archive_dir` to `$HOME/Library/CloudStorage/Dropbox/Vaults/Obsidian Vault 1/...`. Also fixed a latent bug: merged files store `source_file` as a *double-quoted* YAML list, but the extraction never stripped quotes (and the trailing `"` defeated the audio-extension filter) — added a `sed -E 's/^"(.*)"$/\1/'` quote-strip before the ext filter. Connor applies the `~/.zshrc` edit on his machine (not reachable from sandbox). The 37 untitled re-transcription dups were removed by Connor via `rm` (sandbox can't delete from the Dropbox FUSE mount).

**Vault relocated 2026-06-10**: Vault moved from `~/Documents/Vaults/Obsidian Vault 1` to `~/Library/CloudStorage/Dropbox/Vaults/Obsidian Vault 1` (now Dropbox-synced). Updated the hardcoded `vault_dir` (line 28) and `archive_dir` (line 29) in `~/.zshrc` accordingly; backup at `~/.zshrc.bak`. Cowork working folder is now the Dropbox path.

**Output-path fix 2026-06-16**: The `~/.zshrc` `vault_dir`/`archive_dir` vars only control the *dedup scan*, NOT where transcripts are written. Output location is set by `~/scripts/transcribe_to_obsidian.py` → `VAULT_DEFAULT` (the function calls the script without `--vault`, so the default wins). That default was still `~/Documents/Vaults/Obsidian Vault 1/Transcripts`, so new transcripts landed in the OLD vault and never synced — and would get re-billed since dedup scans Dropbox. Fixed by changing `VAULT_DEFAULT` to the `~/Library/CloudStorage/Dropbox/...` path (sed swap of `"Documents" / "Vaults"` → `"Library" / "CloudStorage" / "Dropbox" / "Vaults"`). Connor runs the edit himself (his machine; not reachable from the sandbox).

**Fix applied 2026-06-08**: The skip check originally only scanned `/Transcripts/*.md` for `source_file:` entries and only handled single-line YAML. Two bugs:
1. After merging, source filenames move to `/Archive/` — so they were invisible to the skip check, causing re-transcription
2. Merged transcripts write `source_file:` as a YAML list (`  - filename`), which the original grep never matched

**Fix**: Added `/Archive/` to the grep scope; added a second grep pass for `  - ` list items; filtered both passes to audio file extensions to avoid false matches on other YAML fields (speaker names, etc.).

**Why:** Connor has `~/Recordings/` as the source dir. After a merge+archive cycle, the source audio files remain in `/Recordings/` but the skip list no longer contains them. The fix makes the skip list authoritative across both Transcripts and Archive.

**How to apply:** See `~/.zshrc` line 26. The Python one-liner used to apply it is in the June 8 conversation transcript.

===== FILE: reference_steve_coy_spelling.md =====
---
name: steve-coy-spelling
description: "Worship pastor's name is spelled Steve Coy (C), not Koy; audio transcripts render Koy — normalize"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 55fd91e7-8e3b-4a5c-a883-f54ec0807bed
---

The morning worship pastor (and the contact Connor is routing 4th-service / Sunday-night worship recruiting through) is **Steve Coy** — spelled with a **C** ("Coy"). Connor confirmed 2026-06-22.

AssemblyAI transcripts render the audio as "Steve **Koy**" (K) — e.g. in [[Transcripts/2026-06-16 17.35 ...]] and [[Transcripts/2026-06-22 11.20 ...]]. Do NOT propagate "Koy" into synthesis output, summaries, event notes, or the tracker; normalize to "Coy". Leave transcript bodies as-is (don't edit transcript body content). Same transcription-variant pattern as [[reference_avl_lead_jean_paul]].

===== FILE: reference_avl_lead_jean_paul.md =====
---
name: reference-avl-lead-jean-paul
description: "Grace's current AVL/audio lead is spelled \"Jean Paul\" (not \"John Paul\")"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8b3d0ea3-1a83-4035-b366-107482b5f7de
---

Grace's current AVL / audio lead — Sunday-morning, Sunday-night, and internal events — is spelled **Jean Paul** (J-E-A-N). Confirmed emphatically by Connor on 2026-06-16 and corroborated by the Archive 2024 Dixon/Feliz concert doc.

A 2026-06-15 system audit wrongly normalized the name to "John Paul"; Connor reversed that on 2026-06-16. Use "Jean Paul" everywhere it's a live reference. Do NOT re-normalize to "John Paul." Distinct from John Slye (pastor) and John Randolph (BQ logistics contact).

**Full name (Grace Org Chart, 2/11/2026): JeanPaul Tauler** — surname **Tauler**; the org chart renders the first name solid ("JeanPaul"). "Jean Paul" (two words) stays the everyday first-name reference per Connor; both are the same person. The canonical staff directory lives in the Grace **Office** Dropbox folder (`Grace Org Chart.pdf` + `Staff Contact List.xlsx`) — the first-line name-spelling authority (see [[steve-coy-spelling]] and the speaker-ID/synthesis workflows).

Related: [[reference_grace_staff_contacts]].

===== FILE: feedback_decide_minor_yourself.md =====
---
name: feedback-decide-minor-yourself
description: "Connor: make the call on minor/clear-answer decisions yourself; only escalate when the answer is genuinely unknowable from the sources"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 55fd91e7-8e3b-4a5c-a883-f54ec0807bed
---

Connor doesn't want to be pulled in for minor decisions when an authoritative source already answers them. Decide and act; only come back to him when the answer is **genuinely unknowable** from available sources.

**Why:** he said (2026-06-22) "Things like this are minor and I don't think I should need to intervene unless you genuinely don't know the answer," re: the "Brian Sulk → Sulc" fix and the "JeanPaul Tauler vs Jean Paul" question — both resolvable from the Grace Org Chart.

**How to apply:** if the canonical staff directory (Office folder), /Contacts, prior transcripts, email/calendar, or a clear rule settles it → just do it and note what you did (reversible). Reserve questions for true ambiguity or high-stakes/destructive calls. Don't batch trivial confirmations. Related: [[steve-coy-spelling]], [[reference-avl-lead-jean-paul]].

===== FILE: reference_office_staff_directory.md =====
---
name: reference-office-staff-directory
description: Canonical Grace staff directory + name-spelling authority lives in the Dropbox Office folder
metadata: 
  node_type: memory
  type: reference
  originSessionId: 55fd91e7-8e3b-4a5c-a883-f54ec0807bed
---

The canonical Grace staff directory is in the **Dropbox `Office` folder, now permanently connected as a Cowork folder** at `/Users/connorfrey/Library/CloudStorage/Dropbox/Office/` (in bash it appears under the session mount, e.g. `…/mnt/Office/`). Connected 2026-06-23; persists across sessions, so don't re-request access — just Read/Grep it.
- **`Grace Org Chart.pdf`** — full names + titles (org chart dated 2/11/2026). Reads directly via the Read tool.
- **`Staff Contact List.xlsx`** — names + emails/phones. Dropbox cloud-synced: if a **bash** command errors on it (cloud-only / "Resource deadlock avoided" / BadZipFile), use the **Read tool** (downloads on demand) or have Connor right-click → "Make available offline"; the org chart PDF reads directly regardless.

This is the **first-line spelling authority** for the speaker-identification and synthesis workflows (ahead of Outlook, which has no contacts API and can be disconnected). Precedence: Office staff directory > Outlook > /Contacts > prior transcripts > audio. Org-chart facts: Lead Pastor **John Slye**, Exec Pastor **Derek Adye**, Worship Pastor **Steve Coy** (also Co-Director Racial Unity, with **Julie Coy**), Safety Team Lead **Brian Sulc** (not "Sulk"), Audio Technician **JeanPaul Tauler**, Database Manager **Kay Carter-Corker**. Related: [[steve-coy-spelling]], [[reference-avl-lead-jean-paul]], [[feedback-decide-minor-yourself]].

===== FILE: reference_connor_writing_voice.md =====
---
name: connor-writing-voice
description: "Connor's email/writing voice profile (from Copilot) — clear, structured, action-oriented; with caveat on register"
metadata: 
  node_type: memory
  type: reference
  originSessionId: fd7a9944-0a16-4d98-b53f-43821bba8f1d
---

Connor's writing voice, per a Copilot-generated style guide he provided (2026-06-23). Source register is **professional/business email** (logistics/network-modeling context). Use this as the baseline for work emails; adapt the register for warm/spoken/church-facing contexts, which are looser and more personal than this guide.

**Core principles:** Direct and explicit (no ambiguity on next steps); structured/skimmable; action-oriented; professional but approachable; concise (cut filler).

**Standard structure:** Opening (context + purpose, 1–2 sentences) → Body (structured: bullets or numbered) → Closing (explicit ask). His most common pattern is **Context → Key Points → Next Steps**.

**Body conventions:**
- Updates: bullets labeled "What was done / found / why it matters" under a header like "Key updates:".
- Analysis: logical sequence — Goal → Approach → Result → Implication.
- Assigning work: explicit owner per line ("Connor: finalize X", "Jim: review Y"), with timing if relevant.

**Closing — defining trait:** explicit ask. Prefers "Please let me know any questions." / "Please confirm alignment on this approach." / "Please review and provide feedback by [date]." Avoids "Let me know if you have questions."

**Preferred phrases:** "Key updates:", "Summary:", "At a high level:", "Next steps:", "Please review…", "Please confirm…", "To clarify:", "Specifically:", "This means:".

**Tone:** Confident, assertive but not aggressive; no hedging ("I think maybe we could…"); collaborative inclusive language ("We'll align on…", "Let's confirm…"); no over-apologizing.

**Avoids:** Vague requests ("thoughts?"); long unstructured paragraphs; polite filler ("just checking in…"); passive phrasing ("it might be good to…"); ambiguous ownership.

**Caveat (Claude's note):** The guide above is tuned for structured business email. It does NOT fit warm, casual, spoken/group-message contexts (Sunday intros, men's-ministry group texts), which are playful and personal — bullets and "Next steps:" would be wrong there.

---

## Casual / church-facing register (from a men's "boot camp" group message, 2026-06-23)

This is a distinct, vivid voice — keep it separate from the business profile. Characteristics observed:

- **Punchy fragments and one-liners**, not full structured paragraphs. Lines stand alone: "Roll call!" / "Been quite a while."
- **Themed/playful framing** carried throughout: military/camp metaphor for a men's ministry group ("Boot camp leaders!", "boot camp summer camp", tagline "Don't go AWOL," "going AWOL"). He leans into a motif and runs with it.
- **Warm, communal, inviting tone** — "There seems to be a hunger to reconvene as men," "would love to hear everyone's thoughts," "serve the men's community."
- **Self-aware and humble** — labels his own brainstorm honestly: "Pardon the thought vomit, just trying to get everyone's ideas down." Doesn't pretend to have it all figured out.
- **Still decisive underneath the casual tone** — frames open items as "Critical decision:" and "secondary decision:", and reasons out loud ("Presumably this would be In July. Enough time to plan, but not redundantly close to next session."). The business-voice clarity/directness survives; the corporate scaffolding does not.
- **Concrete, low-friction call to action** — "drop your thoughts in the chat or give me a call," includes his phone number.
- **Conversational asides and ellipses**, em-dashes, casual capitalization. Not buttoned-up; reads like he's talking.

**How to write in this register:** short punchy lines; pick a theme/motif and play with it; warm and inclusive; name your own uncertainty rather than faking polish; still surface the real decisions clearly; end with an easy, specific ask. Drop headers, bullets-as-tasks, and "Please confirm alignment."

Add to / refine this memory as more samples are observed.

===== FILE: reference_sean_liesegang.md =====
---
name: reference-sean-liesegang
description: "Phone 703-732-6696 = Sean Liesegang, Grace Men's Cohort member / World Cup volunteer"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0564596b-d3da-450a-baae-7aacf000fafe
---

The number **703-732-6696** (+17037326696) is **Sean Liesegang**, a Grace Men's Cohort member. Identified by Connor 2026-06-25 after he followed up on Connor's setup/teardown recruitment blast for the 7/19 World Cup Watch Party. Use this when resolving contacts during text-message scans (see [[project_calendar_is_outlook]] context for the Grace second-brain). Not yet in the Office Staff Contact List or Contacts/Vendors.
