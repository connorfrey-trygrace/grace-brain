---
type: changelog
date: 2026-08-12
tier: 3
touches: ["[[Workflows/Open-Actions-Tracker]]","[[Workflows/Open-Actions-Reference]]","[[Workflows/Open-Actions-Transcript-Steps]]"]
trigger: "Connor"
---
# Open-Actions-Tracker split three ways; 36 references repointed at the relevant part

The file was 32.7 KB and read in full every run, but a standalone sweep executes only Steps 0, 2.5, 3, 3.5, 4. Split into **Open-Actions-Tracker** (core sweep, 16.5 KB incl. the new entry-format spec), **Open-Actions-Reference** (schema, field authority, sort order, priority bands, status entry/exit criteria — 15.8 KB, read only when a specific decision needs it) and **Open-Actions-Transcript-Steps** (Steps 1–2, 3.8 KB, full-update mode only). A routing table at the top of the core file says which is which.

Of 79 existing references: 28 repointed to Reference, 8 to Transcript-Steps, 47 correctly stayed on the core file.
