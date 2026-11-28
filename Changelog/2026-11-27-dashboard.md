# 2026-11-27 — Dashboard added to the quick refresh

**Asked by Connor:** "separate out the Sunday service itself as its own thing … check the status of everything else … a dashboard for everything I help with and could look at that during every quick refresh."

**What changed**
- New `Workflows/dashboard.py` → writes `Trackers/Dashboard.md`. Groups live action notes into workstreams (filename rules, overridable with a `workstream:` frontmatter field), computes health, lists Connor's next actions and waits, and plots a 10-week date strip.
- New `Trackers/Milestones.md` — hand-kept fixed dates (events, series starts, travel) for the strip.
- `Workflows/grace-quick-refresh.md`: Phase 3a runs the script after the sweep; report gains Part 0 (the per-stream summary line).

**Why a generated note, not an artifact or Notion:** the refresh already runs in the vault and the data is vault frontmatter; a script-written note can't drift from the source and costs one command per run.

**Later the same day — artifact.** Connor asked for the dashboard as an artifact: [Grace Workstreams](https://claude.ai/artifact/TWyVStuKWc19V79JfW5rCH) (Data type). `dashboard.py --json <dir>` writes its three data files; Phase 3a re-uploads them each refresh and repoints the datasets. The vault note stays the source of truth.
