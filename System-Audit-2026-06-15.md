---
title: "Second Brain — System & AI-Deployment Audit"
date: 2026-06-15
type: audit
tags: [audit, system, meta]
status: implemented-except-3-Connor-actions
---

# System & AI-Deployment Audit — 2026-06-15

Scope: the *deployment* — how I'm instructed to operate (Project panel + CLAUDE.md + /Workflows + schemas) — plus the structural and content gaps that follow from it. Nothing below has been applied. Per the maintenance tiers, structural changes are PROPOSE-ONLY; this doc is the proposal. Pick what to apply at the bottom.

---

## Honest top-line first

The system is well-built and the workflows are unusually disciplined for two weeks old. The real risk isn't sloppiness — it's **accretion outrunning use**. In ~16 days you've stood up 9 workflow files, 3 trackers, 2 instruction layers, and several note types, for a 10-hr/week role processing ~6 transcripts and 3 live events. The Open-Actions workflow alone is now a 100-line, 5-mode state machine. That machinery is impressive, but every rule is a rule I have to keep consistent, and several already contradict each other (below). The single highest-value move is **consolidation, not addition**. I'd push back on any instinct to add more before the existing layers agree with each other.

Biblical angle, since you ask for one and the vault already speaks this language: "all things should be done decently and in order" (1 Cor 14:40) is about order *serving* the body, not the reverse. A second brain that takes more tending than the ministry it supports has inverted that. Build for the 125-person Sunday machine you're stewarding, not for the system's own elegance.

---

## A. Instruction surface (the core "AI deployment" defect)

### A1 — Two instruction layers have diverged. **[Highest priority]**

There are two sets of standing instructions loaded every session, and they no longer agree:

1. **The Project Instructions panel** (app settings, titled "Grace Event Coordinator Second Brain") — describes an *older* system: folders are only `/Transcripts`, `/Synthesis`, `/Archive`; schema has **no `title`, no `processed_date`, no `event` lifecycle**; jobs are just SYNTHESIZE / MERGE / GENERATE; no `/Events`, `/Trackers`, `/Workflows`, `/Raw From Grace`; **no calendar/Outlook rule.**
2. **`/CLAUDE.md`** (in the vault) — the *current, accurate* picture: the full folder set, the `title`/`processed_date` schema, the Workflows-first rule, the Outlook calendar rule, the agent-character section.

When two loaded instruction sets conflict, behavior is non-deterministic — I may follow the stale panel on a fresh session. This is the most important thing to fix.

**Recommendation:** Make CLAUDE.md the single source of truth and reduce the panel to a pointer. I can't edit the panel (it's app config), so this one is yours to paste. Drafted replacement panel text:

> You manage a transcript-synthesis and event-coordination second brain in this Obsidian vault. **The authoritative spec is `/CLAUDE.md` in the vault — always follow it.** Before any task, check `/Workflows` for an applicable procedure and follow it if one exists. Be direct, structured, low-fluff. Report what you did and found, not what you're about to do. Never delete files (move to `/Archive`); never modify `/Raw From Grace`; ask before merging, archiving, or destructive changes.

That keeps the panel from drifting again because it no longer duplicates anything.

### A2 — CLAUDE.md FOLDERS list is incomplete.

`/Agendas`, `/Contacts`, and `/Raw From Grace` all exist and are in active use, but the FOLDERS block omits the first two entirely and only mentions `/Raw From Grace` down in RULES. A fresh session won't know `/Agendas` or `/Contacts` exist. **[Tier 2 — ask first, since it's a schema/structure change]**

Drafted additions to the FOLDERS block:

```
- /Agendas — meeting agendas you draft ahead of syncs/check-ins
- /Contacts — vendor/staff contact sheet and credentials
- /Raw From Grace — READ-ONLY source folder (historical checklists, signs). Never write here.
```

### A3 — Undocumented note types invented ad hoc.

Two note types now exist with no schema or workflow governing them:
- **Day-Of Planner** (`2026-09-20-Sunday-Night-Service-Planner.md`) — a companion to the event note, created 6/15. Good idea, but there's no rule for *when* a planner spins off vs. staying in the event note, and the next planner will be shaped differently.
- **Agendas** — two agenda files exist with no format spec or trigger.

**Recommendation [Tier 3 — propose]:** if the day-of planner is a pattern you want to keep, add a short section to `event-planning-note.md` defining when a planner splits off (suggest: at `active` status, or when the run-of-show needs its own timeline) and its required sections. Same for a lightweight agenda convention. I've left these as proposals, not drafts, because I don't yet know if you want them standardized or were one-offs — **which is it?**

---

## B. Workflow drift & gaps

### B1 — Open-Actions vocabulary doesn't match its own workflow or tracker. **[Tier 1/2]**

- The **workflow** (`Open-Actions-Tracker.md`) defines sections: Active / **In Progress** / Stale / Completed. But Step 2.5 then says "Active, In Progress, **and Monitoring**" — a third term the schema never defines.
- The **live tracker** (`Open Actions.md`) uses: Active / **Monitoring** / Completed / **Stale / Resolved Without Confirmation** — i.e. it dropped "In Progress," renamed it "Monitoring," and renamed "Stale."

Three documents, three vocabularies. Pick one set of section names and make all three agree. My recommendation: **Active / In Progress / Stale / Completed** (the workflow's own canonical set), and treat "Monitoring" as a note, not a section. This is a Tier 1 clarity fix in the workflow text and a Tier 2 relabel in the tracker.

### B2 — MERGE is a named job with no workflow. **[Tier 3 — propose]**

CLAUDE.md lists "MERGE split recordings when asked" as Job #4, and merging has clearly happened (Archive holds split files; the re-transcription logic in synthesis Step 10 exists *because* of merges; speaker-id has a merge edge case). But there's no `/Workflows/merge-recordings.md`. The rules are scattered across three other files. For a destructive-ish, ask-first operation, that's exactly the kind of thing that should be one procedure. I can draft it if you want.

### B3 — No speaker-name format convention. **[Tier 2 — ask first]**

The same person is "Jennifer" in some transcripts and "Jennifer Claffey" in others; "Derek" vs "Derek Adye." Speaker-identification doesn't specify a format, so search and cross-referencing fragment. **Recommendation:** add one line to `Speaker-Identification.md` Step 5 — "Use full name (First Last) on first identification; if only a first name is known, use that consistently. Match the spelling already used in `/Contacts` and prior transcripts." Tier 2 because it's a new rule.

### B4 — Room-setup memory rule isn't baked into the template. **[Tier 2]**

Stored memory says *Connor owns room setup/teardown on all events through ~Dec 2026 — pre-fill, don't leave TBD.* But the `event-planning-note.md` template still shows "Room setup/teardown | Name | TBD," and the Sunday Night note correctly leaves it... as TBD (violating the memory). Fold the rule into the template so it's applied without relying on memory recall: default that row's owner to **Connor** through Dec 2026.

---

## C. Data integrity & content gaps

### C1 — Staff AVL identity is contradicted across three files. **[Flag — needs your fact]**

Who runs AVL is genuinely unclear in the vault:
- `Concert-Checklist.md` → **Joe** (AVL lead)
- `Vendors.md` → "**Joe** — may no longer be in role" + "**Jean Paul** — assumed current AVL lead — confirm"
- `Service-Structure.md`, both event notes, transcripts → "**John Paul**" (Sunday-night sound tech, confirmed)

"Jean Paul" vs "John Paul" is almost certainly one person mangled by transcription, but Joe-vs-John-Paul is a real open question. This affects who gets assigned on every event. **Who currently leads AVL, and is "Jean Paul" the same person as "John Paul"?** Once you tell me, I'll reconcile all three files.

### C2 — World Cup event-note filename is now wrong. **[Ask first — rename]**

The event moved to **July 19**, the frontmatter and body say July 19, but the file is still named `2026-07-11-World-Cup-Viewing-Party.md` and the Events tracker links to that old name. The event-planning-note convention is `YYYY-MM-DD-...`, so the filename violates the spec. Renaming touches the tracker link and the two source references that point at it. Want me to rename to `2026-07-19-...` and fix the inbound links? (Ask-first because it's a structural change.)

### C3 — Trackers lag the event notes. **[Tier 1]**

`Trackers/Events.md` lists only 3 events and doesn't include the **Sunday Night Service Day-Of Planner**, and its World Cup row still implies the date is settled when the note marks it "pending Komar + John." Low-stakes, but the tracker is supposed to be the at-a-glance index. I can refresh it.

### C4 — Transcript date error / probable near-duplicate. **[Flag]**

`2026-06-02 16.10 Connor Onboarding — Initial Intro Meeting.md` has `date: 2026-06-03`, but its source files are both `...06-02...mp4` and the meeting was June 2 — the date field looks like it caught the *processing* date. Separately, that transcript and `2026-06-02 17.01 — Full Onboarding Planning Meeting.md` **both list source file `...16-16.mp4`** and have near-identical summaries — possible overlap/double-coverage of the same recording. Worth a look before the next weekly synthesis double-counts them (the 6/12 weekly already included both). I held off touching transcript frontmatter per the no-edit rule — **want me to investigate and propose a fix?**

### C5 — Plaintext credentials in a cloud-synced vault. **[Security flag]**

`Contacts/Credentials.md` stores the Sign Up Genius password and both WiFi passwords in plaintext, in a Dropbox-synced vault. The WiFi keys are low-sensitivity; the **Sign Up Genius login is a shared account credential** sitting in cloud sync. I'd recommend moving that one out of the vault (password manager) and leaving a pointer, or at minimum acknowledging the exposure. Not mine to decide — flagging it.

### C6 — Orphaned, undocumented assets. **[Tier 2/3]**

- `Trackers/Hours.md` — actively maintained, but no workflow governs it and CLAUDE.md never mentions hour-logging as a job. If logging hours is part of the role, it should be a documented job; if it's personal, fine, but say so.
- `Welcome.md` — still the default Obsidian boilerplate ("delete this note and make the vault your own"). Harmless, but it's literally instructing deletion in a vault whose first rule is "never delete." I'd replace it with a one-paragraph vault map. (Can't delete per rules — I'd overwrite it.)
- "weekly/**monthly** synthesis" appears in the old panel, but only a weekly workflow exists. Decide whether monthly is a real thing or drop the word.

---

## D. Prioritized action list

**Do-now, low-risk (Tier 1 — I can apply on your say-so):**
- B1 workflow-text clarity fix (vocabulary)
- C3 refresh Events tracker
- C6 replace Welcome.md boilerplate with a vault map

**Ask-first (Tier 2 — your call, drafts ready above):**
- A2 add missing folders to CLAUDE.md
- B3 speaker-name convention
- B4 room-setup default in template
- B1 relabel live tracker sections
- C1 reconcile AVL identity (need your fact first)
- C2 rename World Cup note + fix links

**Propose-only (Tier 3 — you decide if they should exist):**
- A1 collapse the Project panel to a pointer *(highest overall priority — only you can edit the panel)*
- A3 standardize Day-Of Planner + Agenda note types
- B2 write a merge-recordings workflow

**Flags needing a fact from you, not a change:**
- C1 (who leads AVL / Jean=John Paul?), C4 (duplicate transcript), C5 (credentials exposure)

---

## My three questions for you
1. **A3:** Is the Day-Of Planner a pattern to standardize, or was the Sunday-night one a one-off?
2. **C1:** Who currently leads AVL, and is "Jean Paul" = "John Paul"?
3. **C4:** Want me to investigate the possible duplicate onboarding transcript?

## Implementation log — 2026-06-15

Implemented (Connor approved "everything else"):
- **A2** — CLAUDE.md FOLDERS list completed (/Agendas, /Contacts, /Raw From Grace named; trackers named; "monthly" dropped); added Job 6 (Agendas) and linked Job 4 (Merge) to its workflow.
- **A3** — Day-Of Planner spec added to event-planning-note.md; new agenda-note.md workflow created (Connor: "standardize").
- **B1** — Fixed "Monitoring" drift in Open-Actions workflow Step 2.5; relabeled live tracker sections to In Progress / Stale.
- **B2** — New merge-recordings.md workflow created.
- **B3** — Speaker-name convention added to Speaker-Identification.md.
- **B4** — Room setup/teardown defaults to Connor (through Dec 2026) in the event-note template.
- **C1** — AVL identity reconciled: Jean Paul = John Paul = current audio lead (per Connor) in Vendors.md; Joe reframed as historical/confirm in Vendors + Concert-Checklist.
- **C2** — World Cup note renamed `2026-07-11…` → `2026-07-19…`; inbound links fixed (Events tracker, check-in agenda, form draft, workflow example).
- **C3** — Events tracker refreshed (pending-date flag, planner link, Chandler Moore status).
- **C5** — Security callout added to Credentials.md (SUG credential left in place pending migration).
- **C6** — Welcome.md boilerplate replaced with a vault map.

Still needs **Connor** (can't be done from here):
1. **A1 — collapse the Project Instructions panel to a pointer.** This is app config, not a vault file. Paste the drafted text in §A1. *Highest-priority item overall — until this is done, the stale panel can still override CLAUDE.md on a fresh session.*
2. **C5 — migrate the Sign Up Genius password** to a password manager, then tell me to redact it from Credentials.md.
3. **C1 — confirm with Brian** whether Joe still covers any concert AVL (John Paul is current audio lead either way).

C4 (possible duplicate onboarding transcript) — skipped per Connor.

## Changelog
- 2026-06-15: Audit created. Tier 3 (new file). Trigger: Connor's request to audit the project / AI deployment.
- 2026-06-15: Implementation log added; 11 of the recommendations applied, 3 left as Connor actions. Trigger: Connor approved implementing all recommendations.
