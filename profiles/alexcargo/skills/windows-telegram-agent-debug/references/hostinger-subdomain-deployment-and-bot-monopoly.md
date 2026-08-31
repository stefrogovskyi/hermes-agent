# Hostinger Subdomain Deployment & Bot Monopoly Guardrails (August 2026 Case Study)

## 1. Multi-Bot Token Isolation & Parent Environment Pollution
- **Problem:** When sub-bots (`richard_bot.py`, `alistair_bot.py`, `callum_vance_bot.py`) are spawned by `hermes serve` or `bot_watchdog.py`, the sub-process inherits `TELEGRAM_BOT_TOKEN` belonging to the main orchestrator (`8682188433`).
- **First-Match Parsing Failure:** If `_load_env()` checks `if k not in os.environ:`, it skips loading `TELEGRAM_BOT_TOKEN` from the sub-bot's own local `.env.local` file.
- **Masked Token Fallback Trap:** Hardcoding dummy masked fallback strings like `"8846249306:***"` or `"8846249306:AAFA..."` in Python constants causes `HTTP Error 401: Unauthorized` on `getUpdates` / `sendMessage`.
- **Duplicate Token Lines:** If `.env.local` contains an old revoked `TELEGRAM_BOT_TOKEN=...` near the top and a valid token near the bottom, naive line-by-line reading grabs the revoked token on the first match.

### Verified Solution Pattern:
1. Always validate candidate tokens against `https://api.telegram.org/bot<token>/getMe` before returning.
2. Ensure `_load_env()` in sub-bots explicitly overwrites `os.environ["TELEGRAM_BOT_TOKEN"]` with the unmasked token from the bot's own local `.env.local` file.
3. Add hard safety guardrail in all sub-bots:
   ```python
   if BOT_TOKEN.startswith("8682188433"):
       raise RuntimeError("CRITICAL SAFETY BLOCK: Sub-bot attempted to use Hermes main bot token (8682188433)!")
   ```

---

## 2. Multi-Process Duplicate Elimination & 409 Conflict Prevention
- **Problem:** When multiple `pythonw.exe` background processes run `richard_bot.py` simultaneously, all instances hit `getUpdates` on the same Telegram token `8846249306`, triggering continuous `HTTP Error 409: Conflict`. This causes total blindness where no messages are ever received or answered.
- **`psutil` Command Line Matching Trap:** Calling `p.kill()` only on the single PID in `richard.lock` misses orphaned duplicate background processes.

### Verified Solution Pattern:
- In `_acquire_lock()` inside every persona bot, explicitly iterate over `psutil.process_iter(['pid', 'name', 'cmdline'])` with `import psutil` imported, match `f"{bot_mod}.py"` in command lines, and kill any duplicate process matching `p.info['pid'] != os.getpid()`.
- On startup, execute an initial `getUpdates` with `offset = -1` to skip old historical message tails and avoid batch processing lag.

---

## 3. Hostinger Subdomain Deployment & Hybrid SPA Routing
- **DNS A-Records:** Creating a subdomain in Hostinger hPanel (`dev.aavalanche.com` / `staging.aavalanche.com`) provisions the directory (`/public_html/dev/`), but requires an explicit DNS A-record (`dev` -> `92.112.183.67`) in the DNS Zone Editor for domain name resolution.
- **Relative Links for Multi-Subpath Support:** Use clean relative paths (`href="services.html"`, `href="pricing.html"`, `href="about.html"`, `href="contact.html"`) instead of leading-slash domain-root paths (`href="/services.html"`). This ensures links work seamlessly on both subdomains (`dev.aavalanche.com/services.html`) and subfolders (`aavalanche.com/dev/services.html`).
- **Static Page Mapping in `.htaccess`:**
  ```apache
  <IfModule mod_rewrite.c>
    RewriteEngine On
    Header set X-Robots-Tag "noindex, nofollow"
    RewriteBase /dev/

    # Direct static page mapping
    RewriteRule ^services/?$ services.html [L,QSA]
    RewriteRule ^pricing/?$ pricing.html [L,QSA]
    RewriteRule ^about/?$ about.html [L,QSA]
    RewriteRule ^contact/?$ contact.html [L,QSA]

    # Allow direct access to physical files
    RewriteCond %{REQUEST_FILENAME} -f [OR]
    RewriteCond %{REQUEST_FILENAME} -d
    RewriteRule ^ - [L]
  </IfModule>
  ```
