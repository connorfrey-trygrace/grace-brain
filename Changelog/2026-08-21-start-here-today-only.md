# 2026-08-21 — Start Here is today-only, and Grace's Sunday morning schedule is a known fact

Two corrections from Connor on the 2026-08-21 quick-refresh report.

## 1. Start Here lists only what he can act on today

**What changed:** [[Workflows/grace-quick-refresh]] § Report Part 1, rule ⭐ — *"Only list items with a Connor-side next physical action"* → *"...that is available **TODAY**."* Rationale paragraph added under it.

**Why:** the report led with the Sunday 8/23 Sour Patch Kid mascot duty, which `actions-index.py --brief` had placed under **This week** at 2 days out. Connor: *"An event in two days, like escorting Felipe, is not something that I can work on today."*

The 2026-08-18 gate already caught items with **no action at all**. This catches the other half — items whose action exists but is not available now. Showing up to a commitment is not work. **`--brief`'s date arithmetic cannot distinguish a due task from a date on the calendar**, so its `This week` block is a candidate list to be filtered by hand, not an answer to paste. Held items are covered by the same rule: a close release date does not unpark anything.

Not enforced in code — a script cannot tell attendance from preparation. Recorded in memory as `start-here-is-today-only`.

## 2. The Sunday morning schedule is fixed, not inferable

The same run's text-sync log flagged Alexis Hendrickson's voice memo — *"We are rehearsing at 7:30 on Sunday"*, no AM/PM — as an unlabelled inference on the mascot note. It is not an inference. Grace's Sunday morning schedule:

| time | what |
|---|---|
| 7:30 AM | Run-through |
| 8:30 AM | Volunteer huddle |
| 9:00 AM | First service |
| 10:15 AM | Second service |
| 11:30 AM | Third service |

~45 minutes per service. A bare time in a Sunday-morning context resolves against this table; **do not hedge it, label it `[inferred]`, or re-raise the AM/PM question.** The log line was corrected in place. Recorded in memory as `grace-sunday-morning-schedule`. This is the *morning* pattern — the Sunday night service launching 9/20 has its own schedule (~4:30 PM run-through, 6:00 PM service).

## 3. Same day, second correction: the gate is a subtraction, not a selection

Applying §1 immediately produced the opposite failure. The report was built from `actions-index.py --brief` alone, then filtered by the new today-only gate. `--brief` returned **2** date-urgent items — the Sunday 8/23 mascot duty and the Monday 8/24 reading — and **both failed the gate**, so the report told Connor he had nothing to do.

He had **22** Connor-owned, unblocked, `active`/`in-progress` items. Among them: the **8/30 key-volunteer leadership lunch, nine days out, with the ask back to John Slye unsent and no invite in existence** — the single most time-sensitive real thing on his plate, invisible to `--brief` because 8/30 is outside its 7-day window.

Connor: *"So I have no open actions? That can't be right."*

**What changed:** [[Workflows/grace-quick-refresh]] § Report Part 1 now opens with a ⚠️ block stating that `--brief` is a **triage view, not the queue** — the queue is every `active`/`in-progress` item Connor owns that is not `blocked_by` an open item, and `--brief` only orders it. Two filters were stacked where one was intended.

**The general shape of the error, worth naming:** a *removal* rule and a *selection* rule are not interchangeable, and applying a removal rule to an already-narrowed set silently empties it. An empty work queue for a man running a service launch in 30 days should have been read as a defect in the query, not as a result.

