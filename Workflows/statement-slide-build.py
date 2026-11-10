#!/usr/bin/env python3
"""
Build a Sunday Night statement slide as a 1920x1080 PNG.

A statement slide is any slide that is just words on the field -- an announcement,
an instruction, a promo. Same house style as the question-of-the-night slide.

Usage:
    python3 "Workflows/statement-slide-build.py" path/to/slide.json

WHY THIS IMPORTS RATHER THAN COPIES. Workflows/peer-discussion-slide.md says
"one renderer, one template, no hand-made one-offs -- that is what keeps the
week-to-week set looking like a set." So this script does not restate the
template, the brand colors, the font paths or the auto-fit script. It loads
discussion-slide-build.py and reuses them. A change to the house style there
reaches this slide automatically; there is no second copy to drift.

The slide follows the same design spec: near-black field, white Lato Light,
auto-fitted type, and NO CHROME -- no eyebrow label, no accent rule, no footer,
no date. Connor, 2026-09-16: that chrome reads as machine-made. The statement
carries the slide by itself, exactly as the question does on the QOTN slide.

The JSON:

    {
      "_source": "where the wording came from",
      "lines": ["first line", "second line", "third line"]
    }

Each entry in "lines" is one visual line. They are NOT auto-wrapped -- you choose
the line breaks, because where a spoken instruction breaks changes how it reads
from the back row.
"""

import importlib.util
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def _load_renderer():
    """Load discussion-slide-build.py as a module (its name has hyphens)."""
    path = HERE / "discussion-slide-build.py"
    spec = importlib.util.spec_from_file_location("discussion_slide_build", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(spec_path):
    r = _load_renderer()
    spec_path = pathlib.Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_dir = spec_path.parent

    lines = spec["lines"]
    if not lines:
        sys.exit("no lines in spec")

    # Same .qotn treatment as the question of the night: Lato Light, centered,
    # auto-fitted.
    #
    # Each line is its own nowrap block, NOT a <br>. With <br> the browser still
    # re-wraps a line that is too wide, and the auto-fit loop happily accepts it
    # because scrollWidth fits once it has wrapped -- so the chosen break survives
    # and an unwanted second break appears next to it. nowrap makes an over-wide
    # line genuinely not fit, which forces the binary search to shrink until every
    # line stands on its own. Your line breaks are the only line breaks.
    rows = "".join(
        f'<div style="white-space:nowrap">{r.esc(line)}</div>' for line in lines
    )
    body = (
        '<div class="qotn" data-fit="1" data-fit-max="150" data-fit-min="44">'
        + rows
        + "</div>"
    )

    common = dict(fonts=r.FONTS.as_uri(), ink=r.INK, white=r.WHITE,
                  blue=r.ACTIVE_BLUE, gray=r.CINDER_GRAY)

    out_png = out_dir / f"{spec_path.stem}.png"
    r.render(r.TEMPLATE.format(body=body, **common), out_png, out_dir)
    print(f"wrote {out_png}")
    return out_png


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
