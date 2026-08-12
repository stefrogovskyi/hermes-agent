---
name: multi-profile-server-setup
description: "Manage multi-profile Hermes systemd daemons and git sync."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [hermes, systemd, multi-profile, gateway, telegram, token-isolation, git-sync]
    related_skills: [hermes-agent]
---

# Multi-Profile Server Setup & Token Isolation

## When to Use
Use when configuring or troubleshooting multi-profile Hermes Agent instances running as systemd background services on Linux servers, or setting up Git workspace synchronization.

- `references/vercel-surge-kanban-sync.md` — Detailed guide for Vercel/Surge CLI deployments, `localStorage` + API dual persistence for Kanban boards, and `notranslate` headers to prevent Japanese auto-translation glitches.
- `references/troubleshooting.md` — Diagnostic steps for gateway logs and systemd services.

## Key Concepts & Architecture

1. **Systemd Services per Profile:**
   - Each Hermes profile (`default`, `richard`, `callum`, `alistair`, `ben`, `liz`) runs as an independent systemd daemon: `hermes-<profile>.service`.
   - Executable command: `hermes --profile <profile> gateway run`.

2. **Telegram Token Isolation:**
   - **Critical Pitfall:** When creating a new profile via `hermes profile create <name> --clone`, the new profile inherits `.env` containing `TELEGRAM_BOT_TOKEN` from the source profile.
   - Running two gateways with the same `TELEGRAM_BOT_TOKEN` causes Telegram API polling conflicts (`Conflict: terminated by other getUpdates request`).
   - **Fix:** Each profile must either have its own unique Telegram bot token in `/opt/hermes/profiles/<name>/.env` OR have Telegram polling disabled in `config.yaml`:
     ```yaml
     platforms:
       telegram:
         enabled: false
     ```

3. **Workspace Git Auto-Sync (`git_autosync_hidden.sh`):**
   - User workspace data (skills, scripts, memories, non-secret configs) across all profiles should be tracked via Git.
   - **Crucial `.gitignore` Rules:** Never track `.env`, `auth.json`, or SQLite databases (`*.db`, `*.db-wal`, `*.db-shm`) to prevent token leaks and binary database corruption:
     ```gitignore
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
     hermes-agent/
     profiles/*/.env
     profiles/*/auth.json
     profiles/*/*.db*
     profiles/*/sessions/
     ```

4. **Remote Electron Gateway Access:**
   - Desktop Electron app connects to the remote server via Remote Gateway settings over SSH/Tailscale IP.
   - Closing the local laptop disconnects the Electron GUI client without interrupting 24/7 background agents on the server.

5. **Multi-Device File Indexing vs Replication (Hard Rule):**
   - **Constraint:** Do NOT attempt full file sync or replication from large remote workstations (5+ TB across PCs) onto a server with limited storage (e.g. 500 GB VPS).
   - **Pattern:** Use a **lightweight metadata & FTS5 index** (paths, filenames, extracted text) and fetch/transfer individual files **on-demand** over Tailscale / SMB / SSH when explicitly requested.

6. **Google Drive Trashed File Recovery & Hierarchy Audit:**
   - Files in Google Drive can be moved to trash directly (`trashed: true`) or implicitly via parent folders.
   - To query trashed items via Drive API: `drive search "trashed=true" --raw-query` or `drive search "name contains 'X' and trashed=true" --raw-query`.
   - To restore a trashed file programmatically: send `PATCH https://www.googleapis.com/drive/v3/files/<file_id>?supportsAllDrives=true` with JSON body `{"trashed": false}` using the OAuth access token.

6. **Windows Remote Access & SMB Inspection over Tailscale:**
   - **Windows SMB Guest Access:** Windows 10/11 blocks anonymous SMB by default (`STATUS_ACCESS_DENIED`). To enable guest SMB access:
     ```powershell
     Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters" -Name "AllowInsecureGuestAuth" -Value 1 -Type DWord
     ```
   - **OpenSSH Server Setup (Windows):**
     ```powershell
     Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
     Start-Service sshd
     Set-Service -Name sshd -StartupType 'Automatic'
     New-NetFirewallRule -Name 'OpenSSH-Server-Inbound' -DisplayName 'OpenSSH Server' -Enabled True -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow
     ```
   - **Python Direct SMB Access:** Use `impacket.smbconnection.SMBConnection` with `conn.login("Guest", "")` to list SMB shares and paths over Tailscale without needing local mount points on Linux.

7. **Master Fallback Chain & Key Synchronization:**
   - **Primary Model:** Standardize all profiles on a reliable primary model (e.g., `google/gemini-3.6-flash`). Ensure both `GEMINI_API_KEY` and `GOOGLE_API_KEY` exist in `.env` for compatibility with both `google` and `gemini` provider specs.
   - **Master Fallback Priority Rule (Free First, Paid Last):** All 12 FREE models (`:free` suffix) MUST be placed at the top of the fallback list. Commercial/paid models (`minimax`, `kimi`, `gpt-4o`, `gpt-4o-mini`) MUST be placed at the very end of the priority chain so they are consumed only as an emergency last resort.
   - **Master 16-Step Fallback Chain:**
     ```yaml
     fallback_providers:
       # --- 1. FREE MODELS FIRST (Steps 1 to 12) ---
       - model: poolside/laguna-s-2.1:free
         provider: nous
       - model: nvidia/nemotron-3-ultra-550b-a55b:free
         provider: openrouter
       - model: nvidia/nemotron-3-super-120b-a12b:free
         provider: openrouter
       - model: google/gemma-4-31b-it:free
         provider: openrouter
       - model: google/gemma-4-26b-a4b-it:free
         provider: openrouter
       - model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
         provider: openrouter
       - model: cohere/north-mini-code:free
         provider: openrouter
       - model: openai/gpt-oss-20b:free
         provider: openrouter
       - model: inclusionai/ling-3.0-flash:free
         provider: openrouter
       - model: nvidia/nemotron-nano-12b-v2-vl:free
         provider: openrouter
       - model: nvidia/nemotron-3-nano-30b-a3b:free
         provider: openrouter
       - model: nvidia/nemotron-nano-9b-v2:free
         provider: openrouter

       # --- 2. PAID / COMMERCIAL MODELS AT THE VERY END (Steps 13 to 16) ---
       - model: minimax-m2.7
         provider: gonka24
       - model: kimi-k2.6
         provider: gonka24
       - model: gpt-4o-mini
         provider: openai
       - model: gpt-4o
         provider: openai
     ```
   - **Verification:** Regularly audit all profile `config.yaml` and `.env` files to guarantee no profile lacks fallback entries or active primary API keys.

9. **Interactive Multi-Agent Kanban Boards & Rollback Prevention:**
   - **Preventing Drag-and-Drop Rollbacks & Blank Screens (Pre-baked SSR HTML):** Unpersisted drag-and-drop or client-side fetch delays can make boards appear blank or reset positions. To fix:
     - **Pre-bake Initial Cards in HTML (SSR):** Render initial cards directly inside static `index.html` column containers so the board displays all cards in 0ms without waiting for client-side API fetches or JS hydration.
     - **Floating Action Button:** Add a fixed floating button (`position: fixed; bottom: 24px; right: 24px; z-index: 9999`) for "+ Добавить Задачу" so task creation is 100% visible on any viewport or mobile device.
     - **Dual Persistence:** Save card positions immediately to `localStorage` (`localStorage.setItem('kanban_state_' + agent, ...)`), then send `POST /kanban_api.php` with `{ agent, action: "move_card", card_id, new_column_id }` to update `kanban_store_<agent>.json` on the server.
   - **Disabling Vercel SSO / Deployment Protection Redirects:**
     - **Pitfall:** Vercel projects may default to SSO/Deployment Protection, serving a 477KB login HTML page instead of the 22KB Kanban HTML.
     - **Fix:** Call Vercel REST API (`PATCH https://api.vercel.com/v9/projects/<project_name>?teamId=<team_id>`) with `{"ssoProtection": null, "passwordProtection": null}` to disable protection and ensure public 200 OK access.
   - **Preventing Browser Auto-Translation Glitches (Japanese/Foreign Translation Fix):**
     - Include `<meta name="google" content="notranslate">` and `<meta http-equiv="Content-Language" content="ru">` in `<head>`, and configure `vercel.json` headers with `"Content-Type": "text/html; charset=utf-8"`.
   - **Kanban Hosting Policy (Hard Rule):** All agent Kanban boards MUST be deployed EXCLUSIVELY to Vercel (`https://<agent>-kanban.vercel.app`). **NEVER** deploy or host Kanban boards on the primary production domain `aavalanche.com/kanban/`.
   - **Agent-Specific Themes:** Assign distinct color themes per agent board (Hermes: Cyber Blue/Emerald, Richard: Gold/Emerald, Callum: Electric Cyan/Indigo, Alistair: Executive Violet/Purple, Liz: Coral/Rose, Ben: Growth Orange/Amber).
   - **Daily 08:00 AM Review Cron:** Schedule a daily cron at 08:00 AM (`0 8 * * *`) that polls `kanban_api.php`, aggregates tasks across all agent boards, and delivers a concise Telegram brief.

10. **Context Bloat & Request Timeout Safeguards:**
    - **Request Timeout (`request_timeout_seconds: 30`):** Set `request_timeout_seconds: 30` in `config.yaml` across all profiles so unresponsive API providers or hanging models time out in 30 seconds max (preventing 15-minute hanging loops).
    - **Auto-Compression (`compression.threshold: 0.25`):** Enable `compression.enabled: true`, `compression.threshold: 0.25`, `compression.target_ratio: 0.15` in `config.yaml` across all profiles so context is compressed automatically at 25% capacity (~25k-50k tokens), preventing 450k+ token context bloat and multi-minute API latency.

9. **Airtable PAT Token Synchronization & Base Audit:**
   - Always verify Personal Access Tokens (`PAT`) against `https://api.airtable.com/v0/meta/bases` to confirm active base permissions before running CRM or outreach workflows.
   - Sync `AIRTABLE_API_KEY` and `AIRTABLE_PAT` in both `/opt/hermes/profiles/richard/.env` and master `.env`.

11. **Sub-Agent Interactive Tool Latency & `clarify()` Suspension Pitfall:**
    - **Pitfall:** Invoking interactive tools like `clarify()` in sub-agent profiles (e.g. Richard) suspends the agent execution loop and blocks the thread waiting for UI inline button clicks (up to 45 minutes / 2560 seconds). If the user sends a new message (e.g. asking for a translation or edit) while `clarify()` is waiting, the agent appears "asleep" or unresponsive.
    - **Rule:**
      1. **Never call `clarify()` in sub-agent profiles or automated workflows.** Reply directly in clean, direct plain text in Telegram.
      2. **Always address the user's LATEST message FIRST.** If the user asks for a translation, explanation, or edit, execute that request immediately before proposing unrelated draft or email workflows.

    - To prevent bare plain-text emails, bind official HTML email templates (e.g. `/root/navo24_email_template.html` or `/opt/hermes/richard_official_signature.html`) directly into outreach senders so signatures, logo images, and blue highlighted links (`color: #0000FF`) are rendered automatically on every outbound message.
    - **Official Richard Marlowe HTML Signature Snippet:**
      ```html
      <div style="font-family: Tahoma, Arial, sans-serif; font-size: 10pt; color: #000000; line-height: 1.35; margin-top: 20px; border-top: 1px solid #E2E8F0; padding-top: 16px;">
        <b>Richard Marlowe</b><br>
        <b>Connections Manager</b><br>
        <div style="margin: 8px 0 10px 0;">
          <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
        </div>
        API-MCP for Logistics &amp; Trade<br>
        +44 203 440 9800<br>
        <a href="mailto:rich@navo24.com" style="color: #0000FF; text-decoration: underline;">rich@navo24.com</a><br>
        30 St Mary Axe, London, EC3A 8BF<br>
        <a href="https://www.navo24.com" style="color: #0000FF; text-decoration: underline;">www.navo24.com</a>
      </div>
      ```

12. **Master Connector & Token Synchronization across Profiles:**
    - **Surge CLI Token:** `SURGE_TOKEN` (`82bd19e64bbf196940cf4c78cf9f835a`) allows instant CLI publishing to `stefan-kanban.surge.sh` without interactive login.
    - **Vercel CLI Configuration:** Set `VERCEL_TEAM_ID` (e.g. `GtuxagVBDyZ4qeqAoxNDvVUg`), `VERCEL_PROJECT_ID`, and `VERCEL_TOKEN` in master `.env` and mirror to all sub-profiles.
    - **Master Env Sync Rule:** Periodically run a sync script to propagate all master environment variables (`SURGE_TOKEN`, `VERCEL_TEAM_ID`, `AIRTABLE_PAT`, `GITHUB_TOKEN`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `GONKA24_API_KEY`, `NOUS_API_KEY`, `OPENROUTER_API_KEY`, `SEARATES_API_KEY`, `NAVO_API_KEY`, `HOSTINGER_API_TOKEN`) into `/opt/hermes/profiles/*/.env` so no sub-agent is blocked by missing credentials.


