import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()

# ---- 1. import the calendar module (soft: never break the index if it's absent)
old_imp = 'import os, re, sys, glob, datetime\nfrom zoneinfo import ZoneInfo\n'
assert old_imp in s, "import block not found"
new_imp = old_imp + '''
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
'''
s = s.replace(old_imp, new_imp, 1)

# ---- 2. awaited-party extraction + shared-meeting annotation
anchor = 'def fmt(n):'
assert anchor in s
helper = '''def awaited_party(waiting_on):
    """The person a waiting-on item is waiting for, from the `waiting_on` field.

    Convention across the folder is "<Name> since YYYY-MM-DD -- <what>", sometimes
    with a routed target in parens: "Derek Adye (-> Jennifer Lonero, Shore
    Accounting) since ...". We want the person Connor would actually talk to,
    which is the name before the paren, not the downstream one.
    """
    if not waiting_on:
        return ""
    head = re.split(r"\\s+since\\s+", waiting_on.strip(), maxsplit=1)[0]
    head = re.sub(r"\\(.*?\\)", "", head)                  # drop routed target
    head = re.split(r"\\s*(?:\\+|,| and )\\s*", head)[0]     # first of several
    head = head.strip(" -\\u2014:")
    return head if re.match(r"^[A-Z][A-Za-z.'-]+(?:\\s+[A-Z][A-Za-z.'-]+)+$", head) else ""


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
    after = datetime.datetime.combine(today, datetime.time.min)
    m, status = CW.next_shared(who, cal=cal, after=after, before=limit)
    if status == "ok":
        return " | next w/ %s: %s" % (who, m["start"].date())
    if status == "none":
        return " | next w/ %s: NONE%s" % (who, " before %s" % limit if limit else "")
    if status == "unknown":
        return " | next w/ %s: unknown" % who
    return ""


'''
s = s.replace(anchor, helper + anchor, 1)

# ---- 3. fmt() carries the annotation
old_fmt_tail = '''    if n["blocked_by"]:
        bits.append("blocked")
    return " | ".join(bits) + " | " + n["file"]'''
assert old_fmt_tail in s
new_fmt_tail = '''    if n["blocked_by"]:
        bits.append("blocked")
    return " | ".join(bits) + " | " + n["file"] + n.get("_shared", "")'''
s = s.replace(old_fmt_tail, new_fmt_tail, 1)

open(p, "w", encoding="utf-8").write(s)
print("patched")

# ---- 4. compute _shared once per run, and add the no-occasion candidate list
s = open(p, encoding="utf-8").read()

old = '''    show = notes if "--all" in args else [n for n in notes if n["status"] in LIVE]
    counts = {}'''
new = '''    show = notes if "--all" in args else [n for n in notes if n["status"] in LIVE]
    # Compute the shared-meeting answer once per note (each call may read the
    # Office xlsx, so don't do it inside fmt()).
    _cal = CW.load(root) if CW else None
    no_occasion = []
    for n in notes:
        n["_shared"] = shared_meeting_note(n, today, _cal)
        if "NONE" in n["_shared"]:
            no_occasion.append("%s%s" % (n["file"], n["_shared"].replace(" | ", " — ", 1)))
    counts = {}'''
assert old in s
s = s.replace(old, new, 1)

old_lists = '''        ("OPEN CLOSURE CANDIDATES (awaiting Connor confirm/dismiss)", candidates, "not auto-closable"),'''
new_lists = '''        ("OPEN CLOSURE CANDIDATES (awaiting Connor confirm/dismiss)", candidates, "not auto-closable"),
        ("WAITING-ON WITH NO SHARED OCCASION (before needs_by/deadline)", no_occasion,
         "computed from Trackers/Calendar-Window.md -- there is no meeting to raise these at, so do not write one into a note. If the wait has to end, the channel is text then call (see connor-works-remotely). 'unknown' means the name could not be resolved and is NOT the same as 'none'"),'''
assert old_lists in s
s = s.replace(old_lists, new_lists, 1)
open(p, "w", encoding="utf-8").write(s)
print("patched part 2")
