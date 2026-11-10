#!/bin/bash
# Grace Brain vault <-> GitHub sync. Run every 15 min by launchd
# (~/Library/LaunchAgents/org.trygrace.grace-brain-sync.plist).
# Commit local changes -> fetch -> merge -> push.
# On a merge conflict it aborts the merge, leaves every file as it was,
# logs it and shows a notification. It never force-pushes or auto-resolves.
# Plan: Reference/Vault-Git-Sync-Plan.md

VAULT="$HOME/Library/CloudStorage/Dropbox/Vaults/Grace Brain"
LOG="$HOME/Library/Logs/grace-brain-sync.log"
LOCK="/tmp/grace-brain-sync.lock"
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"

log() { echo "$(TZ=America/New_York date '+%Y-%m-%d %H:%M ET') $*" >> "$LOG"; }
alert() { /usr/bin/osascript -e "display notification \"$1\" with title \"Grace Brain sync\"" >/dev/null 2>&1; }

mkdir "$LOCK" 2>/dev/null || { log "skip: previous run still going"; exit 0; }
trap 'rmdir "$LOCK"' EXIT

cd "$VAULT" || { log "ERROR: vault folder not reachable"; alert "Vault folder not reachable"; exit 1; }

GITDIR="$(git rev-parse --git-dir 2>/dev/null)"
if [ -z "$GITDIR" ] || [ -f "$GITDIR/MERGE_HEAD" ] || [ -d "$GITDIR/rebase-merge" ] || [ -d "$GITDIR/rebase-apply" ]; then
  log "STOPPED: repo missing or a merge is unfinished. Needs a person."
  alert "Sync stopped: unfinished merge. Ask Claude to look."
  exit 1
fi

git add -A >/dev/null 2>&1
if ! git diff --cached --quiet; then
  n=$(git diff --cached --name-only | wc -l | tr -d ' ')
  git commit -q -m "Mac auto-sync: $n file(s)" || { log "ERROR: commit failed"; exit 1; }
  log "committed $n file(s)"
fi

if ! git fetch -q origin 2>>"$LOG"; then
  log "offline or GitHub unreachable; will retry"
  exit 0
fi

if ! git merge -q --no-edit origin/main >/dev/null 2>&1; then
  files=$(git diff --name-only --diff-filter=U | tr '\n' ';')
  git merge --abort >/dev/null 2>&1
  log "CONFLICT with GitHub, merge aborted, nothing changed: $files"
  alert "Sync conflict: $files Ask Claude to look."
  exit 1
fi

if [ "$(git rev-list --count origin/main..HEAD)" != "0" ]; then
  if git push -q origin main 2>>"$LOG"; then
    log "pushed"
  else
    log "ERROR: push failed (will retry next run)"
  fi
fi
exit 0
