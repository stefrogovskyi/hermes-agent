# Direct Tailscale / SCP Secret Replication & Desktop Failover Daemon Architecture

## Overview
Git-based workspace autosync (`git_autosync_hidden.sh`) intentionally and securely excludes all `.env`, `auth.json`, and API credential files from Git repositories to prevent token leakage and secret exposure. Consequently, updating API credentials or platform tokens locally on the desktop (or on the VPS) does **NOT** propagate secrets across devices via Git.

To keep sub-agents (e.g. Richard, Alistair, Harrison, Callum) and primary daemons fully synchronized without exposing secrets to GitHub, use **Direct Tailscale / SSH Replication** alongside an **Automated Desktop Failover Switcher**.

---

## 1. The Secret Synchronization Failure Pattern & Rule

### Pitfall:
- Claiming "Ecosystem is synchronized" based solely on `git status` / `git push` success.
- User configures keys/tokens in local `.env` files on Desktop (`100.79.157.46`), but on the VPS server (`/opt/hermes/profiles/*/.env`), the sub-agent still has outdated/empty credentials and asks the user for keys again.

### Hard Rule:
- **Never rely on Git for secrets (`.env`, private tokens, SSH keys).**
- When credentials change, execute direct encrypted transfers via **Tailscale SSH / SCP** between Desktop and VPS using `/opt/hermes/scripts/tailscale_env_direct_sync.py`:
  ```bash
  # Direct script sync across all profiles
  python3 /opt/hermes/scripts/tailscale_env_direct_sync.py
  ```
- Hook this direct `.env` sync into the daily 23:00 ecosystem sync reporter (`ecosystem_sync_reporter.py`) as Step 0 before Git autosync.
- After updating `.env`, reload the systemd daemon immediately:
  ```bash
  systemctl restart hermes-<profile>.service
  ```

---

## 1.1 Telegram Bot Token 401 Unauthorized / Revocation Diagnostics & Auto-Exit Trap

### Root Causes of Sudden HTTP 401:
1. **GitHub Secret Scanning Revocation:** If a bot token is committed or pasted into an accessible repo/gist/pastebin, Telegram's security crawler detects it and revokes the token within seconds.
2. **Re-generation via `@BotFather`:** Running `/newtoken` or `/revoke` on BotFather instantly invalidates the existing token.

### Hermes Gateway Behavior & Diagnostic Signature:
- When a profile's `TELEGRAM_BOT_TOKEN` is invalid/revoked, Hermes Gateway encounters a non-retryable startup error:
  `ERROR gateway.run: Gateway hit a non-retryable startup conflict: telegram: Telegram bot token rejected`
  `hermes-<profile>.service: Main process exited, code=exited, status=78/CONFIG`
- Systemd will repeatedly crash-loop the service with status 78.

### Diagnostic & Recovery Recipe:
1. **Direct API Validation Probe:**
   ```bash
   python3 -c "import urllib.request; print(urllib.request.urlopen('https://api.telegram.org/bot<TOKEN>/getMe').read().decode())"
   ```
2. If `HTTP Error 401: Unauthorized` is returned:
   - Ask owner to fetch/generate the fresh token from `@BotFather` (`/token` -> `<bot_username>`).
   - Patch `.env` on both Servarica (`/opt/hermes/profiles/<name>/.env`) and Desktop (`%LOCALAPPDATA%\hermes\profiles\<name>\.env`).
   - Restart service: `systemctl restart hermes-<name>.service`.
   - Update persistent memory with the verified token to prevent regressions.

---

## 2. Desktop Failover Switcher Architecture (`desktop_failover_daemon.py`)

When VPS Servarica undergoes data center maintenance, kernel upgrades, or transient network blackouts, an automated background switcher on the Desktop PC ensures 100% uptime without manual intervention.

### Dual-State Watchdog Cycle:
1. **Standby Mode (Normal Operations):**
   - Polls Servarica IP (`100.99.146.42` / `38.49.219.217`) every 60 seconds via ICMP ping.
   - Local Hermes gateways on the Desktop remain stopped to prevent Telegram Bot 409 Polling Conflicts.
2. **Failover Activation (Servarica Down > 3 consecutive failures):**
   - Launches local Desktop Hermes Gateway daemons (`hermes gateway run`).
   - Sends Telegram emergency notice to Stefan:  
     `🚨 ВНИМАНИЕ: Серварика недоступна (техработы/сбой сети)! Экосистема переключена на ПК.`
   - Shifts polling frequency to **every 10 minutes** to check for Servarica recovery.
3. **Recovery & Resync (Servarica Restored):**
   - Performs `git commit` & `git push` of any local memories or tasks created during failover.
   - Gracefully terminates local Desktop Hermes processes (`pkill` / `taskkill`).
   - Sends Telegram resolution notice:  
     `✅ Серварика снова онлайн! Данные синхронизированы в GitHub, управление возвращено на VPS.`

---

## 3. Playwright Headless Bypassing for Modern Protected Portals

When scraping or monitoring SPA job portals (Google Careers `boq-hiring`, Microsoft Careers, EPAM Systems `careers.epam.com`), simple `urllib` / `requests` fail with `403 Forbidden` or return empty JS skeletons.

- Use Headless Playwright with realistic viewport and User-Agent:
  ```python
  from playwright.async_api import async_playwright

  async with async_playwright() as p:
      browser = await p.chromium.launch(headless=True)
      context = await browser.new_context(
          user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
      )
      page = await context.new_page()
      await page.goto(target_url, timeout=45000)
      await page.wait_for_timeout(8000)
      # Extract DOM elements
  ```
- Always execute with a bounded timeout and catch Pyright missing import exceptions in script headers.
