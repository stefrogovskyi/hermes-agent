# Automated NDR Bounce Triage & Inbox Sanitization Protocol

## Overview & Risk Context
When conducting cold outreach or follow-ups to historical lead databases (e.g. legacy SeaRates inquiry archives 2021–2024), between 20% and 35% of email addresses are stale (inactivated employee mailboxes, abandoned corporate domains, disabled Google Workspace users).

When dispatching via corporate Microsoft 365 / Microsoft Graph API (`/v1.0/users/{rep_email}/sendMail`), these bounces generate Non-Delivery Reports (NDR) with subjects like `Undeliverable: ...` delivered directly into the sales representative's `Inbox`. This creates two critical operational problems:
1. **Inbox Pollution**: 50+ NDR bounce notices bury genuine customer replies and company inbound leads.
2. **Sender Reputation Hazard**: High bounce rates without list sanitization risk Exchange Online tenant throttling or outbound suspension.

---

## 1. Automated NDR Ingestion & Extraction Pattern

Using Microsoft Graph API (`client_credentials` with Azure App application permissions `Mail.ReadWrite`), systematically scan and extract failed addresses:

```python
import re
import requests
from bs4 import BeautifulSoup

def triage_inbox_bounces(user_email, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Fetch NDR messages from Inbox
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/mailFolders/inbox/messages?$filter=startswith(subject,'Undeliverable')&$top=100"
    res = requests.get(url, headers=headers).json()
    messages = res.get('value', [])
    
    bounced_records = []
    
    for m in messages:
        msg_id = m.get('id')
        subj = m.get('subject', '')
        html = m.get('body', {}).get('content', '')
        text = BeautifulSoup(html, 'html.parser').get_text()
        
        # Regex to locate the actual failed external recipient
        recipients = re.findall(
            r'(?:to the following email addresses:|to these recipients or groups:|wasn\'t found at\s*|recipient:\s*)([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)',
            text, re.IGNORECASE
        )
        
        # Extract diagnostic reason (e.g., 550 5.4.310 DNS nonexistent, 550-5.2.1 DisabledUser)
        reason = "Recipient mailbox unavailable or domain nonexistent"
        if "DisabledUser" in text or "inactive" in text:
            reason = "Account inactive / DisabledUser"
        elif "does not exist" in text or "DNS" in text:
            reason = "Domain DNS nonexistent"
        elif "wasn't found" in text or "User unknown" in text:
            reason = "Recipient user not found on host"
            
        for r in recipients:
            clean_email = r.lower().strip('.')
            if 'navo24.com' not in clean_email and 'microsoft.com' not in clean_email:
                bounced_records.append({
                    'msg_id': msg_id,
                    'email': clean_email,
                    'reason': reason
                })
                
    return bounced_records
```

---

## 2. Inbox Sanitization (Moving NDRs to Deleted Items)

To keep the sales representative's active Inbox clean for real client communications, immediately move processed NDR notices to `deleteditems`:

```python
def clean_ndr_messages(user_email, message_ids, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    cleaned_count = 0
    for mid in set(message_ids):
        move_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages/{mid}/move"
        res = requests.post(move_url, headers=headers, json={"destinationId": "deleteditems"})
        if res.status_code in (200, 201):
            cleaned_count += 1
    return cleaned_count
```

---

## 3. CRM & Google Sheets Suppression Update

Never leave bounced leads in `pending` or `sent` status where future follow-up sequences (Touch 2, Touch 3) could hit them again:

1. Locate row by email address in Google Sheets (`🎯 Forwarders & NVOCC`).
2. Update **Status** (`col B`) -> `bounced`.
3. Update **Stage** (`col C`) -> `Bounced (Mailbox/Domain Dead)`.
4. Add note in **Notes** (`col T`) -> `NDR: <Diagnostic reason> (YYYY-MM-DD)`.
5. Append email to local suppression cache (`optout_suppression_list.json`).

---

## 4. Triage of Genuine Inbound Responses

While filtering out NDR bounces, simultaneously inspect real prospect replies:
- **Change of Mail ID / ЛПР update**: (e.g. *"My email id is changed to kunal@shreesatya.com. Regards, Kunal Janwalikar"*).
  * Immediately update the lead's email, name, title, and phone in the master sheet.
  * Advance the lead to `🔄 Follow-ups & Active Trials` under `🎯 Nikita Personal Cold Email` (or personal rep tag).
  * Prepare a rapid 1-on-1 reply acknowledging the new email and offering the test link (`trackingmcp.com/auth/signup`).
- **Company Routed Inbounds**: (addressed to `sales@navo24.com` or website form submissions).
  * Keep strictly separate from personal cold outreach metrics on the monthly dashboard (`🏢 Company Routed` vs `🎯 Personal Cold Email`).
