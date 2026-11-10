---
name: "🔍 Kay Carter-Corker: Find where Rock's person-level PCO Tags attribute pulls its data"
status: completed
priority: P3
owner: "Kay Carter-Corker"
added: 2026-08-24
deadline: none
last_mentioned: "2026-08-28"
resolved: "2026-08-28"
source: "[[Transcripts/2026-08-24 18.15 Sunday Night Rock–PCO Working Session — Sync Confirmed, Tag Teams Adopted]]"
projects:
  - "Sunday Night Launch"
people:
  - "[[People/Kay Carter-Corker]]"
  - "[[People/Jennifer Claffey]]"
---

# 🔍 Kay Carter-Corker: Find where Rock's person-level PCO Tags attribute pulls its data

- [x] Work out what feeds the **`PCO Tags` extended attribute** on a Rock person profile. It is not showing tags the sync demonstrably created.

- **Source**: [[Transcripts/2026-08-24 18.15 Sunday Night Rock–PCO Working Session — Sync Confirmed, Tag Teams Adopted]] — Kay: *"let me look into the— that attribute and see what's the issue"* and, after a successful sync push, *"that means I need to explore what's happening with that attribute and where it's pulling its information from."*
- **The evidence**: Emily Horneffer has `SNL Captain` in her Rock **groups** and the matching tag on her **PCO** profile — the sync history logged it, source = Rock — but the `PCO Tags` attribute on her Rock profile does not list it. Jennifer then noticed the same attribute is also missing her **morning** captain tag, so this predates Sunday night and is not an SNL-specific fault.
- **Priority rationale**: P3 — cosmetic so far. Every load-bearing path (Rock group → PCO tag → PCO team) was verified working in the same session; this is a display field that disagrees with reality. It moves up if anyone starts reading that attribute as truth.
- **Not to be confused with** the other Rock tag class Kay described: an identifier tag she adds by hand (background check, nursery, greeter) *"without creating a whole nother attribute."* Different thing, not synced.
- **Status**: **Completed 2026-08-28** — answered, and the answer is that there is nothing to fix. PCO2 **v1** wrote tags into a Rock **defined value list** that resynced every run; **v2 dropped the defined value list** and writes the marker straight from the Rock group to the PCO team tag. The `PCO Tags` extended attribute is therefore **dead storage** — Kay: *"that space in the person's extended attributes that says PCO tags, that's no longer valid"* — which explains the stale, incomplete, old-entry-filled list, and why Jennifer's morning captain tag was missing too. Kay worked it out with **Melissa** at Rock.
- **Blocked by**: none · **Blocks**: nothing

### 2026-08-28 (transcript synthesis)
- Kay + Melissa traced it: PCO2 v2 retired the defined value list; the attribute is dead storage, not a sync failure
- → status: active → completed
[Source: [[Transcripts/2026-08-28 10.35 Rock–PCO Tag Teams Resolved — Sunday Night Attendance Metrics]]]
