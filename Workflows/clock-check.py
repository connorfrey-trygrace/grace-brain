#!/usr/bin/env python3
"""Prove every ET timestamp in the vault was written at the time it claims.

WHY A FUTURE-CHECK IS NOT ENOUGH — this is the whole design decision.

The obvious test is "is any stamp in the future?" It would have caught the 2026-08-21
near-miss (a 22:15 reading at 18:12 real). It would have **sailed straight past the
actual 2026-08-17 defect**: that marker read `11:40 ET` at `07:49 ET` real, so by the
time anything looked at it, 11:40 was no longer in the future. A UTC-typed stamp is only
detectable-by-future-test for the ~4 hours before reality catches up to it.

The ground truth a run cannot fabricate is the **file's own mtime**, recorded by the OS
in real time. A stamp written from a UTC clock sits ~240 minutes ahead of the mtime of
the write that produced it, at every hour of the day, in both DST regimes.

The test is deliberately **asymmetric**. Only `stamp > mtime + TOL` is a defect — that
means the file claims to have been written later than it actually was. The reverse
(mtime much later than the stamp) is normal and expected: procedure files get edited
again for unrelated reasons long after their marker was set, which moves mtime forward
and must not raise an alarm.

  python3 "Workflows/clock-check.py"           # table + non-zero exit on any defect
  python3 "Workflows/clock-check.py" --quiet   # print only defects

Run as the last step of Phase 2 of `grace-quick-refresh` / `grace-weekly-refresh`, after
the markers and run-log lines are written. Writers live in `Workflows/stamp.py`.
"""

import argparse, datetime, io, os, re, sys
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
TOL_MIN = 20            # generous: a slow write phase is not a defect
UTC_SHIFT_MIN = 240     # EDT; 300 in EST. Reported when the drift matches, as a diagnosis.

# (label, path, regex capturing the LAST occurrence, granularity)
SURFACES = [
    ("m365 marker",       "Workflows/m365-to-obsidian-sync.md",
     r"(?m)^- timestamp: (\d{4}-\d\d-\d\d \d\d:\d\d) ET$", "minute"),
    ("text-scan marker",  "Workflows/text-message-sync.md",
     r"(?m)^- last_run: (\d{4}-\d\d-\d\d)$", "day"),
    ("refresh run log",   "Logs/refresh-run-log.md",
     r"(?m)^- (\d{4}-\d\d-\d\d \d\d:\d\d) ET \|", "minute"),
    ("m365 run log",      "Logs/m365-sync-run-log.md",
     r"(?m)^- (\d{4}-\d\d-\d\d \d\d:\d\d) ET \|", "minute"),
    ("text run log",      "Logs/text-message-sync-run-log.md",
     r"(?m)^- (\d{4}-\d\d-\d\d \d\d:\d\d) ET \|", "minute"),
    ("calendar window",   "Trackers/Calendar-Window.md",
     r"(?m)^generated: (\d{4}-\d\d-\d\d \d\d:\d\d) ET$", "minute"),
]


def vault_root():
    d = os.path.abspath(".")
    while d != "/":
        if os.path.isdir(os.path.join(d, "Trackers", "Actions")):
            return d
        d = os.path.dirname(d)
    sys.exit("error: run from inside the vault (no Trackers/Actions found above cwd)")


def check():
    root = vault_root()
    now = datetime.datetime.now(ET)
    rows, defects = [], []

    for label, rel, pat, gran in SURFACES:
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            rows.append((label, "-", "-", None, "MISSING FILE"))
            defects.append("%s: %s does not exist" % (label, rel))
            continue
        hits = re.findall(pat, io.open(p, encoding="utf-8").read())
        if not hits:
            rows.append((label, "-", "-", None, "NO STAMP FOUND"))
            defects.append("%s: no timestamp matched in %s — the surface moved or was renamed" % (label, rel))
            continue

        raw = hits[-1]
        fmt = "%Y-%m-%d %H:%M" if gran == "minute" else "%Y-%m-%d"
        stamped = datetime.datetime.strptime(raw, fmt).replace(tzinfo=ET)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(p), ET)

        if gran == "day":
            # a date-only stamp can only be wrong by a day; compare dates
            bad = stamped.date() > mtime.date()
            drift = (mtime.date() - stamped.date()).days
            note = "OK" if not bad else "DEFECT — dated after the write (%+d day)" % drift
            rows.append((label, raw, mtime.strftime("%Y-%m-%d"), drift, note))
        else:
            drift = (mtime - stamped).total_seconds() / 60.0
            bad = drift < -TOL_MIN
            note = "OK"
            if bad:
                note = "DEFECT — claims to be written %.0f min after it was" % (-drift)
                if abs(-drift - UTC_SHIFT_MIN) < 30 or abs(-drift - 300) < 30:
                    note += "  ← matches the UTC→ET shift exactly; a bare `date` was used"
            elif stamped > now + datetime.timedelta(minutes=TOL_MIN):
                bad, note = True, "DEFECT — stamp is in the future"
            rows.append((label, raw + " ET", mtime.strftime("%Y-%m-%d %H:%M"), drift, note))

        if bad:
            defects.append("%s (%s): stamped %s, file written %s"
                           % (label, rel, raw, mtime.strftime("%Y-%m-%d %H:%M")))
    return rows, defects, now


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print only defects")
    a = ap.parse_args()
    rows, defects, now = check()

    if not a.quiet:
        print("# Clock check — %s   (tolerance ±%d min; only stamp-later-than-write is a defect)"
              % (now.strftime("%Y-%m-%d %H:%M ET"), TOL_MIN))
        print("%-19s %-21s %-17s %8s  %s" % ("surface", "stamped", "file written", "drift", "verdict"))
        for label, stamped, mtime, drift, note in rows:
            d = "-" if drift is None else ("%+.0f min" % drift if isinstance(drift, float) else "%+d day" % drift)
            print("%-19s %-21s %-17s %8s  %s" % (label, stamped, mtime, d, note))

    if defects:
        print("\n⛔ %d DEFECT(S) — correct the stamp to the real write time, do not honour it as a window:"
              % len(defects))
        for d in defects:
            print("   - " + d)
        print("   Rewrite markers with `Workflows/stamp.py mark --m365` / `mark --text-scan <rowid>`.")
        sys.exit(1)
    if not a.quiet:
        print("\n✅ all %d surfaces consistent with their write times." % len(rows))


if __name__ == "__main__":
    main()
