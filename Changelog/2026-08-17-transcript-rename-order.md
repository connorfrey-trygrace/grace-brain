---
type: changelog
date: 2026-08-17
tier: 1
touches: ["[[Workflows/Transcript-Synthesis]]"]
trigger: "Repeat defect during transcript processing"
---
# Transcript-Synthesis Step 3.5 now states the rename-before-write ordering

The write-titled-file-then-delete-original pattern fails on this vault because `device_bash` cannot delete, and the salvage path (`mv old new`) then overwrites the freshly written frontmatter with the raw original. It cost a regenerate-the-frontmatter cycle on 2026-08-11 and, despite that run logging *"it will recur on the next transcript otherwise,"* it recurred on the very next transcript (2026-08-17). The lesson lived only in `/Logs/refresh-run-log.md`, which is never read on a normal run — so it was never going to be seen at the moment it was needed. One sentence added to Step 3.5, where the rename is actually performed.
