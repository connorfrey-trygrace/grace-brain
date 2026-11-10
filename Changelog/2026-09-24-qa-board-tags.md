# 2026-09-24 — Q&A Board: categories → tags, no catch-all

- **What:** every question now carries 1–3 **tags**, and the first is its main tag. This replaces one category per question and the "Everything else" bucket.
- **Vocabulary (26):** Hearing God · The Holy Spirit · Discernment & decisions · Who God is · Who Jesus is · Suffering & pain · Does God care about me? · Faith & doubt · Worry & anxiety · The Bible · Science & faith · Salvation & the only way · Death & the end times · God's control & free will · Purpose & calling · Formation & habits · Sin & forgiveness · Dating, sex & marriage · Sharing your faith · Faith & culture · Everyday faith · Church & worship · Life at Grace · Words & names · Money & work · Sunday's message.
- **Seed:** `Workflows/qa-board/tag-seed.json` holds 95 questions, hand-tagged on 2026-09-24: every real question on the live board, including 11 submitted after the 9/21 analysis. It's keyed by the first 60 characters of the normalised text. The 6 test submissions ("New test", "This is a test for Sky", etc.) are deliberately untagged. `theme-seed.json` is no longer read by the build.
- **Newer questions:** up to 3 tags from the keyword rules, in priority order. If nothing matches, the question is **Untagged**: the panel's filter shows it, and it counts toward no tag.
- **Behaviour:**
  - The sidebar is **Top tags**: each unanswered, visible question counts once per tag.
  - "Same category" rotation shows questions carrying the QOTN's main tag, and the label names that tag.
  - Panel rows show tag chips: click a chip to make it the main tag, × removes it, and **+ tag** adds one.
  - The panel filter is by tag, with counts and an **Untagged** option.
  - Overrides are stored in `S.tagOverride`; old single-category overrides are dropped.
- **Fix:** titles wrapped in quote marks ("…") now match the seed, because normalisation strips the wrapping quotes.
- **Tested:** in the local mock: Top tags ranking, chips (make main / remove / add), and rotation on the main tag (14 questions tagged "Suffering & pain").
- **Archived:** `Workflows/qa-board/theme-seed.json` moved to `Archive/qa-board/theme-seed.json` (Connor approved). The tag-based build doesn't read it.
