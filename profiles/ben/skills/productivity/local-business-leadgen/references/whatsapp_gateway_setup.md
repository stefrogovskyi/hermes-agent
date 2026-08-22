# WhatsApp Web / Baileys Gateway Setup Guide

## Purpose
Enables direct WhatsApp outreach using an existing WhatsApp account on a phone via the Baileys Multi-Device protocol without risking number loss or requiring Meta WhatsApp Business verification (A2P 10DLC).

## Architecture
1. **Node.js microservice (`index.js`):** Runs locally on port 3050.
2. **Session Storage (`auth_info_baileys/`):** Persistent QR auth tokens.
3. **Endpoints:**
   - `GET /status`: Returns connection state (`qr_ready`, `connected`, `disconnected`) and base64 QR data URL.
   - `POST /send-message`: Takes `{ phone, message }`, validates JID existence on WhatsApp, and dispatches message with rate-limiting safety.
4. **Service Daemon:** Managed via systemd service (`whatsapp-gateway.service`) for auto-restart on reboots.

## Dispatch Automation
- **Rate-Limiting Rule:** In automated batch campaigns, maintain a **5-minute delay (300 seconds)** between messages to protect the WhatsApp account from bans and rate limiting.
- **Multichannel Fallback:** Pair WhatsApp with Hostinger SMTP (`contact@aavalanche.com` with `Reply-To: <personal_inbox>`). If the target number is a landline / not registered on WhatsApp (`sock.onWhatsApp(jid)` is null), fall back to email or mark as landline for manual calling.
- **Process Management:** Prevent dual-process conflicts (error 440 `Connection Replaced`) by running exclusively under `systemctl start whatsapp-gateway` and ensuring no orphan node instances exist before starting.
- **Cron Scheduling:** Schedule daily cron jobs with UTC offset adjustments (e.g. 23:00 Kyiv is 20:00 UTC during EEST / 21:00 UTC during EET).
