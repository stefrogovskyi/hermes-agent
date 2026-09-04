# Team Manager Inbound Polling, Direct Telegram Alerts & Google Sheets CRM Sync

## Overview

When running outreach campaigns on behalf of specific Account Executives / Sales Managers (e.g. Lena Habrelian `olena.h@navo24.com`, Nikita Kurudzhy `nikita@navo24.com`), inbound replies route back to the individual manager's M365 inbox.

This playbook defines the architecture for:
1. Monitoring individual manager mailboxes centrally via MS Graph API application permissions.
2. Filtering, parsing, and triaging inbound client responses.
3. Sending instant real-time Telegram alerts directly to the specific manager's Telegram chat.
4. Auto-updating the campaign Google Sheet / CRM table with contact status and response details.

---

## 1. MS Graph API Multi-Mailbox Inbound Polling

Our Azure App Registration (`Rich email graph inbox api`, Client ID `807fed17-45a8-4c7c-9a28-5997bbd30970`) carries tenant-wide Application Permissions (`Mail.ReadWrite`, `Mail.Send`).

### Polling Endpoint Pattern:
```python
import requests

TENANT_ID = "dc47c5b1-313f-47eb-ab6f-5f0716f400b5"
CLIENT_ID = "807fed17-45a8-4c7c-9a28-5997bbd30970"
CLIENT_SECRET = os.getenv("MS_GRAPH_CLIENT_SECRET")

# Auth token
token_res = requests.post(
    f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    },
    timeout=15
)
access_token = token_res.json()["access_token"]

# Query target manager's inbox
manager_email = "olena.h@navo24.com"
url = f"https://graph.microsoft.com/v1.0/users/{manager_email}/mailFolders/inbox/messages?$top=15&$orderby=receivedDateTime desc"
headers = {"Authorization": f"Bearer {access_token}"}
messages = requests.get(url, headers=headers).json().get("value", [])
```

### Inbound Message Filtering:
- Ignore self-sent messages (`from.emailAddress.address == manager_email`).
- Ignore internal automated bounce reports (`postmaster@`, `microsoftexchange`).
- Persist processed message IDs in a local cache (e.g. `/opt/hermes/profiles/richard/cache/seen_manager_emails.json`).

---

## 2. Manager-Specific Telegram Alerts

Deliver notifications directly to the assigned manager's private Telegram chat:
* **Lena (@OlenaT1):** Telegram User ID `476876665`
* **Nikita (@nikita51155):** Telegram User ID `288669722`

### Telegram Bot API Dispatch:
```python
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = "476876665"  # Lena

text_message = f"""📩 **НОВОЕ ВХОДЯЩЕЕ ПИСЬМО!**
* 👤 **Отправитель:** {sender_name} (`{sender_email}`)
* 🏢 **Компания:** {company_name}
* 📱 **Телефон:** {phone}
* 📌 **Тема:** {subject}

💬 **Оригинал сообщения:**
> {cleaned_body}

🇷🇺 **Перевод на русский язык:**
> {russian_translation}

✍️ **Готовый проект ответа (Navo24):**
{draft_reply}
"""

requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
    json={
        "chat_id": TARGET_CHAT_ID,
        "text": text_message,
        "parse_mode": "Markdown"
    },
    timeout=10
)
```

---

## 3. Two-Way Google Sheets CRM Synchronization

When a client replies, find their row in the campaign Google Sheet (e.g. `SeaRates B2B Requests`, ID `1rfmzmlDLNv3l2O1g2fYjw0PL40IGbsT-sdq6pA2eFZA`) and update their status.

### Authentication Safety Rule:
- Service accounts (`richard-bot@...`) can fail with `invalid_grant: Invalid JWT Signature` or `403 Permission Denied` on user-owned sheets without explicit sharing.
- Always prefer the verified OAuth2 token (`/opt/hermes/profiles/richard/google_token.json`):

```python
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

with open('/opt/hermes/profiles/richard/google_token.json') as f:
    tok = json.load(f)

creds = Credentials.from_authorized_user_info(tok)
sheets_service = build('sheets', 'v4', credentials=creds)

# Search lead by email in Column B
spreadsheet_id = "1rfmzmlDLNv3l2O1g2fYjw0PL40IGbsT-sdq6pA2eFZA"
sheet_name = "'Все запросы (2024-2025)'"

# Update status column to "Replied / Warm"
```
