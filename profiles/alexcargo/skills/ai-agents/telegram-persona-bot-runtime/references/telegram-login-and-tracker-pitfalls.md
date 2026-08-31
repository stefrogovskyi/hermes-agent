# Telegram Login Codes, Google Sheets OAuth, and Snapshot Auto-Update Pitfalls

### 1. Telethon / User Account Login Code Invalidation Trap
- **Symptom:** Entering a Telegram login code received in Telegram returns `The confirmation code has expired` or Telegram sends a security alert: `Incomplete login attempt... The code was entered correctly, but sign in was not allowed, because this code was previously shared by your account`.
- **Root Cause:** Telegram's security system automatically detects and invalidates any login code that is pasted, sent, or forwarded as a text message inside a Telegram chat window (to prevent phishing/hijacking).
- **Fix / Protocol:**
  - NEVER ask the user to post their Telegram 5-digit login code into the agent chat.
  - Instruct the user to run an interactive terminal script (e.g. `python login_telethon.py`) directly on their local CLI machine.
  - The user types the code directly into the local terminal prompt — Telegram validates it, saves `router_telethon_session.session`, and avoids code revocation.

### 2. Google Sheets OAuth Token Revocation (`invalid_grant`)
- **Symptom:** `HTTP Error 400: Bad Request` with error body `{"error": "invalid_grant", "error_description": "Token has been expired or revoked."}` when calling Google Sheets API `values` endpoint.
- **Root Cause:** The `refresh_token` stored in `google_token.json` was revoked or expired upstream.
- **Fix:**
  - Launch a browserless OAuth authorization URL (`https://accounts.google.com/o/oauth2/v2/auth?...`).
  - Have the user grant access in browser, copy the resulting redirect URL (`http://localhost:8080/?code=...`), and exchange the `code` for a fresh `google_token.json`.
  - Ensure `TASKTRACKER_BACKEND=sheets` (not `stub` or `salesloop`) so the client writes directly to Google Sheets.

### 3. Snapshot / Report Auto-Update Pattern
- **Symptom:** Agent responds to a quoted status report / snapshot with *"I see this report, but I need specifics on what tasks to update"* or hallucinates dummy task names.
- **Root Cause:** System prompt lacks explicit instruction on parsing quoted release notes / status reports.
- **Fix:**
  - Add explicit `AUTO-UPDATE & SNAPSHOT RULE` to system prompt:
    1. Call `read_tracker_sheet` to fetch live tasks from the Google Sheet.
    2. Parse the shipped/completed task titles listed in the quoted report (e.g. `Mailbox CC field`, `loadingmcp container auto-select fix`).
    3. Match those task names against sheet titles and extract their task IDs.
    4. Call `update_task` for each matched task to set `percent: 100` / status to Done.
    5. Report the exact list of updated task IDs and titles cleanly.
