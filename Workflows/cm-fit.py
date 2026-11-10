#!/usr/bin/env python3
"""Check Confidence Monitor text against Brian Parker's template box — measured, not estimated.

WHY THIS EXISTS (2026-09-28). Brian reported the 9/27 CM notes didn't fit the monitor. The
cm-notes-from-script skill was sizing blocks by a ~13-line / 37-char rule of thumb, while
Brian had already published the real limit: his blank `Confidence Monitor Template.docx` in the
Office Dropbox (`~/Library/CloudStorage/Dropbox/Office/`), a fixed text box that "shows the amount
of text that can fit on the confidence monitor" — "please don't change the font or size."

SOURCE OF TRUTH (Connor, 2026-10-28): Brian's original in /Office; /Reference now holds an
identical copy. The old 20pt filled-in sample (box shrunk to 206.55pt) is in /Archive — NOT the standard.

GEOMETRY (read from the Office docx XML, not guessed):
  box      351pt x 220.8pt        (wp:extent cx=4457700 cy=2804160 EMU)
  insets   7.2pt left/right, 3.6pt top/bottom   (wps:bodyPr lIns/rIns/tIns/bIns, EMU)
  font     Calibri 28pt (the box's run size, w:sz=56), single spacing, no paragraph spacing
  => usable 336.6pt wide x 213.6pt tall; Calibri line = 1.2207 em = 34.18pt => 6 lines

Word wraps at word boundaries, so a 30-char line of wide letters can wrap where a 40-char
line of narrow ones doesn't. This measures real Calibri glyph widths and wraps the way Word
does, then counts rendered lines.

WHAT IS MEASURED (Connor, 2026-09-28). A PCO Host item's content holds two parts: the
monitor text, and everything else (e.g. the slide-operator cue). Only the monitor text goes on
the monitor. The `Confidence Monitor Notes:` label only marks where it starts — it is not
shown and is not counted. The monitor text runs from that label to the first blank line; the
rest of the item (a `Slide (...)` cue etc.) is off-monitor and is ignored here.

USAGE
  python3 "Workflows/cm-fit.py" FILE        # blocks separated by a line containing only ===
  python3 "Workflows/cm-fit.py" - < FILE
Exit non-zero if any block overflows.
"""
import sys
from PIL import ImageFont

FONT = "/Applications/Microsoft Outlook.app/Contents/Resources/DFonts/Calibri.ttf"
PT = 28
WIDTH_PT = 351 - 2 * 7.2          # 336.6
HEIGHT_PT = 220.8 - 2 * 3.6       # 213.6
LINE_PT = PT * 2500 / 2048        # Calibri winAscent+winDescent / unitsPerEm = 34.18
MAX_LINES = int(HEIGHT_PT // LINE_PT)  # 6

# measure at 10x for sub-point precision
_f = ImageFont.truetype(FONT, PT * 10)
def width(s):
    return _f.getlength(s) / 10

def wrap(line):
    """Word-style wrap: break at spaces; a single word wider than the box breaks by char."""
    if line == "":
        return [""]
    out, cur = [], ""
    for word in line.split(" "):
        trial = word if cur == "" else cur + " " + word
        if width(trial) <= WIDTH_PT:
            cur = trial
            continue
        if cur:
            out.append(cur)
        cur = word
        while width(cur) > WIDTH_PT:          # overlong single token
            i = len(cur)
            while width(cur[:i]) > WIDTH_PT:
                i -= 1
            out.append(cur[:i]); cur = cur[i:]
    out.append(cur)
    return out

def monitor_part(block):
    """Lines between the `Confidence Monitor Notes:` label and the first blank line."""
    lines = block.strip("\n").split("\n")
    if lines and lines[0].strip().lower().startswith("confidence monitor notes"):
        lines = lines[1:]
    if "" in lines:
        lines = lines[:lines.index("")]
    return lines

def check(block):
    src = monitor_part(block)
    rendered = []
    for i, l in enumerate(src, 1):
        for j, r in enumerate(wrap(l)):
            rendered.append((i, j > 0, r))
    return src, rendered

def main():
    text = sys.stdin.read() if len(sys.argv) < 2 or sys.argv[1] == "-" else open(sys.argv[1]).read()
    blocks = [b for b in text.split("\n===\n") if b.strip()]
    bad = 0
    print(f"# CM fit — box {WIDTH_PT:.1f}pt x {HEIGHT_PT:.1f}pt, Calibri {PT}pt, max {MAX_LINES} lines")
    for n, b in enumerate(blocks, 1):
        src, r = check(b)
        wraps = [s for s, w, _ in r if w]
        ok = len(r) <= MAX_LINES
        bad += not ok
        title = src[0] if src else "(empty)"
        print(f"\n[{n}] {'OK  ' if ok else 'OVER'} {len(r)}/{MAX_LINES} lines — {title[:40]}")
        for i, (s, w, txt) in enumerate(r, 1):
            mark = "  ↳" if w else "   "
            over = "  <-- past the box" if i > MAX_LINES else ""
            print(f"  {i:2}{mark} {txt:<44} {width(txt):5.0f}pt{over}")
        if wraps:
            print(f"  wrapped source lines: {sorted(set(wraps))}")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
