# Microsoft Graph Direct Outreach, Threading & Fact-Check Architecture

## 1. Dual Dispatch Strategy: Resend vs. Direct Microsoft Graph API

### Channel Characteristics
- **Resend REST API (`<name>@e.navo24.com`)**:
  - Daily quota cap (100 emails/day on free tier) and risk of invalidation (`401 API key is invalid`).
- **Direct Microsoft Graph API (`nikita@navo24.com`, `rich@navo24.com`)**:
  - Direct delivery from corporate M365 tenant (`dc47c5b1-313f-47eb-ab6f-5f0716f400b5`).
  - Automatically saves in Outlook **Sent Items** (`saveToSentItems: true`).
  - Replies return straight to the personal inbox.
  - Immune to Resend 100/day tier limits.

```python
import requests

TENANT_ID = "dc47c5b1-313f-47eb-ab6f-5f0716f400b5"
CLIENT_ID = "807fed17-45a8-4c7c-9a28-5997bbd30970"
CLIENT_SECRET = "g4d8Q~CNgmzLDEE1g_enAIqTpClyZ4N~VKhK9c63"

# Obtain Application Token
url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
token_res = requests.post(url, data={
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials",
    "scope": "https://graph.microsoft.com/.default"
}, timeout=15).json()
access_token = token_res["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send as authorized rep (e.g. nikita@navo24.com)
send_url = f"https://graph.microsoft.com/v1.0/users/nikita@navo24.com/sendMail"
payload = {
    "message": {
        "subject": subject,
        "body": {
            "contentType": "Text",
            "content": body_text
        },
        "toRecipients": [{"emailAddress": {"address": recipient_email}}],
        "ccRecipients": [{"emailAddress": {"address": "stefan@navo24.com"}}]
    },
    "saveToSentItems": "true"
}
res = requests.post(send_url, headers=headers, json=payload, timeout=15)
# Status 202 = Accepted and Dispatched
```

---

## 2. Follow-Up (Touch 2) Threading & Timing Rules

1. **Email Threading Preservation**:
   - Subject line **MUST** be `RE: {Original Touch 1 Subject}` (verbatim).
   - In individual 1-on-1 replies, populate `In-Reply-To` and `References` headers with `InternetMessageId`.
2. **Safe Follow-up Window**:
   - Touch 2 must be sent **48 to 72 hours (2–3 business days)** after Touch 1.
3. **Touch 2 Content Architecture**:
   - Under 45 words.
   - Focus on D&D Free-Time Calculation across 239 lines and Free Tier link.

---

## 3. Inbound Classification: Company Inbound vs. Personal Cold Replies

When polling a manager's mailbox via MS Graph API (`GET /v1.0/users/{email}/mailFolders/inbox/messages`):
- If `toRecipients` contains `sales@navo24.com` or sender is `submissions@formsubmit.co`:
  - **Tag**: `🏢 Company Routed (General Inbound)`.
  - Website leads or generic sales inquiries, NOT direct responses to cold outreach batches.
- If `toRecipients` is strictly `{manager}@navo24.com` and subject begins with `RE:` matching outbound campaigns:
  - **Tag**: `🎯 Personal Cold Email Reply`.

---

## 4. STRICT ZERO FABRICATION GATE (Pre-Response Verification)

Before outputting ANY draft, quota explanation, pricing breakdown, or error cause:
1. **Source Check**:
   - Quotas & Trials: strictly 5 ocean containers, 100 API calls/mo, no Air AWB on self-serve portal (`Navo24_Sales_Manager_Playbook_RU.docx`).
   - Pricing: strictly PAYG $4.00–$0.60, Annual $3.00–$0.45 (`pricing_calculator.py`).
   - Technical errors / statuses: strictly quotes from engineering team.
2. **Assumption Ban**: If a feature is not in verified docs, state honestly: *"This is not in the documentation; needs developer/Stefan confirmation."*
