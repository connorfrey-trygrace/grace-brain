import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()

old = '''    head = head.strip(" -\\u2014:")
    return head if re.match(r"^[A-Z][A-Za-z.'-]+(?:\\s+[A-Z][A-Za-z.'-]+)+$", head) else ""'''
new = '''    head = head.strip(" -\\u2014:")
    # A single capitalized first name is a real convention here (Skylar, Alex), so
    # accept it. It will usually resolve to 'unknown' downstream -- which is the
    # honest answer and strictly better than printing nothing, because nothing
    # reads as "no wait to compute" rather than "I could not identify this person".
    return head if re.match(r"^[A-Z][A-Za-z.'-]+(?:\\s+[A-Z][A-Za-z.'-]+)*$", head) else ""'''
assert old in s, "awaited_party regex not found"
s = s.replace(old, new, 1)

old2 = '''    limit = first_date(n["needs_by"]) or first_date(n["deadline"])
    after = datetime.datetime.combine(today, datetime.time.min)
    m, status = CW.next_shared(who, cal=cal, after=after, before=limit)
    if status == "ok":
        return " | next w/ %s: %s" % (who, m["start"].date())
    if status == "none":
        return " | next w/ %s: NONE%s" % (who, " before %s" % limit if limit else "")'''
new2 = '''    limit = first_date(n["needs_by"]) or first_date(n["deadline"])
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
    if status == "ok":
        return " | next w/ %s: %s%s" % (who, m["start"].date(),
                                        " (its own date already passed)" if blown else "")
    if status == "none":
        return " | next w/ %s: NONE%s" % (who, " before %s" % limit if limit else " in the window")'''
assert old2 in s, "shared_meeting_note body not found"
s = s.replace(old2, new2, 1)
open(p, "w", encoding="utf-8").write(s)
print("patch2 applied")
