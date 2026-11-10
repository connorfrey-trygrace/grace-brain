#!/usr/bin/env python3
"""
pending-drafts-check.py — finds drafts awaiting Connor's clearance that have gone
stale, so a held-for-approval draft can't die silently the way the 2026-07-29 Boot
Camp Summer Camp invite did: drafted 6/25, never surfaced again, the event died at
T-1 on 7/28 with nobody ever having been invited.

Built 2026-09-15 as the "approval-pending nudge" named in
[[Trackers/Actions/Connor - Fix internal escalation — flagged findings and parked drafts don't reach Connor]]
— candidate direction #2, called out there as "the single highest-value piece and
the cheapest to build." Direction #1 (a delivery channel for flagged items) is
judged already solved by grace-quick-refresh's move to on-demand, Start-Here-first
reporting — see that item's 2026-09-15 closing entry. Direction #3
(trigger-liveness checking on On Hold items) is out of scope here; left for its
own item if it's ever picked up.

WHAT COUNTS AS A PENDING DRAFT
Frontmatter `tags:` includes `draft` — single-line `tags: [a, draft]` or a
multi-line `- draft` list item, both forms already in live use (see
Archive/2026-07-19-World-Cup/2026-07-19-World-Cup-Form-Submission-Draft.md and
Events/2026-07-29-Boot-Camp/*-Invite-Draft.md). This script reads the tag
convention that's already there; it does not invent a new one.

Deliberately NOT a free-text scan for "NOT SUBMITTED" / "NOT SENT" in the body —
tried first, and it was worse than useless: it hit the Weekly Synthesis notes
that merely *discuss* this convention, and Actions notes whose Status prose
happens to say "not sent" about something unrelated to a held draft (e.g. "not
sent [yet], waiting on a sample from Vacca"). Every genuine draft artifact in
this vault already tags itself `draft` — that is the one unambiguous signal,
and prose is not.

STALENESS
Age = days since the file's mtime. The same approximation calendar-window.py's
--check and the Phone-Index watchlist re-resolution pass already use for "has
this gone stale" — there is no `drafted:` date field in the existing convention
to key off instead, and retrofitting one onto every past draft is not this
script's job. A file whose *content* hasn't changed in N days is, by definition,
a draft nobody has touched in N days — which is exactly the signal this needs.

USAGE
  python3 "Workflows/pending-drafts-check.py"              # report, default 5-day threshold
  python3 "Workflows/pending-drafts-check.py" --days 7     # override threshold
  python3 "Workflows/pending-drafts-check.py" --json       # machine-readable, for a sweep to consume

EXCLUDED
/Archive, /Logs, /Changelog, /Raw From Grace, /.git, /.obsidian — a draft that
was actually resolved (approved, submitted, or explicitly cancelled/superseded)
belongs in /Archive per the vault's standing "never delete, archive instead"
rule. Anything this script finds outside /Archive is, by the vault's own filing
convention, still live — so a hit here means either a genuine pending clearance
or a housekeeping miss (resolved content that was never moved). Both are worth
one line to Connor; this script doesn't try to tell them apart.

Detection only — same split as query-messages.py / resolve-phone.py. This script
never writes to the vault; minting or updating a flagged Actions item is the
sweep's call.
"""
import os
import re
import sys
import json
import datetime

EXCLUDE_DIRS = {"Archive", "Logs", "Changelog", "Raw From Grace", ".git", ".obsidian"}
DEFAULT_STALE_DAYS = 5

TAGS_INLINE_RE = re.compile(r"^tags:\s*\[([^\]]*)\]", re.IGNORECASE | re.MULTILINE)
TAGS_LISTITEM_RE = re.compile(r"^\s*-\s*[\"']?draft[\"']?\s*$", re.IGNORECASE | re.MULTILINE)


def vault_root():
    d = os.path.abspath(".")
    while d != "/":
        if os.path.isdir(os.path.join(d, "Trackers", "Actions")):
            return d
        d = os.path.dirname(d)
    sys.exit("error: run from inside the vault (no Trackers/Actions found above cwd)")


def split_frontmatter(text):
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[:end], text[end + 4:]


def is_pending_draft(text):
    fm, _body = split_frontmatter(text)
    m = TAGS_INLINE_RE.search(fm)
    if m and "draft" in [t.strip().strip("\"'").lower() for t in m.group(1).split(",")]:
        return True
    return bool(TAGS_LISTITEM_RE.search(fm))


def scan(root, stale_days):
    now = datetime.datetime.now()
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                continue
            if not is_pending_draft(text):
                continue
            age_days = (now - datetime.datetime.fromtimestamp(os.path.getmtime(path))).days
            if age_days >= stale_days:
                findings.append({"path": os.path.relpath(path, root), "age_days": age_days})
    findings.sort(key=lambda f: -f["age_days"])
    return findings


def main():
    args = sys.argv[1:]
    stale_days = DEFAULT_STALE_DAYS
    as_json = False
    i = 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            stale_days = int(args[i + 1])
            i += 2
        elif args[i] == "--json":
            as_json = True
            i += 1
        else:
            sys.exit(f"unknown arg: {args[i]}")

    root = vault_root()
    findings = scan(root, stale_days)

    if as_json:
        print(json.dumps(findings, indent=2))
        return

    if not findings:
        print(f"# Pending-drafts check — no draft older than {stale_days} days. OK")
        return

    print(f"# Pending-drafts check — {len(findings)} draft(s) >= {stale_days} days old, still outside /Archive")
    for f in findings:
        print(f"  {f['age_days']:>3}d  {f['path']}")


if __name__ == "__main__":
    main()
