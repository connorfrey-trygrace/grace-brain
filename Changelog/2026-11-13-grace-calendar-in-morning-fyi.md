# 2026-11-13 — Grace calendar added to the morning FYI to Personal Claude

**What changed:** the local scheduled task `agent-hub-visit-local` (4 AM + noon) gained **Step 2b**. On the first run of each day (detected by the text-scan marker's run date being before today), it pulls Connor's Outlook calendar for the next 14 days and sends Personal Claude one Agent Mail FYI with a section headed exactly **Grace calendar, next 14 days**. Each event gets one line (day, date, start–end ET, title). The self-blocks Morning/Afternoon Availability and Daily FTJ Conflict are skipped. If Outlook is unreachable, the section reads "Grace calendar unavailable". The FYI is sent even on days with no text findings.

**Why:** Agent Mail MSG-27 (Personal Claude, 2026-11-13). Personal Claude no longer reads Grace Outlook, so Grace Claude covers it. Connor confirmed in chat on 2026-11-13. Prep tasks for Grace events stay in Grace Tasks; Personal Claude only flags cross-calendar clashes.

**Where:** `~/.claude/scheduled-tasks/agent-hub-visit-local/SKILL.md` (pre-change copy in the session scratchpad); [[Trackers/Automation]] row updated.

**Why the 4 AM local run and not the 5 AM cloud routine:** the 4 AM run is the one that already sends Personal Claude its pre-6:15 FYI, and the M365 connector is available locally.
