#!/bin/bash
# git_autosync_hidden.sh — Auto-sync Hermes Agent repo, skills, scripts and memories

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

HERMES_DIR="/opt/hermes"
LOG_FILE="$HERMES_DIR/logs/git_autosync.log"
mkdir -p "$HERMES_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [GitAutosync] $1" | tee -a "$LOG_FILE"
}

# 1. Fetch Github Token from .env
if [ -f "$HERMES_DIR/.env" ]; then
    GH_TOKEN=$(grep -E "^GITHUB_TOKEN=" "$HERMES_DIR/.env" | cut -d= -f2 | tr -d '\r\n')
fi

cd "$HERMES_DIR" || exit 1

# 2. Ensure git config
git config user.name "Stefan Rogovskiy"
git config user.email "dr.reenforce@gmail.com"

# 3. Add changes
git add skills/ scripts/ memories/ memory_v2/ config.yaml SOUL.md mission-control/ profiles/*/config.yaml profiles/*/SOUL.md profiles/*/memories/ profiles/*/skills/ >/dev/null 2>&1

UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
    COMMIT_MSG="auto-sync: update AgentOS, skills, memories, and ecosystem ($(date '+%Y-%m-%d %H:%M'))"
    git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1
    log "Committed $UNCOMMITTED updates: $COMMIT_MSG"
else
    log "No local changes to commit."
fi

# 4. Push to remote if token is present
if [ -n "$GH_TOKEN" ]; then
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "master")
    AUTH_REMOTE="https://stefrogovskyi:${GH_TOKEN}@github.com/stefrogovskyi/hermes-agent.git"
    
    # Push changes
    git push "$AUTH_REMOTE" "$CURRENT_BRANCH" >> "$LOG_FILE" 2>&1
    if [ $? -eq 0 ]; then
        log "Successfully pushed $CURRENT_BRANCH to github.com/stefrogovskyi/hermes-agent!"
    else
        log "Failed to push to GitHub remote."
    fi
else
    log "Skipping push: GITHUB_TOKEN not found."
fi

log "Git Autosync completed."
exit 0
