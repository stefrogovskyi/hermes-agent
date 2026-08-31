# Secret Replication, Token Revocation, Failover Switcher & Aeon Gateway Fallback

## 1. Direct Secret Replication via Tailscale (.env Exclusion from Git)
- **Root Cause & Security Policy:** `.env` files are excluded from Git to prevent accidental token exposure and GitHub Secret Scanning blocks (GH013).
- **Pitfall:** Syncing only via Git causes sub-agents on the VPS to start with stale/missing API credentials when the user configures them locally on their PC.
- **Solution (`tailscale_env_direct_sync.py`):**
  - Use direct point-to-point SSH/SCP queries over Tailscale (`Stefan@100.79.157.46`).
  - Read `%LOCALAPPDATA%\hermes\profiles\<profile>\.env` on the desktop and write directly to `/opt/hermes/profiles/<profile>/.env` on the server.
  - Automatically incorporate this P2P sync into scheduled evening sync audits.

  ```python
  import subprocess
  import os

  DESKTOP_SSH = "Stefan@100.79.157.46"
  HERMES_DIR = "/opt/hermes"
  PROFILES = ["richard", "default", "callum", "harrison", "alistair", "archie", "liz", "ben"]

  def sync_envs_from_desktop():
      print("Checking Tailscale connection to Desktop...")
      res = subprocess.run(f"tailscale ping -c 1 100.79.157.46", shell=True, capture_output=True, text=True)
      if res.returncode != 0:
          print("Desktop is offline, skipping direct .env sync.")
          return

      # Direct scp / cat of .env files from Desktop
      for prof in PROFILES:
          desktop_env_path = f"C:/Users/Stefan/AppData/Local/hermes/profiles/{prof}/.env" if prof != "default" else "C:/Users/Stefan/AppData/Local/hermes/.env"
          local_env_path = f"/opt/hermes/profiles/{prof}/.env" if prof != "default" else "/opt/hermes/.env"
          
          cmd = f"ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no {DESKTOP_SSH} 'type \"{desktop_env_path}\''"
          proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
          if proc.returncode == 0 and len(proc.stdout.strip()) > 50:
              os.makedirs(os.path.dirname(local_env_path), exist_ok=True)
              with open(local_env_path, "w", encoding="utf-8") as f:
                  f.write(proc.stdout)
              print(f"✅ Successfully synced .env for profile [{prof}] directly from PC!")

  if __name__ == "__main__":
      sync_envs_from_desktop()
  ```

## 2. Telegram 401 Unauthorized / Token Revocation Diagnostics
- **Root Cause:** If a bot token is exposed in public GitHub repos, logs, or revoked in `@BotFather` via `/revoke` or `/newtoken`, Telegram API immediately returns `HTTP 401: Unauthorized`.
- **Systemd Behavior:** Hermes treats `401 Token Rejected` as an unrecoverable configuration error (`status=78/CONFIG`), stopping the restart loop to avoid API spam.
- **Diagnostic Command:**
  ```python
  import urllib.request
  urllib.request.urlopen("https://api.telegram.org/bot<TOKEN>/getMe")
  ```
- **Fix:** Obtain fresh token from `@BotFather`, update `.env` both on VPS and PC, and restart `hermes-<profile>.service`.

## 3. Desktop Failover Switcher Architecture (VPS ⇄ PC)
- **Goal:** Provide 100% ecosystem uptime during VPS maintenance/blackouts.
- **Mechanism (`desktop_failover_daemon.py` on PC):**
  - Desktop daemon pings VPS every 60 seconds.
  - If VPS is unreachable 3 times in a row: activates local sub-agents on PC, sends Telegram alert, switches to 10-minute poll interval.
  - As soon as VPS recovers: performs Git push of local changes, shuts down local PC sub-agents (avoiding dual-token 409 collisions), and restores master control to VPS.

## 4. Aeon GitHub Actions Gateway Multi-Provider Fallback
- **Problem:** In Aeon runner workflows, hardcoding `gateway.provider: openrouter` causes total workflow failure when models reach end-of-life (e.g., `stealth/ox-alpha` 404/402 Payment Required).
- **Fix:** Always set `gateway.provider: auto` in `aeon.yml`.
- **Cascade Resolution:**
  1. `Claude Code Subscription (OAuth Token)`
  2. `Anthropic API (Pay-as-you-go)`
  3. `OpenAI API`
  4. `OpenRouter / Free Tier Fallbacks`
