---
title: "Peer Discussion Slide — weekly build"
type: workflow
date: 2026-09-16
tags: [workflow, sunday-night-service, slides]
people:
  - "[[People/Connor Frey]]"
  - "[[People/Brian Parker]]"
  - "[[People/Michael Vacca]]"
  - "[[People/John Slye]]"
---

# Peer Discussion Slide — weekly build

Builds the two 1920×1080 PNGs that carry the Sunday Night peer-discussion block: **the question of the night**, and **the week's discussion prompts**. Runs once a week, after the guide lands and the QOTN is picked.

> ⚠️ **As of 2026-09-23 the QOTN slide is no longer used** (Connor): the question of the night is shown through the live AhaSlides connection. Ship only the **prompts** slide — skip the `-1-QOTN.png` copy and the Q&A Host-item pointer. The renderer still emits both files; ignore the QOTN one.

> 📌 **Now a skill (2026-09-30):** three small skills carry the operating procedure and Connor's standing send-backs (social over theological, local over abstract): `discussion-prompts` → `discussion-slide-ship` → `discussion-pco-check` in `.claude/skills/`. This file is the reference.

**Every discussion graphic is 1920×1080 and built by this workflow.** One renderer, one template, no hand-made one-offs — that is what keeps the week-to-week set looking like a set.

---

## Inputs — the two things that gate the build

| Input | Source | Lands |
|---|---|---|
| **The week's discussion guide** | Brian Parker emails it to Connor; **Alexis Hendrickson sends the wider version Thursday mornings** (Brian, 2026-09-16). Subject is usually `Week N Discussion Guide` or `week N guide`; attachment is `YYYY.MM.DD <Series> Week N.docx` + `.pdf` | Wed–Thu |
| **The question of the night** | The live AhaSlides board — `Sunday Night Service - Q&A 9/13`, https://audience.ahaslides.com/WTUI2/ (`iid5bl9hd6` is the **same board**, not a second one). **John Slye picks it**; the top-voted row is the input to his pick, not the pick itself | Varies — confirm with John |

> ⚠️ **Rebuilt every week (Connor, 2026-10-07):** new prompts, new dated filename, and the PCO Peer Discussion Host item's `Slide:` line updated to match — never carried forward. Find the guide in Outlook with **no tight date cutoff** (search `week N discussion guide`, look back 2+ weeks): on 10/7 a search starting 10/1 missed the Week 5 guide Brian sent 9/30.

> [!warning] The board moves, and the top has already flipped once
> On 2026-09-16 the #1 question changed between a 16:18 pull and a 21:07 pull on a one-vote gap. **Re-pull the board at build time and timestamp the pull in the week's JSON.** Never carry last week's ranking forward, and never quote a rank without the timestamp it came from.

> [!tip] Screen for duplicates before you quote a rank
> The 9/16 board carried two verbatim-identical rows. A split vote at the top changes which question is "#1." Merge before ranking.

---

## Picking the discussion questions

Take them **from that week's guide**, verbatim where possible. Brian's standing permission, 2026-09-06: *"I'll let you determine what you pass on and to whom."* So adapting is sanctioned — but adapt for the room, not for taste, and record every change in the JSON's `_source` field.

**Three or more, and they must be questions you would not mind being asked by a stranger.** The room is strangers by design. The filter, in order of what to reach for first:

1. ✅ **Recall** — "was there anything from tonight's message that stuck with you?" Anyone who was in the room can answer.
2. ✅ **Observation** — "what word, phrase or image caught your attention?" No self-disclosure required.
3. ✅ **Background / story** — "how have you heard churches talk about X?" Generative, and nobody has to reveal anything about themselves.
4. ⛔ **Skip** anything that requires a private disclosure ("which one do you most need right now — and why?"), anything that assumes they did last week's practice, and anything from the guide's independent-preparation section (the "why do I feel this way?" interior questions). Those are group-of-six-who-know-each-other questions. They are not for week one with a stranger.

**Two adaptations you will make almost every week:**
- The guide is written for a midweek group, so `"Sunday's message"` and `"this week's text"` become **`"tonight's"`** — the room just heard both.
- Straight apostrophes become typographic ones (`'` → `’`). The renderer does not do this for you.

> [!note] Watch the on-ramp for people who didn't grow up in church
> Grace's line is *"a church for people who don't go to church,"* and the evening targets 20s–30s. A question opening `"If you grew up in church…"` is a great stranger question for the people it fits and a silent one for the people it doesn't. It is fine to use — just don't use **three** of them.

---

## Build

1. Copy last week's JSON in `Events/2026-09-20-Sunday-Night-Service/Discussion-Slides/` to `YYYY-MM-DD-Week-N.json` and swap the content.
2. Run the renderer:

```bash
python3 "Workflows/discussion-slide-build.py" "Events/2026-09-20-Sunday-Night-Service/Discussion-Slides/2026-09-20-Week-2.json"
```

3. **Look at both PNGs before sending.** The type is auto-fitted by binary search; an overflow bug in the first build silently pushed question 3 off the bottom of the frame and the script reported success. Open the files.

### The JSON

```json
{
  "_source": "where the QOTN came from + its pull timestamp; which guide the questions came from; any adaptation made",
  "qotn": "the single top question, verbatim",
  "questions": ["...", "...", "..."]
}
```

`_source` is documentation, not content — the renderer ignores it. Fill it in anyway; it is the only record of which pull the rank came from.

Output: `<stem>-1-QOTN.png` and `<stem>-2-Discussion.png`, both 1920×1080, written beside the JSON.

---

## Design spec — do not re-derive this per week

> [!important] No chrome. Connor, 2026-09-16: *"Remove the headers and footers — it is too noticeable AI generated."*
> **No eyebrow label, no accent rule, no footer metadata, no date, no scripture reference.** The question sits alone on the field. A small tracked-out label over a thin accent rule with a timestamp in the corner is the house style of every generated deck on the internet — and a room that clocks the slide as machine-made discounts the question on it. Do not add chrome back, per week or per slide.

Locked to [[Reference/Grace-Brand-Guideline]] (Summer 2019, the authoritative book — **not** [[Reference/Grace-Brand-Colors]], which is superseded).

| | Value | Why |
|---|---|---|
| Field | near-black `#111113` | The auditorium is dark during connect time. A white 1920×1080 field is glare. |
| Type | white `#FFFFFF` | Maximum contrast against the field. |
| Accent | **Active Blue `#2F97A0`** (PANTONE 2235 C) | The numerals on slide 2, and nothing else. The **only** brand teal — `#2A95A0` (website) and `#44979D` (7/26 sign) are drift, on contact correct them. |
| Face | **Lato**, vendored at `Workflows/assets/fonts/` | The book specifies Brandon Grotesque Black / Franklin Gothic Heavy, neither licensed here; it names **Lato Black** for pull quotes, so Lato is the sanctioned free substitute rather than an invented choice. |
| Headline | Lato **Light** | The book's signature move: *headers are light and quiet.* Do not set the question in bold. |
| Numerals | Lato **Black**, Active Blue | The only accent left on either slide, and it earns its place — it tells a group which question they are on. |
| Size | auto-fitted, ~170px QOTN / ~76px prompts | Computed to fill the frame, never typed by hand — back-row legibility is the point. Dropping the chrome bought roughly 15% more type. |

Fonts are **vendored in the vault**, so the build needs no network and cannot silently substitute a face.

---

## Handoff

Two steps, both required. The renderer's output lives in the vault; **Vacca works out of Dropbox and PCO and never opens the vault.**

### 1 · Copy to Dropbox

Destination: **`Sunday Visuals/Sunday Night/`** (local: `~/Library/CloudStorage/Dropbox/Sunday Visuals/Sunday Night/`) — the Sunday Night folder alongside Pre-Service Slides, Communion and the rest. **Vacca can reach it** — the booth machine is signed into Dropbox (confirmed by Connor, 2026-09-16), so a path is a usable instruction.

Name them to the house convention already in use in `Sunday Visuals` (`M.D.YY - Description.png`), **dated to the service**, not to the build day:

| Slide | Filename |
|---|---|
| QOTN | `9.20.26 - Question of the Night.png` |
| Prompts | `9.20.26 - Peer Discussion Questions.png` |

```bash
SV="/Users/connorfrey/Library/CloudStorage/Dropbox/Sunday Visuals/Sunday Night"
cp "<stem>-1-QOTN.png"       "$SV/M.D.YY - Question of the Night.png"
cp "<stem>-2-Discussion.png" "$SV/M.D.YY - Peer Discussion Questions.png"
```

### 2 · Point at them from the PCO plan

Service type **`Sunday Night` (1804248)** — not 1814753, the empty duplicate. Put a pointer on the **two Host items** that carry these slides: the one under the **Q&A** header (QOTN) and the one under **Peer Discussion** (prompts).

**The pointer goes in the item's Description, as its own callout**, matching the `Confidence Monitor Notes:` block already there — blank line, label, then the path:

```
Slide (Vacca):
Sunday Visuals > Sunday Night >
"9.20.26 - Question of the Night.png"
```

Leave the `Notes → Audio/Visual` field empty. The pointer was briefly put there instead, on the reasoning that the Description is confidence-monitor copy facing the stage; **Connor's call, 2026-09-16, is the Description** — one place the host and the operator both already read beats a field split by team. One source of truth, not two.

**Match the host notes' line discipline.** They are hand-wrapped to roughly 37 characters so they read on a confidence monitor — keep new lines to that width, and break the *path* across lines rather than the filename.

> [!warning] Read the current Description before you overwrite it
> These notes get edited by hand, late. On 2026-09-16 all four host notes were rewritten roughly an hour after being read — tightened from prose into short monitor lines. Pull the live text (`services_plan_items` with `output_fields: ["description"]`), edit the one line you mean to change, and retype the whole field from *that*, never from an earlier copy.

### Quote the QOTN verbatim

Connor, 2026-09-16: *"Align PCO to the board, we want it to be a direct quote if we can fit it."* The host note and the slide must read the same words — otherwise the host reads one line while a different one is on the screen behind them. Wrap it across lines if it does not fit; do not shorten it.

PCO's connector is **read-only for Services** — no write tool exists — so this is a browser edit. Verify afterwards through the API rather than trusting the screen: `services_plan_items` with `output_fields: ["description"]` returns the saved text.

**Timing (updated 2026-09-30, Connor):** Michael Vacca renders ProPresenter from PCO on **Thursday morning**, so **Wednesday night is the standing due date** (the Tuesday cut below was the 9/16 ask). Get both done by **Tuesday** if possible; Wednesday night is the hard stop.

*Original 9/16 note:* get both done by **Tuesday**. Per Connor, 2026-09-16, *"Thursday is too late for getting things into the slides for Vacca."*

⚠️ **The Tuesday cut and the Thursday guide are in conflict.** Alexis sends Thursday mornings; Brian sent Week 2 on a Wednesday. Either Brian keeps sending Connor the guide early, or the discussion slide ships later in the week than the rest of the deck. Worth settling with Brian rather than re-discovering weekly.

Related: `snl-service-prep` (Mon 9:22 AM, [[Trackers/Automation]]) already flags *"missing discussion prompts"* on the coming Sunday's PCO plan — that job is the reminder that this one is due.

---

## Not scheduled, deliberately

The build gates on two human inputs that don't arrive on a fixed clock — Brian's guide and John's pick. A cron would mostly fire into an empty week. Run it on request once both have landed; `snl-service-prep` provides the nag.
