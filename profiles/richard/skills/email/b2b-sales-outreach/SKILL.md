---
name: b2b-sales-outreach
description: "Draft, translate, and handle B2B sales email outreach."
version: 0.1.0
author: Richard Marlowe, Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Email, Sales, Outreach, Translation, B2B]
    related_skills: [email-inbox-triage, himalaya]
---

# B2B Sales Outreach & Reply Workflows

Guidelines for drafting, translating, and confirming B2B sales email replies for international freight logistics and prospective clients.

## When to Use

- Drafting or translating B2B sales emails for prospective clients.
- Handling client draft feedback from Stefan or team members.
- Qualifying inbound sales leads via email.

## Key Principles

1. **No Snake Emojis & Tool Usage**: NEVER use snake emojis (🐍) in any messages, status reports, email drafts, or Telegram outputs. Prefer using `terminal` over `execute_code` for background tasks and shell scripts to prevent python snake icons from rendering in the platform UI.
2. **Persistent Background Workers**: When running long-lived background workers (like cold outreach daemons), use `terminal(command="PYTHONUNBUFFERED=1 python3 -u script.py >> log 2>&1", background=True)` rather than a transient subshell `nohup &`, which gets terminated when the execution turn closes.
3. **Client Language Matching**: Always match the language of the prospect. If a Chinese client replies in Chinese (e.g. 陈先生 from Qiaoye Logistics), translate questions and draft responses into clear, professional B2B Chinese.
2. **Direct Execution on Feedback**: When the user approves draft direction (e.g., "Billy text is good - translate to Chinese and send") or tells you to stop ("Стоп"), execute the translation, draft, or answer directly without embarking on unnecessary exploratory tool searches or file queries.
3. **Inbound Replies vs. Mass Cold Outreach**:
   - **Inbound Replies (1-on-1 Threading & Russian Translation Mandate)**:
     - **Russian Translation Mandate**: ALWAYS provide Stefan with a clear Russian translation of BOTH the client's message and Richard's proposed draft reply (e.g. 💬 **Сообщение клиента (Оригинал)**, 🇷🇺 **Перевод сообщения клиента**, ✍️ **Предлагаемый черновик ответа (Китайский)**, 🇷🇺 **Русский перевод черновика**).
     - **Thread Headers**: ALWAYS set `In-Reply-To` and `References` headers to the client's original message ID (`msg_id` / `internet_message_id`).
     - **Exact Subject Preservation**: Keep the exact original subject prefixed with `Re: ` (e.g., `Re: 来自 Navo 的初步建立联系`).
     - **Quoted History Below Signature**: Below Richard's official HTML signature, ALWAYS attach the quoted original message history (`----- Original Message -----` + client's previous text/HTML). This ensures Outlook and all mail clients group the reply into the EXACT SAME email thread/conversation rather than opening a new standalone message.
   - **4-Touch Sequence Strategy (Exact Text)**:
     1. **Емейл 1 (Зацепка)**:
        `Здравствуйте, [Имя/Компания]!`
        `Это Ричард из Navo. Ваши контакты мы получили от наших коллег в логистике как сильного агента в Китае для контейнерных и других видов перевозки. Это правильно?`
     2. **Емейл 2 (Завязка диалога - Судоходные линии и объёмы)**:
        `Понятно, спасибо!`
        `Уточните пожалуйста, с какими судоходными линиями вы работаете? Есть ли среди ваших клиентов известные китайские или мировые бренды? Расскажите о ваших сильных сторонах, где самые лучшие ставки у вас? Какой примерный объем перевозок в контейнерах или тоннах вашей компании за год?`
     3. **Емейл 3 (Завязка диалога - ЛПР)**:
        `Принято, спасибо!`
        `По поводу сотрудничества и интеграции Вашей компании в нашу экосистему, подскажите общаться с Вами или с Вашим боссом?`
     4. **Емейл 4 (Полноценный оффер Early Bird)**:
        `Отлично`
        `Мы работаем с экспедиторскими компаниями через принципиально новую экосистему для цифровой логистики... [3 месяца бесплатного тестового периода, бесплатное обновление сайта, калькулятор фрахта, автотрекинг, объединённая сеть тарифов].`
   - **Signature Rule**:
     - **NO EXTRA PARAGRAPHS OR BLANK LINES** at the very top of the email body text.
     - **EXACTLY 1 EXTRA BLANK LINE** before the signature block.
     - **NO HORIZONTAL LINE (`border-top`) BEFORE THE SIGNATURE**.
     - Use ONLY the official HTML signature block (`Richard Marlowe / Connections Manager`, logo `https://bit.ly/4hLg86T`, +44 203 440 9800, 30 St Mary Axe London, `rich@navo24.com`, `www.navo24.com`).
     *(See `references/4-touch-sequence-pattern.md` for full sequence details and HTML signature templates.)*
   - **Mass Cold Outreach & Anti-Spam (100% Dynamic AI Personalization)**:
     - **NO STATIC REPETITIVE TEMPLATES**: Cold outreach MUST use 100% dynamic AI personalization (unique subject line & body text per lead generated from CRM company name, contact person, city, and specialties). Static templates cause Microsoft Exchange Online Protection (EOP) to flag outbound spam and block sending (`550 5.1.8 Access denied, bad outbound sender AS(42004)`).
     - **Safe Sending Cadence**: Use human-like delays of **3–5 minutes (180–300s)** between sends to avoid rate-limiting and anti-spam heuristics on Microsoft 365.
     - **CC Rules**: CC `lxxmng@navo24.com` & `stefan@navo24.com`. **DO NOT CC `sales@navo24.com`** on cold outreach emails.
     - **Exchange Online Distribution List Recovery**: Distribution Lists (Groups) in Exchange Online do NOT store or queue blocked messages. Once rejected, messages cannot be retroactively pulled or claimed. Use **Exchange Admin Center (`admin.exchange.microsoft.com`) -> Message Trace** filtered by `Rejected/Failed` to audit external senders and subjects that were blocked.
     - **Airtable Status Updates**: Update `Stage` and `status` to `"Contacted"` via Airtable PATCH API strictly record-by-record AFTER each email is actually dispatched.
   - **Plain Text Body + HTML Signature Only**: Cold outreach emails MUST use a natural human plain-text body (or simple HTML text). DO NOT send full HTML email newsletter templates, which look like automated marketing blasts. ATTACH ONLY the official HTML signature at the bottom (Richard Marlowe, Senior Sales Manager, domain links).
   - **Verification before Confirming Launch**: Never report a mass outreach batch as "launched/running" based on text alone. Verify that the necessary credentials (full Airtable PAT format `pat<id>.<secret>`, SMTP credentials, or local script) are present and actually executed.
4. **Airtable PAT Authentication & Base Mapping**:
   - Airtable Personal Access Tokens use the full format `pat<id>.<secret>` (e.g. `patzjFlOTnLygbDs0.64e5...`). Single `pat<id>` prefixes will return 401 Unauthorized.
   - Base mapping for Chinese Freight Forwarder outreach:
     * `CN FF 1` = Base ID `appdWYgvtQR2Fgaeq` (Table `CNFF-1`)
     * `CN FF 2` = Base ID `appa1AH0vV4fl1BVQ` (Table `CNFF-2`)
     * `CN FF 3` = Base ID `appVItBOee1awOPHh` (Table `CNFF-3`)

## Pitfalls & Common Mistakes

- **CRITICAL: Distinguish M365 Outbound Block NDRs from True Client Bounces**:
  * Internal Exchange Online Protection (EOP) blocks return `550 5.1.8 Access denied, bad outbound sender AS(42004)`, `was not recognized as a valid sender`, or `suspected of sending spam`.
  * **This is an issue on OUR side (`rich@navo24.com`), NOT an invalid recipient mailbox.**
  * Inbound pollers / bounce handlers MUST NEVER delete or purge CRM records upon receiving `550 5.1.8` NDRs! Doing so deletes valid client leads from the CRM. If records were mistakenly deleted due to M365 blocks, inspect the Inbox NDR headers, extract the affected recipient email addresses, and restore them back into the CRM as `Lead`.
  * Only true recipient-side NDRs (`550 5.1.1 User unknown`, `Host not found`, `Mailbox disabled`) indicate a dead lead that should be deleted/marked bounced.
  * *(See `references/m365-eop-and-crm-bounce-handling.md` for complete M365 EOP error diagnostics, inbound poller code patterns, and Distribution List recovery details.)*
- **CRITICAL: Premature CRM Status Updates**: Never bulk-update Airtable records from `Lead` to `Contacted` in advance or without actually dispatching the emails. Sending a batch of 500 emails with a 1-minute interval physically takes **~8.3 hours** — updating Airtable in seconds without real SMTP/API dispatch corrupts lead tracking and creates false completion reports. Always update Airtable status record-by-record AFTER each email is actually sent.
- **Inbound Poller Duplication (MS Graph)**: Always mark processed MS Graph messages as `isRead = True` and persist their IDs in `/opt/hermes/profiles/richard/processed_msg_ids.json`. Without marking read and persisting seen IDs, the 3-minute poller cron job will repeatedly trigger duplicate alerts for the same messages over 100 times.
- **Faking/Simulating Batch Triggers**: Confirming a mass email launch without executing a real tool or background process results in missed emails and user frustration. Always run real background processes (`terminal(background=True, notify_on_complete=True)`) with proper 60s delays and log files (e.g. `/root/cn_ff_1_outreach.log`).
- **Real SMTP Dispatch Settings**:
  * Host: `smtp.office365.com:587` (STARTTLS)
  * From: `rich@navo24.com`
  * CC List: `lxxmng@navo24.com`, `stefan@navo24.com`
- **Excessive Exploratory Tool Searching**: When the user gives a direct command ("Stop", "Translate to Chinese and send"), execute immediately rather than searching files or running multiple diagnostic queries.
4. **Qualifying Questions Pattern**:
   - Carrier & Route Focus: Ask which primary shipping lines and trade lanes they operate on.
   - Service/Feature Priorities: Ask which platform capabilities (tracking, schedules, loading, API/MCP) matter most to their workflow.
   - Decision-Maker Clarification: Clarify whether to continue direct discussion with the respondent or involve their leadership/management.
5. **Signature & CC Rules**:
   - CC team emails (`lxxmng@navo24.com`, `stefan@navo24.com`) as required.
   - Use standard polite closing (`顺祝商祺， / Best regards,` + `Richard Marlowe`). Let Outlook signature auto-attach without adding redundant custom signatures.
