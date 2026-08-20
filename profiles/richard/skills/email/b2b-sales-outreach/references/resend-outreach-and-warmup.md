# Resend Mass Outreach & Subdomain Warm-Up Specification

## 1. Architecture Overview
- **Sending Service**: Resend REST API (`https://api.resend.com/emails`)
- **Verified Subdomain**: `e.navo24.com` (AWS us-east-1 / Resend verified)
- **Sender Address (`from`)**: `Richard <sales@e.navo24.com>` (or `sales@e.navo24.com`)
- **Reply Address (`reply_to`)**: `richard@navo24.com` (or `rich@navo24.com` -> routes directly to Richard's Outlook inbox)
- **Root Domain Protection**: Root `navo24.com` has DMARC `p=reject` and M365 email. Using `@navo24.com` for bulk cold outreach triggers `550 5.1.8 Bad outbound sender`. Bulk cold sending MUST ALWAYS go through `e.navo24.com` via Resend.

## 2. Mandatory Headers (RFC 8058 / Gmail & Yahoo Bulk Sender Compliance)
Every outreach email dispatched via Resend must include:
```python
headers = {
    "List-Unsubscribe": "<mailto:unsubscribe@navo24.com>, <https://navo24.com/unsubscribe?e={recipient_email}>",
    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
}
```
- Open tracking and click tracking: OFF / disabled.

## 3. Warm-Up Schedule (Daily Caps)
| Stage | Days | Daily Volume Limit | Sending Cadence |
|-------|------|--------------------|-----------------|
| Phase 1 | Day 1–2 | 50 sends / day | 1 email every 8–10 min (spread throughout day) |
| Phase 2 | Day 3–4 | 150 sends / day | 1 email every 3–5 min |
| Phase 3 | Day 5–7 | 500 sends / day | 1 email every 1–2 min |
| Phase 4 | Day 8–10 | 1,000 sends / day | Throttled burst / continuous flow |
| Scale | Day 11+ | 2x every 2–3 days | Monitor bounce < 3%, complaints < 0.1% |

## 4. Code Implementation Pattern
```python
import os
import requests

def send_outreach_resend(recipient, subject, html_content):
    api_key = os.environ.get("RESEND_API_KEY")
    payload = {
        "from": "Richard <sales@e.navo24.com>",
        "to": [recipient],
        "reply_to": "richard@navo24.com",
        "subject": subject,
        "html": html_content,
        "headers": {
            "List-Unsubscribe": f"<mailto:unsubscribe@navo24.com>, <https://navo24.com/unsubscribe?e={recipient}>",
            "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"
        }
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.resend.com/emails", headers=headers, json=payload, timeout=15)
    return response.json()
```
