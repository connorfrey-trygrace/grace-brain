---
type: changelog
date: 2026-08-21
tier: 2
touches: ["[[Workflows/stamp.py]]", "[[Workflows/clock-check.py]]", "[[Workflows/grace-quick-refresh]]", "[[Workflows/grace-weekly-refresh]]", "[[Workflows/m365-to-obsidian-sync]]", "[[Workflows/text-message-sync]]"]
trigger: "Connor, 2026-08-21 — \"How can we structurally fix it?\" after the refresh report flagged a near-miss on the UTC/ET marker"
supersedes: "[[Changelog/2026-08-17-timezone-marker-defect]] (its prose guard is retired)"
---
# Timestamps are written by a script and verified against file mtime; the prose guard that failed twice is retired

**The shell reports UTC.** Both the cloud container and the Mac VM the vault is mounted in return `22:49` when the real time is `18:49 ET`. Any run that reads a bare `date` and labels it "ET" writes a value ~4h ahead (5h in EST).

**Third occurrence.** 2026-08-17: the m365 marker was written `11:40 ET` at `07:49 ET` real — honoured literally, every email arriving that day would have fallen into a dead zone belonging to no window and been permanently skipped. 2026-08-21 11:58: fine. 2026-08-21 18:2x: the same error was made again and caught only because a subagent happened to re-read the clock with `TZ=` before either marker was written.

**The 8/17 fix was a ⚠️ paragraph beside each marker.** Its own changelog closed with *"nothing enforces the rule mechanically... a future run that reaches for a bare `date` will reproduce the defect."* Four days later it nearly did. Per [[verify-fixes-by-measurement]], a repeat failure gets code and a measurement, not edited procedure text.

## The diagnosis that reframed the fix

`ZoneInfo("America/New_York")` does not consult the shell's TZ at all. So **every scripted timestamp in the vault was already immune** — `actions-index.py` and `calendar-window.py` have never had this bug. The vulnerability was never the clock; it was that **six surfaces were typed by hand**: the m365 marker, the text-scan marker, three run logs, and `Trackers/Calendar-Window`'s `generated:` field.

## What landed

- **[[Workflows/stamp.py]] — nothing types a timestamp any more.** `mark --m365`, `mark --text-scan <rowid>`, `log --refresh|--m365|--text "<body>"`, plus `now` / `today`. The caller hands over a ROWID or a line body and never handles a time. `--dry-run` on every mutating command; refuses to move `last_rowid` backwards.
- **[[Workflows/clock-check.py]] — the gate.** Compares all six stamps against each file's real **mtime** and exits non-zero on any that claims to have been written later than it was. Wired into **Phase 2 of both refreshes** as a hard stop, and named explicitly in `grace-weekly-refresh` because nobody is watching a Monday 6 AM run.
- **The prose guards are gone**, replaced by one pointer line each. They were the fourth-such-rule problem from [[Changelog/2026-08-20-calendar-window]]: bytes every run reads that prevented nothing.

## Why mtime, and not "is the stamp in the future"

This was the real design decision. A future-check would have caught the 8/21 near-miss and **would have missed the actual 8/17 defect** — `11:40 ET` stopped being in the future by lunchtime and read clean forever after:

```
future-check run at 2026-08-17 09:00 ET -> DEFECT
future-check run at 2026-08-17 11:19 ET -> DEFECT
future-check run at 2026-08-17 12:30 ET -> clean  <-  MISSED IT
future-check run at 2026-08-21 18:53 ET -> clean  <-  MISSED IT
```

File mtime is recorded by the OS in real time and a run cannot fabricate it. The test is deliberately **asymmetric** — only `stamp > mtime + 20min` is a defect. The reverse is normal: a procedure file gets edited for unrelated reasons long after its marker was set, which moves mtime forward and must not raise an alarm.

## Measured, not asserted — five replayed cases

| case | expected | result |
|---|---|---|
| the real 8/17 defect (`11:40 ET`, written 07:49 ET) | DEFECT, −231 min, UTC-shift diagnosed | ✅ |
| the 8/21 near-miss (`22:15 ET`, written 18:12 ET) | DEFECT, −243 min | ✅ |
| marker set 8/17, prose edited 8/21 (+4 days mtime) | silent — legitimate | ✅ |
| text-scan date rollover (`8/22` written 20:30 ET on 8/21) | DEFECT, +1 day | ✅ |
| a surface renamed (`generated:` → `generated_at:`) | fails loudly, not silently clean | ✅ |

The last case matters most for durability: if someone reformats one of the six surfaces, the checker reports *"no timestamp matched — the surface moved or was renamed"* rather than quietly checking nothing and printing a green tick.

**Noted while testing, same root cause:** `touch -t` also reads the shell TZ, so the first replay attempt set 03:49 ET when it meant 07:49. The bug is ambient in the environment, which is the argument for never reading the shell clock for anything ET-shaped.

## What this does not cover, stated plainly

Dated entry headers inside action and event notes (`### 2026-08-21 (standalone sweep)`) are still typed. A wrong date there is cosmetic — no window arithmetic reads it, nothing is silently skipped — so it is deliberately out of scope rather than overlooked. The live m365 marker was **not** re-stamped when this landed: advancing it to the build time would have opened a dead zone over the 18:12→19:00 mail the run never scanned, which is the exact defect being fixed. Every marker from the next run forward is `stamp.py`-written.
