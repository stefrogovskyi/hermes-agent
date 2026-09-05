# Case: Richard Outbound Sales Safety HITL Rules, Notification Routing & Daily Team Summary Cron

**Date:** 2026-09-04  
**Profiles involved:** `richard`, `default` (Hermes)  
**Domains:** `agent_club`, `business`

---

## 1. Context & Incidents
Richard Marlowe (`@richnavobot`) executed multiple high-volume and bespoke sales operations:
1. Multi-batch cold email sequences for Elena Habrelian (`olena.h@e.navo24.com`) and Nikita (`nikita@navo24.com`) via Resend (`Navo24-3`).
2. Pointed communication with hot incoming leads: Shreesatya Logistics, Olicargo, Gatehouse Maritime, Yuri Golyato, and Dr. Muddassir Ahmed (SCM Sensei).
3. Daily coordination with account executives (Elena, Alena, Nikita, Maria).

During these operations, crucial governance lessons were established regarding human-in-the-loop email safety, notification isolation, and daily team reporting.

---

## 2. Lessons & Established Policies

### A. Human-in-the-Loop (HITL) for Targeted Emails:
* **Incident:** An email draft was dispatched to an Indian lead before full manual verification.
* **Stefan's Directive:** For all bespoke outbound emails, follow-ups, and responses to warm incoming leads, Richard MUST show the full draft to the manager/Stefan (Recipient, Subject, Body, Signature) for explicit approval before sending. Automated sending without prior review is strictly forbidden for point-to-point communications.

### B. Notification Routing Isolation:
* In the cold email campaign for Elena Habrelian (`olena.h@e.navo24.com`), inbound lead replies and bounces were initially flooding notifications.
* **Stefan's Directive:** Route reply notifications strictly to Elena Habrelian in Telegram (`@OlenaT1`). Stefan's DM must remain clean of routine manager alerts.

### C. Commercial & Pricing Policies:
* **Prepaid Wallet Deposits:** Recommended model for new clients (e.g. Yuri Golyato $400, Gatehouse Maritime $4,800). Credit statements provided monthly between the 1st and 7th.
* **Rate Limits:** Peak-season limit increases accommodated calmly (e.g. from 750k to 850k calls) to preserve long-term partner loyalty.
* **Overage Policy:** Hard-cap by default (API key blocks at limit until 1st of month or credit top-up), pending formal company review of soft-cap mechanisms.
* **Anti-AI Fluff in Sales:** When communicating with experienced tech leaders (e.g. Dr. Muddassir Ahmed), avoid speculative AI promises ("agentic workflows"). Point strictly to live production integrations (Shipzy ERP, native `/v1/rates` and `/v1/containers` endpoints).

### D. Daily Team Summary Cron:
* **Stefan's Instruction:** At 21:00 Kyiv (19:00 UTC), create a daily summary cron aggregating all team interactions with Richard across the day.
* **Execution:** Created cron job `richard-daily-team-summary` (`0 19 * * *`), running `/opt/hermes/profiles/richard/scripts/generate_daily_team_summary.py` to compile manager activity and client pipeline status into an evening digest.

---

## 3. Summary of Rules
- **Rule 1 (HITL):** Show full email draft to human supervisor before sending bespoke sales emails.
- **Rule 2 (Alert Routing):** Send campaign response alerts to the campaign owner's Telegram handle only.
- **Rule 3 (Proof-First Sales):** Never sell hypothetical AI features; sell working APIs, documented payloads, and live customer deployments.
