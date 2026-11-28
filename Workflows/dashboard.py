#!/usr/bin/env python3
"""
dashboard.py — writes /Trackers/Dashboard.md: one page, every workstream Connor
helps with, health + next actions + waits + upcoming dates. The weekly Sunday
Night service is collapsed to one line on purpose (Connor, 2026-11-27: "separate
out the Sunday service itself as its own thing") — the Start Here queue already
covers it week to week; this page is for the strategic view.

Inputs (read-only):
  /Trackers/Actions/*.md     frontmatter only, via actions-index.py's loader
  /Trackers/Milestones.md    hand-kept dated milestones table (date | what | workstream)

Workstream = the note's `workstream:` frontmatter if set, else the first
RULES pattern that matches the filename. Add a `workstream:` line to override a
misfile; add a RULES row when a new stream appears.

USAGE (from the vault root)
  python3 "Workflows/dashboard.py"            # write Trackers/Dashboard.md, print a 1-line-per-stream summary
  python3 "Workflows/dashboard.py" --stdout   # print the page instead of writing it
  python3 "Workflows/dashboard.py" --today 2026-12-01

Run by grace-quick-refresh after Phase 3 (the summary goes in the report).
"""
import os, re, sys, datetime, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("ai", os.path.join(HERE, "actions-index.py"))
AI = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(AI)

SUNDAY = "Sunday Service (weekly)"
# (workstream, filename regex) — first match wins. Order matters: specific before general.
RULES = [
    ("Boot Camp", r"Boot Camp|Bootcamp"),
    ("Systems & automation", r"refresh|scheduler|vault|Automation|GitHub|Notion|connector|ProPresenter knowledge"),
    # 2027 programming, split four ways (Connor, 2026-11-27): Bible Labs, Curiosity
    # Dinners, Inspira, Off-ramps (after-service activities: game night, football,
    # Super Bowl party, workshops).
    ("Curiosity Dinners", r"curiosity"),
    ("Inspira", r"Inspira|Country Night"),
    ("Bible Labs", r"Bible teaching|Bible Lab|Revelation"),
    ("Off-ramps", r"off-ramp|Super Bowl|journaling|game night|football|workshop"),
    ("People & leadership pipeline", r"core team|host candidates|availability through|captain|Liz Goodiel|young-professional small groups|feedback"),
    (SUNDAY, r"Sunday Night plan content|Remind Seth|QR landing|roster|lights|audio replacement|worship leader|blockouts|greeter|security|QR code"),
    ("Staff & relationships", r"All Staff|Jeff Brady|Ben Palmer|Heather Noble|Derek|sign"),
]
ORDER = ["Bible Labs", "Curiosity Dinners", "Inspira", "Off-ramps", "People & leadership pipeline", "Boot Camp",
         "Events", "Staff & relationships", "Systems & automation", "Other", SUNDAY]
# Shown even with no open items, so a quiet group still has a line.
ALWAYS = ["Bible Labs", "Curiosity Dinners", "Inspira", "Off-ramps"]
HORIZON_WEEKS = 10
STALE_WAIT_DAYS = 14


def classify(n, fm_ws):
    if fm_ws:
        return fm_ws
    for ws, pat in RULES:
        if re.search(pat, n["file"], re.I):
            return ws
    return "Other"


def workstream_field(path):
    m = re.search(r"^workstream:\s*\"?([^\"\n]+)\"?\s*$", open(path, encoding="utf-8").read().split("\n---", 1)[0], re.M)
    return m.group(1).strip() if m else ""


def load_milestones(root):
    p = os.path.join(root, "Trackers", "Milestones.md")
    out = []
    if not os.path.exists(p):
        return out
    for line in open(p, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3:
            d = AI.first_date(cells[0])
            if d:
                out.append((d, cells[1], cells[2]))
    return out


def due(n):
    return AI.first_date(n["needs_by"]) or AI.first_date(n["deadline"])


def since(n):
    return AI.first_date(n["waiting_on"])


CHECK = re.compile(r"^\s*- \[ \] (.+)$", re.M)
SCHED = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")


def next_step(n, today):
    """(text, scheduled_date) for a to-do's next step (Connor, 2026-11-27: "if my next task
    is a scheduled thing, list the next thing I can do now, or count that scheduled thing
    as a waiting on").

    A checkbox carrying `📅 YYYY-MM-DD` in the future is a scheduled occasion, not work.
    Returns the first open checkbox WITHOUT a future 📅 as (text, None). If every open
    checkbox is scheduled, returns (first one, its date) — the item then counts as
    waiting on that date. No open checkboxes → ("", None) and the title stands.
    """
    try:
        body = open(n["path"], encoding="utf-8").read().split("\n---", 1)[-1]
    except OSError:
        return "", None
    first_sched = None
    for m in CHECK.finditer(body):
        text = m.group(1).strip()
        d = SCHED.search(text)
        sd = datetime.date.fromisoformat(d.group(1)) if d else None
        clean = SCHED.sub("", text).strip(" ·—-")
        if sd and sd > today:
            first_sched = first_sched or (clean, sd)
            continue
        return clean, None
    return first_sched or ("", None)


def kind_of(n, today):
    """todo / waiting / parked, with scheduled-only to-dos counted as waiting."""
    if n["status"] in ("active", "in-progress"):
        return "waiting" if next_step(n, today)[1] else "todo"
    if n["status"] == "waiting-on":
        return "waiting"
    return "parked"


def sched_who(d):
    return "%s %s (scheduled)" % (d.strftime("%a"), "%d/%d" % (d.month, d.day))


def short(f):
    return re.sub(r"^(Connor|[A-Z][a-z]+ [A-Z][\w-]+|Sunday Night hosts) - ", "", f)


def who(n):
    m = re.match(r"^([^-—]+?)(?: since|,|—|$)", n["waiting_on"] or "")
    return (m.group(1).strip() if m else "") or n["owner"]


def health(items, today):
    reasons = []
    for n in items:
        d = due(n)
        if n["status"] in ("active", "in-progress") and n["priority"] == "P1" and d and d < today:
            reasons.append(("red", "P1 past its date: " + short(n["file"])))
        if n["flagged"] and n["priority"] in ("P1", "P2"):
            reasons.append(("red", "flagged: " + short(n["file"])))
        elif n["flagged"]:
            reasons.append(("yellow", "flagged: " + short(n["file"])))
        s = since(n)
        if n["status"] == "waiting-on" and s and (today - s).days > STALE_WAIT_DAYS:
            reasons.append(("yellow", "waiting %dd: %s" % ((today - s).days, short(n["file"]))))
    if any(r[0] == "red" for r in reasons):
        return "🔴", reasons
    if reasons:
        return "🟡", reasons
    return "🟢", reasons


def main():
    args = sys.argv[1:]
    today = AI.datetime.datetime.now(AI.ET).date()
    if "--today" in args:
        today = datetime.date.fromisoformat(args[args.index("--today") + 1])
    root = AI.vault_root()
    notes = [n for n in AI.load(root) if n["status"] in AI.LIVE]
    status_by_file = {n["file"]: n["status"] for n in AI.load(root)}
    streams = {}
    for n in notes:
        streams.setdefault(classify(n, workstream_field(n["path"])), []).append(n)
    miles = load_milestones(root)
    end = today + datetime.timedelta(weeks=HORIZON_WEEKS)

    L = ["# 🧭 Dashboard", "",
         "**Everything Connor helps with, one page. Also live as the [Grace Workstreams](https://claude.ai/artifact/TWyVStuKWc19V79JfW5rCH) artifact. Generated by `Workflows/dashboard.py` — never hand-edited.** "
         "Weekly Sunday service ops are collapsed to one line; the refresh's Start Here covers them.", "",
         "generated: %s ET" % AI.datetime.datetime.now(AI.ET).strftime("%Y-%m-%d %H:%M"), "",
         "Health: 🔴 a P1 past its date or a flagged P1/P2 · 🟡 flagged, or a wait over %d days · 🟢 on track" % STALE_WAIT_DAYS, ""]

    # Horizon
    L += ["## Next %d weeks" % HORIZON_WEEKS, "", "| date | what | stream |", "|---|---|---|"]
    rows = [(d, w, s) for d, w, s in miles if today <= d <= end]
    for n in notes:
        d = due(n)
        if d and today <= d <= end and n["status"] in ("active", "in-progress", "waiting-on"):
            lab = ("needed from %s: " % who(n) if n["status"] == "waiting-on"
                   else "scheduled: " if kind_of(n, today) == "waiting" else "due: ")
            rows.append((d, lab + short(n["file"]),
                         classify(n, workstream_field(n["path"]))))
    for d, w, s in sorted(rows):
        L.append("| %s %s | %s | %s |" % (d.strftime("%a"), d.strftime("%m/%d"), w, s))
    L.append("")

    summary = []
    for ws in ORDER + sorted(set(streams) - set(ORDER)):
        items = streams.get(ws, [])
        if not items and ws not in ALWAYS:
            continue
        h, reasons = health(items, today)
        acts = [n for n in items if kind_of(n, today) == "todo"]
        waits = [n for n in items if kind_of(n, today) == "waiting"]
        holds = [n for n in items if kind_of(n, today) == "parked"]
        summary.append("%s %s — %d to do, %d waiting, %d parked" % (h, ws, len(acts), len(waits), len(holds)))
        if ws == SUNDAY:
            L += ["## %s %s" % (h, ws), "",
                  "%d to do, %d waiting, %d parked — see the refresh's Start Here." % (len(acts), len(waits), len(holds)), ""]
            continue
        L += ["## %s %s" % (h, ws), ""]
        for _, r in reasons[:4]:
            L.append("> %s" % r)
        if reasons:
            L.append("")
        if acts:
            L.append("**Connor's next actions**")
            for n in sorted(acts, key=lambda n: (n["priority"] or "P9", due(n) or datetime.date.max)):
                blk = " · ⛔ blocked" if AI.open_blockers(n, status_by_file) else ""
                d = due(n)
                step = next_step(n, today)[0]
                L.append("- %s [[Trackers/Actions/%s|%s]]%s%s%s" % (n["priority"] or "--", n["file"], short(n["file"]),
                                                                     " — next: %s" % step if step else "",
                                                                     " · by %s" % d.strftime("%m/%d") if d else "", blk))
            L.append("")
        if waits:
            L.append("**Waiting on others**")
            for n in sorted(waits, key=lambda n: since(n) or today):
                s, sd = since(n), next_step(n, today)[1]
                L.append("- %s — [[Trackers/Actions/%s|%s]]%s" % (sched_who(sd) if sd else who(n), n["file"], short(n["file"]),
                                                                  " · %dd" % (today - s).days if (s and not sd) else ""))
            L.append("")
        if holds:
            L.append("**Parked:** " + " · ".join("[[Trackers/Actions/%s|%s]]" % (n["file"], short(n["file"])) for n in holds))
            L.append("")

    if "--json" in args:
        write_json(args[args.index("--json") + 1], today, notes, streams, rows, status_by_file)

    page = "\n".join(L).rstrip() + "\n"
    if "--stdout" in args:
        print(page)
        return
    open(os.path.join(root, "Trackers", "Dashboard.md"), "w", encoding="utf-8").write(page)
    print("Dashboard — %s" % today)
    for s in summary:
        print("  " + s)


def write_json(out_dir, today, notes, streams, horizon_rows, status_by_file):
    """Three {rows, meta} files for the Grace Workstreams artifact (added 2026-11-27).

    streams.json    one row per workstream: health + counts + why
    items.json      one row per live action item (Sunday ops included, flagged as such)
    milestones.json the 10-week date strip
    """
    import json
    os.makedirs(out_dir, exist_ok=True)
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    meta = [{"label": "dashboard.py", "value": src, "type": "code", "lang": "python"},
            {"label": "Input", "value": "Trackers/Actions frontmatter + Trackers/Milestones.md"},
            {"label": "Generated", "value": AI.datetime.datetime.now(AI.ET).strftime("%Y-%m-%d %H:%M ET")}]
    srows, irows = [], []
    by_file = {n["file"]: n for n in notes}
    for ws in ORDER + sorted(set(streams) - set(ORDER)):
        items = streams.get(ws, [])
        if not items and ws not in ALWAYS:
            continue
        h, reasons = health(items, today)
        srows.append({"stream": ws, "health": {"🔴": "red", "🟡": "yellow", "🟢": "green"}[h],
                      "todo": sum(kind_of(n, today) == "todo" for n in items),
                      "waiting": sum(kind_of(n, today) == "waiting" for n in items),
                      "parked": sum(kind_of(n, today) == "parked" for n in items),
                      "why": "; ".join(r for _, r in reasons[:3]), "weekly": ws == SUNDAY})
        for n in items:
            d, s = due(n), since(n)
            kind = kind_of(n, today)
            step, sd = next_step(n, today) if n["status"] in ("active", "in-progress") else ("", None)
            # Who a to-do is really waiting on (Connor, 2026-11-27: "if the next thing for me
            # to do is waiting on someone, I want that listed"): an open blocker's party,
            # else the to-do's own waiting_on.
            waiting_for = ""
            if kind == "todo":
                blk = AI.open_blockers(n, status_by_file)
                if blk:
                    b = by_file.get(blk[0])
                    waiting_for = (who(b) if b else "") or short(blk[0])
                elif n["waiting_on"]:
                    waiting_for = who(n)
            # `next` = the step Connor can do now (or the scheduled step, for a scheduled-only
            # item); the page shows it in place of the title when present.
            irows.append({"item": short(n["file"]), "next": step, "stream": ws, "kind": kind,
                          "priority": n["priority"] or "",
                          "waiting_for": waiting_for, "scheduled": sd.isoformat() if sd else "",
                          "due": d.isoformat() if d else "",
                          "who": (sched_who(sd) if sd else who(n)) if kind == "waiting" else "",
                          "days_waiting": (today - s).days if (kind == "waiting" and s and not sd) else None,
                          "flagged": bool(n["flagged"]), "blocked": bool(AI.open_blockers(n, status_by_file))})
    mrows = [{"date": d.isoformat(), "what": w, "stream": s} for d, w, s in sorted(horizon_rows)]
    for name, rows in (("streams", srows), ("items", irows), ("milestones", mrows)):
        with open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8") as f:
            json.dump({"rows": rows, "meta": meta}, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
