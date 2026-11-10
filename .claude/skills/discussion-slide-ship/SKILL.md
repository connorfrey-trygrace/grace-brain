---
name: discussion-slide-ship
description: Render the three approved discussion prompts to a 1920x1080 PNG and put it in Sunday Visuals. Use after discussion-prompts, or when Connor says "make the slide" or "put it in Sunday Visuals".
disable-model-invocation: true
---

1. Copy last week's JSON in `Events/2026-09-20-Sunday-Night-Service/Discussion-Slides/` to `YYYY-MM-DD-Week-N.json`. Set `questions`; log the guide and any change in `_source`. Ignore `qotn` and the `-1-QOTN.png` (QOTN is on AhaSlides).
2. `python3 "Workflows/discussion-slide-build.py" "<json>"`, then open the PNG. The script says success even if text overflows.
3. Name it `M.D.YY - Peer Discussion Questions.png`, dated to the service. Copy it to `~/Library/CloudStorage/Dropbox/Sunday Visuals/Sunday Night/` and beside the JSON.
4. Same name already there? Move the old one to `Sunday Night/Archive/<name> (superseded M-D).png` first. Never delete.

Due Wednesday night; Vacca renders from PCO Thursday morning. Then run `discussion-pco-check`.
