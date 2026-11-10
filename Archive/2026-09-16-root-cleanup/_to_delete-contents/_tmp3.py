#!/usr/bin/env python3
"""
split-note-log.py — move a note's append-only dated history into a companion
`-Log.md`, leaving a live note that is cheap to read on every run.

Created 2026-08-17 at Connor's request, generalising a pattern the vault had
already invented three separate times by hand:
  - 2026-08-11  event plan note  -> `<Event>-Log.md`   (Launch.md was 93 KB, 78% history)
  - 2026-08-12  workflow file    -> `/Logs/<job>-run-log.md`
  - 2026-08-12  workflow file    -> `/Changelog/<date>-<slug>.md`
The rule underneath all three: A NOTE THAT IS READ ON EVERY RUN MUST NOT CARRY
ITS OWN APPEND-ONLY HISTORY. Action notes were the one class still violating it.

WHY A SCRIPT AND NOT A PROCEDURE STEP: doing this by hand is where the risk is.
The dated history in an action note is *interleaved* with structural bullets
(`- **Blocked by**:`, `- **Status**:`, rationale bullets) rather than parked in
one contiguous block, so "move everything after the last structural bullet"
silently eats live fields. The classifier below is the whole point of the file.

USAGE
  python3 "Workflows/split-note-log.py" --dry-run "<path/to/note.md>"   # show the plan
  python3 "Workflows/split-note-log.py" "<path/to/note.md>"             # write it
  python3 "Workflows/split-note-log.py" --scan                          # list candidates vault-wide
  python3 "Workflows/split-note-log.py" --keep 3 "<path>"               # retain N newest blocks (default 2)

DEFAULT KEEP = 2 IS NOT ARBITRARY. actions-index.py `evidence()` emits the last
2 dated lines of a note so a sweep can clear most candidates without opening the
body at all. Keeping fewer than 2 in the live note would break that cheap path
and force the full read the split exists to avoid.
"""
import os, re, sys, glob, datetime

BLOAT_KB = 15
KEEP_DEFAULT = 2

# A dated block: `### 2026-08-12 (email)` / `## 2026-08-17 — ...` /
# `- **2026-08-11 (email sync) — ...**` / `- **⛓️‍💥 2026-08-11 ...**`
DATED_HEAD = re.compile(r"^#{2,4}\s+.{0,40}?\d{4}-\d{2}-\d{2}")
DATED_BULLET = re.compile(r"^-\s+(~~)?\*\*\s*(?:[^\w\s]+\s*)*\d{4}-\d{2}-\d{2}")
HEAD = re.compile(r"^#{1,6}\s")
TOP_BULLET = re.compile(r"^-\s")

# Structural bullets are the note's LIVE STATE and never move, even though they
# sit between dated blocks. This list is why the split can't be a regex one-liner.
STRUCTURAL = re.compile(
    r"^-\s+(\[[ x]\]\s*)?\*\*("
    r"Priority|Source|Added|Deadline|Needs-by|Needs by|Chase-by|Chase by|Status|Owner|"
    r"Context|Notes|Last mentioned|Blocked by|Blocks|Why it matters|"
    r"Deadline rationale|Needs-by rationale|Chase-by rationale|Flagged|"
    r"Verify before closing|Closure evidence|Re-check"
    r")\*\*", re.I)


def parse_fm(text):
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    return text[:end + 4], text[end + 4:]


def classify(body):
    """Split body into ordered segments: ('live'|'dated', date_or_None, [lines]).

    A dated block ends at the next TOP-LEVEL line that is a heading or a
    structural bullet -- not merely at the next dated line. That distinction is
    the bug this function exists to prevent: in the Kay note `- **Blocked by**`
    and `- **Chase-by rationale**` sit *after* dated bullets, and a naive
    run-to-next-date would have carried both into the log and left the live note
    without its dependency edges.
    """
    lines = body.split("\n")
    segs, cur, mode, curdate = [], [], "live", None

    def flush():
        if cur:
            segs.append((mode, curdate, list(cur)))
            cur.clear()

    for ln in lines:
        is_top = bool(HEAD.match(ln) or TOP_BULLET.match(ln))
        dated = bool(DATED_HEAD.match(ln) or DATED_BULLET.match(ln))
        if dated:
            flush()
            mode, curdate = "dated", first_date(ln)
            cur.append(ln)
            continue
        if mode == "dated" and is_top and (HEAD.match(ln) or STRUCTURAL.match(ln)):
            flush()
            mode, curdate = "live", None
            cur.append(ln)
            continue
        cur.append(ln)
    flush()
    return segs


def first_date(s):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    if not m:
        return None
    try:
        return datetime.date(*(int(g) for g in m.groups()))
    except ValueError:
        return None


def plan(path, keep=KEEP_DEFAULT):
    text = open(path, encoding="utf-8").read()
    fm, body = parse_fm(text)
    segs = classify(body)
    dated_idx = [i for i, (m, _, _) in enumerate(segs) if m == "dated"]
    # Keep the NEWEST blocks by position, not by parsed date: notes are written
    # chronologically and a corrective entry often re-cites an older date in its
    # heading. Position is the honest ordering; the date is prose.
    keep_idx = set(dated_idx[-keep:]) if keep else set()
    move_idx = [i for i in dated_idx if i not in keep_idx]
    live = [seg for i, seg in enumerate(segs) if i not in set(move_idx)]
    moved = [segs[i] for i in move_idx]
    return fm, live, moved, segs


def render(segs):
    out = "\n".join("\n".join(s[2]) for s in segs)
    return re.sub(r"\n{3,}", "\n\n", out).strip() + "\n"


def log_path(path):
    """Action logs go to /Trackers/Action-Logs/, NOT alongside the note.

    This is a deliberate divergence from the event `-Log` files, which do sit
    beside their plan note. The reason is [[Trackers/Open Actions.base]]: its
    global filter is `file.inFolder("Trackers/Actions")` and its `All` and
    `By Project` views carry NO status filter, so any file dropped in that
    folder becomes a blank row in the two views Connor reads most. Excluding
    logs via a Bases filter (`type != "log"`) would be tidier, but a wrong
    filter expression blanks EVERY view over 130 action notes, and Bases
    expressions cannot be tested from outside Obsidian. A sibling folder is
    correct by construction and needs no filter, no `actions-index.py` change
    (its glob is `Trackers/Actions/*.md`), and no test. Revisit if the filter
    is ever verified in-app.
    """
    d, b = os.path.split(path)
    if os.path.basename(d) == "Actions" and os.path.basename(os.path.dirname(d)) == "Trackers":
        return os.path.join(os.path.dirname(d), "Action-Logs", b[:-3] + "-Log.md")
    return path[:-3] + "-Log.md"


def wikilink(root, path):
    return os.path.relpath(path, root)[:-3]


def do_split(path, root, keep=KEEP_DEFAULT, dry=False):
    fm, live, moved, segs = plan(path, keep)
    if not moved:
        return None
    lp = log_path(path)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    name = os.path.basename(path)[:-3]
    live_txt = fm + "\n" + render(live)
    pointer = (
        "\n---\n\n"
        "> 📓 **Earlier history: [[%s]]** — %d dated entries moved there %s so this note "
        "stays cheap to read on every sync run. **Not read on a normal run.** The %d newest "
        "entries are kept below; anything that changes *current* state still gets folded into "
        "the fields and bullets above, not left only in the log.\n"
        % (wikilink(root, lp), len(moved), datetime.date.today().isoformat(), keep))
    # Pointer goes directly under the frontmatter+title so a reader hits it before
    # the body, and an appending writer sees it before deciding where to append.
    m = re.search(r"^(#\s.*\n)", live_txt, re.M)
    live_txt = (live_txt[:m.end()] + pointer + live_txt[m.end():]) if m else live_txt + pointer

    existing = open(lp, encoding="utf-8").read() if os.path.exists(lp) else None
    if existing:
        log_txt = existing.rstrip() + "\n\n" + render(moved)
    else:
        log_txt = (
            "---\ntype: log\nsource_note: \"[[%s]]\"\ntags: [log]\n---\n\n"
            "# %s — History Log\n\n"
            "Append-only history, split out of [[%s]] on **%s** so the live note stays cheap "
            "to read on every run (it was %d KB, and every sync that appended one line read all "
            "of it). Same pattern as the 2026-08-11 event-note split.\n\n"
            "**This file is not read during a normal run** — only when auditing or reconstructing "
            "how a decision was reached. Entries are **oldest-first**; append new history at the "
            "bottom. *(This is a deliberate divergence from the newest-first event `-Log` files: "
            "action notes have always been appended chronologically at the bottom, and flipping "
            "the order would guarantee mis-ordered appends by any writer following the habit.)*\n\n"
            "---\n\n%s"
            % (wikilink(root, path), name, wikilink(root, path),
               datetime.date.today().isoformat(), os.path.getsize(path) // 1024, render(moved)))
    if dry:
        return (lp, len(moved), len(live_txt), len(log_txt))
    open(path, "w", encoding="utf-8").write(live_txt)
    open(lp, "w", encoding="utf-8").write(log_txt)
    return (lp, len(moved), len(live_txt), len(log_txt))


def vault_root():
    d = os.path.abspath(".")
    while d != "/":
        if os.path.isdir(os.path.join(d, "Trackers", "Actions")):
            return d
        d = os.path.dirname(d)
    sys.exit("error: run from inside the vault")


def scan(root):
    """Candidates only. Deliberately narrow -- see the convention note in CLAUDE.md.

    Data caches (Contacts/Phone-Index), rosters (People/Good Noodles), inventories
    (Trackers/Automation) and Synthesis notes are NOT candidates however big they
    get: their size is current-state or they ARE the history. Workflow files are
    already split (run logs -> /Logs, changelogs -> /Changelog).
    """
    pats = ["Trackers/Actions/*.md", "Events/*/*.md"]  # Action-Logs/ is a sibling folder, never scanned
    rows = []
    for pat in pats:
        for p in sorted(glob.glob(os.path.join(root, pat))):
            if p.endswith("-Log.md"):
                continue
            sz = os.path.getsize(p)
            if sz <= BLOAT_KB * 1024:
                continue
            _, live, moved, _ = plan(p)
            rows.append((sz, p, len(moved), len(render(live))))
    for sz, p, nmoved, livesz in sorted(rows, reverse=True):
        print("%6d KB -> %5d KB live | %2d blocks movable | %s"
              % (sz // 1024, livesz // 1024, nmoved, os.path.relpath(p, root)))
    if not rows:
        print("  (no candidates over %d KB)" % BLOAT_KB)


if __name__ == "__main__":
    a = sys.argv[1:]
    root = vault_root()
    keep = int(a[a.index("--keep") + 1]) if "--keep" in a else KEEP_DEFAULT
    dry = "--dry-run" in a
    if "--scan" in a:
        scan(root); sys.exit()
    targets = [x for x in a if x.endswith(".md")]
    if not targets:
        sys.exit(__doc__)
    for t in targets:
        r = do_split(t, root, keep, dry)
        print(("DRY  " if dry else "WROTE") + " %s" % t)
        if r:
            print("      log=%s  moved=%d blocks  live=%d B  log=%d B" % r)
        else:
            print("      nothing movable")
