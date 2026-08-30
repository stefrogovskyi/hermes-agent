# Userbot Session, Vercel Kanban & Timeout Safeguards

## 1. Vercel-Only Kanban Hosting & Pre-Baked SSR Cards

### Hard Policy
All agent Kanban boards MUST be deployed EXCLUSIVELY to Vercel (`https://<agent>-kanban.vercel.app`). **NEVER** deploy or host Kanban boards on the primary production domain `aavalanche.com/kanban/`.

### Pre-Baking HTML Cards (SSR) to Prevent Blank Screens & Rollbacks
- Render initial cards directly inside static `index.html` column containers so the board displays all cards in 0ms on load without waiting for client-side API fetches or JS hydration.
- Avoid redundant floating buttons if header button `+ Новая Задача` is available.

### Smart Merging (`mergeCards`) & Bidirectional Persistence
- Client JS frontend must merge server cards with default cards (`mergeCards(serverCards, defaultCards)`) and use versioned `localStorage` keys so newly added cards on the backend are never hidden by stale browser caches.
- Record exact timestamps on drag-and-drop (`moved_at`) and comment threads (`comments: [{author, text, timestamp}]`) for full auditability during daily 08:00 AM briefs.
- Host `/home/u473746908/domains/aavalanche.com/public_html/dev/kanban_api.php` on Hostinger with CORS enabled (`Access-Control-Allow-Origin: *`).

### Disabling Vercel SSO / Deployment Protection Redirects
When Vercel projects default to SSO/Deployment Protection, Vercel serves a 477KB login HTML page instead of the 22KB Kanban page. To fix:
```python
import requests

v_token = "VERCEL_TOKEN_HERE"
v_team = "navo5"
headers = {"Authorization": f"Bearer {v_token}", "Content-Type": "application/json"}

for proj in ["ben-kanban", "richard-kanban", "callum-kanban", "alistair-kanban", "liz-kanban", "hermes-stevenson-kanban"]:
    url = f"https://api.vercel.com/v9/projects/{proj}?teamId={v_team}"
    body = {"ssoProtection": None, "passwordProtection": None}
    requests.patch(url, headers=headers, json=body)
```

---

## 2. Telethon Userbot Session Authorization & Security

### Security Guard Pitfall
Sending Telegram 5-digit verification codes as chat text triggers Telegram Security Guard blocking and revokes the login attempt.

### Safe Authorization Pattern
- Transfer an authorized `.session` file (e.g. `router_telethon_session.session`) over Tailscale or receive it directly as an un-inlined Telegram document attachment.
- Save to `/opt/hermes/stefan_userbot.session` and set `chmod 600 /opt/hermes/*.session` so the file is readable only by root on Servarica.
- Add `*.session` and `stefan_userbot.session` to `/opt/hermes/.gitignore`.

### Read-Only Sensor Rule
Userbot sessions must strictly operate as READ-ONLY sensors (`get_dialogs`, `get_messages`). Agents must NEVER impersonate the user or send messages from the user account. Sub-bots must send messages only from their own bot tokens.

---

## 3. Context Bloat & Request Timeout Safeguards

Set `request_timeout_seconds: 30` and aggressive compression in `config.yaml` across all profiles:
```yaml
request_timeout_seconds: 30

compression:
  enabled: true
  threshold: 0.25      # Compress when context reaches 25% of limit (~25k-50k tokens)
  target_ratio: 0.15   # Compress down to 15%
```

---

## 4. Cron Schedules & Ukrainian Timezone Alignment

- Server cron schedules run in UTC. To schedule tasks for Ukrainian time (Kyiv / `Europe/Kyiv`):
  - `23:00 Kyiv Time` = `0 20 * * *` UTC.
  - `09:00 Kyiv Time` = `0 6 * * *` UTC.
  - `08:00 Kyiv Time` = `0 5 * * *` UTC.

---

## 5. Bot-to-Bot Loop Shield for Telegram Group Chats

To prevent infinite bot ping-pong loops in group chats:
1. Enable `require_mention: true` in `config.yaml`.
2. Ignore all messages from other bots unless directly tagged via `@mention`.
3. Do not trigger on untagged replies/quotes from other bots.
