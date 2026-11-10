#!/usr/bin/env python3
"""
Build a Sunday Night large-print scripture reading sheet as a PDF.

Usage:
    python3 "Workflows/scripture-reading-sheet.py" SOURCE.docx OUT.pdf \
        --ref "John 14:15-31" --version NIV --date "September 20, 2026" \
        --first-verse 15 --split 2

Reads the passage text straight out of the .docx (never retyped -- scripture does
not get transcribed by hand), marks verse numbers, lays it across exactly two
US Letter pages, and binary-searches the largest type size that still fits both.

Renders with headless Chrome so the type is real Lato, not a font substitute.
Fonts are vendored in Workflows/assets/fonts/ -- no network needed at build time.
"""

import argparse
import pathlib
import re
import subprocess
import sys
import zipfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "assets" / "fonts"

# Grace Brand Guideline, Summer 2019 (Reference/Grace-Brand-Guideline.md).
# Do not substitute eyeballed values -- three wrong Grace teals are already in circulation.
ACTIVE_BLUE = "#2F97A0"   # PANTONE 2235 C
STABLE_BLUE = "#1C3B6B"   # PANTONE 534 C
CINDER_GRAY = "#ABABAB"   # PANTONE 429 C
INK = "#111113"           # near-black body; printed on white, read at arm's length


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def docx_paragraphs(path):
    """Paragraph strings from a .docx, in order, blanks dropped."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        runs = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)
        text = "".join(runs)
        text = (text.replace("&amp;", "&").replace("&lt;", "<")
                    .replace("&gt;", ">").replace("&quot;", '"')
                    .replace("&apos;", "'"))
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            out.append(text)
    return out


def mark_verses(paras, first_verse):
    """Wrap verse numbers in <span class=v>. Walks the expected sequence rather
    than regexing every bare integer, so a number inside the text is never eaten."""
    n = first_verse
    marked = []
    for para in paras:
        buf, i = [], 0
        while True:
            m = re.compile(r"(?<![0-9A-Za-z])%d(?![0-9])\s*" % n).search(para, i)
            if not m:
                break
            buf.append(esc(para[i:m.start()]))
            buf.append(f'<span class="v">{n}</span>')
            i = m.end()
            n += 1
        buf.append(esc(para[i:]))
        marked.append("".join(buf))
    return marked, n - 1


TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>building</title>
<style>
  @font-face {{ font-family:'Lato'; font-weight:300; src:url('{fonts}/Lato-Light.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:400; src:url('{fonts}/Lato-Regular.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:700; src:url('{fonts}/Lato-Bold.ttf') format('truetype'); }}
  @font-face {{ font-family:'Lato'; font-weight:900; src:url('{fonts}/Lato-Black.ttf') format('truetype'); }}

  @page {{ size: 8.5in 11in; margin: 0; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:8.5in; background:#fff; }}
  body {{
    font-family:'Lato', Helvetica, Arial, sans-serif;
    color:{ink}; -webkit-font-smoothing:antialiased;
  }}

  .page {{
    width:8.5in; height:11in; position:relative; overflow:hidden;
    padding:0.58in 0.56in 0.82in 0.56in;
    display:flex; flex-direction:column;
    page-break-after:always; break-after:page;
  }}
  .page:last-child {{ page-break-after:auto; break-after:auto; }}

  /* Brand book: sub-heads are Heavy at 160 tracking; main headers are Light. */
  .eyebrow {{
    font-weight:900; font-size:9.5pt; letter-spacing:.16em; text-transform:uppercase;
    color:{blue};
  }}
  .ref {{
    font-weight:300; font-size:33pt; line-height:1.05; color:{navy};
    margin-top:.10in; letter-spacing:-.005em;
  }}
  .version {{
    font-weight:700; font-size:8.5pt; letter-spacing:.14em; text-transform:uppercase;
    color:{gray}; margin-top:.09in;
  }}
  .rule {{ height:3px; background:{blue}; width:100%; margin:.17in 0 .26in 0; }}

  /* min-height:0 + overflow:hidden so the flex item is BOUNDED by the page.
     Without these it grows to max-content, scrollHeight==clientHeight, and the
     fit search below reports every size as fitting. */
  .body {{ flex:1 1 0; min-height:0; overflow:hidden; }}
  .body p {{
    line-height:1.42; margin-bottom:.62em; text-align:left;
    hyphens:none; -webkit-hyphens:none; text-wrap:pretty;
  }}
  .body p:last-child {{ margin-bottom:0; }}
  .v {{
    color:{blue}; font-weight:900; font-size:.56em;
    vertical-align:.62em; letter-spacing:.02em; margin-right:.22em;
    font-variant-numeric:tabular-nums;
  }}
  .closing {{ font-weight:700; }}

  .foot {{
    position:absolute; left:.56in; right:.56in; bottom:.40in;
    display:flex; justify-content:space-between; align-items:baseline;
    font-weight:700; font-size:8pt; letter-spacing:.14em; text-transform:uppercase;
    color:{gray}; border-top:1px solid #E3E3E3; padding-top:.10in;
  }}
</style></head>
<body>
{pages}
<script>
// Largest type that still clears the bottom of BOTH pages. Back-of-the-room
// legibility from a lectern is the whole point, so the size is computed, never guessed.
(function () {{
  var bodies = Array.prototype.slice.call(document.querySelectorAll('.body'));
  function apply(px) {{ bodies.forEach(function (b) {{ b.style.fontSize = px + 'px'; }}); }}
  function fits() {{
    return bodies.every(function (b) {{ return b.scrollHeight <= b.clientHeight; }});
  }}
  var lo = 10, hi = 60, best = 10;
  for (var i = 0; i < 26; i++) {{
    var mid = (lo + hi) / 2;
    apply(mid);
    if (fits()) {{ best = mid; lo = mid; }} else {{ hi = mid; }}
  }}
  apply(Math.floor(best * 4) / 4);
  var fill = bodies.map(function (b) {{
    return Math.round(100 * b.scrollHeight / b.clientHeight) + '%';
  }}).join(' / ');
  document.title = 'ready ' + (Math.floor(best * 4) / 4) + 'px fill ' + fill;
}})();
</script>
</body></html>
"""


def build(args):
    src = pathlib.Path(args.source).resolve()
    out = pathlib.Path(args.out).resolve()
    paras = docx_paragraphs(src)
    marked, last = mark_verses(paras, args.first_verse)

    def page(inner, num, header=False):
        head = ""
        if header:
            head = (f'<div class="eyebrow">{esc(args.eyebrow)}</div>'
                    f'<div class="ref">{esc(args.ref)}</div>'
                    f'<div class="version">{esc(args.version)}</div>'
                    f'<div class="rule"></div>')
        foot = (f'<div class="foot"><span>{esc(args.ref)}</span>'
                f'<span>Page {num} of 2</span></div>')
        return f'<div class="page">{head}<div class="body">{inner}</div>{foot}</div>'

    def wrap(chunk):
        return "".join(
            f'<p class="closing">{t}</p>' if t.startswith("&quot;Come now")
            or t.lstrip('“"').startswith("Come now") else f"<p>{t}</p>"
            for t in chunk)

    p1 = page(wrap(marked[:args.split]), 1, header=True)
    p2 = page(wrap(marked[args.split:]), 2)

    html = TEMPLATE.format(fonts=FONTS.as_uri(), ink=INK, blue=ACTIVE_BLUE,
                           navy=STABLE_BLUE, gray=CINDER_GRAY, pages=p1 + p2)
    tmp = out.parent / (out.stem + ".build.html")
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--allow-file-access-from-files", "--virtual-time-budget=6000",
         f"--print-to-pdf={out}", tmp.as_uri()],
        check=True, capture_output=True,
    )
    tmp.unlink()
    print(f"wrote {out}")
    print(f"paragraphs: {len(paras)}  verses: {args.first_verse}-{last}  "
          f"split after para {args.split}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--ref", required=True)
    ap.add_argument("--version", default="New International Version")
    ap.add_argument("--eyebrow", default="Sunday Night Service")
    ap.add_argument("--first-verse", type=int, required=True)
    ap.add_argument("--split", type=int, default=2,
                    help="number of paragraphs on page 1")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
