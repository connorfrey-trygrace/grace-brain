---
title: "Second Brain — System & AI-Deployment Audit"
date: 2026-09-15
type: audit
tags: [audit, system, meta]
status: proposed
---

# System & AI-Deployment Audit — 2026-09-15

Third deep audit (after [[System-Audit-2026-06-15]] baseline and [[System-Audit-2026-06-25]]), Connor's explicit request. Scope per [[Workflows/system-audit]] deep mode: full light checklist (9 items) + every workflow read for internal contradictions, changelog discipline, `/Contacts` hygiene and credential exposure, tier-rule adherence, and complexity-vs-usage. Tier-1 items below are already applied (noted inline); everything else is proposed only.

---

## Honest top-line first

Mechanically, the note layer is in good shape — the last two audits' headline defects (three-vocabulary drift, undocumented automation layer) are still resolved, and the vault has clearly kept building real capability since 6/25 (People layer, Automation.md, /Logs, /Changelog, the split-note-log tooling, a functioning `actions-index.py` sweep). But two of the *same three failure classes* from 6/25 have quietly recurred in new forms, plus one new one:

1. **CLAUDE.md drifted behind the automation layer again** — same failure as 6/25 item B, different cause. `grace-weekly-refresh` was retired as a scheduled job on 2026-09-12 (Connor's call — he runs refreshes manually now), and both governing workflow files were correctly updated the same day. CLAUDE.md was not, and neither was `event-checklist-autocopy.md` for its own 2026-08-29 retirement (I fixed the latter directly — see Tier 1 below — but CLAUDE.md itself is Tier 3, propose-only).
2. **A one-time cleanup never became a standing rule, twice.** The 2026-08-12 "94 completed actions archived" cleanup has fully recurred — 96 of 140 action notes (69%) are `status: completed` and un-archived again. And the 2026-08-14 "broken People links" fix recurred once more in a single transcript (already fixed — see Tier 1).
3. **The automatic watchdog is now fully gone, and the tool to verify scheduler state directly is still broken.** `grace-weekly-refresh` carried the *only* scheduled m365-health-check and scheduler-heartbeat duties. Retiring it (a deliberate, reasonable call) means nothing on a cadence checks for silent gaps anymore — only Connor asking for one. In practice he's asking for `grace-quick-refresh` very frequently (4 runs on 9/15 alone), so the trackers themselves look current. But `list_scheduled_tasks` still returns nothing from this session (the same gap flagged 2026-08-10 and restated 2026-09-12) — I cannot independently confirm the retired job is actually disabled at the scheduler level, or that the other four "active" rows in Automation.md match reality.

Nothing below is destructive or urgent-tonight. The credential-migration ask from 6/15 and 6/25 is still open and is the one item I'd genuinely push on again.

---

## A. CLAUDE.md no longer describes the live automation state. **[Tier 3 — propose only, Project-Instructions-equivalent]**

Three concrete mismatches, all sourced against `Trackers/Automation.md` (the vault's declared source of truth):

1. **Job 7 & Job 8** ("Runs via `grace-weekly-refresh` (Mon 6 AM) + on-demand via `grace-quick-refresh`") and the **SOURCES & AUTOMATED JOBS** block ("a couple (Jobs 7–8, plus the Open Actions sweep) run on a weekly floor + on-demand model... see `grace-weekly-refresh.md` for the Monday 6 AM safety net (same phases, run unattended)") — **false since 2026-09-12.** There is no Monday 6 AM run anymore; it's on-demand only, with no scheduled floor under it.
2. **Job 9** ("EVENT CHECKLIST AUTO-COPY... Runs daily 7 AM") — **false since 2026-08-29.** Retired; Callie Taylor now owns discrete events.
3. **FOLDERS → /Trackers** lists only Actions/Action-Logs/Open Actions.base/Events.md/Hours.md/Automation.md — omits `Trackers/Subscriptions.md` (created 2026-08-18, governed, actively used) and `Trackers/Calendar-Window.md` (generated every refresh, referenced by 3 workflows). Also never mentions `/Reference` (see item G), which is real and in active use.

**Draft replacement text** (for Connor to accept/edit — I did not apply this):

> 7. TEXT-MESSAGE SYNC — see /Workflows/text-message-sync.md. Folds Grace-relevant iMessage/SMS into the trackers. Runs on-demand via `grace-quick-refresh` (see /Workflows/grace-quick-refresh.md); the former Monday 6 AM `grace-weekly-refresh` safety net was retired 2026-09-12 — Connor runs refreshes manually now.
> 8. M365 → OBSIDIAN SYNC — see /Workflows/m365-to-obsidian-sync.md. Folds new Outlook email (inbox + sent) into the trackers/event notes. Same on-demand-only model as Job 7.
> 9. EVENT CHECKLIST AUTO-COPY — see /Workflows/event-checklist-autocopy.md. Stands up a Day-Of Planner + copies the checklist when an event is ≤1 week out. **Retired as a scheduled task 2026-08-29** (Callie Taylor now owns discrete events); kept for reference if a discrete Connor-owned event reappears.
>
> — and in FOLDERS: `/Trackers/Subscriptions.md` (recurring paid tools/renewals) and `/Trackers/Calendar-Window.md` (Connor's rolling 3-week Outlook window, regenerated every refresh) added to the /Trackers line; `/Reference` (brand/reference material, e.g. `Grace-Brand-Colors.md`) added as its own FOLDERS line.

---

## B. The only scheduled watchdog is gone, and I still can't verify scheduler state directly. **[Flag — not a defect, a consequence of Connor's own 9/12 call; needs awareness]**

`grace-weekly-refresh.md` correctly documents this: its two watchdog duties (m365 Run Log health check, scheduler heartbeat) plus the frontmatter/body drift check "run here and nowhere else." Retired 2026-09-12, they now only happen if Connor explicitly asks for a weekly-style pass — and the refresh-run-log shows every run since 9/12 has been `grace-quick-refresh`, never the weekly procedure. I ran the substance of both checks by hand as part of this audit:

- **m365 Run Log health check:** clean. Entries in `Logs/m365-sync-run-log.md` are frequent (multiple per day) with no multi-day gaps and no `ERROR:` lines since 9/12.
- **Scheduler heartbeat:** **could not verify.** `list_scheduled_tasks` returns "No scheduled tasks found" from this session — the same structural gap Automation.md's own changelog flagged 2026-08-10 ("not visible as global... appears project-scoped") and restated 2026-09-12 ("this session cannot see or disable the live scheduled task itself"). I cannot confirm from here that `grace-weekly-refresh` is actually disabled at `~/Claude/Scheduled/`, nor verify the real enabled/cadence state of `weekly-synthesis`, `derek-weekly-sync-agenda`, or `persona-refresh-quarterly-sweep`. This has been open, tracked, and unresolved for 5+ weeks across two audit passes now.

**Needs Connor:** check `~/Claude/Scheduled/` directly (or wherever the scheduler UI lives) and confirm (a) `grace-weekly-refresh` is actually off, not just documented as off, and (b) the other four Grace tasks match their Automation.md rows. This session has no path to that verification.

---

## C. Trackers/Actions accretion has fully recurred. **[Tier 2/3 — propose a repeat cleanup + a standing rule]**

The 2026-08-12 changelog entry ("94 completed action notes moved to /Archive/Actions... the folder only ever grew") described exactly the state the folder is back in: **96 of 140 notes (69%) are `status: completed`**, still sitting in the live `/Trackers/Actions/` folder that every sweep, grep, and Base view ranges over. This isn't a speed problem (`actions-index.py` reads the whole folder in tens of milliseconds) — it's the same hygiene argument the 8/12 entry made: sweeps and views shouldn't range over 96 dead items to find the 44 live ones.

**What's missing isn't the fix — it's that the fix was never made a rule.** The 8/12 cleanup was a one-time manual sweep with wikilink repointing, not a policy, so nothing stops it from re-accumulating a third time in another five weeks.

**Propose:**
1. Repeat the 8/12 sweep: move the 96 `status: completed` notes to `/Archive/Actions/`, repoint their inbound wikilinks (the 8/12 precedent repointed 174 links across 35+ files — expect a similar scale). Mechanical, well-precedented, but **non-trivial in size**, so I flagged rather than ran it.
2. Decide a standing rule so this is the last manual sweep needed — e.g., fold "archive `status: completed` notes with `resolved` older than N days" into `grace-quick-refresh`'s Open Actions sweep phase (Step 0/Step 3 area), or add it as a periodic `actions-index.py` flag the way `OVERSIZED NOTES` already works.

---

## D. Orphans & accretion (root + a couple of folders)

- **`/Reference/Grace-Brand-Colors.md`** — real, actively linked from 4 live files (an action note, a Synthesis note, an Agenda), but absent from CLAUDE.md's FOLDERS list. Folded into the item A draft above. Not itself a problem — just undocumented.
- **`/_to_delete/`** — an ad hoc staging folder (3 tmp `.py` scripts, one superseded doc, a `dup-log-copies/` subfolder, a `2026-08-29-deck-render-tmp/` subfolder of slide-render PNGs), all untouched for 2+ weeks, named for a deletion the vault's own rule forbids. It duplicates `/Archive`'s purpose without being documented anywhere. **Propose:** move its contents into `/Archive` (satisfies never-delete, removes the undocumented folder). Ask-first per the non-trivial-move rule — flagged, not moved.
- **Loose files at vault root, outside CLAUDE.md's structure:**
  - `Picture1.png` and `Sunday_Night_Service_Promo_Deck_73026.potx`/`.pptx` (all dated 2026-08-18, ~1 month old) look like Sunday Night Service promo assets that belong in `/Events/2026-09-20-Sunday-Night-Service/`, where the equivalent `Formation-Lunch-Deck` files already correctly live.
  - `GraceCommunity_BrandGuideline_190627 (1).pdf` — dated **today** (2026-09-15 16:05), almost certainly the attachment from Heather Noble's brand-guidelines email that a same-day refresh closed out (`Logs/m365-sync-run-log.md`, 16:16 ET entry: "Heather Noble brand-guidelines email → closed active item"). Needs filing, not yet a problem at 1 day old.
  - `Test Canvas.canvas` (2026-06-25, unreferenced) and `feedback.json` (2026-07-16, unreferenced — this is skill-eval harness output, e.g. `"run_id": "eval-0-full-system-audit-with_skill-run-1"`, literally test debris from evaluating this same audit skill, not vault content at all).
  - **Propose:** file the four Sunday-Night/brand assets into `/Events/2026-09-20-Sunday-Night-Service/` or `/Reference`; archive `Test Canvas.canvas` and `feedback.json`. All ask-first (file moves), none urgent.
- **`Welcome.md` was stale** — fixed directly (Tier 1, see below).
- **`Workflows/event-checklist-autocopy.md` was stale** — fixed directly (Tier 1, see below).
- Not flagging: `Advisory-Audit-2026-07-16.md` and the two prior `System-Audit-*.md` files sitting at vault root are the established, intentional pattern for one-off dated audit docs (per `system-audit.md` itself) — not accretion.
- Not touching: `Workflows/advisory-board-panel.md`'s Provenance Log currently looks mid-update from a separate, already-in-flight persona-refresh pass — expected, per your note, not a finding.

---

## E. Michele Smith has no People representation at all. **[Flag — needs Connor's call, already open 18 days]**

Referenced across 12+ live files (multiple `/Trackers/Actions` notes, 2 transcripts, `Contacts/Phone-Index`, an Agenda) since at least July — she appears to run Planning Center support for the Grace KIDS team. She has **no standalone person note and no Good Noodles roster row**. The 2026-08-28 weekly synthesis already flagged this ("pending your call") on the broken `[[People/Michele Smith]]` link in `Connor - Ask Michele Smith for her Planning Center starter email...` — still broken today, 18 days later. Per [[Workflows/people-notes]]'s own threshold ("Grace staff/a named vendor with an ongoing role" OR "3+ meetings/events"), she likely clears the bar for at least a Good Noodles row, possibly a full person note given the ongoing PCO-support role — genuinely your call, not mine to fabricate. **Needs Connor:** add her (roster row or person note), then the one link gets repointed.

---

## F. `Trackers/Events.md` and `Trackers/Automation.md` both carry a growing inline changelog, despite being read on every relevant run. **[Tier 2/3 — a gap in the convention itself, propose only]**

CLAUDE.md's own rule is unqualified: *"A note that is read on every run must not carry its own append-only history. Vault-wide, no exceptions."* Two files violate this on inspection:

- **`Trackers/Events.md`** — read by the tracker-freshness check every week; carries an 11-entry `## Changelog` going back to 6/19. `split-note-log.py --dry-run` returns "nothing movable" for it — the tool's classifier doesn't recognize this file's structure, and `note-history-splitting.md`'s own "what deliberately does NOT split" list doesn't mention it either. It simply was never evaluated against the rule.
- **`Trackers/Automation.md`** — the vault's "authoritative inventory," read whenever automation state is checked (as I did for item B above); its exemption in `note-history-splitting.md` calls it a "data cache... bulk is current state" at a cited 20 KB. It's now 26 KB, and the bulk of that is a long chronological prose changelog of past scheduling decisions (several are multi-paragraph), not current-state data — the exemption's own reasoning looks stale on re-inspection, even though the file itself isn't large enough to be urgent.

Neither file is large enough to be a cost problem today (Events.md is 14 KB; Automation.md is 26 KB, still well short of `actions-index.py`'s 15 KB threshold's *practical* impact since that check only scopes `/Trackers/Actions`). This is a documentation/convention gap, not an active drift — but it's exactly the failure class the whole convention exists to prevent, and neither file's tooling nor doc coverage currently reaches it. **Propose:** either extend `split-note-log.py`'s classifier to cover these two, or explicitly add them to the "do NOT split" list in `note-history-splitting.md` with updated, honest reasoning (and re-cite Automation.md's real current size). Did not apply — this is a rule/threshold decision, not a mechanical fix.

---

## G. Credential exposure — still open, third quarter running. **[Flag — needs Connor, same push as 6/15 and 6/25]**

`Contacts/Credentials.md` still holds **three** shared plaintext credentials: Sign Up Genius and Instacart (flagged 6/15, still open at 6/25, still open now) plus **YouTube TV** (Derek's account, added 2026-06-26 — also flagged in-file with the same migration warning, also still unmigrated). Nothing here has shrunk in three months of repeated flagging. WiFi keys remain fine to leave as-is. This is the one item across this whole audit I'd genuinely act on rather than file — same stance as 6/25.

---

## H. Minor: undocumented status value. **[Tier 2 — propose, trivial]**

One action note (`Jennifer Claffey - Planning Center support Zoom on PCO tag creation + Rock sync`) carries `status: merged` with a `merged_into` pointer — a deliberate, well-reasoned consolidation (logged in `Logs/refresh-run-log.md`, 2026-08-17: "not archived — that's Connor's call"). `merged` isn't in `Open-Actions-Reference.md`'s declared vocabulary (`active | in-progress | waiting-on | on-hold | closure-candidate | completed`) and has no `Open Actions.base` view — it's invisible in every status-filtered view, visible only in **All** and **By Project**. Single instance, low stakes. **Propose:** either formally document `merged` as a recognized terminal status (and decide if it should ever get its own Base view), or archive merged-away notes instead of leaving them live-but-invisible indefinitely.

---

## Light-check items with nothing to report

- **Filename ↔ frontmatter date drift:** none. All three live event notes (`2026-07-29-Boot-Camp-Summer-Camp` [cancelled], `2026-09-16-Boot-Camp-Fall-Relaunch`, `2026-09-20-Sunday-Night-Service-Launch`) match their folder/filename dates exactly.
- **Vocabulary drift (trackers):** clean apart from the single `status: merged` instance in item H.
- **Broken wikilinks:** apart from the one transcript fixed under Tier 1, zero real broken links. Everything else my scan flagged was one of: memory-slug cross-references to the Claude Code memory system (expected, not vault-navigable — same conclusion as 6/25); illustrative placeholders in workflow prose (`[[People/<Name>]]`, `[[Trackers/Actions/{other item's filename}]]`, etc.); or links inside **dated Synthesis snapshots that have already been explicitly triaged** in prior weekly audits (7/31 through 9/04) and deliberately left as historical record — re-flagging those would re-litigate settled calls, which the tier policy says not to do.
- **Schema adherence:** clean on the 5 most recent processed transcripts apart from the one fixed under Tier 1.
- **Name-spelling consistency:** no cross-transcript spelling drift found (Steve Coy/Koy, Jean Paul/John Paul, and Alexis "Alexa" Hendrickson are all already tracked via `aliases`/notes per the people-notes workflow).

---

## Tier 1 — fixed directly this pass

1. **Split 3 oversized live notes** via `split-note-log.py` (never by hand), per `note-history-splitting.md`'s standing duty ("when a note is named oversized, split it — don't note it and move on"):
   - `2026-09-16-Boot-Camp-Fall-Relaunch.md` (3 blocks → new companion `-Log.md`, live 49→48 KB)
   - `2026-09-20-Sunday-Night-Service-Run-of-Show-Experiment-Plan.md` (2 blocks, live 25→24 KB)
   - `2026-09-20-Sunday-Night-Service-Role-Ask-List.md` (7 blocks, live 19→10 KB)
   - (Left `4th-Service-Volunteer-Signups.md` alone despite 1 movable block in the generic scan — it's explicitly on `note-history-splitting.md`'s "do NOT split" list as a data cache.)
2. **Repointed 6 broken frontmatter `people:` links** in the `2026-08-30 13.10 Sunday Night Formation Lunch` transcript (Sean Liesegang, Emily Horneffer, Liz Goodiel, Brandon Geddes, Simba Kanjanda, Brian Sulc — all Good-Noodles-only, none with standalone notes) to the established piped form `[[People/Good Noodles|Name]]`, matching the exact 2026-08-14/08-28 precedent. Confirmed isolated to this one transcript — the four processed since (9/9, 9/11, 9/13, 9/14) all correctly use the collective `[[People/Good Noodles]]` link for peripherals.
3. **Refreshed `Welcome.md`'s Map section** — it listed only 3 `/Trackers` files and omitted `/People`, `/Logs`, `/Changelog` entirely.
4. **Added a retirement banner to `Workflows/event-checklist-autocopy.md`** — it still opened by describing itself as running 7:02 AM daily; the task was retired 2026-08-29 per `Trackers/Automation.md`. Mirrors the banner already used on `grace-weekly-refresh.md`.

Changelog entry: [[Changelog/2026-09-15-deep-audit-tier1-fixes]].

---

## Needs Connor (Tier 2/3 — nothing below was applied)

| # | Item | Ask |
|---|---|---|
| A | CLAUDE.md automation-cadence + FOLDERS drift | Approve the draft replacement text in section A (or edit it) |
| B | Scheduler visibility gap | Check `~/Claude/Scheduled/` directly — confirm `grace-weekly-refresh` is truly off and the other 4 tasks match Automation.md |
| C | 96 completed action notes to archive | Approve a repeat of the 8/12 sweep, and pick a standing rule so it doesn't recur a third time |
| D | `/_to_delete/` contents, 4 loose root files, `Test Canvas.canvas`, `feedback.json` | Approve moving to `/Archive` (or their real homes) |
| E | Michele Smith — no People record | Roster row or full person note? |
| F | Events.md / Automation.md inline changelogs | Extend the split tool, or formally exempt with honest reasoning |
| G | 3 shared plaintext credentials | Migrate to a password manager (same ask as 6/15, 6/25) |
| H | `status: merged` | Document it, or archive merged notes instead |

---

## Changelog

History lives in [[Changelog/_history/system-audit-changelog]] for this doc's own governing workflow; this dated audit file itself is not re-edited in place — a future audit gets its own new dated file, per [[Workflows/system-audit]].
