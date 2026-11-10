---
type: changelog
date: 2026-10-22
tier: 2
touches: ["Workflows/qa-board/build-bookmarklet.py"]
trigger: "Connor"
---
# Q&A board bookmarklet becomes a short Dropbox loader

The QOTN Q&A-board bookmarklet did nothing on the teaching computer: no alert and no panel, so the script never ran. The likely cause is its size. At 89K characters, the whole board is packed into the bookmark, and that gets cut off by Firefox's 65,536-character limit and by bookmark sync.

`build-bookmarklet.py` now also writes `qa-board.built.js`, the full board, to a file served from a Dropbox shared link. The link is stored in `hosted-url.txt`. The bookmark is now a short loader that fetches that file and evals it. AhaSlides' CSP allows `unsafe-eval` and any `connect-src`. A rebuild reaches every machine, with no re-installing. `install.html` keeps the full bookmark as an offline fallback.
