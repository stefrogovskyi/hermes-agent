# Userbot Session & Vercel Kanban Deployments

## 1. Telegram Userbot Session Setup & Channel Polling

### Problem & Pitfall
Attempting to log into a Telethon userbot session by requesting 5-digit verification codes over Telegram chat triggers Telegram Security Guard blocking. Telegram invalidates the code and blocks the sign-in attempt from new server IPs when the code appears in chat text.

### Solution & Safe Pattern
1. **Reusing Authorized `.session` File:**
   - Copy the existing, pre-authorized `.session` file (e.g., `router_telethon_session.session`) over Tailscale or receive it directly as an un-inlined Telegram document attachment.
   - Place the file on the server at `/opt/hermes/stefan_userbot.session`.

2. **File Permissions & Git Security:**
   - Restrict permissions to root only: `chmod 600 /opt/hermes/stefan_userbot.session`.
   - Add `*.session` and `stefan_userbot.session` to `/opt/hermes/.gitignore`.

3. **Read-Only Channel Polling (`nepovredit_odessa_poller.py`):**
   - Connect via Telethon: `client = TelegramClient("/opt/hermes/stefan_userbot.session", api_id, api_hash)`.
   - Use ONLY read operations: `client.get_entity(TARGET_CHANNEL_ID)` and `client.get_messages(channel, limit=15)`.
   - **User Preference Signal:** Always format scanned signals with exact publication timestamps `HH:MM` (e.g. `15:35`).
   - **Strict Security Rule:** Never call `send_message` or write methods from the userbot session. Sub-bots write only from their own bot tokens.

---

## 2. Vercel Kanban Deployment & SSO Protection Fix

### Problem & Pitfalls
- **Vercel SSO Redirects:** Vercel projects may default to SSO/Deployment Protection, serving a 477KB login HTML page instead of the 22KB Kanban HTML.
- **Client-Side Hydration Wiping Cards:** Pure client-side `fetch()` or `localStorage` reads can clear pre-baked cards or render empty columns if `localStorage` holds `{ cards: [] }`.

### Solution
1. **Disable Vercel SSO Protection via REST API:**
   ```python
   import requests
   
   headers = {"Authorization": "Bearer " + VERCEL_TOKEN, "Content-Type": "application/json"}
   url = "https://api.vercel.com/v9/projects/" + project_name + "?teamId=" + VERCEL_TEAM_ID
   requests.patch(url, headers=headers, json={"ssoProtection": None, "passwordProtection": None})
   ```

2. **Pre-bake Initial Cards in HTML (SSR):**
   - Render card HTML directly inside column containers (`<div class="cards-container" id="cards-todo">{todo_html}</div>`) in static `index.html`.
   - In client JS, protect `localStorage` initialization: if `localStorage` has fewer cards than `DEFAULT_CARDS`, preserve `DEFAULT_CARDS`.

3. **Floating Action Button:**
   - Add a fixed floating button (`position: fixed; bottom: 24px; right: 24px; z-index: 9999`) for "+ Добавить Задачу" so task creation is visible on all screen sizes.
