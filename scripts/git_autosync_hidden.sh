#!/bin/bash
# git_autosync_hidden.sh — Auto-sync Hermes Agent repo, skills, scripts and memories

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

HERMES_DIR="/opt/hermes"
LOG_FILE="$HERMES_DIR/logs/git_autosync.log"
mkdir -p "$HERMES_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [GitAutosync] $1" | tee -a "$LOG_FILE"
}

log "Starting Git Autosync run..."

# 1. Sync hermes-agent repository
if [ -d "$HERMES_DIR/hermes-agent/.git" ]; then
    cd "$HERMES_DIR/hermes-agent" || exit 1
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    
    # Fetch latest
    git fetch origin >/dev/null 2>&1
    
    # Pull rebase if behind
    BEHIND=$(git rev-list --count HEAD..origin/"$CURRENT_BRANCH" 2>/dev/null || echo "0")
    if [ "$BEHIND" -gt 0 ]; then
        log "Pulling $BEHIND new commits on branch $CURRENT_BRANCH..."
        git pull --rebase origin "$CURRENT_BRANCH" >> "$LOG_FILE" 2>&1
    else
        log "hermes-agent repo is up to date on $CURRENT_BRANCH."
    fi
fi

# 2. Check/Initialize Git for /opt/hermes user data (skills, scripts, memories)
if [ ! -d "$HERMES_DIR/.git" ]; then
    log "Initializing git repository in $HERMES_DIR for user workspace sync..."
    cd "$HERMES_DIR" || exit 1
    git init >> "$LOG_FILE" 2>&1
    
    cat << 'EOF' > "$HERMES_DIR/.gitignore"
*.db
*.db-journal
*.db-wal
*.db-shm
*.pid
*.lock
*.log
.env
auth.json
audio_cache/
image_cache/
sessions/
logs/
cache/
state/
kanban/
pairing/
pending_messages/
cron/output/
models_dev_cache.json
hermes-agent/
profiles/*/.env
profiles/*/auth.json
profiles/*/*.db*
profiles/*/sessions/
profiles/*/logs/
profiles/*/cache/
profiles/*/state/
profiles/*/cron/output/
EOF
    git config user.name "Hermes Agent (Stefan Servarica)"
    git config user.email "dr.reenforce@gmail.com"
fi

# Auto-commit local changes to skills, scripts, memories, config (excluding secrets/dbs)
cd "$HERMES_DIR" || exit 1
git add skills/ scripts/ memories/ config.yaml SOUL.md profiles/*/config.yaml profiles/*/SOUL.md profiles/*/memories/ profiles/*/skills/ >/dev/null 2>&1

UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l)
if [ "$UNCOMMITTED" -gt 0 ]; then
    COMMIT_MSG="auto-sync: update skills, memories, and scripts ($(date '+%Y-%m-%d %H:%M'))"
    git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1
    log "Committed $UNCOMMITTED local updates: $COMMIT_MSG"
else
    log "No changes in skills, memories, or scripts."
fi

log "Git Autosync completed successfully."
exit 0
