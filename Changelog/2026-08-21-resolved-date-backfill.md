---
date: 2026-08-21
tier: 1
governs:
  - "Trackers/Actions/Connor - Answer the three open 4th-service registrant questions (Marin, Nayiga, Wertz).md"
  - "Trackers/Actions/Connor - Follow up (again) with John Farah & Jacob on volunteer recruiting.md"
  - "Trackers/Actions/Connor - Text John Slye further Boot Camp table-leader names.md"
---

# Three completed action notes were missing their `resolved:` frontmatter field

**Found by the 2026-08-21 weekly-synthesis light system audit; auto-fixed the same run (Tier 1).**

Three notes carried `status: completed` but no `resolved:` date, which makes them invisible to the "completed this week" view (the aging report keys off `resolved` within the period). The true close dates were already documented in each note's own body, so the dates were read out, not invented:

- **Answer the three open 4th-service registrant questions (Marin, Nayiga, Wertz)** → `resolved: 2026-08-20` (body: all three answered/delivered, status flipped in-progress → completed on 8/20).
- **Follow up (again) with John Farah & Jacob on volunteer recruiting** → `resolved: 2026-08-17` (body: "✅ CLOSED. Answered, and the answer is no." 8/17 live session).
- **Text John Slye further Boot Camp table-leader names** → `resolved: 2026-08-17` (body: "✅ COMPLETE. Names sent; there are no further names." 8/17 live session).

Only the `resolved:` frontmatter field was added; no body/log content was touched.
