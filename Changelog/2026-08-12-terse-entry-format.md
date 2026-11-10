---
type: changelog
date: 2026-08-12
tier: 2
touches: ["[[Workflows/Open-Actions-Tracker]]","[[Workflows/text-message-sync]]","[[Workflows/m365-to-obsidian-sync]]"]
trigger: "Connor"
---
# Sync entries are now terse timestamped lines, not narrative

Dated entries had grown to essays — one bullet in a single action note measured **4,966 bytes**. Since wall-clock on a refresh tracks tokens *generated*, entry length was the largest controllable cost in a run. New mandatory format in Open-Actions-Tracker § Entry format: one line per event (`H:MM AM/PM · who + what`, ≤12 words), no verbatim quotes unless the quote is the content, no interpretation, a `→ field: old → new` line only when something actually changed. Judgment goes in the run report to Connor, not into the note. Both syncs point at it.

Also added: **superseded content is deleted, not struck through** — `~~strikethrough~~` left the wrong version on the page and doubled the bytes every future run read. Cleared from all live action notes.
