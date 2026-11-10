---
type: changelog
date: 2026-09-16
tier: 1
touches: ["[[CLAUDE]]", "[[Workflows/peer-discussion-slide]]", "[[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Launch]]", "[[Reference/Grace-Brand-Guideline]]"]
trigger: "Connor needed the 9/20 peer-discussion slide, and wanted it repeatable week by week"
---

# Peer discussion slides get a renderer instead of a design session

Connor asked for one slide for launch night. The durable half of the ask was the second sentence: *"This should be a repeatable task week by week"* — plus *"all discussion guides should match that dimension."* A graphic made by hand each week drifts; three wrong Grace teals are already in circulation because of exactly that.

## What was built

- **`Workflows/discussion-slide-build.py`** — reads a small JSON per week, renders 1920×1080 PNGs through headless Chrome. Type size is auto-fitted by binary search, so back-row legibility is computed rather than eyeballed.
- **`Workflows/assets/fonts/`** — Lato vendored into the vault (Light/Regular/Bold/Black). The build needs no network and cannot silently substitute a face on a machine that lacks the font.
- **`Workflows/peer-discussion-slide.md`** — the procedure, including the stranger-safety filter for picking questions out of Brian's guide.
- **Job 11 in [[CLAUDE]]**, so the weekly task is findable.

## Decisions Connor made, and what they cost

| Question | Call | Note |
|---|---|---|
| QOTN source | **Live #1** — *"How do I not worry when everything is actually falling apart right now?"* (28 votes, 9/16 21:07 pull) | This is Cluster B. [[Events/2026-09-20-Sunday-Night-Service/2026-09-20-Sunday-Night-Service-Question-Analysis]] recommended Cluster A for the Q&A with the worry question handled inside the message at 14:27. **Confirmed the same day** — picked jointly by Connor and John Slye in person, so the slide is final, not provisional. |
| Format | PNG 1920×1080 | Straight into ProPresenter; no font licensing on the booth machine. |
| Layout | Two slides — QOTN alone, then 3 prompts | "Read from the back row" and "4 questions" fight; splitting resolves it without cutting content. |
| Field | Near-black, white type, Active Blue accents | Connor took near-black over Stable Blue navy. |
| Chrome | **None** — stripped on review | Connor: *"Remove the headers and footers — it is too noticeable AI generated."* The eyebrow label, accent rule and footer metadata came out; the question now sits alone on the field. The tracked-out-label-over-a-thin-rule pattern is a generated-deck tell, and a room that clocks the slide as machine-made discounts the question on it. Bought ~15% more type as a side effect. |

## The bug worth remembering

The first render **silently cut question 3 off the bottom of the frame** and the script reported success. The autofit measured `stage.scrollHeight`, but a centered flex child overflows in both directions without ever growing its parent's scroll height — so the check always answered "fits." Fixed by measuring the content block itself.

**The workflow now says to open the PNGs before sending.** A renderer that can be wrong while exiting 0 is worse than a hand-made slide if nobody looks at the output.

## Delivered to where Vacca actually looks

The vault is not a handoff surface — Michael Vacca works out of Dropbox and PCO. So the workflow now ends in two concrete places rather than at the renderer:

- **`Connor Frey/Sunday Visuals/Sunday Night/`** — a new folder beside Pre-Service Slides and Communion, holding `9.20.26 - Question of the Night.png` and `9.20.26 - Peer Discussion Questions.png`. Named to the `M.D.YY - Description.png` convention already running in `Sunday Visuals`, and **dated to the service, not the build**.
- **Pointers on the 9/20 plan** (service type 1804248, plan 91130954) — on the Host item under **Q&A** and the Host item under **Peer Discussion**.

**The pointers live in each item's Description, as their own `Slide (Vacca):` callout** — alongside the `Confidence Monitor Notes:` block already there.

They went into the item's **Audio/Visual** note first, reasoning that the Description is confidence-monitor copy facing the stage and a file path does not belong in the host's eyeline mid-service. **Connor overruled it, and the override is the better call:** the Description is the one field the host and the operator both already read, and splitting the instruction by team creates two places to keep in sync. One source of truth beats a tidy separation of concerns. The A/V notes were cleared.

**Also aligned: the QOTN is now a direct quote of the board.** The host note read *"…when everything is falling apart?"*; it now reads *"…when everything is **actually** falling apart **right now**?"*, matching the slide word for word so the host is not reading one line with a different one behind them.

PCO's connector is read-only for Services, so all four edits went in through the browser and were **verified back through the API** rather than from the screen.

### The near-miss

Between reading the host notes and editing them, **all four were rewritten by hand** — tightened from prose into short confidence-monitor lines wrapped at roughly 37 characters. Overwriting from the copy read an hour earlier would have silently reverted someone's work. Caught only because the page's rendered text no longer matched what was in hand.

**The workflow now says to re-pull the live Description immediately before editing and retype from that**, never from an earlier read. Shared software is edited by other people while you are looking at it.

## Flagged, not fixed

**The Tuesday cut and the Thursday guide are in conflict.** Slides are due to Michael Vacca by Tuesday (Connor: *"Thursday is too late for getting things into the slides for Vacca"*), but Alexis sends the discussion guide Thursday mornings (Brian, 9/16). Week 2 only worked because Brian sent Connor the guide directly on a Wednesday. Either that early send becomes the standing arrangement or the discussion slide permanently ships later than the rest of the deck.
