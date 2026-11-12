#!/usr/bin/env python3
"""
actions-index.py — compact index over /Trackers/Actions/ so a sweep never has to
read 130+ note bodies into context just to find the handful that need attention.

Created 2026-08-10. Rationale: the Open Actions sweep + the dedup cross-check
required by text-message-sync Step 5 and m365-to-obsidian-sync were reading the
entire folder (132 notes / 428 KB) every run. Every field those steps key on
(status, priority, deadline, needs_by, last_mentioned, flagged) lives in
frontmatter. This emits ~10 KB instead, and marks exactly which notes are worth
opening. Also flags live notes that have themselves grown too big to read cheaply
(OVERSIZED NOTES, threshold BLOAT_KB).

USAGE
  python3 "Workflows/actions-index.py"            # sweep view: live items + computed candidate lists
  python3 "Workflows/actions-index.py" --brief    # "start here" work queue for a working session (14-day horizon)
  python3 "Workflows/actions-index.py" --titles   # every note, "status | filename" (dedup cross-check)
  python3 "Workflows/actions-index.py" --all      # full index incl. completed
  python3 "Workflows/actions-index.py" --drift    # frontmatter vs body consistency check
  python3 "Workflows/actions-index.py" --today 2026-08-10   # override date (testing)

Run it from the vault root. Read bodies ONLY for the files this names.
"""
import os, re, sys, glob, datetime
from zoneinfo import ZoneInfo

# Calendar window (added 2026-08-20). Imported softly: if the module or the
# window file is missing the index must still run -- it just reports 'unknown'
# for shared meetings instead of silently reporting 'none'. Absence of data is
# never allowed to read as absence of the meeting; that conflation is the exact
# failure this whole feature exists to fix.
try:
    import importlib.util as _ilu
    _cwp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar-window.py")
    _spec = _ilu.spec_from_file_location("calendar_window", _cwp)
    CW = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(CW)
except Exception:
    CW = None

# Connor's local timezone. The execution shell reports UTC, so a naive
# date.today() rolls over ~4-5h early and every date computation in this
# script (chase_by, deadline-overdue, needs_by-reached, on-hold release)
# fires a day ahead all evening. Measured 2026-08-17 22:30 ET: the naive
# clock read 2026-08-18 and reported a live chase_by as passed.
ET = ZoneInfo("America/New_York")

LIVE = ("active", "in-progress", "waiting-on", "on-hold", "closure-candidate")
SWEEPABLE = ("active", "in-progress", "waiting-on")   # on-hold is exempt (Open-Actions-Tracker)
NEGLECT_DAYS = 7
BLOAT_KB = 15        # live notes bigger than this get flagged; see OVERSIZED NOTES below
ARCHIVE_DAYS = 14    # completed notes resolved longer ago than this get flagged for archiving
P2_WINDOW, P1_WINDOW = 21, 7

# How far ahead --brief looks when deciding what is date-urgent. 14, not 7, since
# 2026-08-21 (Connor). This is the Start Here HORIZON and is deliberately NOT the
# same number as either 7 above -- NEGLECT_DAYS is how long silence is tolerated
# before flagging, P1_WINDOW is a banding window. Changing one must not change
# the others; they were three unrelated 7s and this one was a bare literal.
#
# Why 14: at 7 days the 2026-08-21 morning queue could not see the 8/30 formation
# lunch nine days out with no invite sent -- Connor's read was "So I have no open
# actions? That can't be right." Measured at the time of the change, widening to
# 14 admitted 6 items a 7-day horizon hid, including the 8/30 lunch and its deck.
# Wider horizon means MORE candidates reaching the today-only gate, not fewer
# judgment calls -- that is the intended trade, since the gate is a subtraction
# and this is the selection it subtracts from.
HORIZON_DAYS = 14
# Conversations (calls, meetings) are surfaced this many days ahead regardless
# of status -- the prep and the time-confirm are Connor's even while the item is
# waiting-on. See meeting_rows().
MEETING_HORIZON_DAYS = 3


def vault_root():
    d = os.path.abspath(".")
    while d != "/":
        if os.path.isdir(os.path.join(d, "Trackers", "Actions")):
            return d
        d = os.path.dirname(d)
    sys.exit("error: run from inside the vault (no Trackers/Actions found above cwd)")


def parse_fm(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]
    fm, key = {}, None
    for line in raw.splitlines():
        if re.match(r"^\s*-\s+", line) and key:
            fm.setdefault(key + "[]", []).append(re.sub(r"^\s*-\s+", "", line).strip().strip('"\''))
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip().strip('"\'')
    return fm, body


def first_date(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    if not m:
        return None
    try:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def first_dt(s):
    """Full date+time when the field carries one, else None.

    `first_date` deliberately drops the time. For `chase_by` that is wrong:
    [[Workflows/Open-Actions-Tracker]] Step 3 sweeps short-fuse items "on the
    clock, not the calendar," and a date-only compare fires a chase_by dated
    TODAY from 00:00 onward — flagging a fuse that is still live. Added
    2026-08-12 after both of that day's chase_by items surfaced as passed at
    12:24 ET when they named 13:00 and 17:00.
    """
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})", s or "")
    if not m:
        return None
    try:
        return datetime.datetime(*(int(g) for g in m.groups()))
    except ValueError:
        return None


def all_dates(s):
    out = []
    for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})", s or ""):
        try:
            out.append(datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    return out


NOT_BLOCKED = {"", "-", "[]", "n/a", "na", "no", "none", "nothing", "nobody", "null", "false"}


def normalize_blocker(v):
    """Empty string for anything that means "not blocked", else the blocker text."""
    return "" if str(v).strip().strip('"\'').lower() in NOT_BLOCKED else v


def load(root):
    out = []
    for p in sorted(glob.glob(os.path.join(root, "Trackers", "Actions", "*.md"))):
        fm, body = parse_fm(open(p, encoding="utf-8").read())
        out.append({
            "file": os.path.basename(p)[:-3],
            "path": p,
            "bytes": os.path.getsize(p),
            "body": body,
            "status": fm.get("status", "?"),
            "priority": fm.get("priority", ""),
            "owner": fm.get("owner", ""),
            "deadline": fm.get("deadline", ""),
            "needs_by": fm.get("needs_by", ""),
            "last_mentioned": fm.get("last_mentioned", ""),
            "flagged": fm.get("flagged", ""),
            "chase_by": fm.get("chase_by", ""),
            # A note that says blocked_by: "none" is NOT blocked. The literal
            # string was being read as truthy, so two actionable P1s (Boot camp
            # relaunch, host/MC) printed as `blocked` and Step 3 skipped them --
            # the neglect sweep was shielding the items it exists to catch.
            # Fixed 2026-08-18. Normalized here so every view inherits it.
            # A YAML block list (`blocked_by:` then `  - "[[...]]"` lines) lands
            # under "blocked_by[]" with an empty scalar -- read both, or a
            # genuinely blocked item prints as actionable. Fixed 2026-09-22.
            "blocked_by": normalize_blocker(fm.get("blocked_by", "")) or "; ".join(fm.get("blocked_by[]", [])),
            "on_hold_since": fm.get("on_hold_since", ""),
            "waiting_on": fm.get("waiting_on", ""),
            # When the item's next step is a conversation Connor will be in
            # (call, meeting) agreed or proposed by text/email and therefore NOT
            # on the Outlook calendar. `YYYY-MM-DD HH:MM` or `YYYY-MM-DD`.
            "meeting": fm.get("meeting", ""),
            "resolved": fm.get("resolved", ""),
            "projects": fm.get("projects[]", []),
        })
    return out


def trigger_dates(on_hold_since):
    """Dates that actually govern an on-hold release.

    Two corrections over a naive scan of the `trigger:` clause (2026-08-11):
      1. Strip parentheticals. Trigger clauses carry provenance citations like
         `(Connor 2026-08-06: "...")`, and that citation date is in the past by
         construction -- so scanning raw prose released the item the moment it
         was parked. This produced a false positive on the Sunday-night worship
         item on two consecutive runs.
      2. Honour the `Date wake-up regardless: YYYY-MM-DD` convention, which is
         the real date-locked backstop and lives AFTER the trigger clause, so
         the old regex (`trigger:.*$`) happened to include it only by accident
         of ordering.
    Undated external triggers still yield nothing -- deliberately; see the
    dead-trigger gap note at the call site.
    """
    m = re.search(r"trigger:\s*(.*)$", on_hold_since or "", re.S | re.I)
    clause = re.sub(r"\([^)]*\)", " ", m.group(1)) if m else ""
    out = list(all_dates(clause))
    w = re.search(r"wake[-\s]?up[^:]*:\s*(\d{4}-\d{2}-\d{2})", on_hold_since or "", re.I)
    if w:
        out += all_dates(w.group(1))
    return out


def awaited_party(waiting_on):
    """The person a waiting-on item is waiting for, from the `waiting_on` field.

    Convention across the folder is "<Name> since YYYY-MM-DD -- <what>", sometimes
    with a routed target in parens: "Derek Adye (-> Jennifer Lonero, Shore
    Accounting) since ...". We want the person Connor would actually talk to,
    which is the name before the paren, not the downstream one.
    """
    if not waiting_on:
        return ""
    head = re.split(r"\s+since\s+", waiting_on.strip(), maxsplit=1)[0]
    head = re.sub(r"\(.*?\)", "", head)                  # drop routed target
    head = re.split(r"\s*(?:\+|,| and )\s*", head)[0]     # first of several
    head = head.strip(" -\u2014:")
    # A single capitalized first name is a real convention here (Skylar, Alex), so
    # accept it. It will usually resolve to 'unknown' downstream -- which is the
    # honest answer and strictly better than printing nothing, because nothing
    # reads as "no wait to compute" rather than "I could not identify this person".
    return head if re.match(r"^[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+)*$", head) else ""


def shared_meeting_note(n, today, cal):
    """' | next w/ X: ...' for a waiting-on item -- the answer to 'when's the moment?'

    Added 2026-08-20. Before this, that question was answered by inference and got
    answered wrong: a report named a meeting the awaited person was not attending.
    Now it is computed, and 'no occasion before the date' is itself the finding.
    """
    if CW is None or n["status"] != "waiting-on":
        return ""
    who = awaited_party(n["waiting_on"])
    if not who:
        return ""
    limit = first_date(n["needs_by"]) or first_date(n["deadline"])
    # A limit that has already passed tells us nothing -- and worse, it suppresses
    # the useful answer. Measured 2026-08-20: the Kay Rock<->PCO item (needs_by
    # 2026-08-15, blown) reported 'NONE before 2026-08-15' while Connor in fact
    # has a Rock/PCO session with Kay on 8/24. The single most useful line in the
    # feature was being hidden by an expired date. Past limit -> answer for the
    # whole window instead, and say the limit is blown.
    blown = bool(limit and limit < today)
    if blown:
        limit = None
    after = datetime.datetime.combine(today, datetime.time.min)
    m, status = CW.next_shared(who, cal=cal, after=after, before=limit)
    # A conversation agreed off-calendar (text/email) is a real occasion the
    # Outlook window cannot see. Prefer it when it comes first. 2026-11-12.
    mt = first_date(n["meeting"])
    if mt and mt >= today and (status != "ok" or mt < m["start"].date()):
        return " | next w/ %s: %s (meeting field, off-calendar)" % (who, mt)
    if status == "ok":
        return " | next w/ %s: %s%s" % (who, m["start"].date(),
                                        " (its own date already passed)" if blown else "")
    if status == "none":
        return " | next w/ %s: NONE%s" % (who, " before %s" % limit if limit else " in the window")
    if status == "unknown":
        return " | next w/ %s: unknown" % who
    return ""


def fmt(n):
    bits = ["%-18s" % n["status"], "%-3s" % (n["priority"] or "--")]
    for label, key in (("dl", "deadline"), ("nb", "needs_by"), ("lm", "last_mentioned")):
        d = first_date(n[key])
        bits.append("%s=%s" % (label, d.isoformat() if d else "-"))
    if n["chase_by"]:
        bits.append("chase=" + (first_date(n["chase_by"]).isoformat() if first_date(n["chase_by"]) else "?"))
    if n["flagged"]:
        bits.append("FLAGGED")
    if n["blocked_by"]:
        bits.append("blocked")
    return " | ".join(bits) + " | " + n["file"] + n.get("_shared", "")


OPEN_BLOCKER_STATUSES = {"active", "in-progress", "waiting-on", "on-hold", "closure-candidate"}


def open_blockers(n, status_by_file):
    """Names of this note's blockers that are still OPEN, resolved against the
    folder. Empty list = nothing is holding it.

    WHY THIS IS CODE (2026-08-31). Open-Actions-Tracker defines the queue as
    "every active/in-progress item Connor owns that is NOT blocked_by an open
    item", and the sweep view has printed a `blocked` marker since 2026-08-18 --
    but `brief()` never read the field, so a blocked item could lead Start Here.
    It did: the 8/29 hold on "Message the Sunday-night volunteers to sign up for
    shifts in PCO" (held on Kay's Rock welcome-email switch, because a volunteer
    who cannot set a PCO password cannot answer the message) was written into the
    body only. Once the frontmatter caught up on 8/31 the sweep view said
    `blocked` and --brief still printed it under "Overdue or due today" on a
    passed needs_by. Same family as the 2026-08-18 waiting-on suppression
    directly above: a queue line has to have a Connor-side action behind it.

    FAILS OPEN, deliberately. A blocker string that resolves to no note in the
    folder suppresses NOTHING. Over-suppression is data loss -- it silently
    removes real work from the only view Connor reads first -- and that is not a
    safe direction to err in. Under-suppression costs one line he can strike.
    """
    out = []
    for m in re.findall(r"\[\[([^\]]+)\]\]", str(n["blocked_by"])):
        target = m.split("|")[0].split("/")[-1].strip()
        if target.endswith(".md"):
            target = target[:-3]
        if status_by_file.get(target) in OPEN_BLOCKER_STATUSES:
            out.append(target)
    return out


def md_dates(s, today):
    """`M/D` dates in free text, resolved to the nearest year (today's, or next
    year's if that is closer). Backstop only -- the `meeting` field is the rule."""
    out = []
    for m in re.finditer(r"(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])", s or ""):
        mo, d = int(m.group(1)), int(m.group(2))
        for y in (today.year, today.year + 1):
            try:
                dt = datetime.date(y, mo, d)
            except ValueError:
                continue
            if (dt - today).days >= -180:
                out.append(dt)
                break
    return out


def meeting_rows(notes, today):
    """Conversations in the next MEETING_HORIZON_DAYS, from any live status.

    Added 2026-11-12. A call with John Slye was agreed by text for Fri 11/13
    (John: "Friday afternoon works"; Connor proposed 3 PM, unconfirmed). The note
    was `waiting-on`, so brief() suppressed it as "nothing for Connor to do," and
    the call was never on Outlook, so Calendar-Window and the `next w/` column
    said the next shared occasion was the 11/17 All Staff. The refresh report the
    day before the call did not mention it. But a pending conversation always has
    Connor-side work: confirm the time, and prep his own agenda items. So these
    rows bypass the waiting-on suppression on purpose.

    Source 1 (the rule): the `meeting` frontmatter field.
    Source 2 (backstop): a waiting-on item with no `meeting` field whose
    `waiting_on` text names an M/D or ISO date in the horizon -- printed with a
    note to set the field, so a missed field degrades loudly, not silently.
    """
    rows = []
    for n in notes:
        if n["status"] not in LIVE:
            continue
        mt_dt, mt = first_dt(n["meeting"]), first_date(n["meeting"])
        unconfirmed = " — time unconfirmed (waiting on %s)" % (awaited_party(n["waiting_on"]) or "reply") \
            if n["status"] == "waiting-on" else ""
        if mt:
            days = (mt - today).days
            if 0 <= days <= MEETING_HORIZON_DAYS:
                when = mt_dt.strftime("%a %-m/%-d %-I:%M %p") if mt_dt else mt.strftime("%a %-m/%-d")
                rows.append((days, n["priority"] or "P?", n["file"], "%s — prep%s" % (when, unconfirmed)))
            continue
        if n["status"] == "waiting-on":
            tail = re.split(r"\s+since\s+\d{4}-\d{2}-\d{2}", n["waiting_on"], maxsplit=1)[-1]
            hits = sorted(d for d in md_dates(tail, today) + all_dates(tail)
                          if 0 <= (d - today).days <= MEETING_HORIZON_DAYS)
            if hits:
                rows.append(((hits[0] - today).days, n["priority"] or "P?", n["file"],
                             "%s named in waiting_on, no `meeting:` field — set it; confirm + prep"
                             % hits[0].strftime("%a %-m/%-d")))
    rows.sort()
    return rows


def brief(notes, today):
    """Work queue for a session Connor is about to start. Urgency only -- this is
    not an inventory; the sweep view is. Ordered most-urgent first, capped."""
    due, week, decide, stalled, unparked = [], [], [], [], []
    status_by_file = {x["file"]: x["status"] for x in notes}
    horizon_days = {}   # file -> days out, so the horizon bucket sorts by date not band
    for n in notes:
        st, pri = n["status"], n["priority"] or "P?"
        if st == "closure-candidate":
            decide.append((pri, n["file"], "confirm or dismiss"))
            continue
        if st == "on-hold":
            hits = [d for d in trigger_dates(n["on_hold_since"]) if d <= today]
            if hits:
                unparked.append((pri, n["file"], "trigger date %s reached" % max(hits)))
            continue

        # Start Here is a work queue, not an inventory: an item earns a place
        # only if the next physical action is Connor's. A `waiting-on` item has
        # exactly one Connor-side action -- a chase -- so a needs_by or deadline
        # firing while someone else holds the ball is not work, it is noise.
        # Suppressed here rather than in the sweep view, which is the inventory
        # and still shows everything.
        #
        # Added 2026-08-18 after Connor struck three of the four items in one
        # run's queue with the same sentence: "if there's nothing to do on this,
        # it shouldn't have been raised." Kay (needs_by passed, staff on it),
        # Callie (replied in-channel the same morning), Heather NFC (she had
        # already said "I'll let you know when I have more info").
        #
        # Corollary worth honouring upstream: a `chase_by` must not be invented
        # against someone who has committed to reporting back. If it is, this
        # guard cannot save the queue -- the note has to lose the field.
        if st == "waiting-on" and not first_date(n["chase_by"]):
            continue
        if st not in SWEEPABLE:
            continue
        # Blocked by something still open -> not this session's work. See
        # open_blockers() for why this lives in code and why it fails open.
        if open_blockers(n, status_by_file):
            continue
        cb, nb, dl = first_date(n["chase_by"]), first_date(n["needs_by"]), first_date(n["deadline"])
        cb_dt = first_dt(n["chase_by"])
        why, bucket = None, None
        # Time-aware, same reason as the sweep view: a chase_by naming a time
        # today is still LIVE until that time. Show it as a live fuse, not a
        # passed one -- the distinction is the whole point of a short fuse.
        if cb_dt and cb_dt > datetime.datetime.now():
            why, bucket = "chase-by %s — live fuse" % cb_dt.strftime("%-I:%M %p"), due
        elif cb and (cb_dt is None or cb_dt <= datetime.datetime.now()) and cb <= today:
            why, bucket = "chase-by %s passed" % cb, due
        elif dl and dl < today:
            why, bucket = "deadline %s (%dd overdue)" % (dl, (today - dl).days), due
        elif (dl and dl == today) or (nb and nb <= today):
            why, bucket = ("due today" if dl == today else "needs_by %s — latest start" % nb), due
        else:
            soon = min([d for d in (nb, dl) if d], default=None)
            if soon and (soon - today).days <= HORIZON_DAYS:
                why, bucket = "%s in %dd" % ("needs_by" if soon == nb else "deadline", (soon - today).days), week
                horizon_days[n["file"]] = (soon - today).days
        if bucket is not None:
            bucket.append((pri, n["file"], why))
        elif n["flagged"]:
            stalled.append((pri, n["file"], n["flagged"][:60]))

    print("# START HERE — %s" % today.strftime("%Y-%m-%d (%a)"))
    meets = meeting_rows(notes, today)
    if meets:
        print("\n## [@] Conversations in the next %d days — confirm + prep (%d)" % (MEETING_HORIZON_DAYS, len(meets)))
        for _, pri, f, why in meets[:8]:
            print("  %-3s %s  <- %s" % (pri, f, why))
    for icon, title, rows, cap in (
        ("[!]", "Overdue or due today", due, 8),
        ("[>]", "Next %d days" % HORIZON_DAYS, week, 12),
        ("[?]", "Decisions waiting on you", decide, 8),
        ("[~]", "Unparked — on-hold trigger reached", unparked, 5),
        ("[.]", "Flagged / stalled", stalled, 5),
    ):
        if not rows:
            continue
        # The horizon bucket sorts by DATE, everything else by band. At a 7-day
        # window band-first ordering was harmless; at 14 it would print a P1 due
        # in 13 days above a P2 due in 8, which is the wrong reading order for a
        # list whose whole meaning is "what is coming at me and when."
        if rows is week:
            rows.sort(key=lambda r: (horizon_days.get(r[1], 99), r[0]))
        else:
            rows.sort(key=lambda r: (r[0], r[1]))
        print("\n## %s %s (%d)" % (icon, title, len(rows)))
        for pri, f, why in rows[:cap]:
            print("  %-3s %s  <- %s" % (pri, f, why))
        if len(rows) > cap:
            print("  ... +%d more (see the full sweep view)" % (len(rows) - cap))
    if not any((meets, due, week, decide, unparked, stalled)):
        print("\n  Nothing urgent. Clear runway.")



DATE_FIELD_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}( \d{1,2}:\d{2})?|none)$")


def malformed_date_fields(notes):
    """deadline/needs_by/chase_by must be a bare date, a date+time, or `none`.

    Free text here is how the same false positive got re-diagnosed on three
    consecutive runs: first_date() finds the first date ANYWHERE in the string,
    so `deadline: "Unstated - week of 2026-08-10"` read as a deadline of 8/10
    and the item showed as overdue. Migrated 2026-08-12; this check stops it
    rotting back. Prose belongs in a `- **<Field> rationale**:` body bullet.
    """
    out = []
    for n in notes:
        for f in ("deadline", "needs_by", "chase_by", "meeting"):
            v = (n.get(f) or "").strip()
            if v and not DATE_FIELD_RE.match(v):
                out.append("%s: %s = %s" % (n["file"], f, v[:60]))
    return out


def evidence(n, limit=2):
    """The body lines a sweep would otherwise open the whole note to find.

    Emitting these is what keeps a candidate from costing a full body read:
    most are cleared or confirmed on the rationale bullet plus the newest
    dated line. Read the body only when these two lines are not enough.
    """
    body = n.get("body") or ""
    rat, dated = [], []
    for line in body.split("\n"):
        t = line.strip()
        if not t:
            continue
        if re.match(r"^- \*\*(Deadline|Needs-by|Chase-by) rationale\*\*", t):
            rat.append(t)
        elif re.match(r"^#{2,4} \d{4}-\d{2}-\d{2}", t) or re.match(
                r"^- (~~)?\*\*(?:[^\w\s]+\s*)?\d{4}-\d{2}-\d{2}", t):
            dated.append(t)
    picked = rat[:1] + dated[-limit:]
    return [re.sub(r"\s+", " ", x)[:150] for x in picked]


# Frontmatter fields whose value must never be restated in the note body.
# The body may EXPLAIN a field -- "- **Deadline rationale**: the launch itself" --
# but it may not carry the value, because a value in two places drifts. 47 rows had
# drifted by 2026-08-22, which is why this is a presence check and not a comparison:
# comparing values only catches the ones that have already gone wrong.
BANNED_BODY_FIELDS = ("Priority", "Deadline", "Needs-by", "Last mentioned",
                      "Added", "Chase-by", "Waiting on", "On hold", "Flagged", "Resolved")
BANNED_RE = re.compile(r"^\s*-\s*\*\*(%s)\*\*:" %
                       "|".join(re.escape(f) for f in BANNED_BODY_FIELDS), re.I | re.M)


def redundant_body_fields(notes):
    """Body bullets that restate a frontmatter field. Presence is the defect."""
    rows = []
    for n in notes:
        for m in BANNED_RE.finditer(n["body"]):
            line = n["body"][m.start():n["body"].find("\n", m.start())].strip()
            rows.append("%s  (- **%s**: ...)  %s" % (n["file"], m.group(1), line[:60]))
    return rows


def status_contradictions(notes):
    """Frontmatter `status` vs the note's prose `- **Status**:` bullet.

    A different severity from the rest of the drift check: a stale Priority or
    Last-mentioned body line is cosmetic (frontmatter is the field authority),
    but a body still reading "Active" under a frontmatter `completed` may mean
    the item was wrongly closed, or is wrongly sitting open. Surfaced in the
    DEFAULT sweep output as well as --drift, because the drift check only runs
    in the weekly refresh and this class went unseen for 17 notes between
    2026-08-10 and 2026-08-22.
    """
    DONE = ("complete", "resolved", "done", "closed", "cancel", "lapsed")
    LIVE_W = ("active", "open", "on hold", "in progress", "waiting")
    contra = []
    for n in notes:
        m = re.search(r"^\s*-\s*\*\*Status\*\*:\s*(.+)$", n["body"], re.M)
        if not m:
            continue
        bv = m.group(1).strip().lower().lstrip("*").strip()
        fs = n["status"]
        if fs == "completed" and not any(w in bv[:70] for w in DONE):
            contra.append((n["file"], "fm=completed", m.group(1).strip()[:70]))
        elif fs in ("active", "in-progress", "waiting-on") and \
                any(bv.startswith(w) for w in DONE) and \
                not any(w in bv[:70] for w in LIVE_W):
            contra.append((n["file"], "fm=" + fs, m.group(1).strip()[:70]))
    return contra


def main():
    args = sys.argv[1:]
    _et_now = datetime.datetime.now(ET).replace(tzinfo=None)
    today = _et_now.date()
    now = _et_now
    if "--today" in args:
        today = first_date(args[args.index("--today") + 1]) or today
    root = vault_root()
    notes = load(root)

    if "--brief" in args:
        brief(notes, today)
        return

    if "--titles" in args:
        print("# %d notes — dedup cross-check index (%s)" % (len(notes), today))
        for n in notes:
            print("%-18s | %s" % (n["status"], n["file"]))
        return

    if "--drift" in args:
        rows = redundant_body_fields(notes)
        contra = status_contradictions(notes)
        print("# STATUS CONTRADICTIONS (high — note may be wrongly closed or wrongly open): %d" % len(contra))
        for f, fs, bv in contra:
            print("  !! %-14s body Status=%-72s | %s" % (fs, bv, f))
        if not contra:
            print("  (none)")
        print()
        print("# REDUNDANT BODY FIELDS: %d across %d notes" % (len(rows), len(notes)))
        print("# a body bullet restating a frontmatter value. Rename it to '<Field> rationale'")
        print("# and drop the literal -- see Open-Actions-Tracker 'The body explains fields, never restates them'.")
        for r in rows:
            print("  - " + r)
        if not rows:
            print("  (none)")
        return

    show = notes if "--all" in args else [n for n in notes if n["status"] in LIVE]
    # Compute the shared-meeting answer once per note (each call may read the
    # Office xlsx, so don't do it inside fmt()).
    _cal = CW.load(root) if CW else None
    no_occasion = []
    for n in notes:
        n["_shared"] = shared_meeting_note(n, today, _cal)
        if "NONE" in n["_shared"]:
            no_occasion.append("%s%s" % (n["file"], n["_shared"].replace(" | ", " — ", 1)))
    counts = {}
    for n in notes:
        counts[n["status"]] = counts.get(n["status"], 0) + 1

    print("# Actions index — %s | %d notes total (%s)" % (
        today, len(notes), ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))))
    print("# Showing %d. Read note BODIES only for files named in the candidate lists below.\n" % len(show))
    for n in sorted(show, key=lambda x: (x["status"], x["priority"] or "P9", x["file"])):
        print(fmt(n))

    neglect, escalate, release, candidates, chase, bloat, stale_completed = [], [], [], [], [], [], []
    by_file = {n["file"]: n for n in notes}
    for n in notes:
        st = n["status"]
        if st in LIVE and n["bytes"] > BLOAT_KB * 1024:
            bloat.append((n["bytes"], "%s (%d KB)" % (n["file"], n["bytes"] // 1024)))
        if st == "closure-candidate":
            candidates.append(n["file"])
        if st == "completed":
            rd = first_date(n["resolved"])
            if rd and (today - rd).days > ARCHIVE_DAYS:
                stale_completed.append("%s (resolved %s, %d days ago)" % (n["file"], n["resolved"][:10], (today - rd).days))
        if st in SWEEPABLE:
            cb_dt = first_dt(n["chase_by"])
            cb = first_date(n["chase_by"])
            # Time-aware when the field names one; date-only fields still
            # fire on the day, as before.
            cb_passed = (cb_dt <= now) if cb_dt else (bool(cb) and cb <= today)
            if cb_passed and not n["flagged"]:
                chase.append("%s (chase_by %s passed)" % (n["file"], n["chase_by"][:40]))
            lm, dl = first_date(n["last_mentioned"]), first_date(n["deadline"])
            if lm and (today - lm).days > NEGLECT_DAYS and not n["flagged"]:
                neglect.append("%s (%d days since last mention)" % (n["file"], (today - lm).days))
            elif dl and dl < today and not n["flagged"]:
                neglect.append("%s (past deadline by %d days)" % (n["file"], (today - dl).days))
            trig = first_date(n["needs_by"]) or dl
            if trig:
                days = (trig - today).days
                want = "P1" if days <= P1_WINDOW else ("P2" if days <= P2_WINDOW else None)
                if want and n["priority"] and want < n["priority"]:
                    escalate.append("%s: %s -> %s (%d days to %s)" % (
                        n["file"], n["priority"], want, days,
                        "needs_by" if first_date(n["needs_by"]) else "deadline"))
        if st == "on-hold":
            # The release trigger is prose ("trigger: ..."), so don't fake precision:
            # surface any on-hold item carrying a date at/behind today, and let the
            # sweep read that one body to decide. Dates are taken from on_hold_since
            # (where a date-locked trigger is recorded) and deadline as a backstop.
            # Only the TRIGGER clause matters. The leading date in on_hold_since is
            # when it was parked (always past) -- keying on that listed every parked
            # item every run. Items whose trigger is an external event with no date
            # ("trigger: the PCO roster being built") can't be computed and are left
            # out deliberately; judging whether such a trigger is still alive is the
            # known dead-trigger gap, and it needs a human read, not a date compare.
            hits = [d for d in trigger_dates(n["on_hold_since"]) if d <= today]
            if hits:
                # Not every on_hold_since spells the release as "trigger: ...".
                # Three notes phrase it as "Wake-up:", "re-activate on ...", or plain
                # prose, and re.search then returns None -- which crashed the whole
                # index (AttributeError on m.group) the first day one of those dates
                # came due, 2026-08-24, taking every candidate list down with it.
                # Fall back to the raw field rather than assuming the keyword.
                m = re.search(r"(?:trigger|wake-?up)\s*:\s*(.*)$",
                              n["on_hold_since"], re.S | re.I)
                why = (m.group(1) if m else n["on_hold_since"]) or ""
                release.append("%s (trigger date reached: %s | %s)"
                               % (n["file"], max(hits), why[:70].strip()))

    for title, rows, note in (
        ("CHASE-BY PASSED (Step 3 — flag immediately, on the clock not the calendar)", chase, "short-fuse items; these jump the 7-day rule"),
        ("NEGLECT CANDIDATES (Step 3 — open body to confirm before flagging)", neglect, ">%d days or past deadline, not already flagged; on-hold exempt" % NEGLECT_DAYS),
        ("ESCALATION CANDIDATES (Step 3.5 — raise band only, never lower)", escalate, "windows: P2 <=%dd, P1 <=%dd" % (P2_WINDOW, P1_WINDOW)),
        ("ON-HOLD RELEASE CHECKS (date-locked trigger reached)", release, "flip to active on the day of, not earlier. Undated external triggers are NOT listed -- check those by hand; a dead trigger will never surface here"),
        ("OPEN CLOSURE CANDIDATES (awaiting Connor confirm/dismiss)", candidates, "not auto-closable"),
        ("WAITING-ON WITH NO SHARED OCCASION (before needs_by/deadline)", no_occasion,
         "computed from Trackers/Calendar-Window.md -- there is no meeting to raise these at, so do not write one into a note. If the wait has to end, the channel is text then call (see connor-works-remotely). 'unknown' means the name could not be resolved and is NOT the same as 'none'"),
        ("REDUNDANT BODY FIELDS (a body bullet restating a frontmatter value — rename to '<Field> rationale', drop the literal)",
         redundant_body_fields(notes),
         "a value in two places drifts; 47 rows had by 2026-08-22. See Open-Actions-Tracker 'The body explains fields, never restates them'"),
        ("STATUS CONTRADICTIONS (frontmatter vs the note's own Status bullet — decide which is true, correct the loser)",
         ["%s  (%s | body Status=%s)" % (f, fs, bv) for f, fs, bv in status_contradictions(notes)],
         "high severity: a note may be wrongly closed, or wrongly sitting open. Closing an item means rewriting its Status bullet too -- see Open-Actions-Tracker 'Closing an item'"),
        ("OVERSIZED NOTES (>%d KB — every sync that appends one line reads the whole file)" % BLOAT_KB,
         [r for _, r in sorted(bloat, reverse=True)],
         "live notes only. FIX IT NOW, do not just note it: python3 \"Workflows/split-note-log.py\" --dry-run \"<path>\" then drop --dry-run. Never split by hand (live fields are interleaved with the history) and never delete content. Convention: Workflows/note-history-splitting.md"),
        ("COMPLETED, UN-ARCHIVED (resolved >%d days ago, still in the live folder)" % ARCHIVE_DAYS,
         sorted(stale_completed),
         "added 2026-09-16 after the 2026-08-12 archive sweep (94 notes) fully recurred by 2026-09-15 (96 of 140) — a one-time cleanup is not a rule. FIX IT NOW: move to /Archive/Actions/, repoint inbound wikilinks, don't just note it. Nothing here is destructive (never delete) — see the 2026-08-12 changelog for the exact method."),
    ):
        print("\n## %s\n#  %s" % (title, note))
        if not rows:
            print("  (none)")
            continue
        for r in rows:
            print("  - " + r)
            hit = next((by_file[k] for k in by_file if r.startswith(k)), None)
            if hit is not None:
                for ev in evidence(hit):
                    print("      | " + ev)

    bad = malformed_date_fields(notes)
    print("\n## MALFORMED DATE FIELDS (must be YYYY-MM-DD, YYYY-MM-DD HH:MM, or none)")
    print("#  free text here silently fabricates deadlines; move prose to a rationale bullet")
    print("\n".join("  - " + b for b in bad) if bad else "  (none)")


if __name__ == "__main__":
    main()
