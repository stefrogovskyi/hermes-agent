# Group Noise, Meta-Commentary Suppression & Database Concurrency

## 1. Group Chat Noise & Meta-Commentary Prevention (HARD RULE)
- **NO META RULE:** A bot must NEVER post self-referential commentary in group chats about tags, triggers, or why it is staying quiet (e.g. *"Still no tag for me — staying out of the group"*, *"No @mention of me in this one — staying quiet"*). If a message is not addressed to the bot — the code MUST REMAIN SILENT without announcing its silence.
- **AUTOMATIC META-SILENCE SUPPRESSION:** Before sending a reply to a group chat (`chat_type != 'private'`), check if `reply` contains meta-silence phrases (`"no @mention"`, `"staying quiet"`, `"staying out of the group"`, `"won't post"`, `"не упомянули"`, `"не обращались"`, `"молчу"`). If any match is found, DISCARD the message and skip `sendMessage`.
- **BOT-TO-BOT FILTERING:** Always check `msg.get("from", {}).get("is_bot")`. Messages from other bots in group chats MUST be skipped immediately (`continue`) unless explicitly replied to or tagged with `@username`.

## 2. Database Concurrency & Crash Persistence
- **SQLite Concurrency:** On all local SQLite DBs (`state.db`, `executions.db`, `kanban.db`, etc.), execute `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=10000;` on connection. This prevents `database is locked` / `session storage could not be written` errors when cron jobs, watchdogs, and main agent sessions access the DB simultaneously.
- **Turn State Journaling (`IN_FLIGHT` Flag):** Before executing a turn, write `{"status": "IN_FLIGHT", "user_message": "..."}` to `session_state.json`. Set status to `COMPLETED` upon sending the reply. On gateway boot, if `status == "IN_FLIGHT"`, the agent detects an interrupted turn, logs to `crash_journal.json`, completes the turn, and delivers the auto-recovery report.
