---
type: index
tags: [changelog]
---
# /Changelog

**One file per change. Never read on a normal run.**

Created 2026-08-12. Before this, every workflow file carried its own `## Changelog` section and `CLAUDE.md` carried the largest one of all — so the full history of every past decision was re-read on every run just to reach the procedure underneath it. `CLAUDE.md` alone was **17.7 KB, 9.7 KB of it changelog**, loaded at the start of every session.

## Writing a change

When you make a change worth recording, create **one new file**:

```
/Changelog/YYYY-MM-DD-short-slug.md
```

```markdown
---
type: changelog
date: 2026-08-12
tier: 2
touches: ["[[Workflows/text-message-sync]]", "[[Trackers/Automation]]"]
trigger: "Connor"
---
# What changed, in one line

Two or three sentences: what changed, why, and what it measured if anything.
```

Rules:

- **Never append to an existing changelog file.** A new change is a new file. That is the whole point — appending recreates the file that has to be read in full.
- **Never put a changelog section in a procedure file.** Procedure files describe what to do now. If a workflow needs to explain *why* it is the way it is, one sentence inline is the budget; the rest belongs here.
- **Never read this folder during a normal run.** Read it when auditing, when a decision looks wrong, or when Connor asks why something is the way it is.

## History

Pre-2026-08-12 changelogs live in `/Changelog/_history/`, one file per procedure, exactly as they were. They were not rewritten — only moved.
