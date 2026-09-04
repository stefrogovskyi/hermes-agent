# 4-Touch Conditional Sequences & Multi-Mailbox NDR Bounce Monitoring

Implementation guide for launching multi-touch sales sequences across historical customer archives and automating inbox/bounce handling.

## 1. Sequence Timing & Copy Pattern

| Step | Offset | Subject | Core Value Hook |
|---|---|---|---|
| **Touch 1** | Day 0 | `quick question, {company}` | Reconnecting as ex-SeaRates team; asking if freight needs are solved or manual. |
| **Touch 2** | Day 4 | `what changed` | Full product suite: TrackingMCP, AirCargoMCP, SchedulesMCP, LoadingMCP, FreightRatesMCP. |
| **Touch 3** | Day 9 | `worth a quick look?` | 15-minute qualification or live test of their specific shipping use case. |
| **Touch 4** | Day 16 | `closing the loop` | Respectful breakup; permanent Free Tier (5 containers, no credit card, no expiry). |

## 2. Sequence Advancement Rules

1. **Stop on Reply:** As soon as an inbound reply from the recipient is detected in MS Graph, halt all future touches for this contact.
2. **Stop on Bounce:** If a delivery failure notification (NDR) is received, mark status as `Bounced` in Google Sheets and halt all future touches.
3. **Threading:** Touches 2, 3, and 4 should set `In-Reply-To` and `References` headers to the Message-ID of Touch 1 to thread naturally in the prospect's inbox.
4. **Pacing & Weekday-Only Constraint:** Send new Touch 1 emails at a controlled rate of 100–150/day strictly on **business days (Mon–Fri)**. Follow-ups (Day 4, 9, 16) also execute strictly on weekdays to maintain professional B2B delivery standards.
5. **Subject Line Fallback:** Use `quick question, {company}`. If the company name is missing in the database, automatically fallback to `quick question, {first_name}`.

## 3. Standardized Account Executive Signature & Pre-Flight Testing

Every sales representative's outbound email must use the standardized HTML signature layout with the official Navo logo:

```html
<div style="margin-top: 24px; font-family: Tahoma, Arial, sans-serif; font-size: 13px; color: #334155; line-height: 1.4; text-align: left;">
  <b>{NAME}</b><br>
  <b>Account Executive</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics & Trade<br>
  {PHONE}<br>
  <a href="mailto:{EMAIL}" style="color: #2563eb; text-decoration: underline;">{EMAIL}</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #2563eb; text-decoration: underline;">www.navo24.com</a>
</div>
```

**Known AE Profiles:**
- **Nikita Kurudzhy:** `nikita@e.navo24.com`, `+380 93 228 5150`, TG `@nikita51155` (ID `288669722`)
- **Elena Habrelian:** `olena.h@e.navo24.com`, `+374 96 798796`, TG `@OlenaT1` (ID `476876665`)

**Mandatory Pre-Launch Test:** Always send a live test email with the exact signature and rendered copy to Stefan (`stefan@navo24.com`) and await explicit approval before launching any batch.

## 4. NDR / Bounce Extraction Pattern

```python
def is_delivery_failure(msg):
    sender = msg.get("from", {}).get("emailAddress", {}).get("address", "").lower()
    subject = msg.get("subject", "").lower()
    bounce_indicators = [
        "mailer-daemon",
        "postmaster",
        "delivery status notification",
        "undeliverable",
        "failure notice",
        "returned to sender"
    ]
    return any(ind in sender or ind in subject for ind in bounce_indicators)

def extract_bounced_recipient(body_text):
    import re
    # Look for Failed-Recipient or typical NDR patterns
    patterns = [
        r"Failed-Recipient:\s*(?:rfc822;)?\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
        r"To:\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
        r"<([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>:\s*(?:550|554|Host not found|User unknown)"
    ]
    for p in patterns:
        m = re.search(p, body_text, re.IGNORECASE)
        if m:
            return m.group(1).lower()
    return None
```

## 5. Google Sheets Status Syncing & Telegram Alerts

When syncing outreach status to the master sheet (`1rfmzmlDLNv3l2O1g2fYjw0PL40IGbsT-sdq6pA2eFZA`):
- `Status`: `Touch 1 Sent` | `Touch 2 Sent` | `Touch 3 Sent` | `Touch 4 Sent` | `Replied / Warm` | `Bounced`
- Maintain timestamp columns (`Touch 1 Date`, `Last Activity`, `Reply Date`).
- **On `Replied / Warm`:**
  - Instantly halt all future sequence touches for this recipient.
  - Deliver a Telegram briefing via `@richnavobot` to both the assigned sales rep (e.g. Elena `@OlenaT1` / ID `476876665`, Nikita `@nikita51155` / ID `288669722`) and Stefan (`330656040`).
  - Card includes sender info, clean original message, full Russian/Ukrainian translation, and ready-to-use proposed reply.
