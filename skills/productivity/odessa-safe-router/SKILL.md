---
name: odessa-safe-router
description: Scan Telegram group 'Не повредит, Одесса' via authorized user session and calculate avoidance routes in Odessa.
category: productivity
tags:
  - telegram
  - router
  - odessa
  - navigation
  - avoidance
---

# Odessa Safe Router & Telegram Group Scanner

Scan live alert signals from the Telegram group **«Не повредит, Одесса»** using Stefan's authorized Telethon user session, extract checkpoints/patrols/traffic roadblocks, and build driving routes with Google Maps.

## Configuration & Credentials
- **Group Title**: `Не повредит, Одесса`
- **Target Group ID**: `-1002050105527`
- **Telegram API ID**: `20400084`
- **Telegram API HASH**: `b2e2d93e1792bc443ae3bd40a9b8979c`
- **Authorized Session Path**:
  - Linux VPS (`stefan1`): `/opt/hermes/stefan_userbot.session`
  - Windows Desktop: `C:\Users\Stefan\AppData\Local\hermes\router\router_telethon_session.session`

## How to Execute

### 1. Python script execution (Linux VPS / Windows):
```bash
# On Linux VPS (stefan1):
/opt/hermes/hermes-agent/venv/bin/python3 /opt/hermes/skills/productivity/odessa-safe-router/scripts/odessa_group_router.py --scan

# With route generation:
/opt/hermes/hermes-agent/venv/bin/python3 /opt/hermes/skills/productivity/odessa-safe-router/scripts/odessa_group_router.py --from-loc "Успенская угол Итальянской" --to-loc "Детская больница"
```

### 2. Session Self-Healing (watchdog)
- Cron job `Odessa Session Watchdog` (id `66619135fb8e`, every 6h, no_agent) runs `/opt/hermes/scripts/odessa_session_watchdog.sh`:
  - Session healthy → refreshes cold backup `/opt/hermes/backups/stefan_userbot.session.bak` (SQLite backup API) + meta (phone/user_id) in `stefan_userbot_meta.json`. Silent.
  - Session file corrupt/deleted → auto-restores from backup, re-verifies auth. Alerts Stefan only if restore fails.
  - Auth key revoked by Telegram (ended in Devices, 2FA change, anti-abuse) → backup CANNOT help; alerts Stefan's DM with re-login instructions.
- Log: `/opt/hermes/backups/session_watchdog.log`.
- **Re-authorization procedure** (when Stefan says «переавторизуй сессию одессы»): run interactive Telethon login in background PTY with phone from `stefan_userbot_meta.json`: `client.start(phone=...)` → Telegram sends code to Stefan → he relays it (MUST be spaced, e.g. «1 2 3 4 5», otherwise Telegram invalidates the code) → submit via process(action='submit'). New session file lands at `/opt/hermes/stefan_userbot.session`; watchdog re-backs it up on next tick.
- NEVER run two clients on the same .session concurrently (AuthKeyDuplicatedError kills the key). VPS and Windows must keep separate sessions.

### 3. Formatted Output Rules:
- Always show exact publication timestamps (`[HH:MM]`).
- Identify reported streets, intersections, and roadblock/patrol markers.
- Provide a direct, clickable Google Maps Directions URL for driving.
