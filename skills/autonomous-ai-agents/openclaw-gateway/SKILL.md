---
name: openclaw-gateway
description: Use when configuring OpenClaw gateways, models and bots.
---

# OpenClaw Gateway Orchestration

OpenClaw is a lightweight TypeScript/Node.js multi-channel AI gateway and autonomous agent daemon created by Peter Steinberger.

## 1. Core Architecture & Files
- **App Directory:** `/opt/openclaw/app` (git repo `openclaw/openclaw`)
- **CLI Executable:** `/usr/local/bin/openclaw` -> `/opt/openclaw/app/dist/entry.js`
- **Configuration:** `~/.openclaw/openclaw.json` (validated via `openclaw config validate`)
- **Auth Profiles:** `~/.openclaw/auth/auth-profiles.json`
- **Systemd Unit:** `/etc/systemd/system/openclaw.service` (port 18789 loopback)

## 2. Telegram Pairing & Approval Flow
When OpenClaw receives a message from an unauthenticated user, it requires pairing approval:
```bash
# Approve pairing for user ID
openclaw pairing approve telegram <PAIRING_CODE>
```
This registers the sender ID in `commands.ownerAllowFrom` in `openclaw.json`.

## 3. Model Fallback Pipeline, Auto-Update & Low-Latency Tuning
To avoid rate limits (429) or token authentication errors (401) without hanging:
1. **Primary & Fallbacks Schema:**
   - For highest performance and direct quota utilization, configure Google provider directly (`api: "google-generative-ai"`) with `google/gemini-3.8-flash` as primary.
   - Avoid volatile `:free` tags as `primary` (which hit frequent 429s or disappear); use solid, high-availability models.
   - Guard against HTTP 402 ("Payment Required / depleted monthly credits") from Hugging Face or empty balance OpenRouter keys by filtering them out of the automated fallback ladder.
   - When configuring Google models, ensure `models.providers.google` explicitly includes `"api": "google-generative-ai"` and `"baseUrl": "https://generativelanguage.googleapis.com/v1beta"`, otherwise OpenClaw skips the primary model during background routines (heartbeat / dream diary) and cascades through all fallbacks, throwing billing / rate limit errors into Telegram.
   In `~/.openclaw/openclaw.json`:
   ```json
   {
     "agents": {
       "defaults": {
         "model": {
           "primary": "google/gemini-3.8-flash",
           "fallbacks": [
             "google/gemini-3.8-flash",
             "google/gemini-3.7-flash",
             "google/gemini-2.5-flash",
             "gonka24/deepseek-v4-flash-0731",
             "gonka24/kimi-k2.6",
             "gonka24/minimax-m2.7"
           ]
         },
         "models": {
           "google/gemini-3.8-flash": {},
           "google/gemini-3.7-flash": {},
           "google/gemini-2.5-flash": {},
           "gonka24/deepseek-v4-flash-0731": {},
           "gonka24/kimi-k2.6": {},
           "gonka24/minimax-m2.7": {}
         },
         "timeoutSeconds": 15
       }
     },
     "models": {
       "providers": {
         "google": {
           "apiKey": "GEMINI_API_KEY",
           "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
           "api": "google-generative-ai",
           "timeoutSeconds": 15
         },
         "gonka24": {
           "baseUrl": "https://api.gonka24.com/v1",
           "timeoutSeconds": 10,
           "models": [
             {"id": "deepseek-v4-flash-0731", "name": "DeepSeek V4 Flash"},
             {"id": "kimi-k2.6", "name": "Kimi K2.6"},
             {"id": "minimax-m2.7", "name": "MiniMax M2.7"}
           ]
         }
       }
     }
   }
   ```
2. **Automated Daily Fallback & Upstream Sync:**
   - **Nightly Fallback Sync (03:00 Kyiv):** `/opt/hermes/scripts/fallback_monitor.py` verifies 43 models across Google, OpenAI, Anthropic, Nous, OpenRouter, HF, Gonka24, tests latency and automatically syncs verified LIVE models directly into `~/.openclaw/openclaw.json` and restarts `openclaw.service`.
   - **Upstream Auto-Updater (every 6h):** `/opt/hermes/scripts/openclaw_auto_updater.py` checks `github.com/openclaw/openclaw` main branch, runs `git pull --ff-only`, builds with `npm run build`, and cleanly restarts the systemd unit.
2. **Provider Key Ingestion & OpenClaw 2.0 Auth Storage (Preventing HTTP 401):**
   In OpenClaw 2.0+, provider keys must NOT only exist in `openclaw.json` or systemd environment variables, but MUST be registered in OpenClaw's internal agent auth SQLite database (`~/.openclaw/agents/main/agent/openclaw-agent.sqlite`).
   If a fallback model (e.g., `gonka24`, `openrouter`, `openai`) is triggered during background routines without an entry in this auth database, OpenClaw halts with:
   `Couldn't sign in. No API key found for provider ... (HTTP 401 Unauthorized)`.
   Always register keys via the CLI:
   ```bash
   # Register API keys into OpenClaw 2.0 auth database non-interactively
   echo -n "$KEY" | openclaw models auth paste-api-key --provider <provider_name>
   # Verify saved profiles
   openclaw models auth list
   ```
   Note: OpenClaw CLI strictly requires custom OpenAI-compatible providers (like `gonka24`) to explicitly declare a `models: [{id, name}]` array inside `models.providers.<name>`, otherwise schema validation fails. Custom top-level keys like `env: {}` or misplaced `fallbacks` are rejected — always structure them within `model: { primary, fallbacks: [] }` and `models: { ... }`.

## 4. Diagnostics & Verification
- `openclaw gateway health` — Check gateway response time.
- `openclaw channels status` — Check Telegram polling connection.
- `journalctl -u openclaw -n 25 --no-pager` — Monitor live inbound/outbound event logs.

## 5. AgentOS Mission Control UI Integration Architecture
- Multi-Agent Orchestration & Command Panel:
  - **1st Level Sidebar:** Agent roster (Hermes, OpenClaw, Richard, Callum, Alistair, Archie, Liz, Ben).
  - **2nd Level Submenu:** Standardized 6 tabs for every agent: `Dashboard`, `Chat`, `Kanban`, `Crons`, `Capabilities` (with filter pills: All/Skills/Tools/MCP/Browse Hub), `Artifacts` (with filter pills: All/Images/Files/Links).
  - **Full-Width Responsive Kanban:** Grid-based layout (`grid-cols-4`) without horizontal scrollbars, rendering cards across To Do, In Progress, Recurring/Cron, Completed from `kanban_api.php`.
  - **Two-Way Live Chat Sync:** Stream from SQLite DB with auto-scroll and instant POST submission to agent message queues.
  - **Settings & Gear Modal:** Hermes Desktop-like controls for primary model, global fallback list, timeouts, retries, and active model catalog.
