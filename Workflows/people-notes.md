# Workflow: People Notes (the /People layer)

Keeps the people layer alive so it stays a true graph backbone instead of rotting. /People holds one **person note** per recurring principal (an outbound hub linking to their meetings/events/threads) and one **[[People/Good Noodles]]** roster for everyone peripheral. Index: [[People/People]].

## Two tiers
- **Person note** (its own file in /People) — for **recurring principals**: Grace staff/leadership and vendors who show up across multiple meetings or events. Currently: Connor, Derek Adye, John Slye, Brian Parker, Jennifer Claffey, Heather Noble, Steve Coy, Kay Carter-Corker, Seth Addison, Jean Paul, Maria Dalton.
- **Good Noodles roster row** — for **peripheral folks**: one-off volunteers, cohort members, helping hands. They get a row in [[People/Good Noodles]] and a `#good-noodle` tag where they appear — **not** their own note.

**Threshold:** give someone their own note when they (a) are Grace staff/a named vendor with an ongoing role, OR (b) have appeared in ~3+ meetings/events. Otherwise they're a Good Noodle. Don't proliferate thin nodes.

## Person note format
Frontmatter: `type: person`, `name`, `role`, `org`, `aliases` (spelling variants — e.g. Steve Coy/"Koy", Jean Paul/"John Paul"), `contact` (link or value), `tags: [person, ...]`. Body: one-line role/relationship, then outbound link sections — **Meetings** (transcripts), **Agendas**, **Events & threads** (events, trackers, contacts). The note links *outward*; it doesn't duplicate content. Changelog line at the bottom like every vault file.

## When a transcript is processed (hook from [[Workflows/Transcript-Synthesis]])
1. Map each `speakers` entry to a person — use the `aliases` to resolve variants and the canonical Office staff directory (Dropbox/Office) spelling.
2. Add a `people:` frontmatter array to the transcript (frontmatter only — never the body): `[[People/<Name>]]` for each principal present, plus `[[People/Good Noodles]]` if any peripheral folks appear.
3. For each **principal** present, append the transcript link to that person note's **Meetings** section.
4. For each **peripheral** person, ensure they have a Good Noodles row (add if new) and tag the transcript `#good-noodle`.
5. **Promotion check:** if a Good Noodle has now hit the threshold (3+ appearances or a newly ongoing role), promote them — create a person note, move their row to a redirect line in Good Noodles, and flag it in the synthesis report. (Nathan Ebikwo and Gina Baucom are the current promotion-watch candidates.)

## When an event/agenda/synthesis note is created or updated
Add or extend a `participants:` frontmatter array (`[[People/<Name>]]`, plus `[[People/Good Noodles]]` when peripheral helpers are involved). Same principle: frontmatter links, no body duplication.

## Rules
- Additive and link-only; never edit transcript bodies. Adding `people:`/`participants:` frontmatter is allowed (it's not body content).
- Keep names canonical (Office directory wins). Update a person's `aliases` rather than spawning a duplicate note.
- Never delete a person note — if someone leaves, note it in their file and move on.

## Changelog

History lives in [[Changelog/_history/people-notes-changelog]]; new changes get their own dated file in [[Changelog/README|/Changelog]]. **Neither is read on a normal run.**
