---
type: changelog
date: 2026-08-12
tier: 3
touches: ["[[Changelog/README]]","[[CLAUDE]]"]
trigger: "Connor"
---
# Changelogs moved out of every procedure file into /Changelog, one file per change

Every workflow carried a `## Changelog` section and `CLAUDE.md` carried the largest — **9.7 KB of its 17.7 KB**, loaded at the start of every session. History moved to `/Changelog/_history/` (one file per procedure, unmodified); the three `/Logs/*-changelog.md` files moved there too. Going forward each change is its own dated file, `/Changelog/YYYY-MM-DD-slug.md`, never appended to and never read on a normal run.

`CLAUDE.md` 17.7 KB → 8.3 KB. Rule added to CLAUDE.md: no changelog sections in procedure files. Connor: *"no need to include a change log in the instructions ok any workflows."*
