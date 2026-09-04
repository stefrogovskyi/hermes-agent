# Domain: Operations & Infrastructure

## Agent Kanbans Architecture
- Host: Vercel (`https://<agent>-kanban.vercel.app` / Hermes: `https://hermes-stevenson-kanban.vercel.app`).
- Legacy URL Cleanup: `https://aavalanche.com/kanban/hermes/` and `https://hermes-kanban.vercel.app/` deprecated and removed.
- Backend API: `https://dev.aavalanche.com/kanban_api.php`.
- Bi-directional sync: Dragging cards, updating comments, and status changes on Vercel reflect back to state.db and agent task tracking.

## Telegram Userbot Parser Infrastructure
- Account session: `@stefrogovskiy` (`/opt/hermes/stefan_userbot.session`).
- Active parsing targets: Channel "Не повредит, Одесса" with precise timestamps (HH:MM).
- Safe auth method: Direct `.session` file import without interactive SMS/OTP codes in chat.

## Aeon Stevenson Framework (@aeondeskbot)
- Host/Engine: Native Aeon (`stefrogovskyi/aeon`) running in GitHub Actions cloud runners (Serverless / Cron Polling).
- Purpose: Background task automation, CI/CD skill execution (`/run <skill>`), self-healing scripts, auto-reviewing PRs.
- Telegram Commands: `/status`, `/harness`, `/run <skill>`, `/cancel`.

## 3-Level Sub-Agent Health Check Protocol
- Level 1 (OS): `systemctl is-active hermes-<agent>`
- Level 2 (Telegram API): `getMe` and `getWebhookInfo` / `getUpdates` (token check & pending_update_count)
- Level 3 (Logs): `journalctl -u hermes-<agent>` for `ReadTimeout`, `TimedOut`, `Blocked unauthorized user`, or silent polling freezes.

## SketchForge-3D Local CAD & MCP Bridge
- Host / Service: `sketchforge.service` on port `3030` (`/opt/sketchforge-3d`).
- Access: `http://100.99.146.42:3030/` (Tailscale) / `http://38.49.219.217:3030/`.
- MCP Bridge: `scripts/sketchforge-mcp-server.mjs` providing native geometry creation, scene reading, and viewport screenshot validation for AI agents.
- Skill: `sketchforge-3d` (`/opt/hermes/skills/creative/sketchforge-3d/SKILL.md`).
- Case: `2026-08-25_sketchforge_3d_mcp_cad_editor.md`.

## Harrison Croft (@harrisoncroftbot) Grant Operations
- Objective: Non-dilutive equity-free grant acquisition for Navo24 (up to $500k).
- Focus regions: EU, Qatar, USA, Australia, China, Japan, Canada, G20 countries.
- Email / Identity: `contact@navo24.com`, signed as Harrison Croft.
- Artifacts: Submission reports, Google Sheet tracking link, direct submission reports to Stefan.

## Git Repository Hygiene & History Scrubbing Protocol
- **Prohibited Tracked Patterns:** `*.env`, `*.env.*`, `*token*.json`, `*secret*.json`, `*service_account*.json`, `*credentials*.json`, `*.session`, `*.tar.gz`, `backups/`, `cache/`, `sessions/`, `logs/`, `node_modules/`.
- **Pre-flight Safety Backup:** Before running any destructive Git history rewrites, create an all-inclusive bundle backup:
  ```bash
  git bundle create /root/hermes_pre_filter_backup.bundle --all
  ```
- **Index Cleanup:** Remove untracked files already in index while preserving files on disk:
  ```bash
  git rm -r --cached <path>
  ```
- **Deep History Purge:** Use `git-filter-repo` (inside venv `/opt/hermes/hermes-agent/venv/bin/git-filter-repo`):
  ```bash
  /opt/hermes/hermes-agent/venv/bin/git-filter-repo --invert-paths --paths-from-file /tmp/paths_to_strip.txt --force
  ```
- **GitHub Secret Scanning Response:** If an API key or token was committed, immediately rotate the credential (GitHub Secret Scanning notifies provider APIs within seconds). Merely deleting the file in a new commit does NOT remove it from commit history or stop automated scanners.

