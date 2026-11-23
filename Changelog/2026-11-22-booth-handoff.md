---
type: changelog
date: 2026-11-22
tier: 2
touches: ["[[Workflows/booth-handoff]]", "[[Workflows/grace-quick-refresh]]", ".claude/skills/discussion-slide-ship", ".claude/skills/cm-notes-from-script", ".claude/skills/pco-flow-check"]
trigger: "Connor"
---
# Laptop Claude ↔ booth Claude handoff via a per-service note in Sunday Visuals

Connor asked for a way to hand off between Claude on his laptop and Claude on the service programming computer. The booth can reach Dropbox, PCO and GitHub only, with no Notion or Agent Mail. So the channel is `Sunday Visuals/Sunday Night/_HANDOFF M.D.YY.md`: the laptop keeps it current whenever it ships files or edits PCO, and the booth replies under `Booth → laptop`. `_START HERE (Claude).md` in that folder bootstraps the booth side. The booth only reads GitHub and never pushes, to avoid a third writer on main. First used for 11.22.26.
