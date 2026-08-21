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
- `references/ai-copywriting-style-priming.md` — Guide on Few-Shot Human Style Priming vs. abstract rules for AI copywriting.
- `references/agentos-and-openclaw-deployment.md` — Complete deployment, systemd daemons, Telegram channel integration, and Admin-gated Hostinger setup for AgentOS (`aavalanche.com/agentos/`) and OpenClaw (`:18789`).

### 17. GitHub Push Protection & Secret Scanning Unblock Pattern
- **Push Protection Block (GH013):** GitHub blocks `git push` if historical commits or tracked markdown files contain strings resembling API keys (Airtable PAT, Vercel tokens, Google Secrets), even on private/personal repos.
- **Resolution Path:**
  1. Inspect the terminal push stderr for generated GitHub unblock URLs (`https://github.com/<owner>/<repo>/security/secret-scanning/unblock-secret/<HASH>`).
  2. Ask the user to click "Allow secret" on those specific links (or remove references and squash/amend git history).
  3. Re-run `git push` immediately after user authorization.

### 18. Multi-Profile Agent Roster
- Added **Harrison Croft** (`harrison`): General Legal Counsel & Chief Compliance Officer at Navo (`hermes-harrison.service`). Focuses on MSA, NDA, API licensing, Maritime/FreightTech compliance (Incoterms 2020, Bill of Lading, FMC, FIATA/BIFA), and enterprise contract redlines.

### 19. Open Pairing Mode & Telegram Allowlist Syntax (Hard Rule)
- **YAML Array Syntax Requirement:** In Hermes Telegram adapter (`platforms.telegram.allow_from` / `group_allow_from`), values must be structured YAML lists, NOT single-quoted JSON string literals:
  ```yaml
  platforms:
    telegram:
      enabled: true
      require_mention: true
      allow_from:
        - "*"
        - "330656040"
      group_allow_from:
        - "*"
  ```
- **Pitfall:** Single-quoted JSON strings like `allow_from: '["*"]'` get evaluated as a literal string set containing `["*"]`, which rejects real numerical Telegram User IDs with `[Telegram] Blocked unauthorized user <ID> in chat <ID>`.

### 20. Telegram Multi-User Consultations vs Owner RBAC Protection
- **Problem & Vulnerability:** When an agent is opened for team-wide consultations (`allow_from: ["*"]`), incoming messages from employees can prompt the bot to offer "Set Home Chat" or allow other users to issue admin slash-commands (`/new`, `/set`, profile reconfiguration), potentially hijacking the bot's delivery destination or changing its persona.
- **Enforcing Owner-Only Governance:**
  1. **Lock `home_channel`:** Explicitly hardcode `home_channel.chat_id: "<OWNER_ID>"` under `platforms.telegram`.
  2. **Restrict `allow_admin_from`:** List exclusively the owner's Telegram ID under `allow_admin_from`.
  3. **Personal Security in `SOUL.md`:** Instruct the agent that Stefan is the sole executive owner; all other team members are clients/colleagues who receive advice but cannot alter system settings.

### 15. Few-Shot Human Style Priming vs Abstract Rules
- **Rule Checklist Pitfall:** Abstract 8-step rules alone do not eliminate the "90% AI" robotic fingerprint.
- **Solution:** Combine Few-Shot Human Examples (`HUMAN_STYLE_GUIDE.md`) with Anti-AI negative prompts and two-pass editing. Route long-form copywriting to Anthropic Claude (Claude 3.5/3.7 Sonnet).
- `references/ai-copywriting-style-priming.md` — Guide on Few-Shot Human Style Priming vs. abstract rules for AI copywriting.

### 15. Agent Identity Recovery & Profile Migration Audits
- **Identity File Hierarchy:** Each profile's persona and core domain boundaries are defined in `/opt/hermes/profiles/<name>/SOUL.md` and `AGENTS.md`, while historical context lives in `/opt/hermes/profiles/<name>/memories/MEMORY.md`.
- **Original Source Audits:** When recovering an agent's original backstory or company context after an "amnesia" report, inspect both the profile's `SOUL.md` and any legacy migration scripts (e.g., `/opt/hermes/scripts/convert_<name>_to_hermes_profile.py` or original Google Drive setup folders) to verify whether the agent originated from a specific entity (e.g. Avalanche Agency / Enlight Group vs Navo).

## Key Concepts & Architecture

1. **Systemd Services per Profile:**
   - Each Hermes profile (`default`, `richard`, `callum`, `alistair`, `ben`, `liz`, `archie`) runs as an independent systemd daemon: `hermes-<profile>.service`.
   - Executable command: `hermes --profile <profile> gateway run`.

16. **OpenClaw & Mission Control Agentic OS Integration:**
    - **OpenClaw Gateway Daemon:** OpenClaw (`/opt/openclaw/app`) runs as `openclaw.service` on loopback port 18789 (`ws://127.0.0.1:18789`). Auth mode configured via `openclaw config set gateway.auth.mode none|token`. CLI executable symlinked to `/usr/local/bin/openclaw`.
    - **Telegram Ingress & Pairing:** OpenClaw Telegram channel uses polling (`openclaw channels add --channel telegram --token <token>`). First-time user messages trigger pairing code approval (`openclaw pairing approve telegram <CODE>`), which sets the user as `commands.ownerAllowFrom`.
    - **Free Model Fallback Architecture & Providers:** To avoid paid tier/401 token expiration traps, configure OpenRouter, HuggingFace, NVIDIA NIM, and Gonka24 free models via `~/.openclaw/openclaw.json` and Hermes `config.yaml`:
      ```yaml
      fallback_providers:
        - provider: google
          model: google/gemini-2.5-flash
        - provider: openrouter
          model: nvidia/nemotron-3.5-lightning:free
        - provider: huggingface
          model: meta-llama/Llama-3.3-70B-Instruct
        - provider: nvidia
          model: nvidia/nemotron-3.5-lightning-30b-a3b
        - provider: gonka24
          model: minimax-m2.7
      ```
      Pass `OPENROUTER_API_KEY`, `HF_TOKEN`, `NVIDIA_API_KEY`, `GONKA24_API_KEY` directly in `openclaw.service` and profile `.env` files.
    - **Mission Control AgentOS Dashboard (`aavalanche.com/agentos/`):**
      - Hosted on Hostinger (`/domains/aavalanche.com/public_html/agentos/index.php`).
      - Protected by Admin-only SQLite session check (`$_SESSION['role'] === 'admin'`).
      - **Critical Redirect Support:** `login.html` MUST read `URLSearchParams(window.location.search).get('redirect')` and redirect back to the target URL after successful login instead of hardcoding `/dashboard`.
      - **Two-Level Submenu Architecture (6 Standard Tabs per Agent):**
        - Leftmost sidebar selects the Agent (`hermes`, `openclaw`, `richard`, `callum`, `alistair`, `archie`, `liz`, `ben`).
        - Secondary submenu renders exactly 6 standard tabs for each agent: `Dashboard`, `Chat`, `Kanban`, `Crons`, `Capabilities`, `Artifacts`.
        - **Subheader Filter Pills:** `Capabilities` filters by `All`, `Skills`, `Tools`, `MCP`, `Browse Hub`; `Artifacts` filters by `All`, `Images`, `Files`, `Links`.
        - **Single-Screen Kanban Grid:** All Kanban boards render in a responsive 4-column layout (`grid-cols-4`) taking 100% viewport width without horizontal wrapping or window scrollbars.
        - **Hermes Desktop Settings Modal:** Accessible via the gear icon in the footer/header; exposes active primary models, parameters, timeouts, and the complete multi-provider catalog (Google, OpenAI, NVIDIA NIM, HF Router, Gonka24, OpenRouter).
        - **Hostinger Proxying & Port Reusability:** When proxying API requests from Hostinger (`agentos/index.php`) to the local VPS daemon (`server.py`), target the external VPS IP (`38.49.219.217:8888`) or configured public proxy, and always enable `SO_REUSEADDR` (`allow_reuse_address = True`) on Python's TCPServer to prevent `Address already in use` (Errno 98) crashes on service restarts.

    - **GitHub Auto-Sync & Permission Scopes (Hard Rule):**
      - **Token Scope Pitfall:** Fine-grained GitHub tokens created without repository write permissions (`Scopes: none` or public-only) will successfully authenticate against user APIs (`https://api.github.com/user`), but fail on `git push` with `403 Forbidden` (`Permission to <repo> denied`).
      - **Automated Sync Workflow:** Ensure `GITHUB_TOKEN` in `.env` has explicit `repo` scope, or configure passwordless SSH (`~/.ssh/id_ed25519.pub` added to GitHub SSH Keys).
      - Cron job `git_autosync_hidden.sh` should execute every 30 minutes (`0302075fc0ce`), automatically staging user data (`skills/`, `memories/`, `memory_v2/`, `scripts/`, `mission-control/`, profile configs), committing updates, and pushing upstream.

    - **Timezone Conversion for Morning Briefs:** Cron expressions in Hermes execute in UTC. To schedule a morning report for 09:00 AM MSK (UTC+3), set the cron schedule to `0 6 * * *` (06:00 UTC). Setting `0 9 * * *` results in delivery at 12:00 PM MSK (3 hours late).
    - **Linux Dynamic Paths in Cron Scripts:** Never hardcode Windows paths (e.g., `C:\Users\Stefan\...`) in scripts executed by cron jobs on Linux servers. Always use `HERMES_HOME = os.environ.get("HERMES_HOME", "/opt/hermes")` and `os.path.join(HERMES_HOME, "cache")` to avoid `FileNotFoundError` during automated background executions.

1.1. **Creating a New Agent Profile Step-by-Step:**
   - Create profile directory structure: `/opt/hermes/profiles/<name>/{memories,skills,platforms/pairing}`.
   - Configure `.env`: set `TELEGRAM_BOT_TOKEN` for the new bot and mirror all master API keys from `/opt/hermes/.env`.
   - Configure `SOUL.md` & `AGENTS.md`: define persona, role, company context, and strict domain boundaries.
   - **Pre-approve Telegram user & RBAC Security:**
     - Write `/opt/hermes/profiles/<name>/platforms/pairing/telegram-approved.json` with owner Telegram ID (`330656040`).
     - In `config.yaml`, configure explicit RBAC to prevent unauthorized users from hijacking Home Chat or administrative commands:
       ```yaml
       platforms:
         telegram:
           enabled: true
           require_mention: true
           home_channel:
             platform: telegram
             chat_id: "330656040"
           allow_admin_from:
             - "330656040"
           allow_from:
             - "*"
           group_allow_from:
             - "*"
       ```
     - In `SOUL.md`, explicitly define the single owner/lead to prevent social engineering / prompt injection aiming to alter agent configuration.
   - **Sync profile metadata to Windows Desktop app across Tailscale:**
     - Copy `SOUL.md`, `AGENTS.md`, `config.yaml`, and `memories/` to `%LOCALAPPDATA%\hermes\profiles\<name>\` on the workstation (`desktop-mst5pt7` / `100.79.157.46`).
   - Systemd unit `/etc/systemd/system/hermes-<profile_name>.service`:
     ```ini
     [Unit]
     Description=Hermes Agent Profile (<profile_name>) Gateway Daemon
     After=network.target network-online.target
     StartLimitIntervalSec=0

     [Service]
     Type=simple
     User=root
     WorkingDirectory=/opt/hermes
     Environment=HERMES_HOME=/opt/hermes
     Environment=HERMES_PROFILE=<profile_name>
     ExecStart=/opt/hermes/hermes-agent/venv/bin/hermes --profile <profile_name> gateway run
     Restart=always
     RestartSec=2s
     KillMode=mixed
     TimeoutStopSec=5s
     StandardOutput=journal
     StandardError=journal

     [Install]
     WantedBy=multi-user.target
     ```
   - Reload and start: `systemctl daemon-reload && systemctl enable hermes-<profile_name>.service && systemctl start hermes-<profile_name>.service`

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

11. **Cross-Profile Isolation Directive & Sub-Agent File Barriers:**
    - **Hard Rule:** Sub-agents (Richard, Callum, Alistair, Liz, Ben, Archie) are strictly prohibited from modifying, editing, or running scripts that alter files, memories, skills, or Kanbans outside their own profile directory (`/opt/hermes/profiles/<self>/`).
    - **Agent Roster & Domain Boundaries:**
      - **Hermes Stevenson** (`@hermes_stevenson_bot`): Orchestrator, cross-profile management, master cron jobs.
      - **Richard Marlowe** (`@richnavobot`): B2B Sales, CRM, outreach, Navo24 leadgen.
      - **Callum Vance** (`@callumvancebot`): Code, GitHub, Vercel/Hostinger deployments, API integrations.
      - **Alistair Sterling** (`@qubicpmbot`): Operations, PM, OODA cycles, strictly managing his own `alistair-kanban` (no cross-agent Kanban control).
      - **Liz Harper** (`@lizharperbot`): HR, onboarding, 10 Human + 10 Digital team synergy.
      - **Ben Jett** (`@benjettbot`): CMO & Growth Manager at **Avalanche Agency & Enlight Group** (PPC, SEO, landing conversions).
      - **Archie Wright** (`@archiewrightbot`): **Content Strategist & Chief Copywriter** (content strategy, copywriting, articles, posts, Tone of Voice).
    - **Sole Orchestrator:** Only the main Hermes Stevenson Orchestrator profile has cross-profile write authority. Sub-agents edit ONLY their own profile and own Kanban (`<agent>-kanban`). Alistair manages strictly `alistair-kanban` and operations; Ben manages strictly `ben-kanban` (PPC/SEO for Avalanche Agency & Enlight Group); Archie Wright manages strictly `archie-kanban` and Content Strategy & Copywriting.

12. **Few-Shot Human Style Priming vs Abstract Rules for AI Copywriting:**
    - **Pitfall:** Writing checklists and multi-step rules alone do NOT eliminate the "90% AI" robotic fingerprint (e.g. "в современном мире", "ключевой аспект", "погрузимся в", excessive bullet lists).
    - **Fix:** Embed 3–5 real human-written text samples into the agent's memory/skill (Few-Shot Style Priming) and use a two-pass editing step with an explicit Anti-AI negative prompt filter.
    - **Model Selection:** Prefer Anthropic Claude (Claude 3.5/3.7 Sonnet) for long-form copywriting tasks over Gemini Flash or GPT-4o-mini due to Claude's lower baseline AI-ism rate.

13. **Windows Desktop App Profile Discovery:**
    - The Hermes Desktop app on Windows scans `%LOCALAPPDATA%\hermes\profiles\`. To make a newly created server profile (e.g. `archie`) appear in the Desktop sidebar, ensure the matching profile directory exists in `%LOCALAPPDATA%\hermes\profiles\<name>\` on the local PC.
    - **Sub-Agent Identity Files & Amnesia Recovery:**
      - Each sub-agent's identity, company affiliation, and domain boundary are defined in `/opt/hermes/profiles/<name>/SOUL.md`, `AGENTS.md`, and `memories/MEMORY.md`.
      - When updating sub-agent identity or memory files from the Orchestrator, pass `cross_profile=True` (if soft guard triggers) and restart the target service (`systemctl restart hermes-<profile>.service`) to apply changes immediately.

12. **Windows Desktop App Profile Discovery:**
    - The Hermes Desktop app on Windows scans `%LOCALAPPDATA%\hermes\profiles\`. To make a newly created server profile (e.g. `archie`) appear in the Desktop sidebar, ensure the matching profile directory exists in `%LOCALAPPDATA%\hermes\profiles\<name>\` on the local PC.

12. **Telegram Group Chat Silence & Bot Loop Shield:**
    - Set `require_mention: true` in `config.yaml` for all group chats.
    - Gateway filter MUST drop messages from `is_bot: true` and untagged replies to prevent infinite bot-to-bot ping-pong chat loops.

13. **Bidirectional Kanban State Persistence & Activity Logging:**
    - **API Backend:** Host `/home/u473746908/domains/aavalanche.com/public_html/dev/kanban_api.php` on Hostinger with CORS enabled (`Access-Control-Allow-Origin: *`).
    - **Client-Side Merging:** JS frontend must merge server cards with default cards (`mergeCards()`) so new tasks added by agents are never hidden by stale browser `localStorage` caches.
    - **Timestamping & Comments:** Record exact timestamps on card drop (`moved_at`) and comment threads (`comments: [{author, text, timestamp}]`) for full auditability during morning 08:00 AM briefs.

14. **Userbot Session Authorization & Security Guardrails:**
    - **Telegram Security Guard Pitfall:** Entering Telegram 5-digit verification codes sent in chat text triggers Telegram Security Guard blocking and revokes the login attempt.
    - **Safe Authorization Pattern:** Copy an authorized `.session` file (e.g. `stefan_userbot.session`) over Tailscale or receive it directly as an un-inlined Telegram document attachment.
    - **Permissions & Git Security:** Always set `chmod 600 /opt/hermes/*.session` so session files are readable only by root on Servarica. Always add `*.session` to `.gitignore`.
    - **Read-Only Sensor Rule:** Userbot sessions must strictly operate as READ-ONLY sensors (`get_dialogs`, `get_messages`). Agents must NEVER impersonate the user or send messages from the user account. Sub-bots must send messages only from their own bot tokens.

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


