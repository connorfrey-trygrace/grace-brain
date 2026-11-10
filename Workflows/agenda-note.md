# Workflow: Agenda Note

Standard format for meeting agendas drafted ahead of a sync or check-in. Stored in `/Agendas`. This is Job #6 in [[CLAUDE.md]].

## When to create
- Ahead of a scheduled recurring sync (e.g., the Connor–Derek sync — **bi-weekly Mondays 4:00–4:45 PM**, confirmed by Connor 2026-09-16; it was weekly Tuesdays 4pm until 2026-09-14). Don't hardcode that cadence anywhere: the `derek-sync-agenda` job checks the Outlook calendar for an actual sync that day and writes nothing when there isn't one, so a future cadence change needs no edit here.
- When a meeting is scheduled and there are open questions or topics to bring.
- When Connor asks for an agenda.

## Filename convention
`YYYY-MM-DD <Meeting Name> Agenda.md` — date is the meeting date.
Example: `2026-06-16 Connor–Derek Weekly Sync Agenda.md`

## Frontmatter
```yaml
---
title: "<Meeting name>"
date: YYYY-MM-DD
time: "H:MM AM/PM"
attendees:
  - Name
format: "in person | Zoom | phone"   # optional
tags: [agenda]
source: "where the agenda items came from — link transcripts, Open Actions, or email threads"
---
```

## Body
- Open with a one-line **Purpose** (callout) when the meeting's intent isn't obvious from the title.
- **Recurring syncs (e.g. the Connor–Derek sync): always include a "Since last time" summary** as the first section, before the discussion items. Cover what's changed since the *prior meeting of this series* (not a fixed 7-day window — on a bi-weekly cadence that window is usually 14 days, and calling it "since last week" would quietly drop half of it) — decisions made, items closed, new developments, and anything the other attendee set in motion. Source it from the dated entries in [[Trackers/Open Actions.base]] and the most recent [[Synthesis]] weekly note; keep it to tight, scannable bullets (a recap, not a discussion item). This orients the room before anything needing a decision.
- Group the remaining items under clear headings (topic or priority order). Keep each item to the decision or question that needs the room — not a status dump.
- **Attribute sources honestly.** If an item comes from Connor's own notes rather than the meeting-owner's stated agenda, say so (the John/Derek/Connor check-in agenda does this well). Don't present Connor's wish-list as the convener's agenda.
- Link the relevant event notes, transcripts, and Open Actions items with `[[...]]`.
- End with two capture sections to fill live: **Notes** and **Action items** — the latter feed [[Workflows/Open-Actions-Tracker]] afterward.

## After the meeting
- Capture decisions and new action items; add the action items to [[Trackers/Open Actions.base]] per [[Workflows/Open-Actions-Tracker]].
- Leave the agenda in `/Agendas` as the record (don't archive unless superseded).

## Changelog

History lives in [[Changelog/_history/agenda-note-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
