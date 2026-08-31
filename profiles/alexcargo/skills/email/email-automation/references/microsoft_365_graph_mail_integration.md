# Microsoft 365 / Exchange / Azure App Registration & Microsoft Graph API Mail Integration for AI Agents

> **Context:** Connecting an AI Agent (e.g. Richard Marlowe `rich@navo24.com`) to Microsoft 365 / Outlook for business email outreach, customer reply monitoring, and Human-in-the-Loop draft approval workflows.

---

## 1. Protocols & Authentication Breakdown

### A. SMTP (Sending Emails)
- **Server:** `smtp.office365.com` (Port `587`, STARTTLS)
- **Authentication:** Standard Basic Auth / User Password works cleanly for outbound email delivery (`rich@navo24.com`).

### B. IMAP Basic Auth Pitfall (Receiving Emails)
- **Problem:** Connecting via `imaplib.IMAP4_SSL("outlook.office365.com", 993)` returns `b'AUTHENTICATE failed.'` even when IMAP is enabled in Microsoft 365 Admin Center (`admin.cloud.microsoft` -> User Details -> Mail -> Manage email apps).
- **Root Cause:** Microsoft Entra ID (Azure AD) has **Security Defaults** active tenant-wide, which overrides Exchange Admin Center settings and blocks legacy Basic Authentication for IMAP.

---

## 2. Microsoft Graph API Solution (Application Permissions)

To allow an AI agent to read inbox messages in real-time without user-present logins:

### Azure Portal App Registration Setup (100% Admin Managed)
1. Go to **Azure Portal** (`portal.azure.com`) as Admin -> **App Registrations** -> **New registration**.
2. Name: `Richard Marlowe Mail Agent` -> Account type: *Single tenant*.
3. Go to **API permissions** -> **Add a permission** -> **Microsoft Graph**:
   - Choose **`Application permissions`** (NOT Delegated!).
   - Under `Mail`, check **`Mail.Read`** or `Mail.ReadWrite`.
   - **CRITICAL STEP:** Click **`Grant admin consent for <Tenant>`** button. (Status column must show green checkmark `Granted`).
4. Go to **Certificates & secrets** -> **New client secret** -> Copy the **`Value`** string.

---

## 3. Azure Portal Setup Pitfalls & Errors

| Error Code | Error Message / Symptom | Root Cause & Exact Fix |
| :--- | :--- | :--- |
| **`AADSTS7000215`** | `Invalid client secret provided. Ensure the secret being sent in the request is the client secret value, not the client secret ID` | The user copied the **`Secret ID`** column instead of the **`Value`** column. In Azure Portal, click "New client secret", copy the string in the **Value** column (`lbN8Q~...`), and use that as `AZURE_CLIENT_SECRET`. |
| **`403 Forbidden` / `ErrorAccessDenied`** | `Access is denied. Check credentials and try again.` | Either the permission was added as **Delegated** instead of **Application**, or the Admin has not clicked the **`Grant admin consent`** button in Azure Portal. Ensure `Mail.Read` is under Application permissions and granted consent. |
| **`URL control chars error`** | `URL can't contain control characters ... $filter=isRead eq false` | `urllib.request` rejects spaces in query parameters. Must URL-encode query string: `$filter=isRead%20eq%20false`. |
| **Telegram `HTTP 400` on notify** | `HTTP Error 400 Bad Request` when forwarding email draft to Telegram | Customer email bodies or LLM drafts contain unescaped HTML tags (`<p>`, `<a>`, `<br>`). Call `html.escape()` on all text fields before formatting into Telegram HTML messages. |

---

## 4. Unread vs Persistent Inbox Polling (`isRead` Pitfall)

### The `isRead` Pitfall
Filtering exclusively on `$filter=isRead eq false` fails when a user opens Outlook Web App (`outlook.office365.com`) in their browser — Outlook automatically marks new incoming emails as `isRead = true`, causing the agent's poller to permanently skip them!

### Robust Polling Recipe
Query the top recent inbox messages ordered by received date, and maintain a persistent tracking file (`processed_email_ids.json`) on disk:

```python
PROCESSED_EMAILS_FILE = "richard_processed_emails.json"

def fetch_recent_inbox_messages():
    url = f"https://graph.microsoft.com/v1.0/users/{EMAIL}/mailFolders/inbox/messages?$orderby=receivedDateTime%20desc&$top=10"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8")).get("value", [])

def poll_inbox_loop():
    processed_ids = load_processed_ids()
    msgs = fetch_recent_inbox_messages()
    for msg in msgs:
        msg_id = msg.get("id")
        if msg_id in processed_ids:
            continue
        
        # Extract FULL HTML body content (NOT bodyPreview!)
        full_body = msg.get("body", {}).get("content") or msg.get("bodyPreview", "")
        
        # Process message, draft reply, and notify user in Telegram
        process_inbound_email(msg, full_body)
        
        save_processed_id(msg_id)
```

---

## 5. Email Threading & Quoted History RFC Compliance

To guarantee that Gmail, Outlook, and Apple Mail group agent replies into the **exact same conversation thread**:

1. **`In-Reply-To` Header:** Pass the parent email's `internetMessageId` (e.g. `<CAB123...@mail.gmail.com>`).
2. **`References` Header:** Pass the space-separated chain of parent message IDs.
3. **Subject Line:** Keep the subject title prefixed with `Re: `.
4. **Signature & Quoted History Order:**
   - **1. Agent Reply Text**
   - **2. Official Corporate HTML Signature Block**
   - **3. Quoted History Block** (`--- Исходное сообщение ---` / full HTML content)

```python
msg = MIMEMultipart("alternative")
msg["From"] = f"Richard Marlowe <{EMAIL_ADDRESS}>"
msg["To"] = to_email
if cc_email:
    msg["Cc"] = cc_email
if in_reply_to:
    msg["In-Reply-To"] = in_reply_to
    msg["References"] = references or in_reply_to

msg["Subject"] = f"Re: {subject}" if not subject.lower().startswith("re:") else subject

full_html = body_html + CORPORATE_HTML_SIGNATURE
if quoted_html:
    full_html += f'''
<br><br>
<div class="gmail_quote" style="border-left: 2px solid #CBD5E1; padding-left: 12px; margin-top: 20px; color: #475569; font-size: 13px;">
  <p style="margin-bottom: 6px; font-weight: bold; color: #64748B;">--- Исходное сообщение ---</p>
  {quoted_html}
</div>
'''

msg.attach(MIMEText(full_html, "html", "utf-8"))
```

---

## 6. Human-in-the-Loop Approval Interceptor Pattern

For early-stage operations or sensitive accounts:
1. **Outreach Campaigns:** Triggered strictly on explicit user command (`/outreach` or "Start email campaign").
2. **Inbound Reply Approval:**
   - AI agent reads customer email via Graph API.
   - AI agent generates draft response.
   - AI agent sends Telegram notification to the owner with `html.escape()` formatting.
   - **Deterministic Approval Interceptor:** When user writes "Отправляй", "Да", "Ок" in Telegram:
     - Handler intercepts approval triggers BEFORE sending prompt to LLM.
     - Loads the pending draft file from `drafts/draft_*.json`.
     - Calls `send_email_direct()`, passing `in_reply_to` and `quoted_html`.
     - Deletes/archives draft file and replies in Telegram: `🚀 ПИСЬМО УСПЕШНО ОТПРАВЛЕНО КЛИЕНТУ!`.

---

## 7. OpenAI Function Calling Tool-Call Normalization Fix (`HTTP 400 Bad Request`)

When using `gpt-4o-mini` or OpenAI-compatible Chat Completions with tools enabled:
- OpenAI response message contains `choice["message"]` with `"content": null` and `"tool_calls": [...]`.
- Appending `choice` directly to `messages` causes OpenAI to reject subsequent calls with `HTTP Error 400 Bad Request: Invalid type for messages[N].content: expected a string, given null`.

**Fix:**
```python
choice = resp["choices"][0]["message"]
msg_to_append = {
    "role": choice.get("role", "assistant"),
    "content": choice.get("content") or "" # Convert None to ""
}
if choice.get("tool_calls"):
    msg_to_append["tool_calls"] = choice["tool_calls"]
messages.append(msg_to_append)
```
