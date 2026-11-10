#!/usr/bin/env python3
"""
Build the Sunday Night peer-discussion slides as 1920x1080 PNGs.

Usage:
    python3 "Workflows/discussion-slide-build.py" path/to/week.json

Reads a week JSON file (see Workflows/peer-discussion-slide.md for the schema),
writes one PNG per slide next to it, and prints what it wrote.

Renders with headless Chrome so the type is real Lato, not a font substitute.
Fonts are vendored in Workflows/assets/fonts/ -- no network needed at build time.
"""

import json
import pathlib
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"

# Grace Brand Guideline, Summer 2019 (Reference/Grace-Brand-Guideline.md).
# Do not substitute eyeballed values -- three wrong Grace teals are already in circulation.
ACTIVE_BLUE = "#2F97A0"   # PANTONE 2235 C
CINDER_GRAY = "#ABABAB"   # PANTONE 429 C
INK = "#111113"           # near-black field; dark auditorium, white type on top
WHITE = "#FFFFFF"

TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>slide</title>
<style>
  @font-face {{ font-family:'Lato'; font-weight:300; src:url('{fonts}/Lato-Light.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:400; src:url('{fonts}/Lato-Regular.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:700; src:url('{fonts}/Lato-Bold.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:900; src:url('{fonts}/Lato-Black.ttf') format('truetype'); }}

  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1920px; height:1080px; overflow:hidden; }}
  body {{
    background:{ink}; color:{white};
    font-family:'Lato', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing:antialiased;
  }}
  /* No eyebrow label, no accent rule, no footer metadata. Connor, 2026-09-16:
     that chrome reads as machine-made. The question carries the slide by itself. */
  .slide {{ width:1920px; height:1080px; padding:110px 140px; display:flex; flex-direction:column; }}

  .stage {{ flex:1; display:flex; flex-direction:column; justify-content:center; }}

  /* Brand book: main header is Light, not bold. Quiet and large. */
  .qotn {{ font-weight:300; line-height:1.12; letter-spacing:-.005em; text-align:center; }}

  .qlist {{ display:flex; flex-direction:column; justify-content:center; gap:var(--gap,56px); }}
  .qrow {{ display:flex; align-items:baseline; gap:38px; }}
  .qnum {{ font-weight:900; color:{blue}; flex:0 0 auto; font-variant-numeric:tabular-nums; }}
  .qtext {{ font-weight:300; line-height:1.2; }}
</style></head>
<body>
<div class="slide">
  <div class="stage" id="stage">{body}</div>
</div>
<script>
// Fit the type as large as it will go inside the stage. Back-row legibility is the
// whole point of the slide, so size is computed, never guessed.
(function () {{
  var stage = document.getElementById('stage');
  var targets = Array.prototype.slice.call(document.querySelectorAll('[data-fit]'));
  var max = parseFloat(targets[0].getAttribute('data-fit-max'));
  var min = parseFloat(targets[0].getAttribute('data-fit-min'));

  function apply(px) {{
    targets.forEach(function (el) {{
      var ratio = parseFloat(el.getAttribute('data-fit')) || 1;
      el.style.fontSize = (px * ratio) + 'px';
    }});
    var list = document.querySelector('.qlist');
    if (list) list.style.setProperty('--gap', Math.round(px * 0.62) + 'px');
  }}

  // Measure the content block itself, not the stage. A centered flex child overflows
  // in both directions without ever growing the stage's scrollHeight, so measuring the
  // stage silently reports "fits" while the last question is off the bottom of the frame.
  var content = stage.firstElementChild;
  var BREATHE = 48; // px of air kept top and bottom

  function fits() {{
    return content.scrollHeight <= (stage.clientHeight - 2 * BREATHE)
        && content.scrollWidth <= stage.clientWidth;
  }}

  var lo = min, hi = max, best = min;
  for (var i = 0; i < 24; i++) {{
    var mid = (lo + hi) / 2;
    apply(mid);
    if (fits()) {{ best = mid; lo = mid; }} else {{ hi = mid; }}
  }}
  apply(Math.floor(best));
  document.title = 'ready';
}})();
</script>
</body></html>
"""


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;"))


def render(html, out_png, workdir):
    tmp = workdir / (out_png.stem + ".html")
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--allow-file-access-from-files",
         "--virtual-time-budget=6000", "--window-size=1920,1080",
         f"--screenshot={out_png}", tmp.as_uri()],
        check=True, capture_output=True,
    )
    tmp.unlink()


def build(spec_path):
    spec_path = pathlib.Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_dir = spec_path.parent
    stem = spec_path.stem

    common = dict(fonts=FONTS.as_uri(), ink=INK, white=WHITE, blue=ACTIVE_BLUE,
                  gray=CINDER_GRAY)
    written = []

    # Slide 1 -- question of the night, alone, as large as it will go.
    qotn_body = (
        f'<div class="qotn" data-fit="1" data-fit-max="170" data-fit-min="52">'
        f'{esc(spec["qotn"])}</div>'
    )
    p1 = out_dir / f"{stem}-1-QOTN.png"
    render(TEMPLATE.format(body=qotn_body, **common), p1, out_dir)
    written.append(p1)

    # Slide 2 -- the guide questions, numbered.
    rows = []
    for i, q in enumerate(spec["questions"], start=1):
        rows.append(
            f'<div class="qrow">'
            f'<div class="qnum" data-fit="0.78" data-fit-max="110" data-fit-min="34">{i}</div>'
            f'<div class="qtext" data-fit="1" data-fit-max="110" data-fit-min="34">{esc(q)}</div>'
            f'</div>'
        )
    list_body = '<div class="qlist">' + "".join(rows) + "</div>"
    p2 = out_dir / f"{stem}-2-Discussion.png"
    render(TEMPLATE.format(body=list_body, **common), p2, out_dir)
    written.append(p2)

    for p in written:
        print(f"wrote {p}")
    return written


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
