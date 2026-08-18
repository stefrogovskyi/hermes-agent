# Alistair Tasktracker & Google OAuth Live Recovery (2026-07-31)

## Symptom
Alistair (`@qubicpmbot`) was failing to read and update tasks in the Google Sheet (`Navo Tasktracker`). When requested to process a quoted Telegram snapshot from Sort It Bot and update tasks, he was either returning errors ("task not found") or claiming he could not access the price list / tracker.

## Hypothesis & Verification
1. **OAuth Expiry**: Google OAuth token (`google_token.json`) was missing valid refresh scopes -> re-authenticated via Google OAuth URL exchange (`refresh_google_auth.py` and `exchange_google_code.py`). Verified with `read_tracker_sheet()`.
2. **Backend Mismatch**: `TASKTRACKER_BACKEND` was set to `salesloop` in `.env.local`, causing `update_task` calls to route to Kanban instead of Google Sheets -> forced `TASKTRACKER_BACKEND=sheets` in `alistair_bot.py`.
3. **ID Matching Issue**: `read_tracker_sheet()` formatted rows as physical row numbers while `update_task` required exact UUIDs -> updated `tasktracker_client.py` to format row IDs cleanly (`ID 1`, `ID 2`, etc.) and map them back to Google Sheet rows.
4. **LLM Routing / Stub Check**: `alistair_bot.py` stub check blocked Direct Gemini API calls when NOUS key was unavailable -> patched stub check and routed LLM calls to `google/gemini-2.5-flash` via OpenRouter.
5. **System Prompt Instruction**: System prompt lacked explicit rules for parsing quoted Telegram messages -> updated `system_prompt.md` with auto-update rules for quoted snapshots.

## Fix
1. Exchanged fresh Google OAuth token -> verified live read of 70 tasks in `Navo Tasktracker`.
2. Patched `tasktracker_client.py`, `alistair_bot.py`, and `system_prompt.md`.
3. Restarted Alistair via watchdog.

## Reflection / Rule
- Always verify the backend setting (`TASKTRACKER_BACKEND`) when a bot delegates to a multi-backend client.
- When formatting tabular data for LLM consumption, ensure IDs presented match the exact identifiers expected by the update tool.
