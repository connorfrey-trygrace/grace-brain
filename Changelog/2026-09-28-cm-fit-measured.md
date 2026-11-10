---
type: changelog
date: 2026-09-28
tier: 2
touches: ["[[Workflows/cm-fit.py]]", ".claude/skills/cm-notes-from-script/SKILL.md", "[[Reference/Confidence Monitor Template]]"]
trigger: "Connor, 2026-09-28 — Brian said the last CM notes didn't fit; \"use the tool he already put out there\""
---
# CM notes are measured against Brian's template box, not a rule of thumb

The cm-notes-from-script skill sized blocks at ~13 lines / 37 chars. Brian's `/Reference/Confidence Monitor Template.docx` box (351×206.55pt, insets 7.2/3.6pt, Calibri 20pt single-spaced) holds **8 lines**. The 9/27 Inspira and Welcome blocks measure 11 and 10 — consistent with Brian's report.

New `Workflows/cm-fit.py` wraps with real Calibri glyph widths and fails on overflow; validated against the template's own sample text (fills exactly 8/8). Skill and memory now gate on it. Revised same day (Connor): the `Confidence Monitor Notes:` label and anything after the first blank line (slide cues) stay in the item content but are off-monitor and not counted.
