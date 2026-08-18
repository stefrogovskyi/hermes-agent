# Case: Odessa Safe Router & Telegram Group Scanner

## Symptoms & Root Cause
- **Symptom:** When requested in Telegram to scan group «Не повредит Одесса» and build an avoidance route, Hermes orchestrator failed with *"У меня нет прямого доступа к сообщениям группы"* or *"Cannot find any entity corresponding to 'Не повредит Одесса'"*.
- **Root Cause:**
  1. Telegram gateway runs on Linux VPS (`stefan1`).
  2. The skill `odessa-safe-router` was not packaged as an official skill or synced to VPS.
  3. When attempting on-the-fly execution, Hermes used an invalid `api_id` and looked up the group by raw string `"Не повредит Одесса"` instead of the exact Telegram entity ID `-1002050105527` (`Не повредит, Одесса`).
  4. Telethon user session `stefan_userbot.session` (Stefan ID `330656040`) was already authorized on VPS at `/opt/hermes/stefan_userbot.session` and on Windows at `C:\Users\Stefan\AppData\Local\hermes\router\router_telethon_session.session`, but lacked a single unified CLI runner.

## Fix & Verification
- Created skill `odessa-safe-router` with executable runner `scripts/odessa_group_router.py`.
- Synchronized to both Windows (`C:\Users\Stefan\AppData\Local\hermes\skills\productivity\odessa-safe-router\`) and Linux VPS (`/opt/hermes/skills/productivity/odessa-safe-router/`).
- Verified live scan returns 150+ live signals with exact timestamps (`[HH:MM]`), parses roadblocks/patrols (`##блокпост`, `тцк`, etc.), and outputs Google Maps route URLs.

## Telethon Session Watchdog & Self-Healing
- **Watchdog Script:** `/opt/hermes/scripts/odessa_session_watchdog.py` (and launcher `/opt/hermes/scripts/odessa_session_watchdog.sh`).
- **Mechanism:** Runs every 6 hours (`0 */6 * * *`). Tests session validity via Telethon `get_me()`. On success, takes an atomic backup (`/opt/hermes/backups/stefan_userbot.session.bak`) and updates `/opt/hermes/backups/stefan_userbot.session.meta.json`.
- **Alerting & Recovery:** If session is invalidated (e.g. revoked key), immediately sends Telegram alert to Stefan with recovery instructions (`python3 /opt/hermes/scripts/reauth_userbot.py`).
- **Hermes Cron:** Registered as internal Hermes cron job `66619135fb8e` (`Odessa Session Watchdog`).
