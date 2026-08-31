# Telethon User Client, Group Scanning & Group Bot Name Triggers

## 1. Local Terminal Security for Telethon Authentication
When logging into a Telegram user client via Telethon (`TelegramClient`):
- **DO NOT** ask the user to post their 5-digit Telegram SMS/app login code into the conversation chat.
- **Telegram Security Mechanism:** Telegram automatically detects when a login verification code string is posted or forwarded inside a Telegram chat, and immediately invalidates/blocks that code (`The confirmation code has expired` / `Incomplete login attempt blocked`).
- **Correct Workflow:**
  Provide a single 1-line interactive script (`python login_telethon.py`) that the user runs directly inside their local terminal / CMD prompt. The script calls `client.start(phone=...)`, prompting the user to type the 5-digit code directly into the terminal `stdin`. Once typed, the `.session` file is saved locally to disk (`router_telethon_session.session`), and future background scripts reuse the session file without needing codes ever again.

## 2. Russian Declensions & Word Boundaries in Group Bot Name Triggers
When an agent is configured to monitor Telegram groups and react when mentioned by name:
- **Common Bug:** Using a naive regex like `re.compile(r"(алистер|alistair)", re.IGNORECASE)` only matches the nominative case (`Алистер`).
- **Result:** Team members in Russian groups who address the bot in oblique cases (*"Алистера добавили в трекер"*, *"Алистеру скинули таск"*, *"спроси у Алистера"*) get ignored, and the bot stays silent.
- **Fix:** Use full declension prefix matching with word boundaries:
  ```python
  NAME_RE = re.compile(r"\b(алистер[а-я]*|alistair[a-z]*|allister|alister|алику?)\b", re.IGNORECASE)
  ```
  This matches `Алистер`, `Алистера`, `Алистеру`, `Алистером`, `Алистере`, `Alistair`, `Alistair's`, etc. cleanly across all Russian and English sentence structures.

## 3. Windows Output Encoding (UnicodeEncodeError / charmap)
Python scripts running as background processes or embedded shells on Windows default to the system codepage (CP1251 / CP1252) for `sys.stdout` and `sys.stderr`.
- When printing emojis (🗓️, 💡, 📊, 🚀, 🔑) or multi-byte UTF-8 strings to stdout or log files, the process crashes with `UnicodeEncodeError: 'charmap' codec can't encode character...`.
- **Fix:** Force UTF-8 stream reconfiguration at the top of every python script right after `sys` is imported:
  ```python
  import sys
  if hasattr(sys.stdout, 'reconfigure'):
      try:
          sys.stdout.reconfigure(encoding='utf-8', errors='replace')
          sys.stderr.reconfigure(encoding='utf-8', errors='replace')
      except Exception:
          pass
  ```

## 4. Telethon Group Scanning & Avoidance Routing Workflow
1. **Entity Lookup by ID, Not Title:** Always pass the target group's integer ID (e.g. `-1002050105527`), NEVER a string title (like `"Не повредит Одесса"`). String lookups fail with `Cannot find any entity corresponding to...` if the entity is not in dialogs cache or punctuation differs (e.g. `"Не повредит, Одесса"`).
2. **Multi-Host Session Path Resolution:** Telethon userbot sessions live at different paths across environments:
   - Linux VPS (`stefan1`): `/opt/hermes/stefan_userbot.session`
   - Windows Desktop: `C:\Users\Stefan\AppData\Local\hermes\router\router_telethon_session.session`
   Runner scripts must check candidate paths sequentially rather than hardcoding a single host.
3. **Fetch & Filter:** Fetch live messages using `client.iter_messages(entity, limit=200)` for the current date/window (e.g. last 12-24h).
4. **Signal Extraction:** Filter messages for target location keywords (`БП`, `##блокпост`, `тцк`, `патрули`, `проверка`, `люстры`, `каблуки`, `облава`, street names, intersections).
5. **Route Generation:** Build a direct Google Maps Directions URL (`https://www.google.com/maps/dir/?api=1&origin=...&destination=...&travelmode=driving`) with waypoint avoidance. Include exact publication timestamps (`[HH:MM]`) for all cited signals.

