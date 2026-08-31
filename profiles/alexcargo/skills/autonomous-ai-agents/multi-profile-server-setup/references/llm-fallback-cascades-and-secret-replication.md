# LLM Provider Fallback Cascades, Stale Free Model Hazards & Direct P2P Secret Synchronization

## 1. Dead/Experimental Model Traps & Spurious Authentication Error Cascades
- **The Pitfall:** Free testing models (e.g. `stealth/ox-alpha`, `:free` tiers on OpenRouter like `nvidia/nemotron-*:free`, `google/gemma-*:free`, `cohere/*:free`, `openai/gpt-oss-20b:free`, `inclusionai/ling-3.0-flash:free`, `poolside/laguna-s-2.1:free`) are frequently deprecated, renamed, or converted to paid/exhausted without warning.
- **The Cascading Error Loop:** When primary model calls fail (e.g., Google API 404 on `gemini-3.7-flash`), Hermes iterates through the `fallback_providers` list in `config.yaml`.
  - If a sub-agent's `.env` carries an invalid, expired, or truncated API key for a fallback provider (e.g., `OPENROUTER_API_KEY`), **every single free model attempt emits an AuthenticationError (`HTTP 401 User not found`)**.
  - This floods the user's chat with rapid-fire failure notifications and ultimately causes the agent gateway to hit non-retryable errors and shut down silently.
  - **Important:** Check OpenRouter credits regularly: `https://openrouter.ai/settings/credits`.
- **Remediation & Best Practice:**
  1. **Clean Fallback Chains:** Strip out volatile `:free` OpenRouter tags from production agent `config.yaml`.
  2. **Reliable Commercial Fallback Hierarchy:**
     - 🥇 Primary: `google/gemini-2.5-flash` (provider: `google`)
     - 🥈 Fallback 1: `gpt-4o-mini` (provider: `openai`)
     - 🥉 Fallback 2: `gpt-4o` (provider: `openai`)
     - 🏅 Fallback 3: `minimax-m2.7` / `kimi-k2.6` (provider: `gonka24`)
     - 🎖 Fallback 4: `deepseek/deepseek-chat` / `meta-llama/llama-3.3-70b-instruct` (provider: `openrouter`)

---

## 2. Direct P2P Secret Replication (.env) over Tailscale vs Git Sync
- **The Problem:** Git synchronization (`git_autosync_hidden.sh`) deliberately excludes `.env` and `auth.json` to prevent secret leaks and GitHub Secret Scanning blocks. When the user configures API keys locally on a Desktop workstation, Git does NOT propagate them to the VPS, leaving the server-side agent with missing or stale credentials.
- **The Pattern (`tailscale_env_direct_sync.py`):**
  - Run a direct, authenticated P2P sync over Tailscale SSH (`Stefan@100.79.157.46`) to read `%LOCALAPPDATA%\hermes\profiles\<name>\.env` and update `/opt/hermes/profiles/<name>/.env` without committing secrets to version control.
  - Automatically validate synced API keys against provider healthcheck endpoints before restarting agent systemd services.

---

## 3. Telegram Bot Token Revocation (`HTTP 401 Unauthorized`) Diagnostics
- **Symptom:** Gateway daemon crashes on startup with `status=78/CONFIG` and error `telegram: Telegram bot token rejected: The token was rejected by the server`.
- **Causes:**
  1. Automated Telegram / GitHub security crawler detected token string and revoked it.
  2. Manual `/revoke` or `/newtoken` issued in `@BotFather`.
  3. Trailing invisible control characters or truncated strings during manual edits.
- **Verification Probe:**
  ```python
  import urllib.request
  urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/getMe")
  ```
- **Fix:** Obtain fresh token from `@BotFather`, update both VPS `/opt/hermes/profiles/<name>/.env` and Desktop PC `.env`, then run `systemctl restart hermes-<name>.service`.

---

## 4. Aeon Framework Gateway Failover (`provider: auto`)
- In serverless/GitHub Actions Aeon implementations (`aeon.yml`), hardcoding `gateway.provider: openrouter` causes skill runs (e.g. `skill: heartbeat`) to fail when upstream models shift.
- Set `gateway.provider: auto` in `aeon.yml` so the gateway dynamically cascades through available secrets: `Claude OAuth` ➔ `Anthropic API` ➔ `OpenAI` ➔ `OpenRouter`.
