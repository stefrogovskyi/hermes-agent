# Telegram Gateway Network Resilience, Identity Security & Group Pairing

## 1. Network Reconnect Timeouts (Preventing "Gateway Shutting Down")
On Windows hosts, brief Wi-Fi or ISP network drops can cause Telegram long-polling to time out.
If the gateway's default watchdog deadline (180s) is exceeded, Hermes shuts down the gateway with:
`⚠️ Gateway shutting down — Your current task will be interrupted.`

**Fix:** Set fast network reconnect timeouts in `profiles/<name>/.env`:
```env
HERMES_TELEGRAM_INIT_TIMEOUT=10
HERMES_TELEGRAM_HTTP_CONNECT_TIMEOUT=10
```
This forces the gateway to attempt rapid reconnects within 5-10 seconds rather than hanging for 3 minutes and shutting down.

---

## 2. Hard Identity Guardrail: No User Account Impersonation
Sub-agents and bots MUST write ONLY via their official Bot API tokens (`@qubicpmbot`, `@richnavobot`, `@callumvancebot`, `@lizharperbot`, `@benjettbot`).
- **NEVER** use user account tokens or MTProto userbots to post messages on behalf of the owner (Stefan).
- Every bot must interact exclusively as its own character/persona.

---

## 3. Team Authorization in Group Chats (`telegram-approved.json`)
When `group_response_mode: mention` is active, messages from group members whose Telegram user IDs are not listed in `telegram-approved.json` are dropped as `[Telegram] Blocked unauthorized user`.

**Fix:** Ensure all authorized team members (e.g., COO, Tech Lead, Ops PMs) are pre-approved in `profiles/<name>/platforms/pairing/telegram-approved.json`:
```json
[
  "330656040",
  "1022586369",
  "363779334"
]
```

---

## 4. Self-Contained Vercel Trello Kanban Integration
Each profile or agent can have its own self-contained interactive Trello-style Kanban board deployed to Vercel (`https://agentname-kanban.vercel.app`).
- **API Endpoint:** Use Vercel Serverless Functions (`/api/kanban`) so state management is 100% self-contained on Vercel without relying on external host domains.
- **Persistence:** Ensure POST actions (`move_task`, `add_comment`, `add_task`) update the board JSON state persistently so drag-and-drop card movements never roll back on lambda cold-starts.
