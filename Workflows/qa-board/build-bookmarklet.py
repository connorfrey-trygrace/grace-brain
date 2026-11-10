#!/usr/bin/env python3
"""Rebuild qa-board.built.js and install.html from qa-board.js. Run after editing qa-board.js:
    python3 "Workflows/qa-board/build-bookmarklet.py"

qa-board.built.js is the full board, served from a Dropbox shared link whose URL lives in
hosted-url.txt. The bookmark itself is a short loader that fetches it, so it fits in any
browser's bookmark limit and every machine picks up a rebuild without re-installing.
"""
import hashlib, html, pathlib, re, urllib.parse

here = pathlib.Path(__file__).parent
import base64
src = (here / "qa-board.js").read_text()
logo = here.parent / "assets" / "brand" / "grace-logo-white.png"
src = src.replace("__LOGO_DATA_URI__", "data:image/png;base64," + base64.b64encode(logo.read_bytes()).decode())
import json
src = src.replace("__TAG_SEED__", json.dumps(json.load(open(here / "tag-seed.json")), ensure_ascii=False, separators=(",", ":")))
src = src.replace("__BUILD_VERSION__", hashlib.sha1(src.encode()).hexdigest()[:10])
# drop full-line // comments; leave everything else as-is (no minifier dependency)
body = "\n".join(l for l in src.splitlines() if not re.match(r"\s*//", l))
# every non-ASCII char (emoji, arrows, dashes) lives inside a string literal, so \u-escape them:
# the bookmarklet then works no matter how the page or URL gets decoded
body = "".join(c if ord(c) < 128 else "".join(f"\\u{u:04x}" for u in (lambda b: [int.from_bytes(b[i:i+2], "big") for i in range(0, len(b), 2)])(c.encode("utf-16-be"))) for c in body)
(here / "qa-board.built.js").write_text(body)
bm = lambda js: "javascript:" + urllib.parse.quote(js, safe="!$&'()*+,/:;=?@[]{}<>|^~.-_ ")
full = bm(body)

# Dropbox share link -> direct-content host; it serves the raw file to fetch(), and the
# AhaSlides CSP allows unsafe-eval, so the loader evals it in the page like the full bookmark
url_file = here / "hosted-url.txt"
share = url_file.read_text().strip() if url_file.exists() else ""
if share:
    u = urllib.parse.urlsplit(share)
    q = "&".join(kv for kv in u.query.split("&") if kv and not kv.startswith(("dl=", "raw=", "st=")))
    direct = urllib.parse.urlunsplit(("https", "dl.dropboxusercontent.com", u.path, q, ""))
    href = bm("(()=>{fetch(" + json.dumps(direct) + ",{cache:'no-store'})"
              ".then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.text()})"
              ".then(t=>(0,eval)(t))"
              ".catch(e=>alert('Grace Q&A Board could not load from Dropbox: '+e.message))})()")
else:
    href = full

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Grace Q&amp;A Board: install</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@300;700;900&display=swap">
<style>body{{font-family:Lato,system-ui,sans-serif;background:#E3E3E3;color:#0F2340;max-width:680px;margin:48px auto;padding:0 16px;line-height:1.5}}
h1{{font-weight:300;font-size:36px;margin:0 0 4px}}.eb{{font-weight:900;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#2F97A0}}
a.bm{{display:inline-block;margin:20px 0;padding:12px 22px;background:#1C3B6B;color:#fff;border-radius:8px;text-decoration:none;font-weight:700;cursor:grab}}
ol li{{margin-bottom:8px}}code{{background:#fff;padding:1px 5px;border-radius:4px}}</style></head><body>
<div class="eb">Grace · Sunday Night</div><h1>Q&amp;A Board</h1>
<p>Drag this button to your bookmarks bar:</p>
<a class="bm" href="{html.escape(href, quote=True)}">Grace Q&amp;A Board</a>
<p style="font-size:14px">Offline fallback (full board in the bookmark, about {len(full)//1000}K characters; Firefox and bookmark sync can cut it off): <a href="{html.escape(full, quote=True)}">Grace Q&amp;A Board (offline)</a></p>
<ol>
<li>Open the AhaSlides presentation at <code>presenter.ahaslides.com/presentation/…</code> and make sure you're logged in.</li>
<li>Click <b>Grace Q&amp;A Board</b> in your bookmarks bar. The moderator panel opens on top of AhaSlides.</li>
<li>Click <b>Open display window</b>, drag it to the projector, and double-click it to go fullscreen.</li>
<li>Curate from the panel. <b>Esc</b> hides the panel; click the bookmark again to bring it back.</li>
</ol>
<p>Read-only: the board only <i>reads</i> AhaSlides' question list and never changes the deck. Your curation is saved in this browser per presentation.</p>
</body></html>"""
(here / "install.html").write_text(html)
print(f"qa-board.built.js + install.html written, bookmarklet {len(href):,} chars" + ("" if share else " (no hosted-url.txt yet: full bookmark only)"))
