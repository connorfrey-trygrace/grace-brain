---
date: 2026-08-18
tier: 1
governs:
  - "[[Workflows/grace-quick-refresh]]"
  - "[[Workflows/grace-weekly-refresh]]"
  - "Workflows/actions-index.py"
---

# Start Here only lists items Connor can act on

**Connor, 2026-08-18, three times in one reply:** *"if there's nothing to do on this, it shouldn't have been raised."*

## What happened

The 8/18 quick-refresh report led with four overdue-or-due-today items. **Connor struck three of them**, each for the same reason — the ball was someone else's:

| Item | Why it was raised | Why that was wrong |
|---|---|---|
| Kay Carter-Corker — Rock↔PCO service type + sync tags | `needs_by: 2026-08-15` passed | `waiting-on`; Kay and Jennifer Claffey are on it; Connor emailed 8/17. No chase to make. |
| Callie Taylor — 8/30 lunch food + location | `needs_by: 2026-08-18` reached | She replied in-channel at 10:20 that morning and Connor answered at 11:34. The ball had already changed hands twice that day. |
| Heather Noble — NFC tap cards | `chase_by: 2026-08-18` fired | **She had already answered.** 8/14: *"I'll let you know when I have more info on the Tap cards."* |

The Heather one is the instructive failure. Its `chase_by` was **self-derived** — the recorded rationale was *"the window to settle NFC vs QR while there is still runway before the 9-03 needs-by,"* which names no external event. Once that invented date existed, three consecutive entries built a *"third consecutive live exchange without the question attached"* narrative on top of it, and the 8/18 sweep flagged the item. Read against the actual thread, Heather answered the banner question definitively, committed to reporting back on the tap cards, and sent Connor a deck he'd asked for the day before. **That is a colleague doing her job.** Calling it a three-time miss is the same reflex the ticket-number chase was retired for on 8/17 — [[Changelog/2026-08-17-ticket-number-chase-retired]].

## The fix, in code and in prose

**Code** (`actions-index.py`, `brief()`): a `waiting-on` item with no live `chase_by` is skipped. The only Connor-side action a `waiting-on` item can have is a chase; a `needs_by` or `deadline` firing while someone else holds the ball is not work. The sweep view is unchanged — that is the inventory and still shows everything.

**Measured on the same vault in the same minute:** overdue-or-due-today **4 → 1**. Kay and Callie dropped out; Heather survived the guard because of the invented `chase_by`, and that field was removed from the note by hand.

**Prose** ([[Workflows/grace-quick-refresh]] § Report Part 1, and [[Workflows/grace-weekly-refresh]] § Report by reference): the gate is now the **first** of three rules, ahead of "name the next physical action" and "don't pad it."

## The corollary the guard cannot enforce

**Never write a `chase_by` against someone who has committed to reporting back.** A manufactured chase defeats the suppression at its source — which is precisely how the Heather item got through a guard designed to catch it. The standing rule already said a date needs a named external event; this is the cost of not honouring it.
