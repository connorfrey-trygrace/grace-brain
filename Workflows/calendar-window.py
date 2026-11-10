#!/usr/bin/env python3
"""Read /Trackers/Calendar-Window.md — the refresh's snapshot of Connor's real Outlook
calendar — and answer questions about it.

WHY THIS EXISTS (2026-08-20). The Open-Actions workflow referenced the calendar as an
evidence source in four separate places ("calendar (if accessible)", "a calendar hit",
"a confirmed future date/meeting") and NO phase of the refresh ever fetched it. Outlook
was present in the procedure as a permission and absent as a fact — so the gap got
filled by inference, and on 2026-08-20 the refresh report told Connor to raise a stalled
item with John Slye "at the Mon 8/24 session." 8/24 is Kay's PCO/Rock tutorial with Kay,
Jennifer and Connor. John is not on it, and no occasion existed before that item's 9/6
needs_by where the two of them were on the same call. See
[[Changelog/2026-08-20-calendar-window]].

The fix is not a rule telling a future run to remember. It is making the fact present.

USAGE
  python3 "Workflows/calendar-window.py" --check
        staleness + counts. Non-zero exit if the file is missing or stale.
  python3 "Workflows/calendar-window.py" --who "John Slye" [--before 2026-09-06]
        next meeting where Connor and that person are both attendees.
  python3 "Workflows/calendar-window.py" --meetings
        the window's real meetings, one per line.

IMPORTED BY actions-index.py for the waiting-on next-shared-meeting column.

WRITING THE FILE is the agent's job, not this script's — Outlook is reachable only
through the M365 connector, which a python script has no access to. The refresh pulls it
once in Phase 1 and writes this file; the format is documented in
[[Workflows/calendar-window-format]] and validated by --check.
"""

import os, re, sys, glob, datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
CONNOR = "connor.frey@trygrace.org"
STALE_DAYS = 4          # a window older than this is not trustworthy for "is X on it?"
REL_PATH = os.path.join("Trackers", "Calendar-Window.md")

# Self-blocks Connor puts on his own calendar to shape availability. They are not
# meetings and must never be reported as an occasion to raise something at.
PLACEHOLDER_SUBJECTS = ("morning availability", "afternoon availability",
                        "daily ftj conflict", "evening availability")


def vault_root():
    d = os.path.abspath(".")
    while d != "/":
        if os.path.isdir(os.path.join(d, "Trackers", "Actions")):
            return d
        d = os.path.dirname(d)
    sys.exit("error: run from inside the vault (no Trackers/Actions found above cwd)")


def _rows(text, heading):
    """Markdown table rows under `## <heading>`, as lists of stripped cells."""
    m = re.search(r"^##\s+%s\s*$(.*?)(?=^##\s|\Z)" % re.escape(heading), text, re.M | re.S)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or set("".join(cells)) <= set("-: "):
            continue                       # separator row
        if cells[0].lower() in ("start", "start (et)"):
            continue                       # header row
        out.append(cells)
    return out


def _dt(s):
    s = s.strip()
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s, f)
        except ValueError:
            pass
    return None


def load(root=None):
    """{generated, window_start, window_end, meetings[], ooo[]} or None if absent."""
    root = root or vault_root()
    path = os.path.join(root, REL_PATH)
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()

    def field(name):
        m = re.search(r"^%s:\s*(.+)$" % re.escape(name), text, re.M)
        return m.group(1).strip() if m else ""

    meetings = []
    for cells in _rows(text, "Meetings"):
        if len(cells) < 4:
            continue
        start, end, subject, attendees = cells[0], cells[1], cells[2], cells[3]
        if subject.strip().lower() in PLACEHOLDER_SUBJECTS:
            continue
        meetings.append({
            "start": _dt(start), "end": _dt(end), "subject": subject,
            "attendees": [a.strip().lower() for a in attendees.split(",") if a.strip()],
        })
    ooo = []
    for cells in _rows(text, "Out of office"):
        if len(cells) < 3:
            continue
        ooo.append({"start": _dt(cells[0]), "end": _dt(cells[1]), "subject": cells[2]})

    meetings = [m for m in meetings if m["start"]]
    meetings.sort(key=lambda m: m["start"])
    return {
        "path": path,
        "generated": _dt(re.sub(r"\s*ET$", "", field("generated"))),
        "window_start": _dt(field("window").split("→")[0]) if field("window") else None,
        "window_end": _dt(field("window").split("→")[-1]) if field("window") else None,
        "meetings": meetings, "ooo": ooo,
    }


# ---------------------------------------------------------------- people

def staff_emails():
    """{'first last': [emails]} from the canonical Office staff list.

    Authoritative source for name→email; the vault should never guess this.
    Path handling mirrors resolve-phone.py, including the /sessions/*/mnt glob —
    the literal Dropbox path does not exist inside the device shell, so the glob
    is the branch that actually resolves there.
    """
    out = {}
    bases = ["/Users/connorfrey/Library/CloudStorage/Dropbox/Office"]
    bases += sorted(glob.glob("/sessions/*/mnt/Office"))
    bases += sorted(glob.glob(os.path.expanduser("~/mnt/Office")))
    for base in bases:
        xlsx = os.path.join(base, "Staff Contact List.xlsx")
        if not os.path.exists(xlsx):
            continue
        try:
            import warnings, openpyxl
            warnings.filterwarnings("ignore")
        except ImportError:
            return out
        wb = openpyxl.load_workbook(xlsx, data_only=True)
        for ws in wb:
            for row in ws.iter_rows(values_only=True):
                cells = [str(c).strip() for c in row if c not in (None, "")]
                if len(cells) < 2 or cells[0].upper() == "NAME":
                    continue
                mails = [c.lower() for c in cells if "@" in c]
                if mails:
                    out.setdefault(cells[0].lower(), []).extend(mails)
        break
    return out


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def emails_for(name, cal=None, staff=None):
    """Every address that plausibly IS this person, within this window.

    Three sources, in order of trust:
      1. the Office staff list (authoritative);
      2. a local-part match against attendees actually present in the window —
         this is what catches a personal address used to organize a work meeting
         (Kay Carter-Corker organizes from kcartercorker@gmail.com while the staff
         list has kay.cartercorker@trygrace.org);
      3. nothing. An unresolvable name returns an empty set and every caller must
         treat that as UNKNOWN, never as "no meeting" — the whole point of this
         module is to stop absence of data reading as absence of the thing.
    """
    staff = staff if staff is not None else staff_emails()
    found = set()
    key = (name or "").strip().lower()
    for k, v in staff.items():
        if k == key or _norm(k) == _norm(key):
            found.update(v)
    parts = [p for p in re.split(r"[\s]+", key) if p]
    if parts:
        first, last = parts[0], parts[-1]
        cal = cal if cal is not None else load()
        seen = {a for m in (cal or {}).get("meetings", []) for a in m["attendees"]}
        for addr in seen:
            local = _norm(addr.split("@")[0])
            if len(_norm(last)) >= 4 and _norm(last) in local and (
                    _norm(first) in local or local.startswith(_norm(first)[:1])):
                found.add(addr)
    return found


def next_shared(name, cal=None, after=None, before=None):
    """Next meeting where Connor and `name` are both attendees.

    Returns (meeting|None, status) where status is one of:
      'ok'       -- meeting found
      'none'     -- person resolved, genuinely no shared meeting in range
      'unknown'  -- could not resolve the person to any address; DO NOT read as 'none'
      'no-window'-- Calendar-Window.md missing; DO NOT read as 'none'
    """
    cal = cal if cal is not None else load()
    if not cal:
        return None, "no-window"
    mails = emails_for(name, cal=cal)
    if not mails:
        return None, "unknown"
    after = after or datetime.datetime.now(ET).replace(tzinfo=None)
    for m in cal["meetings"]:
        if m["start"] < after:
            continue
        if before and m["start"].date() > before:
            break
        att = set(m["attendees"])
        if CONNOR in att and mails & att:
            return m, "ok"
    return None, "none"


def check(cal=None):
    cal = cal if cal is not None else load()
    if not cal:
        print("MISSING: %s has never been written. "
              "Phase 1 of the refresh is supposed to write it." % REL_PATH)
        return 1
    today = datetime.datetime.now(ET).replace(tzinfo=None).date()
    age = (today - cal["generated"].date()).days if cal["generated"] else None
    print("Calendar window: %s → %s" % (
        cal["window_start"].date() if cal["window_start"] else "?",
        cal["window_end"].date() if cal["window_end"] else "?"))
    print("  generated   %s (%s)" % (
        cal["generated"] or "?", "today" if age == 0 else "%d days ago" % age if age is not None else "?"))
    print("  meetings    %d" % len(cal["meetings"]))
    print("  out-of-office blocks %d" % len(cal["ooo"]))
    rc = 0
    if age is not None and age > STALE_DAYS:
        print("  ⚠️ STALE (>%d days) — re-pull before trusting any 'is X on it?' answer." % STALE_DAYS)
        rc = 1
    if cal["window_end"] and cal["window_end"].date() < today + datetime.timedelta(days=7):
        print("  ⚠️ window ends within 7 days — extend it on the next pull.")
        rc = 1
    if not staff_emails():
        print("  ⚠️ Office staff list unreadable — name→email resolution is degraded, "
              "so shared-meeting answers will read 'unknown', not 'none'.")
        rc = 1
    return rc


def main():
    args = sys.argv[1:]
    cal = load()
    if not args or "--check" in args:
        sys.exit(check(cal))
    if "--meetings" in args:
        if not cal:
            sys.exit("no calendar window written yet")
        for m in cal["meetings"]:
            print("%s  %-52s %s" % (m["start"], m["subject"][:52], ", ".join(m["attendees"])))
        for o in cal["ooo"]:
            print("%s  OOO: %s → %s" % (o["start"], o["subject"], o["end"]))
        return
    if "--who" in args:
        name = args[args.index("--who") + 1]
        before = None
        if "--before" in args:
            before = datetime.datetime.strptime(args[args.index("--before") + 1], "%Y-%m-%d").date()
        m, status = next_shared(name, cal=cal, before=before)
        if status == "ok":
            print("%s: next shared meeting %s — %s" % (name, m["start"], m["subject"]))
        elif status == "none":
            print("%s: NO shared meeting%s. There is no occasion to raise it at; "
                  "the channel is text, then call." % (name, " before %s" % before if before else " in the window"))
        elif status == "unknown":
            print("%s: UNKNOWN — could not resolve to an email address. "
                  "This is not the same as 'no meeting'." % name)
        else:
            print("no calendar window written yet — cannot answer")
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
