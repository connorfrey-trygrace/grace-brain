---
type: workflow
---
# Grace Quick Refresh — Reference

Incident write-ups behind the corrected/hardened rules in [[Workflows/grace-quick-refresh]] (and, since both share phases 0–3, [[Workflows/grace-weekly-refresh]]). Split out **2026-09-09** so the main procedure file stays cheap to read on every run.

**Not part of the standard read for a refresh.** The main file carries the operational rule and a one-line "why"; come here when the reasoning behind one is genuinely in question, or when calibrating judgment on a new edge case.

---

## Why this routine exists at all (2026-07-21)

The prior design ran email sync 3x/day and text scan 1x/day on fixed cadences. Connor's read: that was "sometimes less than I need and very often more than I need," and he still had to manually kick off a scan anyway before working sessions that didn't line up with the schedule. This routine replaces the fixed daily/3x-daily cadences with an on-demand pull, backed by `grace-weekly-refresh` as a once-a-week safety net so nothing goes silently stale if Connor doesn't ask for a while.

## Why the calendar pull is a phase step, not a rule (2026-08-20)

The calendar was already referenced as an evidence source in **four places** in [[Workflows/Open-Actions-Tracker]] — *"calendar (if accessible)"*, *"a calendar hit"*, *"a confirmed future date/meeting"* — and **no phase of this routine ever fetched it.** Outlook was present in the procedure as a permission and absent as a fact, so the gap got filled by inference: the 8/20 report told Connor to raise a stalled item with John Slye *"at the Mon 8/24 session."* 8/24 is Kay's Rock/PCO tutorial with Kay, Jennifer and Connor. John is not on it, and no occasion existed before that item's 9/6 `needs_by` where the two of them were on the same call. Adding a rule saying *check the calendar first* would have been the fourth such rule. Fetching it makes the fact present instead. See [[Changelog/2026-08-20-calendar-window]].

The daily self-blocks (`Morning Availability`, `Afternoon Availability`, `Daily FTJ Conflict`) were 47 of the 57 events in the first pulled window — the exclusion isn't cosmetic, it's most of the raw data.

## Why the clock gate checks mtime, not "is the stamp in the future" (2026-08-21)

A future-check would have caught that day's near-miss and would have **missed the real 2026-08-17 defect**: that marker read `11:40 ET` at `07:49 ET` real, so it stopped being "in the future" by lunchtime and read clean forever after. Measured across four replayed cases — mtime catches the UTC shift at every hour of the day and stays silent when a procedure file is legitimately edited days after its marker was set. See [[Changelog/2026-08-21-clock-enforced-in-code]].

## Why timing and token usage are measured, not estimated

On 2026-08-11 Connor asked why a refresh had taken ~30 minutes and nothing in the vault recorded elapsed time — the answer had to be reconstructed from file mtimes, which can't distinguish thinking from reading and can't see anything a phase did without writing. A per-phase total is what separates "the email pull was slow" from "one 93 KB note ate the run," and it makes a regression visible on the next line instead of after the next complaint.

**The fifth stamp exists because of a near-miss:** on 2026-08-12 the report-writing and verification step cost ~8m, more than Phase 3 itself, and it was invisible because instrumentation stopped at the last phase. A phase that isn't stamped can't regress in a way anyone notices.

**`wrote N KB` vs the older `out:` field:** `out:` counts the *size of the files touched*, which overstates cost by an order of magnitude — a 27 KB note that received a one-line append shows as 27 KB when generation cost ~200 bytes. Wall clock tracks tokens generated, so bytes-actually-added is the field that correlates with elapsed time; `out:` stays because it still answers "how much of the vault did this run reach."

**Token usage (added 2026-09-02):** closes the gap Connor asked about — elapsed time was tracked, tokens weren't. Reuses the same two stamps `elapsed`/`wrote` already require, no new measurement.

## Report Part 1 — the incidents behind the today-gate

**The brief-alone miss (2026-08-21).** The 8/21 report was built from `actions-index.py --brief` alone and then filtered by the today-only gate, and the two filters stacked. `--brief` returned 2 date-urgent items, both of which failed the today gate (one was a Sunday commitment, one a Monday read), so the report told Connor he had **nothing to do** — while **22 Connor-owned, unblocked, active items** sat in the folder, including an 8/30 leadership lunch nine days out with **no invite sent**. Connor: *"So I have no open actions? That can't be right."* This is why Part 1 must be built from the full `actions-index.py` list, with `--brief` used only to order/prioritize it, never as the sole input.

**The struck-three-of-four incident (2026-08-18).** Connor struck three of four items in that day's queue with the same sentence: *"if there's nothing to do on this, it shouldn't have been raised."* The three: Kay Carter-Corker's Rock↔PCO item (`needs_by` passed, but staff were on it and there was no chase to make), Callie Taylor's lunch (she'd replied in-channel that same morning), and Heather Noble's NFC tap cards (she had already said "I'll let you know when I have more info" — an answer, not a silence). This is the direct evidence for the "only list an item with a Connor-side action available today" gate.

**The attendance-vs-prep incident (2026-08-21).** The 8/21 report led with the Sunday 8/23 Sour Patch Kid mascot duty because `--brief` put it under "This week" at 2 days out. Connor: *"An event in two days, like escorting Felipe, is not something that I can work on today."* Attending a commitment is not work; preparing for it is, and only if the prep is due now. This is the direct evidence that a near deadline is not the test — an available physical action is.

**The manufactured-chase incident.** `actions-index.py --brief` suppresses `waiting-on` items with no live `chase_by` (added 2026-08-18; measured, the 8/18 queue went from 4 overdue to 1). The Heather Noble NFC item defeated that suppression because its `chase_by` rationale was *"the window to settle NFC vs QR,"* a self-derived window, not a named external event — a manufactured chase. Same failure family as [[Changelog/2026-08-17-ticket-number-chase-retired]]: this is a church, and a colleague saying "I'll let you know" is a person keeping their word, not an open ticket. Hence the corollary rule: never write a `chase_by` against someone who has already committed to reporting back.
