---
name: peer-discussion-slide
description: Build the week's Sunday Night peer-discussion slide (three prompts, 1920x1080 PNG), put it in Sunday Visuals under the exact name the PCO plan points to, and archive the superseded copy. Use when Connor says "make the discussion slide", "peer discussion questions", "the prompts for Sunday", or the week's discussion guide lands from Brian Parker or Alexis Hendrickson.
---

# Peer discussion slide

Three prompts, one PNG, ready for Michael Vacca. Full procedure, JSON shape and PCO pointer format: `Workflows/peer-discussion-slide.md` (read it only for steps this file doesn't cover).

**Due Wednesday night.** Vacca renders ProPresenter from PCO on Thursday morning, whoever runs it Sunday.

## 1. Write the prompts — social, not theological

Source: the week's guide (Brian Parker's email, `YYYY.MM.DD <Series> Week N.docx`; the week's guide is for the *following* Sunday, so check the date in the filename). Pull the theme, then write prompts a stranger can answer.

Send-backs so far — Connor has corrected every one:
- **More surface than the guide.** Friendship, not "why Jesus said friends instead of servants." Nothing that needs Bible knowledge.
- **No private disclosure.** Nothing that assumes they did last week's practice or must reveal something personal.
- **Local beats abstract.** One prompt can name Arlington / the DMV (e.g. making friends here).
- **Start each with a different verb** (Share / Talk about / Discuss). Never two "Share" in a row.
- "tonight's", never "Sunday's message." Typographic apostrophes (’), em dash with spaces.

Show Connor the three lines. Change only what he sends back.

## 2. Render

1. Copy last week's JSON in `Events/2026-09-20-Sunday-Night-Service/Discussion-Slides/` to `YYYY-MM-DD-Week-N.json`; set `questions`, fill `_source` (guide used, every change). `qotn` is a placeholder the renderer requires — QOTN is on AhaSlides; ignore the `-1-QOTN.png`.
2. `python3 "Workflows/discussion-slide-build.py" "<json>"`
3. **Open the PNG.** The script reports success even when a line overflows the frame.

## 3. Ship to Sunday Visuals

- Name: `M.D.YY - Peer Discussion Questions.png`, dated to the **service** (`10.4.26 - ...`). The PCO Peer Discussion item already points at this name — match it, don't invent a new one.
- Copy it to `~/Library/CloudStorage/Dropbox/Sunday Visuals/Sunday Night/` and copy it beside the JSON in the vault.
- A file by that name already there? Move it to `Sunday Night/Archive/<name> (superseded M-D).png` first. Never delete, never overwrite.

## 4. Check the PCO pointer

Pull the plan's Peer Discussion Host item (service type 1804248, `services_plan_items`, `description`). It should name the same file. If the name differs, tell Connor — PCO descriptions are hand-edited late and are his to change.

## 5. Report in two lines

The three prompts, and whether the file is in Sunday Visuals and matches PCO. If the slide changed after Connor uploaded to PCO Slides, say he needs to re-upload.
