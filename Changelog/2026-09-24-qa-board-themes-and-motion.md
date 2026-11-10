# 2026-09-24 — Q&A Board: themes sidebar + motion pass

- **What:** a right-hand sidebar titled "What the room is asking" ranks the top 6 themes by number of questions (default) or votes, across all questions or unanswered only. "Everything else" is excluded. Each question in the moderator panel has a theme dropdown for overrides. A motion pass responds to "doesn't feel as alive":
  - a pulsing **Live** dot
  - counters that pulse when they change
  - new cards rise in, staggered on first open
  - theme bars grow and rows slide into their new rank instead of jumping
  - the rank's count flashes when a theme gains a question
  - reactions float the full height of the screen
  - the question-of-the-night rule slowly breathes between Active Blue and Cloud Gray
- **How themes are assigned:** in order, (1) moderator override; (2) exact-text match against `Workflows/qa-board/theme-seed.json`, which holds 84 questions from the editorial grouping in `Events/2026-09-20-Sunday-Night-Service/2026-09-27-Sunday-Night-Service-Question-Board.html` (themes A–I, plus W for Worry & peace from the answered set); (3) keyword rules in `qa-board.js`; (4) Everything else.
- **Architecture change:** the display is now built once, and each region (hero, cards, themes, footer, stats) updates in place against its own key. A vote ticking over no longer redraws, and re-animates, the whole board. Cards that would be clipped by the footer are hidden whole. All reads use `cache: 'no-store'`.
- **Tested:** in a local mock with seed-text fixtures and simulated activity: 4 new questions reordered the themes, and a reaction burst, counter tick and pop-up all showed up in screenshots.
- **Caveat:** keyword rules are coarse. New questions after 9/21 can land in the wrong theme until they're re-seeded or overridden.
- **Follow-up (same day):** the themes sidebar now counts only unanswered questions, at Connor's request. The all/unanswered toggle was removed, and the sidebar subtitle reads "Unanswered · by number of questions".
- **Follow-up 2:** vote counts now use an outline thumbs-up SVG in currentColor (Feather's `thumbs-up`, MIT) instead of `▲`. The sidebar is titled "Top categories". The display window no longer shows `about:blank`: it opens AhaSlides' plain-text `/robots.txt` (same origin, no app scripts), writes the board over it, and renames the URL to `/grace-sunday-night-qa` with `history.replaceState`. The tab title is "Grace · Sunday Night Q&A". **Refreshing that window breaks it**, because the renamed URL doesn't exist on AhaSlides; reopen it from the panel instead.
