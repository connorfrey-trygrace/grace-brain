# 2026-11-10 — Vault synced to a private GitHub repo

**Changed:** the vault is now a git repo (git data at `~/GraceBrain.git`, outside Dropbox), pushed to private `connorfrey-trygrace/grace-brain`. `Workflows/vault-git-sync.sh` commits → fetches → merges → pushes; Claude Code `SessionStart`/`SessionEnd` hooks run it. Excluded from GitHub: `Contacts/Credentials.md`, all `*.vcf`, `Contacts/Phone-Index.md`, `Archive/_Stray-Vault-Content-2026-07-01/`, and machine-local clutter.

**Why:** the 5am cloud routine can't write the vault through the Dropbox connector (no overwrite). A git clone it can push to fixes that. Plan and progress: [[Reference/Vault-Git-Sync-Plan]].

**Deviation from the plan:** a 15-min launchd job was the original step 5. macOS refused it access to the Dropbox folder, so the sync moved to session hooks. The hooks need no security-setting changes.

**Also fixed:** `.claude/settings.local.json` had a missing comma, so Claude Code was ignoring the whole file, including the PCO auto-mode allow rule.

**Result:** the 5am routine now clones the repo and pushes to main. First test failed with a 403 (the Claude GitHub App wasn't installed); the retest after Connor installed it pushed `95ba213`, and the Mac merged it cleanly.
