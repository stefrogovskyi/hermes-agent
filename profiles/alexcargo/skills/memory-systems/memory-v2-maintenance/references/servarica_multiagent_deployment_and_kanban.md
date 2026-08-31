# Servarica Multi-Agent Cluster Deployment & Vercel Kanban Integration

## 1. Servarica KVM VPS Cluster Architecture
- **Host Specs:** Servarica KVM Slim Slice 4 (`stefan1` @ `38.49.219.217`), Ubuntu 24.04 LTS, 4 vCPU, 16 GB RAM, 500 GB NVMe SSD.
- **Tailscale Mesh Network:** Private IPv4 `100.99.146.42` connecting Servarica Cloud VPS directly to Stefan's Desktop (`100.79.157.46` / OpenSSH Port 22 / SMB Port 445) and Phone (`100.82.254.104`).
- **24/7 Systemd Daemon Services:**
  - `hermes-default.service` (Hermes Stevenson Orchestrator)
  - `hermes-callum.service` (Callum Vance Tech Lead)
  - `hermes-richard.service` (Richard Marlowe Sales)
  - `hermes-alistair.service` (Alistair Sterling PM)
  - `hermes-liz.service` (Liz Harper CPO)
  - `hermes-ben.service` (Ben Jett Marketing)

## 2. Hard Security Guardrails
- **User Impersonation:** NO agent or sub-bot may EVER post or send messages as Stefan / user account. Every agent writes strictly from its own official Bot API account.
- **Auto Git Commit & Push:** All code changes and web updates must automatically commit and push to GitHub (`git commit -am "..." && git push origin main`) with zero manual push steps required from Stefan.
- **DP World Vacancies Isolation:** DP World vacancies cron poller belongs SOLELY to Hermes Stevenson DM ONLY (`chat_id: 330656040`). Sub-agents must never monitor or handle it.

## 3. Systemd Environment & Multi-Agent Operations Pitfalls
- **Systemd `HERMES_HOME` Profile Root:** In systemd unit files (`hermes-<profile>.service`), always set `Environment=HERMES_HOME=/opt/hermes` (base installation root). Do NOT set `HERMES_HOME=/opt/hermes/profiles/<profile>` when passing `--profile <profile>` to `hermes gateway run`. Setting `HERMES_HOME` to the profile directory causes Hermes to search for nested `profiles/<profile>` subfolders, resulting in path fallback pollution and stray Windows directories (`/root/C:\Users\...`) on Linux.
- **Cross-OS Cron Job Isolation:** Syncing `cron/jobs.json` across Windows Desktop and Linux VPS via Git causes Windows-specific path scripts (`C:\Users\...`) to execute on Linux and duplicate heavy tasks (FTS indexers, memory harvests). Separate execution responsibilities: VPS runs 24/7 Telegram gateways, background pollers, and server watchdogs; Desktop handles local GUI and Windows file indexing.
- **`memory_v2` Case File Synchronization:** Mirror `memory_v2/cases/` and `principles/` from the Windows host to `/opt/hermes/memory_v2/` on VPS so sub-agents running as systemd services can execute local keyword queries (`recall.py`) across all historical case files.

## 3. Per-Agent Vercel Trello-Style Kanban Boards
Each agent manages their own distinct Vercel Kanban Board with custom color themes:
- **Hermes Stevenson:** `https://hermes-stevenson-kanban.vercel.app` (100% Vercel Serverless API `/api/kanban`, no third-party domain dependencies)
- **Callum Vance:** `https://callum-vance-kanban.vercel.app` (Cyan Tech Theme)
- **Richard Marlowe:** `https://richard-marlowe-kanban.vercel.app` (Gold Sales Theme)
- **Alistair Sterling:** `https://alistair-sterling-kanban.vercel.app` (Royal Purple Ops Theme)
- **Liz Harper:** `https://liz-harper-kanban.vercel.app` (Magenta HR Theme)
- **Ben Jett:** `https://ben-jett-kanban.vercel.app` (Neon Amber Marketing Theme)
- **Daily Briefing Cron:** Hermes Stevenson runs `hermes_kanban_daily_briefing` daily at 08:00 AM MSK (`0 8 * * *`), reviewing board cards and delivering a short status summary to Stefan in Telegram DMs.
