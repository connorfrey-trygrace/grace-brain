---
title: "Second Brain — System & AI-Deployment Audit"
date: 2026-06-25
type: audit
tags: [audit, system, meta]
status: implemented-except-1-Connor-action
---

# System & AI-Deployment Audit — 2026-06-25

Second deep audit, ten days after the [[System-Audit-2026-06-15]] baseline. Scope per [[Workflows/system-audit]] deep mode: full light checklist + every workflow read end-to-end, changelog discipline, /Contacts hygiene and credential exposure, tier-rule adherence, and complexity-vs-usage. Nothing below is applied — this is the proposal. Pick what to apply at the bottom.

---

## Honest top-line first

The mechanical health is **excellent** and better than the 6/15 baseline. Concretely verified this pass: wikilinks are clean (the only unresolved `[[…]]` strings are illustrative placeholders in workflow docs and memory-slug cross-refs in the migration backup — zero real broken links across ~40 notes); event-note filenames all match their `date`; the Open-Actions tracker and its workflow now **agree** on section vocabulary (Active → In Progress → Waiting On → On Hold → Stale → Completed), which closes the three-vocabularies drift that was the headline defect last time. The disciplined changelog habit is holding across CLAUDE.md, trackers, workflows, and contacts.

So the problem is no longer drift *inside* the note system. It's that **the system grew a whole second body — an automation layer — that the documentation doesn't describe, and that documentation is already going stale.** In ten days you added a text-message source, an email-to-Obsidian sync, a contacts/phone-resolution subsystem, six scheduled tasks, and a project migration. CLAUDE.md still describes the smaller 6/16 system. The only inventory of what runs automatically lives in a folder explicitly marked "delete after verifying." And you just changed the automation cadence (paused the hourly text scan), which now contradicts what two files still claim.

Biblical angle, since you ask for one: last time I cited "decently and in order" (1 Cor 14:40). The follow-on is stewardship — "it is required of stewards that they be found faithful" (1 Cor 4:2). Faithfulness here isn't more machinery; it's making the machinery you've already built *legible* so it can be trusted and handed off. A second brain whose automation only its builder can enumerate isn't yet robust — it's load-bearing tribal knowledge. The single highest-value move this round is **writing the automation layer down in a durable place**, not adding capability.

---

## A. The automation layer is undocumented and its docs are already stale. **[Highest priority]**

Six scheduled tasks run (or ran) automatically against this vault:

| Task | Cadence | Governing workflow | Touches |
|---|---|---|---|
| `weekly-synthesis` | Fri 4:09 PM | [[Workflows/weekly-synthesis]] | /Synthesis, light audit |
| `daily-stale-sweep` | Mon–Fri 5:32 PM | [[Workflows/Open-Actions-Tracker]] | /Trackers/Open Actions |
| `m365-to-obsidian-sync` | 8a/12p/4p daily | *(none — undocumented)* | trackers, event notes (from Outlook) |
| `event-checklist-autocopy` | 7:02 AM daily | event-planning-note / Internal-Event-Checklist | /Events Day-Of Planners |
| `grace-text-scan-hourly` | hourly *(paused 6/25)* | [[Workflows/text-message-sync]] | trackers, event notes (from iMessage) |
| `daily-finance-scan` | 6:04 AM daily | *(none — different vault)* | Personal Finance vault, not Grace |

Three problems:

1. **No durable record.** The only place all six are inventoried is `_Migration/MIGRATION-GUIDE.md`, which says of itself: *"This `_Migration/` folder is temporary — remove it once the migration is verified."* When that folder is archived, the only map of what runs automatically against the vault disappears. A fresh session — or you in three months — has no way to know what's firing, when, or why a tracker changed overnight.

2. **The record is already stale.** That inventory lists `grace-text-scan-hourly` as hourly and active. You paused it today. `text-message-sync.md` (intro line 3 **and** its changelog) still states *"Runs hourly via the scheduled task `grace-text-scan-hourly`."* Both now misdescribe reality.

3. **Two tasks have no governing workflow at all.** `m365-to-obsidian-sync` writes email-derived content into trackers and event notes three times a day, and `event-checklist-autocopy` auto-creates Day-Of Planners — neither has a `/Workflows` procedure. They're pure tribal knowledge living only in the scheduled-task SKILL.md files outside the vault.

**Recommendation — create `/Trackers/Automation.md`** (or an "Automated jobs" section in CLAUDE.md): one row per task — id, cadence, enabled/paused, governing workflow, what it reads, what it writes, last-changed note. Make *that* the source of truth the migration guide currently impersonates. **[Tier 2/3 — propose; I can draft it from the table above.]**
**Tier-1 companion fix (can apply now):** update `text-message-sync.md` intro + changelog to reflect the new on-demand / when-working cadence instead of "hourly," matching the 6/25 schedule change.

---

## B. CLAUDE.md no longer describes the live system. **[Tier 2/3 — propose]**

CLAUDE.md's JOBS list (1 speaker-ID, 2 synthesis, 3 event notes, 4 merge, 5 weekly synthesis, 6 agendas) is the same six from 6/16. But the system now also, as standing behavior:

- **Reads Connor's texts** as a first-class source feeding the trackers (`text-message-sync`) — and requires the **Messages folder mounted** (`~/Library/Messages`) to do it. A fresh session reading only CLAUDE.md wouldn't know texts are a source, that `chat.db` is read read-only, or that the Sky 1:1 thread is hard-excluded.
- **Reads Outlook email/calendar** and folds it into trackers (`m365-to-obsidian-sync`). Yet `weekly-synthesis` still carries the rule *"Source is always /Transcripts/; never substitute calendar events or email."* Those are reconcilable (synthesis ≠ the sync job) but the seam is undocumented, and a fresh session could read the rule as "ignore email" while a daily job does the opposite.
- **Runs a contacts/phone-resolution subsystem** (`Contacts/Phone-Index.md` + a `.vcf` export), none of which CLAUDE.md mentions alongside `/Contacts`.

On 6/23 you deliberately chose to keep the texts workflow out of CLAUDE.md ("workflow-only"). That was reasonable for one workflow. Three sources and four automated jobs later, the cumulative effect is that **CLAUDE.md under-describes the deployment** — which is exactly the "two instruction layers diverging" failure mode that was item A1 last time, just relocated from the panel to CLAUDE.md itself.

**Recommendation:** add a short **"Sources & automated jobs"** block to CLAUDE.md naming texts and Outlook as live sources, the Messages/Office mounts they need, and a pointer to `/Trackers/Automation.md`. Keep it to ~8 lines — a map, not a duplicate of the workflows. **[Tier 2 — your call; I'll draft before applying.]**

---

## C. Orphans & accretion

- **`/Grace Brain`** — empty folder at vault root, created 6/26, no governing mention anywhere. Almost certainly an accidental artifact (it shares the project's display name). **Recommend: remove (move to /Archive). [Ask-first.]**
- **`Untitled.base`** — empty Obsidian Bases file (a stub `views: table` with no data source), orphaned at root. **Recommend: archive, or build it into something real (e.g. a Bases view over /Events). [Tier 1 once you say which.]**
- **`_Migration/`** — the migration appears **complete**: this session is running on the Dropbox vault, all 6 tasks are present, and memory is intact (15 files; backup and live index agree — the guide's "16" was approximate). Per the guide's own instruction, once you confirm you're satisfied, **archive the folder**. Note: `_Migration/memory-backup.md` is the source of the 15 "broken link" warnings Obsidian's graph will show — they're memory-slug refs, harmless, and they vanish when the folder is archived. **[Ask-first — it's the documented final migration step.]**
- **Accretion check:** 13 workflow files for a 10-hr/week role is at the edge of "more system than ministry," but unlike 6/15 I can't point to a workflow that isn't earning its keep — each maps to a real recurring task. Holding the line, not flagging. The thing to watch is *task* accretion (6 scheduled jobs), which is why A and B matter more than trimming workflows.

---

## D. Schema / date drift (transcripts). **[Flags — ask-first, touches transcript frontmatter]**

- **`2026-06-21 16.28 Nathan Ebikwo …`** has `date: 2026-06-22`, but its `source_file` is `Meeting 2026-06-21 16.21.mp4` and the filename prefix is 06-21 — the call was **June 21**. The `date` caught the processing day. Confirmed off by one.
- **`2026-06-02 16.10 … Initial Intro Meeting`** still has `date: 2026-06-03` against a 06-02 recording — the same C4 flag from 6/15 (you skipped it then), plus the unresolved near-duplicate question with the 17.01 onboarding transcript (overlapping `source_file`). Still open.

Neither affects a live deliverable, but both will mislead any date-based synthesis. Want me to correct the two `date` fields (frontmatter only, bodies untouched) and finally settle the duplicate question? **[Ask-first.]**

---

## E. Credential exposure has grown, not shrunk. **[Flag — needs Connor; I'd actually push on this one]**

At 6/15 I flagged one shared password (Sign Up Genius) sitting in plaintext in a cloud-synced vault and recommended migrating it to a password manager. It wasn't migrated — and on 6/18 a **second** shared credential (Instacart business account) was added, also plaintext. So the exposure **doubled** since the last audit: two shared `jennifer.claffey@trygrace.org` account passwords now live in `Contacts/Credentials.md`, synced to Dropbox and every linked device, plus a payment-card-ending and delivery address.

This is your call, not mine, and I'm not going to nag it into every future report — but you asked me to challenge you, so plainly: this is the one finding in this audit I'd act on today rather than file. The WiFi keys are fine. The two shared logins are the kind of thing that, if the vault sync is ever compromised or shared too broadly, hands someone a staffer's volunteer-management and purchasing accounts. Move both to 1Password/Bitwarden, leave a pointer in the file, and tell me — I'll redact the values the same minute.

---

## F. Prioritized action list

**Do-now, low-risk (Tier 1 — I can apply on your say-so):**
- A · Update `text-message-sync.md` (intro + changelog) to the new on-demand cadence (currently says "hourly").
- C · Archive `Untitled.base` (or repurpose it — your pick).

**Ask-first (Tier 2 — your call, I'll draft before touching):**
- A · Create `/Trackers/Automation.md` as the durable scheduled-task inventory.
- B · Add a "Sources & automated jobs" block to CLAUDE.md (texts + Outlook + mounts + pointer).
- C · Remove `/Grace Brain` (empty) to /Archive.
- C · Archive `_Migration/` (documented final migration step) once you confirm you're satisfied.
- D · Fix the two transcript `date` fields + resolve the onboarding near-duplicate.

**Propose-only (Tier 3 — you decide if they should exist):**
- A · Write governing workflows for `m365-to-obsidian-sync` and `event-checklist-autocopy` (currently undocumented automated jobs).

**Flags needing a decision, not a change:**
- E · Migrate the two shared credentials out of the vault (Sign Up Genius + Instacart).

---

## My questions for you

1. **A/B:** Do you want the automation inventory as a new `/Trackers/Automation.md`, folded into CLAUDE.md, or both (CLAUDE.md points at the tracker)?
2. **D:** Correct the two transcript dates and finally settle the 6/02 duplicate, or leave them?
3. **E:** Are you willing to migrate the two shared passwords now so I can redact them?
4. **C:** Confirm migration is verified so I can archive `_Migration/`?

## Implementation log — 2026-06-25

Connor confirmed all questions/proposals. Applied:

- **A · Automation cadence + inventory.** `grace-text-scan-hourly` rescheduled hourly → **daily 8 AM** (`0 8 * * *`) + on-demand (Connor's call: hourly wasteful, fully-manual suboptimal). `text-message-sync.md` intro + changelog corrected off "hourly." Created **/Trackers/Automation.md** as the durable scheduled-task inventory (all 6 tasks, mounts, daily-over-hourly preference) — replaces the temp `_Migration` table.
- **A (Tier 3) · Governing workflows written** for the two undocumented jobs: **/Workflows/m365-to-obsidian-sync.md** and **/Workflows/event-checklist-autocopy.md** (mirrored from the live task definitions).
- **B · CLAUDE.md now describes the live system.** Added a SOURCES & AUTOMATED JOBS section + Jobs 7–9 (text/email/checklist); named texts + Outlook as first-class sources; added Automation.md + Phone-Index.md to FOLDERS; clarified weekly synthesis stays transcripts-only.
- **C · Orphans archived.** `Untitled.base`, the empty `/Grace Brain`, and the completed `_Migration/` all moved to /Archive. Migration confirmed complete (15 memories intact).
- **D · Transcript dates fixed.** Nathan Ebikwo `2026-06-22 → 2026-06-21`; Initial Intro `2026-06-03 → 2026-06-02`. **Duplicate settled:** "Initial Intro Meeting" (combined, both source clips, 53.8 min) kept as canonical; the two split re-transcriptions ("Full Onboarding Planning" `16-16` + "Intro Clip" `16-01`, 45.5+8.3=53.8) archived as DUPs; the 5 inbound links in Weekly 2026-06-12 repointed to the canonical note and its count corrected 5→4.

Verified after changes: zero real broken wikilinks; root cleaned; 15 workflows; one onboarding transcript remains.

**Still needs Connor (the one item I left):**
- **E · Credential migration.** Both shared passwords (Sign Up Genius + Instacart) are still in `Contacts/Credentials.md` — I left the values in place so your access isn't broken. Move them to a password manager, then tell me and I'll redact them the same minute.

## Changelog
- 2026-06-25: Implementation log added; all items applied except the Connor-only credential migration. Trigger: Connor confirmed all proposals.
- 2026-06-25: Second deep audit created (10 days after baseline). Verified 6/15 vocabulary drift is resolved; new headline is the undocumented automation layer + stale automation docs. Tier 3 (new file, proposal-only). Trigger: Connor's request to audit the vault and make the system robust.
