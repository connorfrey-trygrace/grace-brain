---
title: "Booth handoff — laptop Claude ↔ programming-computer Claude"
type: workflow
date: 2026-11-22
tags: [workflow, sunday-night-service, slides]
people:
  - "[[People/Connor Frey]]"
  - "[[People/Michael Vacca]]"
---

# Booth handoff

Two Claudes work on Sunday Night: **laptop Claude**, which has the vault and builds the slides and PCO content, and **booth Claude**, on the service programming computer, which builds ProPresenter. Booth Claude can reach **Dropbox, PCO and GitHub** but not Notion or Agent Mail. They talk through **one note per service** in the folder both of them already use:

`Sunday Visuals/Sunday Night/_HANDOFF M.D.YY.md` (dated to the service, like the slides)

**PCO plan (service type 1804248) is the source of truth.** The note only says what changed, where the files are, and what's missing. It never repeats PCO content.

## Laptop Claude: write it

Do this **in the same turn** as any of these: shipping a file to `Sunday Visuals/Sunday Night/`, or creating, deleting, reordering or retitling a PCO item on that service's plan.

1. If the note doesn't exist, create it from the sections below. If it does, **edit it in place**: it shows the current state, not a running log.
2. Sections, in this order:
   - `## Changed since <last booth read / Vacca's Thursday render>`: one bullet per change, newest last.
   - `## Order of service`: one line, in PCO headers.
   - `## Files in this folder for tonight`: a table with the file and where it goes (main screen + PCO item, or side LEDs + segment).
   - `## Not available`: anything missing (a graphic never sent, Seth's TBD lyrics). Logistics are fine here; this note isn't PCO.
   - `## Booth → laptop`: **booth Claude writes in this section; laptop Claude only reads it.** Never overwrite it.
3. Head the note: `Last updated by laptop Claude <day time>`.

## Booth Claude: read it

1. Read `_START HERE (Claude).md` in this folder, then this note.
2. Re-pull the plan (`services_plan_items`, plan for that date) and build from PCO. Trust the note over memory, and PCO over the note.
3. Put questions, problems or "done" lines under `## Booth → laptop`, with a timestamp: `- 6:05 PM · Communion graphic not in Anna's outline file — used the morning slide`.
4. **Don't edit vault files or push to GitHub.** The repo is for reading this procedure only. Main is written by the Mac auto-sync and the 5 AM cloud routine, so a third writer would cause conflicts.

## Laptop Claude: read replies

Any Sunday Night work and any quick refresh before or on a service day: open the coming service's note and act on new `Booth → laptop` lines. Tell Connor about them. Fold anything that matters into the plan's action note or the event's `-Log.md`.

## After the service

Monday's first laptop run moves the note to `Sunday Night/Archive/` (never delete).
