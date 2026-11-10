---
title: "World Cup Event — Meeting Contribution Sankey"
event: "World Cup Viewing Party (2026-07-19)"
generated: 2026-07-06
source: "action_items frontmatter from the 6 World Cup transcripts, 2026-06-09 through 2026-06-25"
participants:
  - "[[People/Connor Frey]]"
  - "[[People/Derek Adye]]"
  - "[[People/Brian Parker]]"
  - "[[People/Jennifer Claffey]]"
  - "[[People/Heather Noble]]"
  - "[[People/Good Noodles]]"
tags:
  - world-cup-event
  - analysis
---

# What this is

A hand-built SVG, not a plugin diagram — no Sankey layout engine reordering nodes, no Mermaid rank algorithm to fight. Vertical position is the actual calendar date, June 8 through July 19. Solid colored chips are the six meetings (from transcripts); dashed outline chips are solo work sessions pulled from `/Trackers/Hours.md`, filtered to daily-log entries that explicitly mention "World Cup" and aren't already one of the six meeting dates (6/8, 6/15, 6/17). Those three don't have outgoing flow lines because Hours.md logs hours and a one-line note, not itemized decisions the way a transcript's `action_items` list does — adding fake edge weights for them would be fabrication. Two dashed horizontal lines mark today (7/6) and the event date (7/19), with the multi-day gaps between the last meeting, today, and the event labeled explicitly rather than compressed away. Color is a single blue ramp from light (earliest) to dark navy (latest). Line thickness = count of distinct action items/decisions from the six meetings' `action_items` frontmatter. Two items were open questions rather than firm decisions (Nathan Ebikwo's regular Sunday-evening commitment; Derek's photo follow-up) — included as contributions since they were concrete outputs of the call, not because they were resolved.

# Diagram

![[2026-07-19-World-Cup-Contribution-Timeline.svg]]

This is a static image, not an interactive plugin block — it will always render the same way regardless of Obsidian theme or installed community plugins.

# Underlying table (audit trail)

| Date | Meeting | Workstream fed | # items | Notes |
|---|---|---|---|---|
| 2026-06-09 AM | Planning Meeting | Venue/Room Layout | 3 | Youth space walkthrough, Komar space-check, March Madness photos for layout |
| 2026-06-09 AM | Planning Meeting | Comms/Marketing | 1 | Submit Rock comms request |
| 2026-06-09 AM | Planning Meeting | Registration/Rock Ops | 1 | Set up $5–10 paid registration |
| 2026-06-09 AM | Planning Meeting | Programming/Activities | 1 | Halftime programming + props/prizes |
| 2026-06-09 AM | Planning Meeting | Budget/Approval | 1 | Propose budget to Derek |
| 2026-06-09 AM | Planning Meeting | Volunteers/Outreach | 1 | Recruit high-energy connectors |
| 2026-06-09 AM | Planning Meeting | AV/Streaming | 1 | Brian's streaming test + AV orientation |
| 2026-06-09 PM | Weekly Sync | Date/Scheduling | 2 | Decision to pursue July 19 (final) over July 11; casual sign-off text to John |
| 2026-06-09 PM | Weekly Sync | Venue/Room Layout | 1 | Wait on Komar's July 19 confirmation |
| 2026-06-09 PM | Weekly Sync | Registration/Rock Ops | 1 | Schedule ROC orientation with Kay |
| 2026-06-16 | Streaming Confirmed | AV/Streaming | 2 | Drums/Jean Paul coordination for auditorium contingency; Brian AV walkthrough |
| 2026-06-16 | Streaming Confirmed | Venue/Room Layout | 2 | Komar finalized youth space; photos requested (non-critical) |
| 2026-06-16 | Streaming Confirmed | Comms/Marketing | 1 | Comms request now submittable — all inputs in hand |
| 2026-06-18 | Heather Marketing Intro | Comms/Marketing | 3 | Merch-shop prize link; team producing graphic/social/feature-email/photographer; Gina drafting feature-email copy |
| 2026-06-18 | Heather Marketing Intro | Programming/Activities | 1 | Halftime prizes resolved via merch shop (custom shirts ruled out) |
| 2026-06-21 | Nathan Volunteer Call | Volunteers/Outreach | 1 | Nathan added to top of WC volunteer list |
| 2026-06-25 | Welcome Announcement Prep | Comms/Marketing | 2 | Connor's on-stage script; Brian's ProPresenter confidence-monitor slides |

# What this surfaces

Two things worth naming, not just displaying:

**Comms/Marketing is the heaviest-fed workstream (7 items) but arrived latest and most fragmented** — one item from the first planning call (6/9), then nothing until 6/16, then a burst on 6/18 (Heather) and 6/25 (announcement prep). Venue/Room Layout front-loaded almost everything by 6/16. That's a real pattern: logistics got locked early, marketing got bolted on later and in pieces across three separate people (you, Heather, Brian). Worth checking whether anything Heather's team needs (photographer scheduling, feature-email fact-check) still has a live deadline you haven't tracked in Open Actions.

**Date/Scheduling only shows up once (6/9 PM) but it was the highest-leverage decision in the whole set** — moving from July 11 to July 19 unblocked the youth-space availability, the AV contingency test, and arguably made the whole event viable given your bachelor-party conflict. A raw item-count Sankey undersells it because it's one edge with weight 2, sitting next to Comms/Marketing's edge of weight 3. If "intellectual complexity" is really what you're after, that single date-change conversation was probably more consequential than the entire Heather meeting — the diagram won't tell you that; the dated table will.
