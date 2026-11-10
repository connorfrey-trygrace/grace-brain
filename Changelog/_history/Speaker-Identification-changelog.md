---
type: changelog-history
governs: "[[Workflows/Speaker-Identification]]"
tags: [changelog]
---
# Speaker-Identification-changelog — changelog (pre-2026-08-12 history)

Split out of the procedure file on **2026-08-12** so procedure text stays cheap to read. **Never read on a normal run.** New changes go in their own dated file under `/Changelog/`, not here.

---

## Changelog
- 2026-06-03: Initial creation — procedure for identifying and renaming generic Speaker A/B/C labels before synthesis, including merged-transcript edge case handling, tier 1, trigger: Connor's request
- 2026-06-15: Added name-format convention to Step 5 (full name on first ID, consistent spelling matched to /Contacts, normalize transcription variants). Tier 2 (new rule). Trigger: 2026-06-15 system audit, approved by Connor.
- 2026-06-22: Added an **Outlook spelling-verification rule** — every name must be checked against Outlook (via `outlook_email_search` / `outlook_calendar_search`, since there's no contacts API; the email display name + address is canonical) before finalizing, with precedence Outlook > /Contacts > prior transcripts > audio; pre-verify before presenting the Step 3 table. Tier 2 (new rule). Trigger: Connor's request, prompted by the "Steve Koy" (audio) vs "Steve Coy" (correct) split.
- 2026-06-22: **Promoted the Grace _Office_ Dropbox staff directory (`Grace Org Chart.pdf` + `Staff Contact List.xlsx`) to the FIRST-line spelling authority, ahead of Outlook.** It's the official, local, connector-independent source; Outlook is now the second-line fallback. New precedence: Office staff directory > Outlook > /Contacts > prior transcripts > audio. Tier 2 (changed rule). Trigger: Connor pointed me to the Office folder; org chart confirmed "Steve Coy" and surfaced corrections (e.g. "Brian Sulc," not "Sulk").
- 2026-06-23: Recorded the **concrete connected path** for the Office staff directory (`/Users/connorfrey/Library/CloudStorage/Dropbox/Office/`), now that it's mounted as a Cowork folder — replaced the "may be a cloud-only placeholder / may not materialize" caveat with Read-tool / make-available-offline guidance. Tier 1 (path + availability). Trigger: Connor connected the Office folder.