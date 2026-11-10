---
name: cm-notes-from-script
description: Turn a stage script (host intro, announcement, YP answer, any spoken segment) into Confidence Monitor Notes for a Sunday Night PCO plan item, sized to fit the monitor, and write them into the plan. Use when Connor says "make the CM notes", "put this in PCO", "update the confidence monitor", "make sure it fits the monitor", or hands over a script that someone will read from stage.
---

# Confidence Monitor notes from a script

A PCO Sunday Night **Host**-type item's Description is what the speaker reads off the confidence monitor. This skill converts a finished script into that block and puts it in the plan. Format rules live in the agent memory `confidence-monitor-notes-format` — read it first; this file is the procedure.

## 1. Start from the live item, not your draft

- Pull the target plan's items with `services_plan_items` (service type **1804248**, output `title, sequence, length, description, updated_at`).
- **If the item's `updated_at` is newer than your last write, someone (usually Connor) edited it. Their wording wins.** Build from the live text, not from the vault draft. Ask only if an edit looks accidental (e.g. a garbled word) — and then fix only that word.

## 2. Convert script → cue lines

- First line is literally `Confidence Monitor Notes:`
- **Terse cues, not sentences.** One idea per line. `->` for sub-points, CAPS for a hard cue, `SPEAKER:` line when the voice changes (`SKY:`).
- Abbreviate cue lines: `wk`, `svc`, `Sun night`, `w/`, `Qs`, `Qtr`, `10+`.
- **Quoted lines are read aloud.** Keep them close to the script. Don't invent abbreviations inside quotes; keep ones Connor chose himself (he wrote `"YoPros had 1 event"` on 2026-09-23).
- Hand-wrap lines at natural breaks; the fit gate below decides whether they fit, not a character count.
- **Host - Welcome always ends `PLEASE STAND - join us in worship`** — the cue before the worship leader starts (Connor, 2026-10-21). Never cut it for fit; if Welcome splits, the stand cue ends the last part, `Host - Welcome (cont.)`.
- **`Host - Q&A` stays one item** (app instructions + top/new Qs, Connor 2026-10-07) — compress it, don't split it.
- Keep the hand-off cue at the end (`-> Sky?`, `For-real QOTN -> Brandon + Will`).
- Stage content only. No logistics, TBDs, timings, or production notes (see memory `pco-carries-stage-content-only`).

## 3. Make it fit — split rather than cram

- ⛔ **Fit gate — run it, don't estimate:** `python3 "Workflows/cm-fit.py" <file>` (blocks separated by `===`). It measures real Calibri 28pt widths against Brian Parker's blank box in the Office Dropbox, `Office/Confidence Monitor Template.docx` (336.6pt usable width, **6 lines of monitor text — the label and anything after the first blank line are not counted**) and wraps the way Word does. Non-zero exit = a block overflows; fix it before showing Connor. The `/Reference` copy is a filled-in 20pt sample, not the standard (Connor, 2026-10-28). At 28pt a line holds only ~25–28 characters.
- **Item content = monitor part + off-monitor part** (Connor, 2026-09-28). Everything lives in the item's content (never the A/V note). `Confidence Monitor Notes:` is only a label marking where the monitor text starts — it is not on the monitor and not counted. Monitor text runs to the first blank line (≤6 lines, measured by `Workflows/cm-fit.py`). After the blank line: off-monitor cues, e.g. `Slide:` + path — no operator name (Connor, 2026-09-28).
- If it runs past 6, **split into consecutive items at the natural hand-off** (speaker change or topic change), each with its own `Confidence Monitor Notes:` header. Name them `<Speakers> - <Topic>` (e.g. `Con/Sky - YoPros Q`, `Con/Sky - Inspira`) and divide the original length between them.
- Show Connor the block(s) before writing unless he already asked for the write.

## 4. Write to PCO (browser — the connector is read-only for Services)

**Preferred (2026-09-28): the PCO API from the logged-in tab, no clicks.** In Claude in Chrome on the plan page, `javascript_tool` → `fetch('https://api.planningcenteronline.com/services/v2/service_types/1804248/plans/<plan>/items/<id>', {method:'PATCH', credentials:'include', headers:{'Content-Type':'application/json','X-CSRF-Token':document.querySelector('meta[name=csrf-token]').content}, body: JSON.stringify({data:{type:'Item',id,attributes:{description}}})})`. POST to `/items` with `title, description, length, sequence` creates an item at that position. No keystrokes land on the plan page, so the single-key-shortcut hazard below can't fire. Fall back to the UI steps only if the API refuses.

Use Claude in Chrome on `services.planningcenteronline.com/plans/<plan_id>`.

- Open an item: **double-click its title text** (coordinates from a screenshot; a `find` ref double-click sometimes doesn't open the panel).
- Title: triple-click the title field, type. Length: triple-click the `min` and `sec` boxes separately. Description: click inside, `cmd+a`, type. Click a neutral area in the panel to trigger save; confirm the green **Saved** badge.
- **New item:** blur focus (click the column header), hover the row, press **`i`** — PCO inserts a New Item **above** the hovered row and opens it. Put the *earlier* half in the new item and move the later half into the existing one, rather than dragging (drag from the Add menu doesn't work).
- ⚠️ **PCO's plan view has single-key shortcuts (`i` = new item, `h` = header, plus others).** Any keystroke that lands on the page instead of a text field silently creates or removes items. On 2026-09-23 this created blank items and removed the Prayer item. **Before every `type` or `key`, be sure a text field has focus (take a screenshot if unsure). Never type after clicking somewhere you haven't confirmed.**
- `form_input` does not stick on the Description textarea — use click + `cmd+a` + `type`.

## 5. Verify, then log

- Re-pull `services_plan_items` and confirm: item count as expected, no `New Item` rows, no item missing versus the pre-edit pull, text matches exactly.
- If anything else changed, compare it against the pre-edit pull. Restore what you broke; don't touch what someone else changed.
- Close the Chrome tab.
- Append one dated line to the event's `-Log.md` (e.g. `Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Launch-Log.md`): which items changed, split or not, verified.
- Mirror the final wording into the vault draft if one exists (e.g. `2026-09-27-Connor-Host-Intro-Draft.md`) so the draft and the plan don't drift.
