#!/usr/bin/env python3
"""
resolve-phone.py — canonical number->name resolver for the text-message sync.

WHY THIS EXISTS
Contact resolution used to be done by ad-hoc grep for the number as formatted in
the Phone-Index (e.g. "434-996-6618"). Two defects made that silently unreliable:

  1. FORMAT BLINDNESS. The macOS vCard export stores TEL values in mixed formats
     ("(434) 996-6618", "+1 (571) 641-1084", "1 (717) 989-3315", "973-670-0581",
     "+14108043644"). A literal grep for the dashed form misses every parenthesised
     entry. Measured 2026-07-28: 334 of 631 TEL entries (52%), 328 distinct people,
     were unreachable this way — including Jake Lindo, who sat "unknown" on the
     watchlist for two scans while his card was in the file the whole time.

  2. MALFORMED EXPORT. 219 of 640 TEL lines (34%) are missing the CRLF before the
     next property, so the value runs into it:
         TEL;type=pref:732-379-8679CATEGORIES:Imported on 6/22
     Taking the LAST 10 digits of that yields 379-867-9622 — a number that does not
     exist. 218 entries are affected. This defect is worse than a miss: it produces
     a confident WRONG match. Always truncate the TEL value at the first embedded
     property name before extracting digits.

  3. PHANTOM NUMBERS (added 2026-08-10). A number can reach the watchlist without
     ever having existed: 571-344-1742 sat there from 2026-07-10 to 2026-08-10 and
     survived TEN re-resolution passes, but chat.db has no such handle -- the real
     handle was +17033441742 (Liz Goodiel) and a prior run transcribed the area
     code wrong, most likely off the 571-3xx handles sharing that group chat.
     Every pass then dutifully reported it "genuinely absent from every source",
     which was true and useless. A number that is not a handle in chat.db cannot
     be an unidentified texter, so it is now checked and labelled PHANTOM.

USAGE
    python3 resolve-phone.py 434-996-6618 "(704) 956-4975" +12402941234 ...
    python3 resolve-phone.py --audit          # health report on the vCard export

Every queried number is also checked against chat.db's handle table (defect 3).
Sources this script CANNOT reach, which the workflow must cover by hand:
  * Rock (trygrace.rockcloud.com) -- person-search by Phone. There is no Rock
    connector; use Claude in Chrome. This is the ONLY source that covers Grace
    visitors/attendees, who are by definition absent from Connor's own contacts.
    202-294-5417 (Nathan Wilkens) was resolved this way 2026-08-10 after the
    vCard structurally could not have held him.

Any input format works; everything is compared on last-10-digits.
Exit code 1 if any queried number went unresolved.
"""

import glob
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUNK = re.compile(r"[A-Za-z]{2,}[;:]")  # embedded next-property, per defect #2


def digits(value):
    """Last 10 digits of a TEL value, after stripping any run-on property."""
    value = JUNK.split(value)[0]
    d = re.sub(r"\D", "", value)
    return d[-10:] if len(d) >= 10 else None


def newest_vcf():
    cards = glob.glob(os.path.join(VAULT, "Contacts", "*.vcf"))
    return max(cards, key=os.path.getmtime) if cards else None


def load_vcf(path):
    """{last10: name} from a vCard export. Unfolds RFC-6350 line folding first."""
    raw = open(path, errors="replace").read()
    raw = re.sub(r"\r?\n[ \t]", "", raw)
    out = {}
    for card in raw.split("BEGIN:VCARD"):
        fn = re.search(r"^FN:(.*)$", card, re.M)
        if not fn:
            continue
        name = fn.group(1).strip()
        for tel in re.findall(r"^TEL[^:]*:(.*)$", card, re.M):
            d = digits(tel)
            if d:
                out.setdefault(d, name)
    return out


def load_phone_index():
    """{last10: name} from the Phone-Index '## Confirmed' table ONLY.

    The '## Unconfirmed / inferred' watchlist must never be read as a source: its
    rows are open questions, not answers. Reading the whole file made the resolver
    self-confirming — every watchlist number 'resolved' to its own watchlist row.
    """
    path = os.path.join(VAULT, "Contacts", "Phone-Index.md")
    if not os.path.exists(path):
        return {}
    out, section = {}, None
    for line in open(path, errors="replace"):
        if line.startswith("## "):
            section = line.strip()
            continue
        if section != "## Confirmed" or not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 2 or cols[0].startswith(("-", "Phone")):
            continue
        d = digits(cols[0])
        if d:
            out.setdefault(d, cols[1].replace("**", ""))
    return out


def load_phone_property():
    """{last10: note title} for vault notes carrying a `phone:` frontmatter field.

    Added to the workflow 2026-07-17 after the Brandon Brys miss. Only frontmatter
    counts — a number merely *mentioned* in a note's body is a mention, not a name.
    """
    out = {}
    for path in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, VAULT)
        if rel.startswith(("Archive", "Raw From Grace")):
            continue
        head = open(path, errors="replace").read(2000)
        fm = re.match(r"---\n(.*?)\n---", head, re.S)
        if not fm:
            continue
        for m in re.finditer(r"^phone:\s*(.+)$", fm.group(1), re.M):
            d = digits(m.group(1))
            if d:
                out.setdefault(d, os.path.splitext(os.path.basename(path))[0])
    return out


def load_mentions():
    """{last10: 'file — line'} anywhere in the vault. CONTEXT ONLY, never a name.

    Kept separate and reported as a mention so a number that only appears inside
    the text-sync's own run notes is not mistaken for an identification.
    """
    out = {}
    for path in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, VAULT)
        if rel.startswith(("Archive", "Raw From Grace")) or rel.endswith("Phone-Index.md"):
            continue
        for line in open(path, errors="replace"):
            for m in re.finditer(r"\+?\d[\d\-\.\(\)\s]{8,}\d", line):
                d = digits(m.group(0))
                if d:
                    out.setdefault(d, f"{rel} — {line.strip()[:100]}")
    return out


def find_chat_db():
    """Locate the Messages database. The mount tail is NOT stable across sessions
    (observed: mnt/Messages, mnt/Library--Messages, mnt/connorfrey--Library--Messages),
    so never match a literal name -- glob for the file and exclude the
    System--Library--Messages mount, which holds app resources and no chat.db."""
    for pattern in (
        os.path.expanduser("~/Library/Messages/chat.db"),
        "/sessions/*/mnt/*/chat.db",
    ):
        for hit in sorted(glob.glob(pattern)):
            if "System--Library" in hit:
                continue
            if os.path.exists(hit):
                return hit
    return None


def load_handles():
    """{last10} -- every phone handle that actually appears in chat.db.

    Membership here is what makes a number REAL. Absence means no such texter
    exists, i.e. the number was mistyped or invented upstream (defect 3).
    Returns None (not an empty set) when chat.db is unreachable, so a missing
    mount is never mistaken for 'this number is fake'.
    """
    path = find_chat_db()
    if not path:
        return None
    import sqlite3, shutil, tempfile
    # 2026-08-20 FIX: this opened the db with immutable=1, which tells SQLite to
    # ignore the -wal file. Recent messages live in the WAL until a checkpoint,
    # so any number Connor first texted in the last few minutes/hours was
    # invisible here -- and absence from `handle` is what produces the PHANTOM
    # verdict. Measured failure: 617-460-3994 (Victoria Nayiga, first texted
    # 2026-08-20 12:57 ET) came back PHANTOM while handle 2746 plainly existed.
    # Since the workflow says PHANTOM -> "do not re-resolve; correct or drop it,"
    # the defect actively discarded a live, correct, Grace-relevant number.
    # Same root cause the text-sync workflow retired on 2026-08-17; the resolver
    # never got the same fix. Copy db + -wal + -shm to a scratch dir and open
    # the copy read-write so the WAL is replayed.
    tmp = None
    try:
        tmp = tempfile.mkdtemp(prefix="resolvephone-")
        local = os.path.join(tmp, "chat.db")
        shutil.copy2(path, local)
        for ext in ("-wal", "-shm"):
            side = path + ext
            if os.path.exists(side):
                try:
                    shutil.copy2(side, local + ext)
                except OSError:
                    pass
        con = sqlite3.connect(local)
        out = set()
        for (ident,) in con.execute("select id from handle"):
            d = digits(ident or "")
            if d:
                out.add(d)
        con.close()
        return out
    except (sqlite3.Error, OSError, shutil.Error):
        return None
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def load_office():
    """{last10: name} from the canonical Office staff list (authority wins)."""
    out = {}
    # NB: never hardcode a /sessions/<name>/ path -- the session slug changes every
    # run. This previously pointed at a dead session and silently returned {}.
    bases = ["/Users/connorfrey/Library/CloudStorage/Dropbox/Office"]
    bases += sorted(glob.glob("/sessions/*/mnt/Office"))
    for base in bases:
        xlsx = os.path.join(base, "Staff Contact List.xlsx")
        if not os.path.exists(xlsx):
            continue
        try:
            import openpyxl
        except ImportError:
            return out
        wb = openpyxl.load_workbook(xlsx, data_only=True)
        for ws in wb:
            for row in ws.iter_rows(values_only=True):
                cells = [str(c) for c in row if c is not None]
                nums = [d for d in (digits(c) for c in cells) if d]
                if nums and cells:
                    out.setdefault(nums[0], cells[0])
        break
    return out


def audit(vcf_path):
    raw = open(vcf_path, errors="replace").read()
    tels = re.findall(r"^TEL[^:]*:(.*)$", raw, re.M)
    junk = [t for t in tels if JUNK.search(t)]
    unreachable = 0
    for t in tels:
        d = digits(t)
        if not d:
            continue
        variants = [f"{d[:3]}-{d[3:6]}-{d[6:]}", d, f"+1{d}"]
        if not any(v in raw for v in variants):
            unreachable += 1
    print(f"vCard: {os.path.basename(vcf_path)}")
    print(f"  TEL lines                              {len(tels)}")
    print(f"  malformed (run-on property, defect 2)  {len(junk)}"
          f"  ({len(junk) * 100 // max(len(tels), 1)}%)")
    print(f"  invisible to literal grep (defect 1)   {unreachable}"
          f"  ({unreachable * 100 // max(len(tels), 1)}%)")
    print(f"  resolvable by this script              {len(load_vcf(vcf_path))} unique numbers")


def main():
    args = sys.argv[1:]
    vcf = newest_vcf()
    if not args or args[0] == "--audit":
        if not vcf:
            sys.exit("no *.vcf in Contacts/")
        audit(vcf)
        return

    # Authority order per Phone-Index: Office list wins, then the index cache,
    # then vCard, then phone:-property notes. Mentions are reported, never trusted.
    sources = [
        ("Office Staff Contact List", load_office()),
        ("Phone-Index (Confirmed)", load_phone_index()),
        ("phone: property note", load_phone_property()),
    ]
    if vcf:
        sources.insert(2, (f"vCard ({os.path.basename(vcf)})", load_vcf(vcf)))
    mentions = load_mentions()
    handles = load_handles()
    if handles is None:
        print("note: chat.db unreachable -- phantom check SKIPPED this run\n")

    missing = False
    phantoms = []
    for arg in args:
        d = digits(arg)
        if not d:
            print(f"{arg:18} SKIP — not a 10-digit number")
            continue
        pretty = f"{d[:3]}-{d[3:6]}-{d[6:]}"
        real = None if handles is None else (d in handles)
        for label, table in sources:
            if d in table:
                print(f"{pretty}  {table[d][:60]:60}  [{label}]")
                if real is False:
                    print(f"{'':14}  note: named, but no handle in chat.db "
                          f"(fine for an email/Rock/roster contact who has never texted)")
                break
        else:
            if real is False:
                print(f"{pretty}  ⚠️  PHANTOM — no such handle in chat.db; this number never "
                      f"texted Connor.\n{'':14}  Do NOT keep re-resolving it. Find the run that "
                      f"introduced it and correct the digits, or drop it.")
                phantoms.append(pretty)
                continue
            hint = mentions.get(d)
            print(f"{pretty}  UNRESOLVED — keep on watchlist"
                  + (f"\n{'':14}  mention only (NOT a name): {hint}" if hint else "")
                  + f"\n{'':14}  next: Rock person-search by Phone (Claude in Chrome) — the "
                    f"only source covering visitors/attendees.")
            missing = True
    if phantoms:
        print(f"\n{len(phantoms)} phantom number(s): {', '.join(phantoms)}")
    sys.exit(1 if (missing or phantoms) else 0)


if __name__ == "__main__":
    main()
