# Vault → GitHub sync: setup plan (draft for Connor's approval)

**Goal:** let the 5am cloud routine read *and write* the vault, which the Dropbox connector can't do because it can't overwrite files (found 2026-11-10).

## One change from what we discussed: the vault doesn't move

Git's internal folder (`.git`) is the part Dropbox corrupts. So we keep it **outside Dropbox** (`~/GraceBrain.git`) and point it at the vault folder where it already is. That way:
- No path changes. All 8 scheduled tasks, Claude's memory folder, `.claude/settings.local.json` and this desktop session keep working untouched. Each of them has the current Dropbox path written in.
- Dropbox keeps syncing the files as it does now. It becomes a second backup, not the sync mechanism.
- Obsidian still opens the same folder.

## Steps

| # | Who | What |
|---|-----|------|
| 1 | Connor | Create (or sign in to) a GitHub account and make one **private** repo, e.g. `grace-brain`. Free. |
| 2 | Claude | Write `.gitignore` (below), run a secrets scan over everything that *would* be committed, and show you the list before anything leaves the Mac. |
| 3 | Claude | Create the repo with its `.git` folder at `~/GraceBrain.git`, make the first commit, and generate an SSH key for this Mac. |
| 4 | Connor | Paste that SSH public key into the repo's **Deploy keys** with write access. This works on this one repo only, not your whole GitHub account. |
| 5 | Claude | First push, then add a background job (a macOS `launchd` agent) that runs `Workflows/vault-git-sync.sh` every 15 min: commit local changes → pull → push. **If a pull hits a conflict, it stops, leaves both versions untouched and logs it.** It never auto-resolves or force-pushes. |
| 6 | Connor | On claude.ai, connect GitHub to Claude and allow the `grace-brain` repo for the routine's cloud environment. |
| 7 | Claude | Rewrite the 5am routine's prompt to work on the cloned repo, commit, and push. Dropbox stays only for reading `/Office`. You review the prompt before it's saved. |
| 8 | Both | Test run → check the commit on GitHub and that the Mac pulled it. If it works, retire `agent-hub-visit-local` (4 AM), or keep it for the text scan only. |

## Kept out of GitHub (`.gitignore`)

- `Contacts/Credentials.md`: passwords never leave the Mac.
- `Contacts/*.vcf`: your exported address book (720 contacts).
- `Contacts/Phone-Index.md`: phone number → name map. Only the Mac's text scan uses it.
- `.obsidian/workspace*`, `.DS_Store`, `.claude/settings.local.json`: machine-local clutter.
- `Archive/_Stray-Vault-Content-2026-07-01/`: the old Connor–Sky finance vault plus a migration zip (personal, not Grace). Found by the step-2 scan.
- All `*.vcf` anywhere, including the two archived contact exports.

**Effect:** the cloud run can't see these files, which is fine, because none of its steps use them.

## Risks, honestly

- **Two writers at once:** the background job and a local Claude task could edit the same note within the same 15 minutes. Different lines merge fine. Same-line edits stop the sync and wait for a fix, rather than silently losing an edit.
- **Private ≠ secret:** GitHub staff and anyone you add to the repo can read it. The vault holds names, phone numbers and church-internal notes, so this is the same trust call as Dropbox, just with a different company.
- **Undo:** stop the job, delete `~/GraceBrain.git`, and the vault is exactly what it is today.

## Progress

- 2026-11-10: steps 2–3 done. `.gitignore` written, secrets scan clean (only false positives in Obsidian plugin code), local repo at `~/GraceBrain.git` with the first commit (1,086 files), deploy key `~/.ssh/grace_brain_deploy` generated.

- 2026-11-10: steps 4–5 done. Repo `connorfrey-trygrace/grace-brain`, first push OK. **Change to step 5:** macOS blocked the launchd job from reading the Dropbox folder ("Operation not permitted"), so the sync now runs from Claude Code session hooks instead: `SessionStart` (async) and `SessionEnd` in `.claude/settings.local.json`, calling `Workflows/vault-git-sync.sh`. Every Claude session in this vault syncs, the scheduled tasks included. Log: `~/Library/Logs/grace-brain-sync.log`. The unused launchd plist is in `Archive/LaunchAgents/`.

- 2026-11-10: steps 6–8 done. Routine prompt rewritten (see [[Reference/5am-Routine-Prompt-Draft]]) with the repo attached. First test failed with a 403 (GitHub connected but the Claude GitHub App wasn't installed). After Connor installed it, the retest pushed `95ba213` to main, the Mac pulled it, and clock-check passed.

## What I need from you

Nothing more. Open decision: what happens to the 4 AM local task (`agent-hub-visit-local`) now that the cloud covers email + Notion.
