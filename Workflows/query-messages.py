#!/usr/bin/env python3
"""The ONLY sanctioned way to read chat.db. Nothing else may open it — not the scan,
not a probe, not a spot check, and NOT a verification pass.

WHY THIS EXISTS (2026-08-28). The Sky 1:1 exclusion has been a prose rule since the
workflow was written, and it was strengthened in prose on 2026-08-17 after a probe query
returned excluded bodies ("this applies to EVERY query ... including the cheap probe").
On 2026-08-28 it failed again, in the one place the prose did not name: the refresh's
subagent applied the exclusion correctly at SQL level, and then the parent agent ran its
own verification query to double-check the subagent's work — with no exclusion — and
decoded 6 messages from the 1:1 thread. Nothing was recorded, but reading is the breach.

The lesson is the same one clock-check.py taught (see Changelog/2026-08-21-clock-enforced-in-code):
a third prose rule would have been the third prose rule. The exclusion has to live in the
only code path that can reach the data, so that omitting it is not an option a future run
has. Every subcommand below applies it before a single body is decoded; there is no
subcommand that takes arbitrary SQL, deliberately.

USAGE
  python3 "Workflows/query-messages.py" probe
        counts only, no text columns selected. Answers "is anything new?"
  python3 "Workflows/query-messages.py" scan --since-rowid 192338
        the real pass: decoded bodies, excluded threads already gone.
  python3 "Workflows/query-messages.py" verify --rowids 192342,192344
        re-read named rows for a double-check. SAME exclusion. This subcommand exists
        so that "let me just check that myself" has a guarded path to take.
  python3 "Workflows/query-messages.py" self-test
        proves the guard works by measurement: runs the excluded query both ways and
        reports the delta. Non-zero exit if the guard leaks.

Excluded threads are defined once, in EXCLUDED_HANDLES below, matched on the last 10
digits. 1:1 threads only — group chats that include an excluded person are in scope, per
Connor. See Workflows/text-message-sync.md § Excluded contacts.
"""

import argparse, glob, os, re, shutil, sqlite3, sys, tempfile, datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

# --- the guard. One definition, applied by every code path in this file. ---
EXCLUDED_HANDLES = ["9087980030"]        # Sky — 1:1 / direct thread only

# GLOB, NEVER HARDCODE (2026-08-31). This list was three literal paths, and on
# 2026-08-31 the session mounted the Messages folder as "Library--Messages" rather than
# "connorfrey--Library--Messages" — none of the three matched, self-test exited, and the
# whole text phase would have read empty. text-message-sync.md § Source & access rule 1
# has said "glob for the mount, never hardcode it — this has been wrong three times for
# naming a literal path" since it was written; this file was the fourth time. So the glob
# now lives in the code path instead of in the prose telling the code what to do.
# A "System--Library--Messages" hit is the wrong mount (no chat.db) — the existence check
# below is what rejects it, so patterns may be generous.
DB_GLOBS = [
    os.path.expanduser("~/mnt/*Library--Messages/chat.db"),
    os.path.expanduser("~/mnt/*Messages*/chat.db"),
    os.path.expanduser("~/Library/Messages/chat.db"),
]


def _db_path():
    seen = []
    for pattern in DB_GLOBS:
        for p in sorted(glob.glob(pattern)):
            seen.append(p)
            if os.path.exists(p):
                return p
    sys.exit(
        "chat.db not found. Globs tried: " + ", ".join(DB_GLOBS)
        + (" | candidates seen: " + ", ".join(seen) if seen else " | no candidates matched")
    )


def _open():
    """Copy db + wal + shm to a temp dir and open the copy (never the live file)."""
    src = _db_path()
    tmp = tempfile.mkdtemp(prefix="msgq-")
    for suffix in ("", "-wal", "-shm"):
        s = src + suffix
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(tmp, "chat.db" + suffix))
    return sqlite3.connect(os.path.join(tmp, "chat.db")), tmp


NORM = "substr(replace(replace(replace(replace({c},'+',''),'-',''),' ',''),'()',''), -10)"


def _excluded_chat_ids(cur):
    """chat_ids of 1:1 threads with an excluded handle.

    ⚠️ The 1:1 test counts EVERY handle in the chat, not just the matching one. The first
    version of this function put the match in the WHERE and the count in a HAVING, so the
    count only ever saw the one filtered row and every group chat containing the excluded
    person came back as 1:1. self-test caught it: 89 chats excluded instead of 1, which
    would have silently dropped Grace group threads the workflow says are in scope.
    Over-exclusion is a data-loss bug, not a safe direction to err in.
    """
    ids = set()
    for last10 in EXCLUDED_HANDLES:
        rows = cur.execute(f"""
            SELECT DISTINCT chj.chat_id
            FROM chat_handle_join chj
            JOIN handle h ON h.ROWID = chj.handle_id
            WHERE {NORM.format(c='h.id')} = ?
              AND (SELECT COUNT(DISTINCT handle_id) FROM chat_handle_join
                   WHERE chat_id = chj.chat_id) = 1
        """, (last10,)).fetchall()
        ids.update(r[0] for r in rows)
    return ids


def _guarded_where(excluded_ids):
    """SQL removing excluded threads. Two clauses, and both are load-bearing:

    1. chat_id NOT IN (excluded 1:1 threads) — the real guard.
    2. an orphan row (no chat_message_join) whose handle is an excluded person is dropped
       too. Without this, a message that lost its chat join would bypass clause 1.
    """
    if excluded_ids:
        chat_clause = "(cmj.chat_id IS NULL OR cmj.chat_id NOT IN (%s))" % ",".join(
            str(i) for i in sorted(excluded_ids))
    else:
        chat_clause = "1=1"
    orphan = " AND ".join(
        "NOT (cmj.chat_id IS NULL AND h.id IS NOT NULL AND %s = '%s')" % (NORM.format(c='h.id'), lh)
        for lh in EXCLUDED_HANDLES) or "1=1"
    return "(%s) AND (%s)" % (chat_clause, orphan)


def _decode(text, ab):
    if text:
        return text
    if not ab:
        return ""
    s = ab.decode("utf-8", errors="ignore")
    m = re.search(r"streamtyped.*?NSString.{0,8}?\+(.*?)\x02i", s, re.S)
    if not m:
        m = re.search(r"streamtyped.*?\+(.*?)\x02i", s, re.S)
    body = m.group(1) if m else s
    return re.sub(r"^[\x00-\x1f]+", "", body)[:2000]


def _ts(apple_ns):
    return (datetime.datetime(2001, 1, 1, tzinfo=datetime.timezone.utc)
            + datetime.timedelta(seconds=apple_ns / 1e9)).astimezone(ET)


def _rows(cur, where_extra, params, with_text):
    excluded = _excluded_chat_ids(cur)
    guard = _guarded_where(excluded)
    cols = "m.ROWID, m.is_from_me, m.date, cmj.chat_id, h.id"
    if with_text:
        cols += ", m.text, m.attributedBody"
    q = f"""SELECT {cols}
            FROM message m
            LEFT JOIN handle h ON m.handle_id = h.ROWID
            LEFT JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            WHERE ({guard}) AND ({where_extra})
            ORDER BY m.ROWID"""
    return excluded, cur.execute(q, params).fetchall()


def cmd_probe(args):
    con, tmp = _open(); cur = con.cursor()
    excluded, rows = _rows(cur, "m.ROWID > ?", (args.since_rowid,), with_text=False)
    mx = cur.execute("SELECT MAX(ROWID) FROM message").fetchone()[0]
    print(f"guard: {len(excluded)} excluded 1:1 thread(s) — chat_id {sorted(excluded)}")
    print(f"new since ROWID {args.since_rowid}: {len(rows)} in scope; db max ROWID {mx}")
    shutil.rmtree(tmp, ignore_errors=True)


def cmd_scan(args):
    con, tmp = _open(); cur = con.cursor()
    excluded, rows = _rows(cur, "m.ROWID > ?", (args.since_rowid,), with_text=True)
    mx = cur.execute("SELECT MAX(ROWID) FROM message").fetchone()[0]
    print(f"# guard: excluded 1:1 chat_id {sorted(excluded)} | in scope {len(rows)} | db max ROWID {mx}")
    for rid, fm, d, cid, hid, text, ab in rows:
        print(f"[{rid}] chat{cid} {hid} {'ME' if fm else 'THEM'} {_ts(d):%Y-%m-%d %H:%M} :: {_decode(text, ab)!r}")
    shutil.rmtree(tmp, ignore_errors=True)


def cmd_verify(args):
    ids = [int(x) for x in args.rowids.split(",") if x.strip()]
    con, tmp = _open(); cur = con.cursor()
    ph = ",".join("?" * len(ids))
    excluded, rows = _rows(cur, f"m.ROWID IN ({ph})", tuple(ids), with_text=True)
    got = {r[0] for r in rows}
    print(f"# guard: excluded 1:1 chat_id {sorted(excluded)}")
    for rid in ids:
        if rid not in got:
            print(f"[{rid}] WITHHELD — excluded thread, or no such row. Not readable by any path in this file.")
    for rid, fm, d, cid, hid, text, ab in rows:
        print(f"[{rid}] chat{cid} {hid} {'ME' if fm else 'THEM'} {_ts(d):%Y-%m-%d %H:%M} :: {_decode(text, ab)!r}")
    shutil.rmtree(tmp, ignore_errors=True)


def cmd_self_test(args):
    """Measure the guard instead of asserting it in prose."""
    con, tmp = _open(); cur = con.cursor()
    excluded = _excluded_chat_ids(cur)
    ok = True
    if not excluded:
        print("FAIL: no excluded 1:1 thread resolved — the guard has nothing to exclude.")
        ok = False
    else:
        raw = cur.execute("SELECT COUNT(*) FROM chat_message_join WHERE chat_id IN (%s)"
                          % ",".join(str(i) for i in excluded)).fetchone()[0]
        _, guarded = _rows(cur, "1=1", (), with_text=False)
        leaked = [r for r in guarded if r[3] in excluded]
        print(f"excluded 1:1 chat_id {sorted(excluded)}: {raw} messages exist, {len(leaked)} returned through the guard")
        if leaked:
            print("FAIL: the guard leaked."); ok = False
        # a group chat containing the excluded handle must still be in scope.
        # Over-exclusion is the failure this half catches, and it has already happened once.
        grp = cur.execute(f"""
            SELECT chj.chat_id FROM chat_handle_join chj JOIN handle h ON h.ROWID=chj.handle_id
            WHERE {NORM.format(c='h.id')} = ?
              AND (SELECT COUNT(DISTINCT handle_id) FROM chat_handle_join
                   WHERE chat_id = chj.chat_id) > 1
            LIMIT 1
        """, (EXCLUDED_HANDLES[0],)).fetchone()
        if grp:
            in_scope = grp[0] not in excluded
            print(f"group chat {grp[0]} (includes the excluded handle): {'in scope OK' if in_scope else 'WRONGLY EXCLUDED - over-exclusion'}")
            if not in_scope: ok = False
        else:
            print("no group chat with the excluded handle to test over-exclusion against")
    shutil.rmtree(tmp, ignore_errors=True)
    print("✅ guard holds" if ok else "❌ guard does not hold")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("probe"); p.add_argument("--since-rowid", type=int, default=0); p.set_defaults(fn=cmd_probe)
    p = sub.add_parser("scan"); p.add_argument("--since-rowid", type=int, required=True); p.set_defaults(fn=cmd_scan)
    p = sub.add_parser("verify"); p.add_argument("--rowids", required=True); p.set_defaults(fn=cmd_verify)
    p = sub.add_parser("self-test"); p.set_defaults(fn=cmd_self_test)
    a = ap.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
