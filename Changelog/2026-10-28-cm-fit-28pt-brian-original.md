---
type: changelog
date: 2026-10-28
tier: 2
touches: ["[[Workflows/cm-fit.py]]", ".claude/skills/cm-notes-from-script/SKILL.md", "memory: confidence-monitor-notes-format"]
trigger: "Connor, 2026-10-28 — \"double check that they all fit per the check document from Brian Parker in the office dropbox\" → \"Brian's original is the standard (28pt, 6 lines). Rewrite/split the 11/1 CM blocks to fit and update cm-fit to match.\""
---
# CM fit is 6 lines at 28pt — Brian's blank Office template, not the /Reference sample

The 9/28 cm-fit measured against `/Reference/Confidence Monitor Template.docx`, which turned out to be a **filled-in copy**: sample text at Calibri 20pt, box shrunk to 206.55pt tall → 8 lines. Brian's blank original in `Office/Confidence Monitor Template.docx` has the box at 351×220.8pt with the run size at **28pt** ("please don't change the font or size") → **6 lines**, ~25–28 chars each.

- `Workflows/cm-fit.py`: PT 20→28, height 206.55→220.8pt; docstring names the Office file as source of truth.
- `cm-notes-from-script` skill + memory: 8→6 lines; Welcome may split with the stand cue ending `Host - Welcome (cont.)`; `Host - Q&A` stays one item.
- 11/1 Sunday Night plan 92214542: all 9 CM blocks rewritten/split to ≤6 lines, verified from live PCO. Every block written 9/28–10/25 was ~2+ lines over this standard.
- `/Reference/Confidence Monitor Template.docx` replaced with Brian's Office original (same name, links unchanged); the 20pt filled copy moved to `/Archive/Confidence Monitor Template (20pt filled sample, superseded 2026-10-28).docx` (Connor OK, 2026-10-28).
