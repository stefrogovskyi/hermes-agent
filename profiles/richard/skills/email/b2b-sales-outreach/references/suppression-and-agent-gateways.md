# Operational Reference: Suppression, Gateways & Reporting Standards

## 1. Multi-Agent WhatsApp Gateway Isolation
- **Port 3050:** Ben Jett (`+1 302 401 9315` / Avalanche LeadGen). Service: `whatsapp-gateway.service`.
- **Port 3060:** Richard Marlowe (`+44 7360 065904` / Navo24 London). Service: `richard-whatsapp-gateway.service`.
- **Strict Rule:** Richard MUST NEVER send messages via port 3050. All WhatsApp communications for Navo24 must target `http://localhost:3060/send-message` with JSON `{"phone": "<clean_number>", "message": "<text>"}`.

## 2. Centralized Opt-Out & Suppression List
- **Registry File:** `/opt/hermes/profiles/richard/cache/optout_suppression_list.json`
- **Execution Checklist on User Opt-Out Request:**
  1. Add email address to `/opt/hermes/profiles/richard/cache/optout_suppression_list.json`.
  2. Search and purge records across:
     - Navo CRM (`appbxvl9BBaTiLMlf`)
     - Online Outreach (`appdJR8VVczRxcVke`)
     - Rich Outreach (`appEoWQjvhgN8LIX7`)
     - Google Sheets pipelines (Radar, Sales Tracker)
     - Local lead archives (`/opt/hermes/profiles/richard/searates_archive/parsed_leads.json`).
  3. All outreach scripts (`daily_online_outreach_engine.py`, `nikita_forwarders_outreach_engine.py`) load this JSON and skip any matching recipient automatically.

## 3. Email Deliverability: Restrictive / Chinese Domains
- **Microsoft 365 (MS Graph):** Frequently rejects outbound emails to Chinese mail hosts (`189.cn`, `163.com`, `qq.com`, `siyang-china.com`) with `550 5.7.708 Service unavailable. Access denied, traffic not accepted from this IP`.
- **Resend REST API:** Verified domain `e.navo24.com` on AWS SES authenticated IP pool. Has 100% deliverability to Asian and strict enterprise servers.
- **Failover Rule:** If M365 blocks or bounces with `550 5.7.708`, failover immediately to Resend (`rich@e.navo24.com` / `nikita@e.navo24.com`) with `Reply-To` pointing to the corporate inbox (`@navo24.com`).

## 4. Telegram Reporting Standards (Markdown Only)
- Reports delivered to Telegram must use standard Markdown formatting:
  - `**bold**` instead of `<b>`
  - `*italic*` instead of `<i>`
  - `` `code` `` instead of `<code>`
- Never output raw HTML tags in user-facing Telegram messages.
