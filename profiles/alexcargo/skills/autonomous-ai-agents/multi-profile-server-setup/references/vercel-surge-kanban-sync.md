# Vercel & Surge Kanban Sync, Auto-Translate Fix & Sub-Agent Execution Rules

## 1. Deploying & Persisting Interactive Agent Kanbans

1. **Dual State Persistence (Preventing Card Movement Rollbacks):**
   - **Frontend (JavaScript):**
     - Attach `draggable="true"` and HTML5 Drag & Drop handlers (`ondragstart`, `ondragover`, `ondrop`).
     - On `ondrop`, update local UI immediately and save state to `localStorage.setItem('kanban_state_' + agent, JSON.stringify(currentState))`.
     - In the background, send `POST https://dev.aavalanche.com/kanban_api.php` with `{ agent, action: "move_card", card_id, new_column_id }`.
   - **Backend (`kanban_api.php` on Hostinger):**
     - Supports `action: "move_card"`, `action: "add_card"`, `action: "add_comment"`.
     - Writes updated JSON to `/home/u473746908/domains/aavalanche.com/public_html/kanban_store_<agent>.json`.

2. **Preventing Japanese / Foreign Language Auto-Translate Glitches:**
   - Browsers (Chrome/Safari) may misidentify Cyrillic UTF-8 HTML on Vercel/Surge edges and auto-translate to Japanese or trigger SSO redirects.
   - **Fix:** Include `<meta name="google" content="notranslate">` and `<meta http-equiv="Content-Language" content="ru">` in HTML `<head>`.
   - Configure `vercel.json` with explicit HTTP response headers:
     ```json
     {
       "version": 2,
       "routes": [{ "src": "/(.*)", "dest": "/index.html" }],
       "headers": [
         {
           "source": "/(.*)",
           "headers": [
             { "key": "Content-Type", "value": "text/html; charset=utf-8" },
             { "key": "Content-Language", "value": "ru" }
           ]
         }
       ]
     }
     ```

3. **Kanban Deployment Policy (Hard Rule):**
   - ALL agent Kanban boards MUST be deployed exclusively to Vercel (`https://<agent>-kanban.vercel.app` / `https://hermes-stevenson-kanban.vercel.app`).
   - **NEVER** host or deploy Kanban boards on the primary production domain `aavalanche.com/kanban/`.

4. **Deploying via Vercel & Surge CLI:**
   - **Surge CLI Token:** `SURGE_TOKEN=82bd19e64bbf196940cf4c78cf9f835a` (Account: `stefan.rogovskiy@aavalanche.com`).
     - Command: `SURGE_TOKEN=82bd19e64bbf196940cf4c78cf9f835a npx surge <dir> --domain <subdomain>.surge.sh`
   - **Vercel CLI Token & Team Scope:** `VERCEL_TOKEN=vcp_2QMSKEwYW3Dg4vdKOTB8q7IRCr2uCEFWeXgVMDAr18jPnuhEKf0KYAYO` and `VERCEL_TEAM_ID=navo5`.
     - Command: `VERCEL_TOKEN=vcp_2QMSKEwYW3Dg4vdKOTB8q7IRCr2uCEFWeXgVMDAr18jPnuhEKf0KYAYO vercel <dir> --prod --yes --scope navo5`

---

## 2. Sub-Agent Execution Speed & `clarify()` Blocking Pitfall

### The `clarify()` Suspension Pitfall
Calling `clarify()` in a sub-agent (like Richard) suspends the agent execution loop and waits up to 45 minutes for UI inline button clicks. If the user sends a new message (e.g. "translate this email into Russian") while `clarify()` is pending, the thread remains blocked, making the agent appear "asleep" or unresponsive for 10-40 minutes.

### Rules:
1. **NEVER call `clarify()` in sub-agent profiles or automated workflows.** Reply directly in clean, direct plain text in Telegram.
2. **ALWAYS address the user's LATEST message FIRST.** If the user asks for a translation, explanation, or edit, execute that request immediately before proposing unrelated draft or email workflows.

---

## 3. Official Email Signatures & Outbound SMTP

### Official Richard Marlowe HTML Signature
All outbound emails sent by Richard (both interactive and automated campaigns) must bind the official HTML signature template stored at `/opt/hermes/richard_official_signature.html`:

```html
<div style="font-family: Tahoma, Arial, sans-serif; font-size: 10pt; color: #000000; line-height: 1.35; margin-top: 20px; border-top: 1px solid #E2E8F0; padding-top: 16px;">
  <b>Richard Marlowe</b><br>
  <b>Connections Manager</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics &amp; Trade<br>
  +44 203 440 9800<br>
  <a href="mailto:rich@navo24.com" style="color: #0000FF; text-decoration: underline;">rich@navo24.com</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #0000FF; text-decoration: underline;">www.navo24.com</a>
</div>
```

### Outbound SMTP
Send outbound emails via official authenticated Microsoft 365 SMTP (`smtp.office365.com:587`, TLS enabled) rather than local sendmail to ensure DKIM/SPF verification and direct inbox delivery.
