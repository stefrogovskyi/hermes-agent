# AgentOS (Mission Control) & OpenClaw Gateway Architecture

## 1. OpenClaw Setup & Systemd Service
- **Source/Directory:** `/opt/openclaw/app` (Node.js v22.x + pnpm build)
- **Binary CLI:** symlinked at `/usr/local/bin/openclaw`
- **Systemd Service:** `/etc/systemd/system/openclaw.service`
  ```ini
  [Unit]
  Description=OpenClaw Gateway Service
  After=network.target

  [Service]
  Type=simple
  User=root
  WorkingDirectory=/opt/openclaw/app
  Environment=PATH=/usr/local/bin:/usr/bin:/bin:/root/.local/bin
  Environment=NODE_ENV=production
  Environment=OPENROUTER_API_KEY=<key>
  Environment=HF_TOKEN=<token>
  Environment=NVIDIA_API_KEY=<key>
  Environment=GONKA24_API_KEY=<key>
  ExecStart=/usr/bin/node /opt/openclaw/app/dist/entry.js gateway run --port 18789 --bind loopback
  Restart=always
  RestartSec=5

  [Install]
  WantedBy=multi-user.target
  ```
- **Gateway Endpoint:** `ws://127.0.0.1:18789` and Web UI at `http://<tailscale-ip>:18789`
- **Telegram Channel Configuration & Pairing:**
  1. Add channel: `openclaw channels add --channel telegram --token "<BOT_TOKEN>"` (Connected to `@clawstevensonbot`).
  2. First inbound user message will prompt for device pairing approval. Run:
     `openclaw pairing approve telegram <PAIRING_CODE>`
  3. This configures the user as `commands.ownerAllowFrom`.

- **5-Tier Multi-Provider Fallback Cascade:**
  To eliminate 401 Unauthorized errors and multi-minute rate limit hanging, configure tight timeouts (6–8s) and the 5-tier fallback cascade in `~/.openclaw/openclaw.json`:
  1. **Tier 1 (OpenRouter Free):** `openrouter/nvidia/nemotron-3.5-lightning:free` (0.4s), `google/gemma-4-26b-a4b-it:free`, `openai/gpt-oss-20b:free`.
  2. **Tier 2 (Nous Research):** Direct token profile in `auth-profiles.json`.
  3. **Tier 3 (Hugging Face Router):** `huggingface/meta-llama/Llama-3.3-70B-Instruct` & `Qwen/Qwen2.5-72B-Instruct` via `https://router.huggingface.co/v1`.
  4. **Tier 4 (NVIDIA NIM Direct Cloud API):** `nvidia/nvidia/nemotron-3.5-lightning-30b-a3b`, `nvidia/nvidia/llama-3.3-nemotron-super-49b-v1.5`, `nvidia/meta/llama-3.1-8b-instruct` via `https://integrate.api.nvidia.com/v1`.
  5. **Tier 5 (Gonka24 API):** `gonka24/deepseek-v4-flash-0731`, `gonka24/kimi-k2.6`, `gonka24/minimax-m2.7` via `https://api.gonka24.com/v1`.

## 2. AgentOS Enterprise UI Deployment & Hosting

### A. Local VPS Backend & SQLite Proxy API
- **Location:** `/opt/hermes/mission-control/` (`index.php`, `server.py`)
- **Systemd Service:** `/etc/systemd/system/mission-control.service` (Port 8888)
- **Socket Reusability (`SO_REUSEADDR`):** Python's `socketserver.TCPServer` must set `allow_reuse_address = True` in `server.py` to prevent `Address already in use` (Errno 98) on rapid daemon restarts.
- **API Endpoints:**
  - `GET /api/messages?profile=<name>&limit=50` — real-time extraction from SQLite `/opt/hermes/state.db` and `/opt/hermes/profiles/<name>/state.db`.
  - `POST /api/send_message` — live 2-way message submission directly into profile SQLite databases.
  - `GET /api/kanban?profile=<name>` — live cards from `https://dev.aavalanche.com/kanban_api.php`.
  - `GET /api/crons` — live cron tasks from `/opt/hermes/cron/jobs/*.json`.
  - `GET /api/capabilities` — skills, tools, MCP servers, and browse hub.
  - `GET /api/artifacts` — generated images, files, and external links.
  - `GET /api/settings` — global parameters and multi-provider model catalog.

### B. Production Hostinger Gateway (`aavalanche.com/agentos/`)
- **Location on Hostinger:** `/home/u473746908/domains/aavalanche.com/public_html/agentos/index.php`
- **Security & Role Gate:**
  Integrated with existing SQLite database (`/home/u473746908/domains/aavalanche.com/public_html/data/database.sqlite`).
  Protected strictly for users with `role === 'admin'`.
  Unauthorized/non-admin visits automatically redirect to `/login.html?redirect=/agentos/`.
- **Redirect Bugfix in `login.html`:** The frontend checks `new URLSearchParams(window.location.search).get('redirect')` upon login success and forwards to the target path instead of hardcoding `/dashboard`.
- **Public IP Proxying:** Hostinger cannot reach internal Tailscale IPs directly. The API proxy in `agentos/index.php` targets the VPS public IP (`38.49.219.217:8888`).

## 3. Navigation Hierarchy & 6 Standard Tabs per Agent
- **Level 1 (Leftmost Sidebar):** Master Core (`Hermes Stevenson`, `OpenClaw Gateway`), Autonomous Sub-Agents (`Richard`, `Callum`, `Alistair`, `Archie`, `Liz`, `Ben`), Feeds (`Career Scanner`, `Odessa Router`).
- **Level 2 (Secondary Submenu - 6 Standard Tabs for ALL Agents):**
  1. **Dashboard:** Status, metrics, cluster overview.
  2. **Chat:** Live 2-way conversation stream synced with SQLite and Telegram, instant send via `Enter`.
  3. **Kanban:** Single-screen 4-column responsive grid (`grid-cols-4`) across 100% viewport width without horizontal wrapping or window scrollbars. Backed by `https://dev.aavalanche.com/kanban_api.php`.
  4. **Crons:** Active cron tasks and schedules.
  5. **Capabilities:** Subheader filter pills (`All`, `Skills`, `Tools`, `MCP`, `Browse Hub`).
  6. **Artifacts:** Subheader filter pills (`All`, `Images`, `Files`, `Links`).

## 4. Hermes Desktop Settings Modal
- Accessible via the gear icon in the footer/header.
- Exposes active primary model, request timeout, retries, and the full multi-provider catalog (Google, OpenAI, NVIDIA NIM, HF Router, Gonka24, OpenRouter).
