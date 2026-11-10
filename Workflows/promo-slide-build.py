#!/usr/bin/env python3
"""
Build a Sunday Night PROMO slide as a 1920x1080 PNG.

Usage:
    python3 "Workflows/promo-slide-build.py" path/to/slide.json

WHY THIS IS NOT THE STATEMENT/QOTN RENDERER. Connor, 2026-09-22, on the first
Inspira attempt: "That slide is SOOOO boring. This should not be the same style
as a QOTN slide, this should amp people up."

He is right, and the distinction is real. The question-of-the-night slide is
deliberately quiet -- one question, no chrome, nothing competing with it, because
the room is being asked to think. A promo is the opposite job: it is selling a
night to people who have not decided to come yet, and it has to carry WHO / WHAT /
WHEN / WHERE at a glance from the back row. Quiet would be a failure here.

So the no-chrome rule in Workflows/peer-discussion-slide.md is scoped to the
discussion set and does NOT apply to this renderer. What carries over is the
brand: the palette below is the Summer 2019 book (Reference/Grace-Brand-Guideline),
and the face is Lato, the one brand-sanctioned family that is freely licensed.

The JSON:

    {
      "_source":  "where every fact came from",
      "photo":    "cover.jpg",                    # optional, relative to the JSON
      "kicker":   "small tracked line above the hero",
      "hero":     ["COUNTRY", "SWING"],        # one entry per hero line
      "subhead":  "at Inspira Dance",
      "standfirst": "one sentence under the subhead",
      "bg_glyph": "?",                            # optional plane of glyphs as the backdrop
      "glyph":    "?",                            # optional giant glyph replacing the badge
      "badge":    {"dow": "Sunday", "day": "4", "month": "October", "time": "7:30 PM"},
      "schedule": [{"time": "7:30", "what": "Beginner lesson"}, ...],
      "qr_url":   "https://...",                 # rendered as a QR in the footer
      "cta":      {"big": "Scan to RSVP", "small": "partiful.com"},
      "price":    {"amount": "$10", "per": "at the door"}
    }

Everything is optional except hero. Keep the copy short -- this is a slide, not a flyer.
"""

import importlib.util
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent

# Grace Brand Guideline, Summer 2019. Four colors, and that is the whole palette.
ACTIVE_BLUE = "#2F97A0"   # PANTONE 2235 C
STABLE_BLUE = "#1C3B6B"   # PANTONE 534 C
CINDER_GRAY = "#ABABAB"   # PANTONE 429 C
CLOUD_GRAY = "#E3E3E3"    # PANTONE 427 C
WHITE = "#FFFFFF"


def _load_renderer():
    """Reuse the discussion renderer's Chrome screenshot call and HTML escaper."""
    path = HERE / "discussion-slide-build.py"
    spec = importlib.util.spec_from_file_location("discussion_slide_build", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
    font-family:'Lato', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing:antialiased;
    background:#0B1A2E;
  }}

  .slide {{ position:relative; width:1920px; height:1080px; overflow:hidden; }}

  /* --- the photo -------------------------------------------------------
     A real photo of the room beats any generated texture, so when one is
     supplied it goes full bleed and the drawn field becomes a scrim over it.
     Two problems a bare photo has on a Grace slide, both handled here:
     (1) club lighting is warm yellow/orange and the brand is cool teal/navy,
         so a Stable Blue multiply pulls it toward the palette without
         flattening it into a duotone -- the energy survives, the clash does not;
     (2) type over a crowd is unreadable, so the scrim is opaque on the left
         where the words are and falls away to the right where the picture
         should breathe. */
  /* Blurred on purpose: the photo is atmosphere, not information. Sharp faces
     compete with the headline and pull the eye into the crowd instead of the
     words. scale(1.06) hides the feathered edge blur leaves at the frame. */
  .photo {{ position:absolute; inset:0; background-size:cover; background-position:center 32%;
            filter:saturate(1.12) contrast(1.06) brightness(1.05) blur({blur}px);
            transform:scale(1.06); }}
  .photo-tone {{ position:absolute; inset:0; background:{stable}; mix-blend-mode:color; opacity:.28; }}
  .photo-deepen {{ position:absolute; inset:0; background:{stable}; opacity:.10; }}
  .scrim {{
    position:absolute; inset:0;
    background:
      linear-gradient(90deg, rgba(10,21,38,.96) 0%, rgba(10,21,38,.88) 30%,
                             rgba(12,32,56,.52) 54%, rgba(12,32,56,.10) 100%),
      linear-gradient(0deg, rgba(10,21,38,.90) 0%, rgba(10,21,38,.30) 20%, rgba(10,21,38,0) 40%);
  }}

  /* --- the field -------------------------------------------------------
     Stable Blue is the base, not a flat fill: a warm Active Blue bloom sits
     behind the hero so the type reads off a lit field rather than a dead one,
     and the corners fall away so nothing competes with the headline. */
  .field {{
    position:absolute; inset:0;
    background:
      radial-gradient(1100px 760px at 22% 38%, rgba(47,151,160,.55) 0%, rgba(47,151,160,0) 68%),
      radial-gradient(900px 700px at 88% 84%, rgba(47,151,160,.22) 0%, rgba(47,151,160,0) 70%),
      linear-gradient(150deg, {stable} 0%, #12294A 45%, #0A1526 100%);
  }}

  /* Motion: skewed bands sweeping up to the right. Swing dancing is diagonal
     and fast; a grid or a straight rule would say "agenda," not "go dance." */
  .streaks {{ position:absolute; inset:-20%; transform:rotate(-18deg); opacity:.5; }}
  .streak {{
    position:absolute; height:2px; left:0; right:0;
    background:linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.30) 18%,
                                       rgba(47,151,160,.75) 52%, rgba(255,255,255,0) 100%);
  }}
  .streak.thick {{ height:5px; opacity:.85; }}

  /* A single oversized ring, cropped by the frame. Gives the composition a
     centre of gravity on the right so the type block is not floating. */
  .ring {{
    position:absolute; right:-260px; top:-200px; width:1120px; height:1120px;
    border-radius:50%; border:2px solid rgba(227,227,227,.16);
  }}
  .ring.inner {{ right:-140px; top:-80px; width:880px; height:880px; border-color:rgba(47,151,160,.38); }}

  .content {{ position:relative; width:100%; height:100%; padding:96px 120px 84px; display:flex; flex-direction:column; }}
  .upper {{ display:flex; align-items:center; gap:70px; }}
  .lede {{ flex:1; min-width:0; }}

  /* The date badge. The first version of this slide left the right third empty
     and buried the date in the fact row -- for a promo the date IS the message,
     so it gets its own mass and anchors the composition against the hero. */
  .badge {{
    flex:0 0 auto; width:430px; aspect-ratio:1; border-radius:50%;
    background:radial-gradient(circle at 34% 30%, rgba(47,151,160,.95) 0%, rgba(30,104,116,.92) 55%, rgba(21,72,86,.95) 100%);
    box-shadow:0 30px 90px rgba(0,0,0,.45), inset 0 0 0 3px rgba(227,227,227,.30);
    display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;
  }}
  .badge .b-dow {{ font-weight:900; font-size:40px; letter-spacing:.30em; text-transform:uppercase; color:rgba(255,255,255,.88); }}
  .badge .b-day {{ font-weight:900; font-size:168px; line-height:.92; color:{white}; letter-spacing:-.03em; margin:4px 0 2px; }}
  .badge .b-mon {{ font-weight:900; font-size:52px; letter-spacing:.20em; text-transform:uppercase; color:{white}; }}
  .badge .b-time {{ font-weight:700; font-size:38px; color:rgba(255,255,255,.92); margin-top:16px;
                    border-top:2px solid rgba(255,255,255,.35); padding-top:14px; }}

  .kicker {{
    font-weight:900; font-size:30px; letter-spacing:.42em; text-transform:uppercase;
    color:{active}; margin-bottom:26px;
  }}

  .hero {{ font-weight:900; text-transform:uppercase; color:{white};
           font-size:178px; line-height:.88; letter-spacing:-.022em;
           text-shadow:0 18px 60px rgba(0,0,0,.45); }}

  .subhead {{ font-weight:900; font-size:74px; line-height:1.06; color:{active};
              margin-top:26px; letter-spacing:-.01em; }}

  .standfirst {{ font-weight:300; font-size:44px; line-height:1.3; color:{cloud};
                 margin-top:24px; max-width:1180px; }}

  /* Two-line running order. A promo that only gives a start time makes the
     reader guess how long they are committing to; the lesson/dancing split is
     also the objection-killer for anyone who has never done this. */
  /* Right rail. Rows are flush right rather than column-aligned on the time --
     against the frame edge a ragged right reads as a mistake, a ragged left does not. */
  /* Bubble: the footer holds three unlike things (a code, a price, a running
     order). Containing the times gives the eye a third object to land on and
     stops them reading as a caption hanging off the price. */
  .schedule {{ display:flex; flex-direction:column; gap:12px; margin-left:auto; text-align:right;
               background:rgba(10,21,38,.55); border:2px solid rgba(47,151,160,.45);
               border-radius:26px; padding:26px 36px;
               backdrop-filter:blur(6px); }}
  .srow {{ display:flex; align-items:baseline; gap:24px; justify-content:flex-end; }}
  .stime {{ font-weight:900; font-size:42px; line-height:1; color:{active};
            flex:0 0 auto; letter-spacing:-.015em; }}
  .slabel {{ font-weight:300; font-size:36px; line-height:1.1; color:{cloud}; }}

  .spacer {{ flex:1; }}

  /* ---- layout: qr-right -------------------------------------------------
     Connor, 2026-09-22: "put the qr on the right half of the page - it should
     be almost as big as possible." The QR stops being a footnote and becomes
     half the composition, so the date badge goes (no room, and the date reads
     fine as a line) and everything else stacks down the left. */
  .split {{ width:100%; height:100%; display:flex; align-items:center; gap:76px; }}
  .split .lede {{ flex:1; min-width:0; }}
  .split .hero {{ font-size:148px; }}
  .split .subhead {{ font-size:58px; margin-top:20px; }}
  .when {{ font-weight:900; font-size:52px; color:{white}; margin-top:30px; letter-spacing:-.01em; }}
  .split .schedule {{ margin:30px 0 0 0; text-align:left; }}
  .split .srow {{ justify-content:flex-start; }}
  .split .price {{ display:flex; align-items:baseline; gap:18px; margin-top:28px; }}
  .split .price .amt {{ font-size:76px; }}
  .split .price .per {{ font-size:30px; margin-top:0; }}
  .qrpane {{ flex:0 0 {qrsize}px; }}
  .qrpane .qr {{ width:{qrsize}px; height:{qrsize}px; padding:34px; border-radius:34px; }}

  /* Connor, 2026-09-22: "SOOO much text." A promo is read in about two seconds
     from the back row, so the slide carries the hook, the date and the way in --
     and nothing else. The fact row with a caption under every column went. */
  /* Optional giant glyph (e.g. "?") in the badge's place -- Connor 2026-10-07, curiosity-themed dinner. */
  .glyph {{ flex:0 0 auto; font-weight:900; font-size:760px; line-height:.8; color:{active};
            opacity:.92; text-shadow:0 20px 60px rgba(0,0,0,.35); margin-right:30px; }}
  .gplane {{ position:absolute; inset:0; overflow:hidden; }}
  .gplane span {{ position:absolute; font-weight:900; color:{active}; line-height:1; }}
  .footer {{ display:flex; align-items:center; gap:44px;
             border-top:2px solid rgba(227,227,227,.22); padding-top:34px; }}
  .qr {{ flex:0 0 auto; width:262px; height:262px; background:{white};
         border-radius:22px; padding:20px; }}
  .qr img {{ width:100%; height:100%; display:block; }}
  .qrwrap {{ flex:0 0 auto; display:flex; flex-direction:column; align-items:center; }}
  .price {{ flex:0 0 auto; }}
  .price .amt {{ font-weight:900; font-size:96px; line-height:1; color:{active}; letter-spacing:-.03em; }}
  .price .per {{ font-weight:300; font-size:32px; color:{cinder}; margin-top:6px; }}
</style></head>
<body>
<div class="slide">
  {backdrop}
  <div class="content">{content}</div>
</div>
</body></html>
"""


def build(spec_path):
    r = _load_renderer()
    spec_path = pathlib.Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_dir = spec_path.parent
    esc = r.esc

    def qr_svg(url, dark, eye_dark, eye_inner, light="#FFFFFF", badge=None):
        """Grace's house QR style, matched against the real artifact rather than
        a description: Heather Noble's 'Volunteer - Sunday Night_white.pdf'
        (emailed 2026-09-11) and the Boot Camp sign she made 2026-09-10.

        What that artifact actually does, read off the PDF:
          - data modules are small separated DOTS, navy (Stable Blue)
          - finder eyes are ROUNDED SQUARES -- a thick rounded ring with a solid
            CIRCLE inside, not a square
          - a teal (Active Blue) disc sits dead centre carrying the white Grace
            'g', which is why the symbol needs error correction H: the badge
            occludes real modules.

        Drawn by hand from segno's matrix because segno only emits squares.
        """
        import segno
        m = [list(r) for r in segno.make(url, error="h").matrix]
        n = len(m)
        eyes = [(0, 0), (0, n - 7), (n - 7, 0)]

        def in_eye(r, c):
            return any(er <= r < er + 7 and ec <= c < ec + 7 for er, ec in eyes)

        # Clear a disc of modules under the centre badge so the art sits on white
        # rather than on half-drawn dots.
        cx = cy = n / 2
        hole = (badge or {}).get("radius", 0)

        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}">']
        for r in range(n):
            for c in range(n):
                if not m[r][c] or in_eye(r, c):
                    continue
                if hole and ((c + .5 - cx) ** 2 + (r + .5 - cy) ** 2) ** .5 < hole + .6:
                    continue
                out.append(f'<circle cx="{c + .5}" cy="{r + .5}" r=".40" fill="{dark}"/>')
        for er, ec in eyes:
            out.append(f'<rect x="{ec}" y="{er}" width="7" height="7" rx="2.2" fill="{eye_dark}"/>')
            out.append(f'<rect x="{ec + 1}" y="{er + 1}" width="5" height="5" rx="1.6" fill="{light}"/>')
            out.append(f'<circle cx="{ec + 3.5}" cy="{er + 3.5}" r="1.5" fill="{eye_inner}"/>')
        if badge:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{hole}" fill="{badge["fill"]}"/>')
            if badge.get("mark_uri"):
                gw = hole * 1.15
                out.append(f'<image href="{badge["mark_uri"]}" x="{cx - gw / 2}" '
                           f'y="{cy - gw / 2}" width="{gw}" height="{gw}" '
                           f'preserveAspectRatio="xMidYMid meet"/>')
        out.append("</svg>")
        return "".join(out)

    photo = spec.get("photo")
    if photo:
        import base64
        raw = (spec_path.parent / photo).read_bytes()
        uri = "data:image/jpeg;base64," + base64.b64encode(raw).decode()
        backdrop = (
            f'<div class="photo" style="background-image:url({uri})"></div>'
            '<div class="photo-tone"></div>'
            '<div class="photo-deepen"></div>'
            '<div class="scrim"></div>'
        )
    else:
        streaks = "".join(
            f'<div class="streak{" thick" if i % 3 == 0 else ""}" '
            f'style="top:{90 + i * 86}px"></div>'
            for i in range(13)
        )
        backdrop = ('<div class="field"></div>'
                    f'<div class="streaks">{streaks}</div>'
                    '<div class="ring"></div><div class="ring inner"></div>')
        if spec.get("bg_glyph"):
            # A plane of glyphs (e.g. "?") instead of streaks/rings -- Connor 2026-10-07.
            import random
            rnd = random.Random(7)
            g = esc(spec["bg_glyph"])
            cells = []
            for row in range(7):
                for col in range(13):
                    x = col * 156 - 30 + (78 if row % 2 else 0) + rnd.randint(-14, 14)
                    y = row * 162 - 20 + rnd.randint(-14, 14)
                    size = rnd.randint(110, 190)
                    rot = rnd.randint(-28, 28)
                    op = rnd.choice([.07, .09, .12, .15])
                    cells.append(f'<span style="left:{x}px;top:{y}px;font-size:{size}px;'
                                 f'transform:rotate({rot}deg);opacity:{op}">{g}</span>')
            backdrop = ('<div class="field"></div><div class="gplane">' + "".join(cells) + '</div>')

    hero = "<br>".join(esc(line) for line in spec["hero"])

    kicker = (f'<div class="kicker">{esc(spec["kicker"])}</div>'
              if spec.get("kicker") else "")
    subhead = (f'<div class="subhead">{esc(spec["subhead"])}</div>'
               if spec.get("subhead") else "")
    standfirst = (f'<div class="standfirst">{esc(spec["standfirst"])}</div>'
                  if spec.get("standfirst") else "")

    schedule = ""
    if spec.get("schedule"):
        schedule = ('<div class="schedule">' + "".join(
            f'<div class="srow"><div class="stime">{esc(r["time"])}</div>'
            f'<div class="slabel">{esc(r["what"])}</div></div>'
            for r in spec["schedule"]) + "</div>")

    b = spec.get("badge")
    badge = ""
    if b:
        badge = (
            '<div class="badge">'
            + (f'<div class="b-dow">{esc(b["dow"])}</div>' if b.get("dow") else "")
            + (f'<div class="b-day">{esc(b["day"])}</div>' if b.get("day") else "")
            + (f'<div class="b-mon">{esc(b["month"])}</div>' if b.get("month") else "")
            + (f'<div class="b-time">{esc(b["time"])}</div>' if b.get("time") else "")
            + "</div>"
        )

    if spec.get("glyph"):
        badge = f'<div class="glyph">{esc(spec["glyph"])}</div>'

    footer = ""
    cta, qr_uri = spec.get("cta"), None
    if spec.get("qr_url"):
        import base64
        mark = HERE / "assets" / "brand" / "grace-g-white.png"
        mark_uri = ("data:image/png;base64," +
                    base64.b64encode(mark.read_bytes()).decode()) if mark.exists() else None
        svg = qr_svg(spec["qr_url"], dark=STABLE_BLUE, eye_dark=STABLE_BLUE,
                     eye_inner=STABLE_BLUE,
                     badge={"fill": ACTIVE_BLUE, "radius": 4.2, "mark_uri": mark_uri})
        qr_uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    if qr_uri or cta or spec.get("price"):
        parts = []
        if qr_uri:
            parts.append(f'<div class="qrwrap"><div class="qr"><img src="{qr_uri}"></div></div>')
        pr = spec.get("price")
        if pr:
            parts.append(
                '<div class="price">'
                + f'<div class="amt">{esc(pr["amount"])}</div>'
                + (f'<div class="per">{esc(pr["per"])}</div>' if pr.get("per") else "")
                + "</div>")
        if schedule:
            parts.append(schedule)
        footer = '<div class="footer">' + "".join(parts) + "</div>"

    if spec.get("layout") == "qr-right":
        qr_card = (f'<div class="qrpane"><div class="qr"><img src="{qr_uri}"></div></div>'
                   if qr_uri else "")
        pr = spec.get("price")
        price_html = ""
        if pr:
            price_html = ('<div class="price">'
                          f'<div class="amt">{esc(pr["amount"])}</div>'
                          + (f'<div class="per">{esc(pr["per"])}</div>' if pr.get("per") else "")
                          + "</div>")
        when = (f'<div class="when">{esc(spec["when"])}</div>' if spec.get("when") else "")
        content = ('<div class="split"><div class="lede">'
                   + kicker + f'<div class="hero">{hero}</div>' + subhead + standfirst
                   + when + schedule + price_html
                   + "</div>" + qr_card + "</div>")
    else:
        content = ('<div class="upper"><div class="lede">' + kicker
                   + f'<div class="hero">{hero}</div>' + subhead + standfirst
                   + "</div>" + badge + "</div>"
                   + '<div class="spacer"></div>' + footer)

    html = TEMPLATE.format(
        fonts=r.FONTS.as_uri(), white=WHITE, active=ACTIVE_BLUE,
        stable=STABLE_BLUE, cinder=CINDER_GRAY, cloud=CLOUD_GRAY,
        backdrop=backdrop, blur=spec.get('photo_blur', 7),
        qrsize=spec.get('qr_size', 840),
        content=content,
    )

    out_png = out_dir / f"{spec_path.stem}.png"
    r.render(html, out_png, out_dir)
    print(f"wrote {out_png}")
    return out_png


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
