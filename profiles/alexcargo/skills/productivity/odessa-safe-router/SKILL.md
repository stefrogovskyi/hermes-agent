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

### 2. Formatted Output Rules:
- Always show exact publication timestamps (`[HH:MM]`).
- Identify reported streets, intersections, and roadblock/patrol markers.
- Provide a direct, clickable Google Maps Directions URL for driving.
