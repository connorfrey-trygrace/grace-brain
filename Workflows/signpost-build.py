#!/usr/bin/env python3
"""
Build the Sunday Night run-of-show signposts for the LED side screens (393x1080).

Usage:
    python3 "Workflows/signpost-build.py" path/to/signposts.json

Shape comes from the existing LED side panels
(Sunday Visuals/YouTube Thumbs/LED Panels/*_393x1080.png); the look is the
discussion-slide theme (near-black field, white Lato Light, Active Blue accent).

One PNG per segment: the whole night listed top to bottom, the current segment
lit, the rest dimmed -- a YouTube chapter bar turned on its side. Plus an
overview panel (nothing lit) for walk-in.

JSON: {"date": "9.27.26", "segments": [["Worship"], ["Question", "of the Night"], ...]}
Each segment is a list of lines (the panel is too narrow to wrap automatically).
"""

import json
import pathlib
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"

ACTIVE_BLUE = "#2F97A0"   # PANTONE 2235 C -- Reference/Grace-Brand-Guideline.md
INK = "#111113"
WHITE = "#FFFFFF"
W, H = 393, 1080

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>signpost</title>
<style>
  @font-face {{ font-family:'Lato'; font-weight:300; src:url('{fonts}/Lato-Light.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:900; src:url('{fonts}/Lato-Black.ttf') format('truetype'); }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{w}px; height:{h}px; overflow:hidden; background:{ink}; }}
  body {{ color:{white}; font-family:'Lato', Helvetica, Arial, sans-serif; -webkit-font-smoothing:antialiased; }}
  .stage {{ width:{w}px; height:{h}px; padding:90px 30px; display:flex; flex-direction:column;
           justify-content:center; gap:58px; }}
  .seg {{ font-weight:300; font-size:40px; line-height:1.12; opacity:.28;
          padding-left:20px; border-left:6px solid transparent; }}
  .seg.all {{ opacity:1; }}
  .seg.on {{ opacity:1; transform:scale(1.12); transform-origin:left center; border-left-color:{blue}; }}
</style></head>
<body><div class="stage">{body}</div></body></html>
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(html, out_png):
    tmp = out_png.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--allow-file-access-from-files",
         "--virtual-time-budget=4000", f"--window-size={W},{H}",
         f"--screenshot={out_png}", tmp.as_uri()],
        check=True, capture_output=True,
    )
    tmp.unlink()


def build(spec_path):
    spec_path = pathlib.Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    segs = spec["segments"]
    common = dict(fonts=FONTS.as_uri(), ink=INK, white=WHITE, blue=ACTIVE_BLUE, w=W, h=H)
    written = []

    # 0 = overview (all lit), 1..n = that segment lit.
    for lit in range(len(segs) + 1):
        rows = []
        for i, lines in enumerate(segs, start=1):
            cls = "all" if lit == 0 else ("on" if i == lit else "")
            rows.append(f'<div class="seg {cls}">' + "<br>".join(esc(l) for l in lines) + "</div>")
        name = "Overview" if lit == 0 else " ".join(segs[lit - 1])
        out = spec_path.parent / f"{spec['date']} - Signpost {lit} - {name}.png"
        render(TEMPLATE.format(body="".join(rows), **common), out)
        written.append(out)

    for p in written:
        print(f"wrote {p}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
