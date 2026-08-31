---
name: microsoft-365-agent-email
description: "Connect AI agents to Microsoft 365 email via Graph API."
---

# microsoft-365-agent-email

Class-level workflow for connecting AI agents to Microsoft 365 / Exchange Online email accounts (outbound SMTP, inbound Graph API, and Human-in-the-Loop draft approval).

## When to use
- Connecting an AI agent or persona bot to Microsoft 365 / Outlook corporate email (`@domain.com`).
- Configuring email outreach, draft approvals, or Exchange Online authentication.

## Key Technical Architecture

### 1. Outbound SMTP Sending
- **Server:** `smtp.office365.com`, Port `587` (STARTTLS).
- **Authentication:** Works with user credentials (`email` + `password`).

### 2. Corporate HTML Signatures on Programmatic Sends
- **Pitfall:** Exchange Online / Microsoft 365 does NOT automatically append OWA/Outlook browser signatures when sending messages programmatically via SMTP or Graph API.
- **Solution:** Embed the exact corporate HTML signature template (see `templates/corporate_signature_template.html` for boilerplate) inside the agent's sending module so every outgoing message HTML body automatically includes the signature.
- **NO HORIZONTAL RULES RULE:** NEVER add horizontal divider lines (`<hr>` tags or `border-top` CSS borders) above the corporate signature unless explicitly requested by the user. Keep the transition from body text to signature clean (e.g. 2 `<br>` breaks).
- **Exact Styling & Working Image URLs:** Ensure image URLs in HTML signatures are verified and working (e.g. hosted CDN / Bitly link) rather than broken inline SVGs or placeholder tags. Format links with explicit blue styling (`color: #0000FF; text-decoration: underline;`).
- **CRITICAL Placement Rule:** The corporate signature MUST be inserted IMMEDIATELY below the agent's reply text, and ABOVE the quoted email history block (`--- Исходное сообщение ---`), NOT at the very bottom of the entire email chain.
- **Detailed Reference:** See `references/email_threading_and_approval_guide.md` for RFC headers, body ordering, and deterministic approval intercepts.

### 3. Outbound Email Deliverability & Authenticated SMTP/Graph API
- **Pitfall — Unauthenticated Sendmail Rejection:** Sending emails via unauthenticated local Linux `sendmail` or raw MTA scripts on cloud VPS (Hetzner/Servarica) without valid SPF, DKIM, and DMARC records causes recipient mail servers (Gmail, Outlook, Yahoo) to reject or silently drop the messages (`550 5.7.26 Unauthenticated email`).
- **Solution:** ALWAYS route outbound emails through authenticated Office 365 / Exchange SMTP (`smtp.office365.com:587` with STARTTLS + user credentials) or Microsoft Graph API (`/me/sendMail` or `/users/{id}/sendMail`). Authenticated sending applies valid tenant SPF/DKIM signatures, guaranteeing 100% inbox delivery.

### 3. RFC Email Threading & `Reply-To` Header
- **Preserving Email Threads (Gmail/Outlook):**
  1. Pass `In-Reply-To: <Message-ID>` and `References: <Message-ID>`.
  2. Prefix subject with `Re: `.
  3. Include quoted previous email history block BELOW the signature.
- **`Reply-To` Header:** Always explicitly set `Reply-To: Agent Name <email@domain.com>`. Without this header, email clients like Gmail can substitute the user's own CC address when clicking "Reply", causing the user to draft a self-reply instead of replying to the agent.

### 4. Inbound IMAP vs Microsoft Graph API
- **IMAP Basic Auth Restriction:** In Microsoft 365, IMAP Basic Auth returns `b'AUTHENTICATE failed'` when tenant Security Defaults or Conditional Access policies are active in Microsoft Entra ID (Azure AD), even if IMAP is checked in Exchange Admin Center.
- **Solution — Microsoft Graph API (`client_credentials` grant):**
  1. Register an App in Azure Portal (`portal.azure.com`) under Admin account.
  2. Add API Permission: **Microsoft Graph** -> **Application permissions** -> **`Mail.Read`** (or `Mail.ReadWrite`).
  3. Click **Grant admin consent**.
  4. Create a **Client Secret** and copy the **Value** (not Secret ID!).
  5. Fetch inbox messages via `GET https://graph.microsoft.com/v1.0/users/<email>/mailFolders/inbox/messages?$orderby=receivedDateTime%20desc&$top=10` (ensure URL query is percent-encoded).

### 5. Inbound Polling & OWA `isRead` Pitfall
- **Pitfall:** If a human user opens the mailbox in Outlook Web App (OWA) or Outlook Desktop, Exchange automatically marks incoming messages as `isRead = true`. If the agent's Graph API query uses `$filter=isRead eq false`, opened/synced emails are completely ignored and missed by the agent!
- **Solution:** Query recent messages ordered by date descending (`$orderby=receivedDateTime desc&$top=10`) WITHOUT filtering on `isRead`, and track processed message IDs in a local JSON state file (`seen_email_ids.json`).
- **`bodyPreview` vs Full HTML Body:** `m.get("bodyPreview")` is only a 255-character teaser snippet. To preserve the FULL accumulated conversation history across multiple turns, ALWAYS extract `msg.get("body", {}).get("content")` (the full 8000+ char HTML body) and pass it as `quoted_html`. `Re:` in subject keeps the thread grouped, while the full HTML body ensures no previous turn history is lost.

## 6. Real Semantic Health Check Standard for Bot Watchdogs
- **Pitfall:** Checking `psutil.pid_exists(pid)` ALONE in a watchdog or cron audit is a flawed health check — a Python process can be running in Task Manager while its LLM model or API key is dead (`403 Forbidden` / `401 Unauthorized`), causing the bot to output stencil error messages (`"LLM-ключ не подключён"` or `"lost the line to the desk"`).
- **Solution:** Watchdogs (`bot_watchdog.py` and daily self-heal crons) MUST perform a **REAL SEMANTIC LLM MESSAGE TEST** (`run_agent('ping')`). If a bot fails the semantic test, hangs, or returns a stencil error, the watchdog immediately repairs its API keys and restarts the process silently via `pythonw.exe`.

## Tool-Calling & LLM Agent Loop Gotcha
- **OpenAI Tool Call Normalization:** When an LLM model returns a message with `tool_calls`, `choice.get("content")` is `None` (null). When building the messages history array for follow-up turns (both on the first tool call and inside the `while choice.get("tool_calls")` loop), `content` MUST be normalized to `""` (empty string) instead of `None`, otherwise OpenAI API returns `HTTP Error 400: Invalid type for messages[N].content: expected a string, given null`.
- **Background Daemon Environment Scope:** Background processes (`pythonw.exe` / `bot_watchdog.py`) do not inherit host terminal environment variables. `_load_env()` MUST explicitly load `AppData/Local/hermes/.env` before module-level variables (`MODEL = os.environ.get(...)`) evaluate, otherwise LLM calls fall back to unauthenticated endpoints and throw 401/403 or trigger generic error fallbacks (e.g., "lost the line to the desk").
- **`_TypingTicker` Class Definition Order:** When `run_agent()` starts a background typing indicator thread via `_TypingTicker(token, chat_id)`, the `_TypingTicker` class must be defined BEFORE `run_agent()`. Unhandled `NameError` in `run_agent()` triggers exception handlers that return fallback stub responses.

## Human-in-the-Loop Draft Approval Guardrail & Deterministic Intercept
- **Campaigns:** Triggered only on explicit user command.
- **Inbound Customer Replies:**
  1. Read incoming email via Graph API.
  2. Generate professional B2B draft response.
  3. **DO NOT send automatically!**
  4. Send draft notification to user in Telegram:
     - Sender, Subject, Customer Query
     - Draft Response Text
     - Wait for explicit user confirmation ("Отправляй" / "Oк") before sending.
  5. **Deterministic Approval Intercept (Fast-Path):**
     - When the user in Telegram replies "Отправляй", "Да", "Ок", "Send", or quotes the draft notification, the bot handler MUST intercept the approval at the telegram loop level, load the pending draft from `drafts/<draft_id>.json`, and call `send_email_direct()` directly.
     - Do NOT route approval commands through an unguided LLM chat turn — without explicit pending draft context in the LLM prompt, the LLM will hallucinate ("I cannot send emails" or "What should I send?") instead of executing the send.
  6. **No Re-asking Rule:** When the user replies "Отправляй", "Да", "Ок", or confirms the draft, the agent MUST immediately send the email and NEVER re-ask "Are you sure?" or "Please confirm again". A single "Yes" / "Send" is an immediate execution command.
