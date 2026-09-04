# Case: Git Leak Remediation, Git-Filter-Repo History Scrubbing & Security Hygiene

**Date:** 2026-09-04  
**Category:** `ai_infra` / `ops_infrastructure` / `security`  
**Status:** Resolved (History purged, tracked count reduced from 106,703 to 8,613)

---

## 1. Context & Incident Description
On 2026-09-03 at 05:52 UTC, commit `bd697340` (`fix(openclaw): properly configure nous provider with access_token and wire clean fallbacks`) was pushed to `stefrogovskyi/hermes-agent.git`.
During git staging, 99,760 untracked and service files were accidentally swept into the commit, including:
- Large backup archives (`backups/richard_profile_backup_*.tar.gz` >57MB).
- Google OAuth credentials (`google_token.json`, `google_client_secret.json`).
- Telegram & WhatsApp session credentials (`stefan_userbot.session.bak`, `auth_info_baileys/`).
- Cache files containing an old Resend API key (`re_HYSmY1vz...`).

GitHub Secret Scanning immediately detected the key signature upon receiving the push, notified Resend's partner security endpoint, and Resend revoked the key automatically, triggering an email alert to Alexey.

---

## 2. Analysis & Core Principles from Stefan
1. **Merely Deleting Files in a New Commit Fails:**
   Removing files via `git rm` in a subsequent commit leaves the files and secrets embedded in previous commit trees. Automated scrapers, GitHub Secret Scanning, and forks retain access to `.git/objects/`.
2. **Strict `.gitignore` Boundary:**
   The repository must enforce unambiguous exclusion patterns:
   - `*.env`, `*.env.*`, `*.key`, `*.pem`
   - `*token*.json`, `*secret*.json`, `*service_account*.json`, `*credentials*.json`
   - `*.session`, `*.session.bak`, `*.tar.gz`
   - `backups/`, `cache/`, `sessions/`, `logs/`, `state/`, `node_modules/`
3. **Heavy Archives (>50MB) Prohibition:**
   GitHub issues soft warnings above 50MB and rejects objects >100MB. Profile backups and heavy dumps belong exclusively in local unversioned storage (`/opt/hermes/backups/`) or cloud object storage.

---

## 3. Resolution Steps

### Step 1: Pre-Flight Safety Backup
Before altering git history, a complete local bundle backup was created:
```bash
git bundle create /root/hermes_pre_filter_backup.bundle --all
```

### Step 2: Strict `.gitignore` Overhaul
Updated `/opt/hermes/.gitignore` with exhaustive rules blocking all secret masks, session files, node_modules, and cache directories across root and profile subdirectories.

### Step 3: Git Index Pruning
Untracked all matching files from the Git staging index while leaving disk files intact:
```bash
python3 -c "
import subprocess
patterns = [
    'services/whatsapp-gateway/auth_info_baileys',
    'profiles/richard/services',
    'profiles/*/lsp',
    'profiles/richard/searates_archive',
    'profiles/*/state.db*',
    'backups'
]
for p in patterns:
    subprocess.run(['git', 'rm', '-r', '--cached', p], check=False)
"
```
Tracked files dropped from 106,703 to 8,613 clean files.

### Step 4: Full History Scrubbing via `git-filter-repo`
Using `git-filter-repo` installed in the active venv (`/opt/hermes/hermes-agent/venv/bin/git-filter-repo`):
```bash
/opt/hermes/hermes-agent/venv/bin/git-filter-repo \
    --invert-paths \
    --paths-from-file /tmp/paths_to_strip.txt \
    --force
```
All historical occurrences of tokens, sessions, WhatsApp credentials, and heavy tarballs were purged from all tree objects in Git history.

---

## 4. Verification & Artifacts
- Git log verified clean with revised commit tree hashes (`7fc451e`, `26e3db1`, `04fe4c2`).
- Tracked file count: **8,613** (only code, scripts, skills, and configuration templates).
- Pre-filter safety bundle stored at `/root/hermes_pre_filter_backup.bundle`.
