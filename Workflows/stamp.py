#!/usr/bin/env python3
"""Write every ET timestamp the refresh produces, so no run ever types one.

WHY THIS EXISTS (2026-08-21). The execution shell — both the cloud container and the
Mac VM the vault is mounted in — reports **UTC**. A bare `date` therefore reads ~4h
ahead of ET, and a run that labels that reading "ET" corrupts whatever it wrote.

  2026-08-17  the m365 marker was written `11:40 ET` when the real time was `07:49 ET`.
              Honoured literally, the next window would have opened 4 hours in the
              future and every email arriving that day would have fallen into a dead
              zone belonging to no window — permanently skipped. See
              [[Changelog/2026-08-17-timezone-marker-defect]].
  2026-08-21  the same error was made again and caught only because a subagent
              happened to re-read the clock with TZ= before the marker was written.

The 8/17 fix was a ⚠️ paragraph next to each marker telling a future run to use
`TZ=America/New_York`. That changelog's own closing line: *"nothing enforces the rule
mechanically... a future run that reaches for a bare `date` will reproduce the defect."*
Four days later it nearly did.

THE STRUCTURAL POINT. `ZoneInfo("America/New_York")` does not consult the shell's TZ at
all, so anything a *script* stamps is already correct — `actions-index.py` and
`calendar-window.py` have always been immune. The vulnerability is not the clock; it is
that six surfaces were typed by hand. This script owns all six. The caller hands over a
ROWID or a log-line body and never handles a time.

  python3 "Workflows/stamp.py" now                     -> 2026-08-21 19:05 ET
  python3 "Workflows/stamp.py" today                   -> 2026-08-21
  python3 "Workflows/stamp.py" mark --m365 --window-end "2026-09-04 13:00"
  python3 "Workflows/stamp.py" mark --text-scan 191931
  python3 "Workflows/stamp.py" log --refresh "grace-quick-refresh | total 14m | ... | OK"
  python3 "Workflows/stamp.py" log --m365    "<body>"
  python3 "Workflows/stamp.py" log --text    "<body>"

Add --dry-run to any mutating command to print the exact replacement and write nothing.

Enforced by `Workflows/clock-check.py`, which compares every stamp against the file's
real mtime. Writing a marker by hand is not forbidden — it is simply detected.

MARKER SEMANTICS (changed 2026-09-04, Connor's call). `mark --m365` used to always stamp
the run's completion time (`et_stamp()` at the moment the command ran). But
m365-to-obsidian-sync.md's own § Source & window treats the marker as "the point mail
has been scanned through" — the end of the search window, not when the write happened.
Those are the same instant only when analysis and writing are simultaneous, and
grace-quick-refresh splits them into Phase 1 (analysis) and Phase 2 (writing), so they
never are. See [[Trackers/Actions/Connor - Decide whether the m365 sync marker should
record scan-window end instead of run-completion time]] for the defect history (a
2h25m dead zone opened on 2026-08-25) and [[Changelog/2026-09-04-m365-marker-window-end]]
for this fix. `--window-end "YYYY-MM-DD HH:MM"` (ET, no seconds) now records that instant
instead. Passing nothing falls back to the old completion-time behavior with a printed
warning — every caller should pass it going forward; the fallback exists only so a stale
invocation doesn't hard-crash.
"""

import argparse, datetime, io, os, re, sys
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

M365_WORKFLOW = os.path.join("Workflows", "m365-to-obsidian-sync.md")
TEXT_WORKFLOW = os.path.join("Workflows", "text-message-sync.md")
LOGS = {
    "refresh": os.path.join("Logs", "refresh-run-log.md"),
    "m365":    os.path.join("Logs", "m365-sync-run-log.md"),
    "text":    os.path.join("Logs", "text-message-sync-run-log.md"),
}

PROVENANCE = ("*(Written by `Workflows/stamp.py` from `ZoneInfo(\"America/New_York\")`, "
              "never from the shell clock — the shell reports UTC. Prior value: `%s ET`.)*")


def now():
    return datetime.datetime.now(ET)


def et_stamp():
    return now().strftime("%Y-%m-%d %H:%M ET")


def et_date():
    return now().strftime("%Y-%m-%d")


def vault_root():
    d = os.path.abspath(".")
    while d != "/":
        if os.path.isdir(os.path.join(d, "Trackers", "Actions")):
            return d
        d = os.path.dirname(d)
    sys.exit("error: run from inside the vault (no Trackers/Actions found above cwd)")


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s, dry, label):
    if dry:
        print("DRY RUN — %s would become:\n%s" % (label, s))
        return
    io.open(p, "w", encoding="utf-8").write(s)
    print("%s -> %s" % (label, s.strip().splitlines()[0] if s else ""))


def mark_m365(dry, window_end=None):
    p = os.path.join(vault_root(), M365_WORKFLOW)
    t = read(p)
    pat = re.compile(r"(?m)^- timestamp: (\d{4}-\d\d-\d\d \d\d:\d\d) ET\n^ *\*\(.*?\)\*$")
    m = pat.search(t)
    if not m:
        sys.exit("error: could not find the '- timestamp: ... ET' marker block in %s" % M365_WORKFLOW)
    old = m.group(1)
    if window_end:
        try:
            datetime.datetime.strptime(window_end, "%Y-%m-%d %H:%M")
        except ValueError:
            sys.exit("error: --window-end must be \"YYYY-MM-DD HH:MM\" (ET, no seconds), got %r" % window_end)
        new = window_end + " ET"
    else:
        new = et_stamp()
        print("⚠️  no --window-end given — falling back to run-completion time (%s). "
              "Pass --window-end so the marker records what was actually scanned through, "
              "not when the write happened. See the module docstring." % new, file=sys.stderr)
    block = "- timestamp: %s\n  %s" % (new, PROVENANCE % old)
    if dry:
        print("DRY RUN — %s\n  old: %s\n  new: %s" % (M365_WORKFLOW, m.group(0), block))
        return
    io.open(p, "w", encoding="utf-8").write(t[:m.start()] + block + t[m.end():])
    print("m365 marker: %s ET -> %s" % (old, new))


def mark_text_scan(rowid, dry):
    p = os.path.join(vault_root(), TEXT_WORKFLOW)
    t = read(p)
    pat = re.compile(r"(?m)^- last_rowid: (\d+)\n^- last_run: (\d{4}-\d\d-\d\d)$")
    m = pat.search(t)
    if not m:
        sys.exit("error: could not find the '- last_rowid: / - last_run:' block in %s" % TEXT_WORKFLOW)
    old_row, old_run = m.group(1), m.group(2)
    if int(rowid) < int(old_row):
        sys.exit("error: refusing to move last_rowid backwards (%s -> %s). A marker only ever advances."
                 % (old_row, rowid))
    block = "- last_rowid: %s\n- last_run: %s" % (rowid, et_date())
    if dry:
        print("DRY RUN — %s\n  old: %s\n  new: %s" % (TEXT_WORKFLOW, m.group(0), block))
        return
    io.open(p, "w", encoding="utf-8").write(t[:m.start()] + block + t[m.end():])
    print("text marker: rowid %s -> %s, run %s -> %s" % (old_row, rowid, old_run, et_date()))


def append_log(which, body, dry):
    p = os.path.join(vault_root(), LOGS[which])
    line = "- %s | %s" % (et_stamp(), body.strip())
    if dry:
        print("DRY RUN — would append to %s:\n%s" % (LOGS[which], line))
        return
    t = read(p).rstrip()
    io.open(p, "w", encoding="utf-8").write(t + "\n\n" + line + "\n")
    print("appended to %s:\n%s" % (LOGS[which], line))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("now", help="print the current ET timestamp")
    sub.add_parser("today", help="print today's ET date")

    mk = sub.add_parser("mark", help="rewrite a sync marker with the real ET now")
    g = mk.add_mutually_exclusive_group(required=True)
    g.add_argument("--m365", action="store_true")
    g.add_argument("--text-scan", metavar="ROWID")
    mk.add_argument("--window-end", metavar="\"YYYY-MM-DD HH:MM\"",
                     help="m365 only: the end of the scanned window (ET, no seconds), e.g. the current-time "
                          "bound passed to outlook_email_search. Replaces run-completion time as the marker's "
                          "meaning; see the module docstring's MARKER SEMANTICS section.")
    mk.add_argument("--dry-run", action="store_true")

    lg = sub.add_parser("log", help="append one correctly-stamped run-log line")
    g2 = lg.add_mutually_exclusive_group(required=True)
    for k in LOGS:
        g2.add_argument("--%s" % k, action="store_true")
    lg.add_argument("body")
    lg.add_argument("--dry-run", action="store_true")

    a = ap.parse_args()
    if a.cmd == "now":
        print(et_stamp())
    elif a.cmd == "today":
        print(et_date())
    elif a.cmd == "mark":
        if a.m365:
            mark_m365(a.dry_run, a.window_end)
        else:
            mark_text_scan(a.text_scan, a.dry_run)
    elif a.cmd == "log":
        which = next(k for k in LOGS if getattr(a, k))
        append_log(which, a.body, a.dry_run)


if __name__ == "__main__":
    main()
