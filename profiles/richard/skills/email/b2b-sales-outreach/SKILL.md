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

1. **No Snake Emojis & Clean Telegram Output**:
   - NEVER use snake emojis (🐍) in any messages, status reports, email drafts, or Telegram outputs.
   - To prevent platform UI progress bubbles (like `🐍 Running code` or `💻 terminal`) from appearing in Telegram chats, set `display.tool_progress: none` and `display.interim_assistant_messages: false` in Hermes config (`hermes config set display.tool_progress none --profile richard`).
2. **Context & Quoted Reply Evaluation Rule**:
   - When the user replies to a quoted message (`[Replying to: "..."]`), ALWAYS evaluate their instruction strictly relative to the quoted text or last proposed question in that context, rather than relying on stale generic conversation history.
   - **Strict Context Isolation (Anti-Contamination Rule)**: When starting a new task or analyzing an incoming screenshot, forwarded text, or client inquiry, evaluate it strictly on its own merits and standalone content. NEVER auto-link or assume a newly submitted image or text belongs to an unrelated previous prospect, session, or thread unless explicitly specified.
3. **Inbound Attachments & Screenshot Inspection (MS Graph API)**:
   - Always check for both regular attachments and inline screenshots (`cid:` images) via `GET /me/messages/{id}/attachments` (as `hasAttachments` can return `False` for inline images).
   - Save extracted attachments into `/opt/hermes/profiles/richard/attachments/` and use vision/document tools to analyze client screenshots (e.g. Postman responses, error logs, rate sheets) before formulating draft replies.
4. **Tracking API Asynchronous Flow Support (POST vs GET Workflow)**:
   - When onboarding technical clients (e.g. IT heads testing via Postman), clearly explain that `POST /v1/containers` returns `202 Accepted` ("Tracking started") as an asynchronous registration step.
   - Guide them to fetch complete shipment milestones, container numbers, vessel AIS, and ETA via `GET /v1/containers/{id}` (or by booking/container number), or subscribe to real-time Webhook push events.
5. **Persistent Background Workers**: When running long-lived background workers (like cold outreach daemons), use `terminal(command="PYTHONUNBUFFERED=1 python3 -u script.py >> log 2>&1", background=True)` rather than a transient subshell `nohup &`, which gets terminated when the execution turn closes.
4. **Client Language Matching & Strategic Carrier/Freight Positioning**:
   - **Language Matching**: Always match the language of the prospect. If a Chinese client replies in Chinese (e.g. 陈先生 from Qiaoye Logistics, Tom Ma from Soho Logistics), translate questions and draft responses into clear, professional B2B Chinese.
   - **Forwarder Capabilities & Digital API Tariff Integration Strategy**: When Chinese freight forwarders describe their logistics capabilities (e.g., FTL nationwide pickup, fixed LTL routes to Central Asia/CIS, OOG/FR special containers, or DG handling), adopt a platform-aggregator perspective:
     * Thank them warmly for presenting their routes and service capabilities.
     * State that as a digital logistics platform, Navo is very interested in offering their freight services to our global client base.
     * Proactively propose integrating and sharing their freight tariffs, routes, and schedules via **API or digital data interface (Data Feed)** to broadcast them directly to end customers.
5. **Direct Execution on Feedback, Verbatim Approval & No Hanging Queues**:
   - When the user approves draft direction (e.g., "Billy text is good - translate to Chinese and send") or confirms sending ("Да", "Отправляй", "OK"), execute the send **IMMEDIATELY in that turn**.
   - **VERBATIM DRAFT DISPATCH MANDATE**: Upon receiving approval confirmation ("Да", "Отправляй", "OK"), ALWAYS dispatch **strictly and verbatim the exact draft text** displayed in the approval card word for word. NEVER unilaterally rewrite, translate, or swap language unless explicitly instructed.
   - **Silent Watchdog Execution Mandate (no_agent cronjobs)**: For background poller cron jobs (e.g., WhatsApp watchdog, email inbound poller), scripts configured with `no_agent: True` must remain 100% silent (zero stdout output) when no new events are found. NEVER output informational status like "No new events" to stdout, as it causes unneeded notification spam in Telegram.
   - **Full Untruncated Inbound Triage & Russian Translation Mandate**: When surfacing inbound emails or WhatsApp messages:
     * Strip away quoted thread histories, external email warnings, and legal disclaimers to isolate the clean new message body.
     * Extract the complete body (avoid Microsoft Graph `bodyPreview` 255-character truncation).
     * ALWAYS provide a complete Russian translation of the incoming message, a business breakdown of lines/quotas, AND a complete Russian translation of Richard's proposed draft response.
     * **Individual Sales Team Testimonials Loop**: Weekly Monday reminders (`send_weekly_sales_testimonial_reminder.py` / `0 5 * * 1` UTC) must send separate, individual personalized emails addressed by first name (`Алёна`, `Екатерина`, `Лилия`, `Никита`, `Олег`) with `CC: stefan@navo24.com, lxxmng@navo24.com`.
     * **Sales Team Onboarding & Context Files**: When granting Telegram access to sales colleagues (e.g. Nikita `@nikita51155` ID `288669722`), add their numeric ID to `TELEGRAM_ALLOWED_USERS` in `.env` and `platforms.telegram.allow_from` in `config.yaml`, maintain `platforms.telegram.user_allowed_commands: ['start', 'help', 'status', 'new', 'clear', 'info']`, create a dedicated profile under `/opt/hermes/profiles/richard/team/<username>.md`, and operate strictly in `SENIOR SALES MENTOR` mode without leaking server secrets.
   - **NO ARTIFICIAL CRON QUEUES**: NEVER defer approved responses into a lingering 1-hour cron job or background batch when immediate dispatch is expected. Lingering queues cause loss of conversation sequence, duplicate approvals, and stale context.
   - When Stefan says "Стоп", stop immediately without exploratory searches.
3. **Inbound Replies vs. Mass Cold Outreach**:
   31. **Inbound Replies (1-on-1 Threading, Timestamps & Russian Translation Mandate)**:
        - **Mandatory Timestamps**: ALWAYS include the exact Date and Time the email was received (`🕒 Время получения: YYYY-MM-DD HH:MM:SS MSK/UTC`).
        - **Mandatory Russian Translation**: ALWAYS provide Stefan with a clear Russian translation of BOTH the client's message AND Richard's proposed draft reply (e.g. 💬 **Цитата сообщения клиента (оригинал)**, 🇷🇺 **Перевод сообщения клиента на русский**, ✍️ **Предлагаемый черновик ответа (Richard Marlowe)**, 🇷🇺 **Перевод черновика ответа на русский**). Never omit translations when presenting incoming Chinese/foreign client messages.
        - **Microsoft Graph API 1-on-1 Reply Workflow**:
          * Auth: OAuth2 Client Credentials (`grant_type: client_credentials`, `TENANT_ID = "dc47c5b1-313f-47eb-ab6f-5f0716f400b5"`, `CLIENT_ID = "807fed17-45a8-4c7c-9a28-5997bbd30970"`, using Azure App `Rich email graph inbox api` with Application permissions `Mail.Send` / `Mail.ReadWrite`).
          * Endpoint: `https://graph.microsoft.com/v1.0/users/rich@navo24.com/...`.
          * Replying: Call `POST /users/rich@navo24.com/messages/{id}/createReply`, update draft with Richard's HTML response + official signature before original body, set CCs (`stefan@navo24.com`, `lxxmng@navo24.com`, `support@navo24.com`), and send via `POST /users/rich@navo24.com/messages/{draft_id}/send`.
          * Navo CRM Lead Logging: Automatically create/update records in Navo CRM (`appbxvl9BBaTiLMlf`) table `Leads` with fields: `Lead Title`, `Email`, `Status` (`Open`), `Source` (`Email Outreach`), `Owner` (`Richard Marlowe (AI)`), `Comments`.
        - **Strict Deduplication**: Never send duplicate notifications for the exact same email message ID (`msg_id`).
        - **Internal M365 Bounce vs Client Bounce**: NEVER auto-delete CRM records on internal M365 outbound errors (`550 5.1.8 Bad outbound sender` or `550 5.7.708 Tenant outbound restriction`). See `references/m365-eop-and-crm-bounce-handling.md` for self-service unblocking steps via `Diag: Outbound Email Blocked`.
        - **Thread Headers**: ALWAYS set `In-Reply-To` and `References` headers to the client's original message ID (`msg_id` / `internet_message_id`).
        - **Exact Subject Preservation**: Keep the exact original subject prefixed with `Re: ` (e.g., `Re: 来自 Navo 的初步建立联系`).
        - **Quoted History Below Signature**: Below Richard's official HTML signature, ALWAYS attach the quoted original message history (`----- Original Message -----` + client's previous text/HTML). This ensures Outlook and all mail clients group the reply into the EXACT SAME email thread/conversation rather than opening a new standalone message.
   32. **Contract & Commercial Agreement Drafting (Wemelogistics LTD / Navo24)**:
        - **Contract Structure**: B2B client contracts for Navo24 subscriptions MUST combine Part 1 (**Commercial Offer & Special Conditions**) and Part 2 (**General Terms and Conditions of Use** from `T_C Navo.docx`).
        - **Bilateral B2B Formulations (No Unilateral Website Disclosures)**: Convert unilateral B2C website disclosures ("We reserve the right to amend these Terms at any time", "We may periodically update or alter the content") into formal mutual B2B agreement language:
          * *Clause 5.1 (Changes to Terms):* "The Parties agree that the Provider may, at its discretion, update or amend these Terms to reflect regulatory changes or platform optimizations, provided that the Provider gives the Client prior written notification or publishes updated terms on the Platform..."
          * *Clause 5.2 (Changes to Platform):* "The Client acknowledges and agrees that the Provider may, at its discretion, periodically update, enhance, alter, or refresh the content, features, and functionality of navo24.com and associated Digital Solutions..."
          * *Clause 10.3 (Fee Adjustments):* Require at least thirty (30) days' prior written notice for renewal rate adjustments.
        - **Numbered Subheadings & Section Formatting**: Ensure Section 4 (`Supplementary Policies`) and all numbered sections have clear, distinct, numbered subheadings (`4.1 Privacy Policy`, `4.2 Membership / Service Agreements`), bold prefixes, and clean vertical paragraph spacing.
        - **Critical Precedence Clause**: Part 1 (Commercial Offer) MUST explicitly state that in case of any conflict or inconsistency, Part 1 **shall strictly prevail and take precedence** over Part 2 General T&C.
        - **Service Provider Details**: **WEMELOGISTICS LTD** (Company Number: `14081751`, registered at 1 Robin Hood House, Kingston Vale, London, SW15 3AL), represented by Director **Oleksii Shatunov**.
        - **Agreed Commercial Logic (PAYG)**:
          * Pricing Model: Pay As You Go (PAYG) based on unique shipments tracked / API calls executed.
          * Calculation Window: Calculated from the Subscription Activation Date through the end of that relevant calendar month (e.g. 1 Sep – 30 Sep, or 15 Sep – 30 Sep for mid-month activation).
          * Invoicing & Payment: Issued monthly in arrears, payment due Net 14 days from invoice date. Client pays net amounts + applicable VAT and intermediary bank transfer/wire fees.
        - **Format**: Always generate as a formatted Word document (`.docx`) with signature blocks for Oleksii Shatunov (Director, Wemelogistics Ltd) and the Client.
   33. **Interactive Agent Kanban Board Rules (Vercel Deployments)**:
        - **Single Vercel URL**: Each agent's Kanban board is hosted EXCLUSIVELY on Vercel (`https://<agent>-kanban.vercel.app`, e.g. `https://richard-kanban.vercel.app`).
        - **No Floating Bottom Buttons**: DO NOT render a floating "Add Task" / "Добавить задачу" button at the bottom right. Task creation is triggered via the top header button (`+ Новая Задача`).
        - **Interactive Detail Modals**: Every card MUST be clickable (`onclick="openCardDetailModal(cardId)"`) to open a rich modal containing card title, tag, assignee, status, description, comments section, and full activity timeline log.
        - **Escape Key Modal Dismissal**: Include a global keyboard listener (`window.addEventListener('keydown', e => if (e.key === 'Escape') closeModal())`) to immediately close all active modals on Esc keypress.
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
   - **Google Drive API File Retrieval**: When files (such as statutory/incorporation documents in `Navo / Statute`) are not synced locally on the server filesystem, use the stored Google OAuth token at `/opt/hermes/google_token.json`. Refresh the access token via `https://oauth2.googleapis.com/token` with `refresh_token`, `client_id`, and `client_secret`, and query `https://www.googleapis.com/drive/v3/files` directly to list and download files from Google Drive.
   - Signature Rule:
   - **NO EXTRA PARAGRAPHS OR BLANK LINES** at the very top of the email body text.
   - **EXACTLY 1 EXTRA BLANK LINE** before the signature block.
   - **NO HORIZONTAL LINE (`border-top`) BEFORE THE SIGNATURE**.
   - Use ONLY the official HTML signature block (`Richard Marlowe / Connections Manager`, logo `https://bit.ly/4hLg86T`, +44 203 440 9800, 30 St Mary Axe London, `rich@navo24.com`, `www.navo24.com`).
   *(See `references/4-touch-sequence-pattern.md` for full sequence details, `references/19-sources-daily-outreach-engine.md` for the complete 19-source lead ingestion pipeline, `references/inbound-triage-and-testimonials-workflow.md` for verbatim draft approval, silent watchdog semantics, full untruncated triage & team testimonials loop, `references/whatsapp-and-voice-telephony-pipeline.md` for WhatsApp gateway, voice PTT & Twilio setup, `references/competitor-radar-and-weekly-sales-loops.md` for weekly testimonial loops, competitor radar 3-tier rules & Twilio voice pipeline, `references/telegram-team-access-and-isolation.md` for sales team colleague onboarding and session isolation, `references/25-sources-audit-and-scrapers.md` for the complete 25-source technical audit and scrapers, `references/b2b-contract-and-kanban-rules.md` for contract drafting and Vercel Kanban UI rules, and `references/technical-api-inquiries-and-schedules.md` for Tracking & Schedules REST API inquiry patterns, SeaRates comparison, and billing rules.)*
   - **RFC 5322 Recipient Header Formatting Rule**:
     * In all outbound cold emails and responses, ALWAYS format the `To` field as `f"{person_name} <{email}>"` (e.g. `Colin Charnock <c.charnock@tglobal.com>`). Passing bare email strings causes mail user agents (Outlook, Apple Mail) in CC copies to suppress the recipient display name or collapse the field.
   - **Multi-Source Diversity & Strict Regional Filtering Mandate**:
     * **Strict Multi-Source Distribution & Single-Pass Full Run**: Distribute daily outreach across all 19 active sources evenly (19 sources x 5 leads = 95 verified emails per morning run). Run in a full single pass rather than small fragmented batches of 20-30.
     * **SeaRates Founding Team Pedigree Value Prop**: In cold outreach intros, ALWAYS cite that Navo24 was founded by the key founding and engineering team behind SeaRates to immediately establish credibility with forwarders and BCOs.
     * **STRICT Anti-Generic Mailbox Policy**: NEVER send outreach to departmental or generic mailboxes (`info@`, `sales@`, `pricing@`, `export@`, `import@`, `ocean@`, `procurement@`, `dispatch@`, `overseas@`, `operations@`, `customs@`, `quotes@`, `help@`, `desk@`). Filter via `is_personal_decision_maker_email()` to target ONLY named personal executive emails (`first.last@`, `flast@`, `name@` for VP Supply Chain, Ocean Freight Director, Head of Logistics, C-Level).
     * **Cross-CRM Deduplication Mandate**: Before dispatching, cross-check candidate emails across ALL active CRM bases (`Online Outreach` `appdJR8VVczRxcVke`, `Navo CRM` `appbxvl9BBaTiLMlf` Leads & Contacts, and `Rich Outreach` `appEoWQjvhgN8LIX7`) to ensure ZERO duplicate outreach.
     * **Strict Regional & Geographic Tagging (No Generic "Global")**: When targeting specific regions (e.g., Western Hemisphere / North & South America), enforce strict country-level filtering (`country_iso in ['US', 'CA', 'MX', 'BR', 'AR', 'CL', 'CO', 'PE']`) and tag each lead with its exact country name (United States, Canada, Mexico, Brazil, Argentina, Chile). NEVER assign a lazy "Global" label when regional targeting is requested.
     * **Full 5-Product Suite Inclusion**: Every cold outreach email body MUST list the full 5-component portfolio:
       1. `Tracking API (Ocean & Air)` (234 ocean carriers, DCSA events, observed ETAs, D&D free-time)
       2. `Schedules API` (72,000+ sailings, reliability benchmarks, 255 ports)
       3. `FreightRates API` (Live ex-Asia spot rates benchmarking, container indices)
       4. `AirTracking API` (Real-time AWB status across global airlines)
       5. `Loading 3D` (Container load optimization, CTU Code / IMDG compliance)
     * **Weekday-Only B2B Scheduling**: All recurring cold outreach cron jobs MUST run strictly on business weekdays (`0 4 * * 1-5` / Monday through Friday), leaving weekends completely silent to maintain professional B2B delivery standards.
   - **Commercial Quotation & Negotiation Guidelines**:
     * **Volume Quota Interpretation**: Always confirm whether shipment volumes represent a total contract pool or a monthly recurring allowance (e.g., 300 shipments/mo on a 12-month contract = 3,600 total shipments; unit rate = Total Price / 3,600).
     * **Concise Price Presentation**: When presenting updated pricing to prospects (e.g., short-term 3-month contracts in local currency like IDR), keep the email clean, direct, and focused on the bottom-line price and deliverables rather than displaying long multi-step arithmetic.
     * **Dynamic Currency & Tax Inquiries**: When quoting foreign currencies (e.g., IDR, EUR, AED), specify that billing is issued from the international legal entity for client convenience and recommend local tax advisor review for cross-border withholding tax implications.
   - **Zero Tolerance to Template-Guessed Email Patterns (Anti-Pattern Hallucination Rule)**:
     * When sourcing executive emails, NEVER construct/guess email addresses via speculative syntax (`first.last@domain` or `f.last@domain`) without verifying that specific mailbox via an API SMTP handshake (Hunter.io / Snov.io / Prospeo) or using verified member directory exports (e.g. `dfa_members.xlsx`).
     * Domain-level DNS/MX check only proves the company mailserver exists, NOT that the specific mailbox address is valid. Speculative patterns cause bounces (e.g., `a.melgaard@scangl.com` vs real `amelg@scangl.com`). Always ensure live mailbox validation before dispatch.
   - **Target Audience Scope (BCOs, Trading Conglomerates & Shippers First)**:
     * Never restrict prospecting solely to freight forwarding directors.
     * High-volume priority: BCOs (Beneficial Cargo Owners), Commodity Trading Houses (Agri, Energy, Metals), Chemical and Industrial Manufacturers shipping 100s–1,000s of containers directly (e.g. Bunge, ADM, Dow, BASF, Trafigura). Target: `Head of Logistics`, `VP Supply Chain`, `Director of International Trade`, `Import/Export Director`, `Commercial General Manager`.
   - **Mass Cold Outreach & Anti-Spam (100% Dynamic AI Personalization & High Combinatorics)**:
     - **Primary Outbound Channel Rule (User Direct Mandate)**:
       * All primary email sending, 1-on-1 replies, and outbound communications must be sent **directly from Richard (`rich@navo24.com`)** via Microsoft Graph API / M365.
       * Do **NOT** use `sales@e.navo24.com` / Resend for outreach or replies unless Stefan explicitly gives a direct instruction to switch.
     - **Outbound Spam Filter Protection & Anti-Repetition Rules**:
       * **Zero-Overlap Unique Phrasing Mandate**: When sending responses, qualification questions, or follow-ups to a batch of prospective clients, **every email must be 100% uniquely phrased (0 identical boilerplate paragraphs or questions)**. EOP heuristics flag repeated corporate blurbs across multiple outbound messages. Run a script check to ensure cross-email sentence intersection is 0 before batch execution.
       * **Same-Name Contact Disambiguation**: When handling prospects with identical first names (e.g., multiple "Alex" contacts), NEVER merge them into a single email without verifying if they belong to different branches, domains, or individuals. Keep separate, uniquely tailored threads for each.
       * **All Outreach & Follow-ups in Simplified Chinese**: All outgoing messages and replies to Chinese freight forwarders MUST be written strictly in fluent, professional Simplified Chinese.
       * **M365 NDR 550 5.7.708 Remediation & Failover**: If M365 blocks outbound with `550 5.7.708` (does not clear automatically overnight), use Microsoft 365 Admin Center `Help & Support -> 550 5.7.708 / Diag: Outbound Email Blocked` to delist, or failover immediately to Resend API (`sales@e.navo24.com` with `reply_to: rich@navo24.com`).
       * **Cadence**: Enforce a **5-minute (300s) delay** between sends for all multi-recipient batches.
       * **M365 Policy Replication**: After modifying Exchange Online policies via PowerShell (`Set-HostedOutboundSpamFilterPolicy`), allow **30–60 minutes for edge cluster replication** before retrying rejected recipients.
     - **Mass Cold Outreach via Resend (`e.navo24.com`) [On Explicit User Direction Only]**:
       * Outbound bulk cold emails MUST be sent from `sales@e.navo24.com` via Resend REST API (`https://api.resend.com/emails`), with `Reply-To: rich@navo24.com` (routes directly to Richard's active M365 inbox) and RFC 8058 `List-Unsubscribe` headers.
       * Strictly adhere to the warm-up ramp (Day 1-2: 50, Day 3-4: 150, Day 5-7: 500, Day 8-10: 1,000/day).
       *(See `references/resend-outreach-and-warmup.md` for full implementation and sending code).*
     - **NO STATIC REPETITIVE TEMPLATES**: Cold outreach MUST use 100% dynamic AI personalization with high combinatorial variety (25+ unique subject lines, 12+ greetings, 10+ intros, 12+ contexts, 12+ CTAs -> 500,000+ unique email variations). Static templates cause Microsoft Exchange Online Protection (EOP) to flag outbound spam and block sending (`550 5.1.8 Access denied, bad outbound sender AS(42004)`).
     - **Safe Sending Cadence & User Preference**: Default cold outreach interval is **5 minutes (300s)** per message (~12 emails/hour) for primary Microsoft 365 mailboxes, or **2 minutes (120s)** (~30 emails/hour) if explicitly requested by Stefan. Always respect the user's interval choice.
     - **Qualified Leads Retry & Follow-Up Cadence**: When retrying dispatches or sending 1-on-1 qualification follow-ups to batches of interested leads after unblocking or policy changes, enforce a **5-minute (300s) delay** between each message and **100% unique text phrasing** per recipient to prevent triggering repetitive outbound content filters.
     - **Pausing & Delay Timers**: When Stefan requests a pause for N hours (e.g., "stop for 2 hours, then resume with 5 min interval"), kill the active process immediately, set the sleep script interval to 300s, and launch a background timer process (`sleep <N*3600> && PYTHONUNBUFFERED=1 python3 -u script.py >> log 2>&1 &`). Confirm exact resume time.
     - **CC Rules**: CC `lxxmng@navo24.com` & `stefan@navo24.com`. **DO NOT CC `sales@navo24.com`** on cold outreach emails.
     - **Exchange Online Distribution List Recovery**: Distribution Lists (Groups) in Exchange Online do NOT store or queue blocked messages. Once rejected, messages cannot be retroactively pulled or claimed. Use **Exchange Admin Center (`admin.exchange.microsoft.com`) -> Message Trace** filtered by `Rejected/Failed` to audit external senders and subjects that were blocked.
     - **Telegram Group Response Rules**: In Telegram group chats (e.g., "Navo Agents"), respond ONLY if (1) `@mentioned` (`@richnavobot`), (2) replied/quoted to, or (3) explicitly addressed by name (*Ричард*, *Richard*, *Рич*, *Ричи*). Never jump into group threads unprompted.
     - **Airtable Status Updates**: Update `Stage` and `status` to `"Contacted"` via Airtable PATCH API strictly record-by-record AFTER each email is actually dispatched.
   - **Plain Text Body + HTML Signature Only**: Cold outreach emails MUST use a natural human plain-text body (or simple HTML text). DO NOT send full HTML email newsletter templates, which look like automated marketing blasts. ATTACH ONLY the official HTML signature at the bottom (Richard Marlowe, Senior Sales Manager, domain links).
   - **Verification before Confirming Launch**: Never report a mass outreach batch as "launched/running" based on text alone. Verify that the necessary credentials (full Airtable PAT format `pat<id>.<secret>`, SMTP credentials, or local script) are present and actually executed.
5. **Contract & Commercial Agreement Drafting (Wemelogistics LTD / Navo24)**:
   - **Contract Structure**: B2B client contracts for Navo24 subscriptions MUST combine Part 1 (**Commercial Offer & Special Conditions**) and Part 2 (**General Terms and Conditions of Use** from `T_C Navo.docx`).
   - **Bilateral B2B Formulations (No Unilateral Website Disclosures)**: Convert unilateral B2C website disclosures ("We reserve the right to amend these Terms at any time", "We may periodically update or alter the content") into formal mutual B2B agreement language:
     * *Clause 5.1 (Changes to Terms):* "The Parties agree that the Provider may, at its discretion, update or amend these Terms to reflect regulatory changes or platform optimizations, provided that the Provider gives the Client prior written notification or publishes updated terms on the Platform..."
     * *Clause 5.2 (Changes to Platform):* "The Client acknowledges and agrees that the Provider may, at its discretion, periodically update, enhance, alter, or refresh the content, features, and functionality of navo24.com and associated Digital Solutions..."
     * *Clause 10.3 (Fee Adjustments):* Require at least thirty (30) days' prior written notice for renewal rate adjustments.
   - **Numbered Subheadings & Section Formatting**: Ensure Section 4 (`Supplementary Policies`) and all numbered sections have clear, distinct, numbered subheadings (`4.1 Privacy Policy`, `4.2 Membership / Service Agreements`), bold prefixes, and clean vertical paragraph spacing.
   - **Critical Precedence Clause**: Part 1 (Commercial Offer) MUST explicitly state that in case of any conflict or inconsistency, Part 1 **shall strictly prevail and take precedence** over Part 2 General T&C.
   - **Service Provider Details**: **WEMELOGISTICS LTD** (Company Number: `14081751`, registered at 1 Robin Hood House, Kingston Vale, London, SW15 3AL), represented by Director **Oleksii Shatunov**.
   - **Agreed Commercial Logic (PAYG)**:
     * Pricing Model: Pay As You Go (PAYG) based on unique shipments tracked / API calls executed.
     * Calculation Window: Calculated from the Subscription Activation Date through the end of that relevant calendar month (e.g. 1 Sep – 30 Sep, or 15 Sep – 30 Sep for mid-month activation).
     * Invoicing & Payment: Issued monthly in arrears, payment due Net 14 days from invoice date. Client pays net amounts + applicable VAT and intermediary bank transfer/wire fees.
   - **Format**: Always generate as a formatted Word document (`.docx`) with signature blocks for Oleksii Shatunov (Director, Wemelogistics Ltd) and the Client.
4. **Airtable Ownership, CRM Dual-Tracking & Base Mapping**:
   - **Exclusive Domain Responsibility (Airtable & Interface Designer)**: Airtable CRM operations, data structures, and Airtable Interface Designer configurations belong EXCLUSIVELY to Richard Marlowe (AI Senior Sales Manager). DO NOT redirect Airtable CRM interface/workflow requests to Callum Vance — Richard owns Airtable CRM and Airtable Interface Designer layouts (e.g., Kanban by status/stage, record detail sidebars, accounts/contacts lists).
   - **CRM Dual-Tracking Rule (Prospecting Base -> Main Navo CRM)**:
     * When any prospect replies from the outbound prospecting bases (`CN FF 1-3`), perform dual-layer tracking:
       1. In the Prospecting Base (`CN FF 1-3`), update the record: `Stage` -> `"Pitched"` (or `"Lead"`), `status` -> `"Replied - <key topic>"` (e.g. `Replied - API tariffs offered`).
       2. In the Main **Navo CRM** (`appbxvl9BBaTiLMlf`), create or update the corresponding card in table **`Leads`** (`Lead Title`, `Email`, `Phone/WeChat`, `Status: Open`, `Source: Email Outreach`, `Owner: Richard Marlowe (AI)`, `Comments` with full Russian synthesis of company strengths, contact details, and next steps).
   - **Primary Navo CRM vs Online Outreach Bases**:
     * **Navo CRM** = Base ID `appbxvl9BBaTiLMlf` (Main B2B CRM with 5 core tables: `Accounts`, `Contacts`, `Leads`, `Opportunities`, `Timeline Events`). Reserved EXCLUSIVELY for qualified inbound responses, active client discussions, and deal pipeline.
     * **Online Outreach** = Base ID `appdJR8VVczRxcVke` (Table `Outreach Leads`). Dedicated database for multi-source cold outreach (17 sources, DFA, WCA, ImportYeti, Volza, Trademo, etc.). Records initial ingestion, `Source Platform`, sent HTML bodies, Resend IDs, and `Stage: Contacted`.
     * **Prospecting Outbound Bases**:
       - `CN FF 1` = Base ID `appdWYgvtQR2Fgaeq` (Table `CNFF-1`)
       - `CN FF 2` = Base ID `appa1AH0vV4fl1BVQ` (Table `CNFF-2`)
       - `CN FF 3` = Base ID `appVItBOee1awOPHh` (Table `CNFF-3`)
     * **Rich Outreach** = Base ID `appEoWQjvhgN8LIX7` (Specialized IT, Logistics, Finance, Trade lists).
     * **Outreach Component Bullet Hierarchy & Testing Link**:
       - In component bullet lists, always place **AirCargoMCP at the very bottom** of the list with no URL link.
       - The self-serve testing link in the CTA MUST point strictly to **`navo24.com`** (`<a href="https://navo24.com" target="_blank">navo24.com</a>`), not `trackingmcp.com/track`.
     * **Email Layout & Visual Formatting Rules (Natural 1-on-1 vs Marketing Newsletter)**:
       - **Strict Left Alignment**: Cold outreach and 1-on-1 business emails must look like natural, human emails written from Outlook or Gmail. NEVER wrap email bodies in centered marketing card containers (`max-width: 620px; margin: 0 auto;`). Always use strict left alignment (`text-align: left; max-width: 100%;`).
       - **No Dividing Horizontal Rule Before Signature**: Before Richard's signature block, NEVER insert horizontal divider lines (`<hr>` or `border-top: 1px solid #...`). Leave exactly 1 standard blank line / paragraph margin before the signature.
     * **Target Audience Expansion (BCOs, Shippers & Trading Conglomerates)**:
       - Do NOT restrict outbound prospecting only to logistics and freight forwarder directors.
       - Priority focus: high-volume **BCOs (Beneficial Cargo Owners), Export/Import Trading Houses, Commodity Traders, and Industrial Manufacturers** shipping hundreds/thousands of containers directly (e.g., agribusiness, chemicals, metals, consumer goods, machinery). Target: `Head of Logistics`, `VP Supply Chain`, `Director of International Trade`, `Import/Export Director`, `Commercial General Manager`.
     * **Outreach & 1-on-1 Reply-To & CC Routing Rules**:
       - **Reply-To Mandate**:
         * **Western / Online Outreach (17 sources)**: `Reply-To: sales@navo24.com`.
         * **Chinese Outreach & Correspondence (CNFF 1-3 / Chinese partners)**: **`Reply-To: rich@navo24.com`** (ALWAYS routes to Richard's active M365 mailbox).
       - **1-on-1 CC Mirroring Rule**: In individual thread replies, mirror the exact CC list from the client's incoming email. If the client had CC recipients, keep them in CC; if the incoming message had no CC, keep CC empty.
       - **Mass Outreach Headers**: `From: Richard Marlowe <rich@e.navo24.com>`, `Reply-To: sales@navo24.com` (or `rich@navo24.com` for CN), `CC: support@navo24.com`.
     * **Zero Hallucination & Zero-Mock Policy for Lead Sourcing**:
       - **ABSOLUTE BAN ON SYNTHETIC / MOCKED DATA**: NEVER fabricate, mock, or hallucinate lead names, company domains, email addresses, or scraper results. If a source lacks an active parser or API integration, report its status honestly as pending development — never simulate successful extraction or invent records.
       - **100% Genuine Verified Sources Only**: Ingest leads strictly from real, verified files (e.g. DFA directory `dfa_members.xlsx`) or live, tested API queries (Apollo, Hunter, Snov, Prospeo).
       - **Pre-Send DNS & MX Verification**: Before dispatching, verify that recipient domains have active MX mail exchangers (`socket.getaddrinfo(domain, 25)`). Skip dead or unregistered domains.
     * **Airtable Database Segregation**:
       - **Online Outreach** (`appdJR8VVczRxcVke`, Table `Outreach Leads`): Dedicated base for cold multi-source outreach (STRICTLY 17 sources, DFA, WCA, ImportYeti, etc.). NEVER mix old SeaRates clients or Chinese FF bases into this table.
       - **Navo CRM** (`appbxvl9BBaTiLMlf`, Table `Leads`): Reserved strictly for qualified inbound responses, active discussions, and deal pipeline.
     * **Telegram Multi-User Access & Slash Command Handling**:
       - Dual-layer authentication: update both `.env` (`TELEGRAM_ALLOWED_USERS`) and `config.yaml` (`platforms.telegram.allow_from`) with numeric Telegram user IDs and wildcard `*`.
       - Enable non-admin bot activation: explicitly specify `platforms.telegram.user_allowed_commands: ['start', 'help', 'status', 'new', 'clear']` so team members clicking the Telegram Start button do not get access denied errors.
     * **Timezone Synchronization for Cron Jobs (UTC vs Kyiv Time)**:
       - The underlying Linux VM operates in **UTC**. Always offset cron expressions to match Kyiv / Ukraine time:
         - **07:00 AM Kyiv (EEST, UTC+3)** -> `0 4 * * 1-5` (04:00 UTC).
         - **22:00 (10 PM) Kyiv (EEST, UTC+3)** -> `0 19 * * *` (19:00 UTC).
   - **Zero Mock Simulation & Live Execution Mandate**:
     * NEVER print simulated/mock progress logs claiming outreach was sent or records were created when no real HTTP network requests or DB writes occurred.
     * Every dispatch and CRM operation must be verified by live API execution returning valid transaction IDs (e.g. Resend ID, Airtable record ID `rec...`).
   - **17-Source Online Outreach Engine & Database Mapping**:
     * **Daily Cadence & Norms**: 17 sources x 5 verified leads = 85 leads/day sent on weekdays at 07:00 Kyiv time (`0 4 * * 1-5` UTC cron).
     * **Strict Database Segregation**: Ingest strictly into base **`Online Outreach` (`appdJR8VVczRxcVke`)** in table **`Outreach Leads`**. NEVER mix old SeaRates clients or Chinese FF bases (CN1-3) into this database, and NEVER push cold unverified outreach directly into the main **`Navo CRM` (`appbxvl9BBaTiLMlf`)**.
     * **Dynamic Variation & Spintax Anti-Spam Mandate**: To prevent spam filter detection, enforce dynamic subject line rotation (4 distinct variations) and source-specific personalized hooks (`{First Name}`, `{Company Name}`, source context).
     * **Component Hierarchy & Testing Link**:
       - In component bullet lists, always place **AirCargoMCP at the very bottom** of the list with no URL link.
       - The self-serve testing link in the CTA MUST point strictly to **`navo24.com`** (`<a href="https://navo24.com" target="_blank">navo24.com</a>`), not `trackingmcp.com/track`.
     * **Credential & Session Sync from Windows PC via Tailscale**:
       - When credentials or browser session profiles are configured on Stefan's PC (`100.79.157.46`), use SSH/SCP directly over Tailscale to sync `.env` keys (Apollo, Hunter, Snov, Prospeo, Lusha, Clay) and session profiles (`volza_browser_profile/Default/Network/Cookies`) to the Linux server.
     * **Source Real-Connection Status**:
       - *Live Active*: DFA database, WCAworld/JCtrans open directories, Apollo API (`APOLLO_API_KEY`), Hunter API (`HUNTER_API_KEY`), Snov API (`SNOV_USER_ID`/`SNOV_SECRET`), Prospeo API (`PROSPEO_API_KEY`).
       - *WAF / Browser-Dependent*: ImportYeti (headless Playwright Cloudflare bypass), Volza (Playwright session cookies).
   - **Outreach Audit & Completion Rule**: When auditing prospecting bases (`CN FF 1-3`), any records missing an `email` address cannot receive email outreach and should be marked `Stage: Postponed` / `status: Postponed` with a comment `[Audit] No email address provided in base profile. Marked Postponed.` to cleanly achieve 100% processing of reachable contacts without leaving records stuck as uncontacted `Lead`.
   - **Excel Multi-Recipient Cleaning & Parsing**:
     * In client databases (`Customers.xlsx`), email cells may contain multiple addresses delimited by `;`, `/`, or annotated with non-ASCII text (e.g. `maritimeproductmanagement@...; Vicky.Papaioannou@...` or `email@domain.com - не актуальный`).
     * The outreach parser must strip out non-ASCII suffixes and split multi-value cells into distinct, clean individual email dispatches so zero valid recipient inboxes are skipped.
   - Airtable Personal Access Tokens use the full format `pat<id>.<secret>` (e.g. `patzjFlOTnLygbDs0.64e5...`). Single `pat<id>` prefixes will return 401 Unauthorized.

## Pitfalls & Common Mistakes

- **M365 NDR 550 5.7.708 (Tenant Outbound IP Restriction) & Instant Failover**:
  * `550 5.7.708 Service unavailable. Access denied, traffic not accepted from this IP` is an Exchange Online Protection tenant outbound IP block that **does not resolve automatically overnight**.
  * **Remediation**:
    1. Admin delisting: M365 Admin Center -> `Help & Support` -> search `550 5.7.708` -> run `Diag: Outbound Email Blocked` to request automated delisting.
    2. Instant failover: If client replies or approved emails must go out immediately without waiting for Microsoft support, dispatch via Resend REST API (`from: Richard Marlowe <sales@e.navo24.com>`, `reply_to: rich@navo24.com`, CC Stefan/Alexey).
- **CRITICAL: Distinguish M365 Outbound Block NDRs from True Client Bounces**:
  * Internal Exchange Online Protection (EOP) blocks return `550 5.1.8 Access denied, bad outbound sender AS(42004)`, `was not recognized as a valid sender`, or `suspected of sending spam`.
  * **This is an issue on OUR side (`rich@navo24.com`), NOT an invalid recipient mailbox.**
  * Inbound pollers / bounce handlers MUST NEVER delete or purge CRM records upon receiving `550 5.1.8` NDRs! Doing so deletes valid client leads from the CRM. If records were mistakenly deleted due to M365 blocks, inspect the Inbox NDR headers, extract the affected recipient email addresses, and restore them back into the CRM as `Lead`.
  * Only true recipient-side NDRs (`550 5.1.1 User unknown`, `Host not found`, `Mailbox disabled`) indicate a dead lead that should be deleted/marked bounced.
  * *(See `references/m365-eop-and-crm-bounce-handling.md` for complete M365 EOP error diagnostics, inbound poller code patterns, and Distribution List recovery details.)*
- **CRITICAL: Premature CRM Status Updates**: Never bulk-update Airtable records from `Lead` to `Contacted` in advance or without actually dispatching the emails. Sending a batch of 500 emails with a 1-minute interval physically takes **~8.3 hours** — updating Airtable in seconds without real SMTP/API dispatch corrupts lead tracking and creates false completion reports. Always update Airtable status record-by-record AFTER each email is actually sent.
- **Inbound Poller Duplication & MS Graph API Credentials**:
  * MS Graph Inbound endpoint: `https://graph.microsoft.com/v1.0/users/rich@navo24.com/mailFolders/inbox/messages?$top=15&$orderby=receivedDateTime desc`.
  * Authentication: OAuth2 Client Credentials (`grant_type: client_credentials`, `TENANT_ID = "dc47c5b1-313f-47eb-ab6f-5f0716f400b5"`, `CLIENT_ID = "807fed17-45a8-4c7c-9a28-5997bbd30970"`, Azure App `Rich email graph inbox api`).
  * Attachments & Screenshots: Always fetch `/users/rich@navo24.com/messages/{id}/attachments` (capturing both regular files and inline `cid:` images even when `hasAttachments` is False), save to `/opt/hermes/profiles/richard/attachments/`, and inspect via vision/document tools.
  * Filter out and auto-record system bounce/undeliverable messages (`microsoftexchange`, `postmaster`, `undeliverable`) so they do not trigger false alerts.
  * Always persist seen message IDs in `/opt/hermes/profiles/richard/processed_msg_ids.json`.
- **Cron Job Model Drift Protection Recovery**: When the active profile LLM model is upgraded or changed (e.g., `gemini-3.6-flash` -> `gemini-3.7-flash`), Hermes Spend Protection skips cron runs with a drift alert. To recover, update the cron job configuration and `model_snapshot` in `/opt/hermes/profiles/richard/cron/jobs.json` to match the active model.
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
- **1-on-1 Direct Client Correspondence (Non-Broadcast)**:
  * **From:** `Richard Marlowe <rich@e.navo24.com>` (via Resend REST API).
  * **Reply-To:** `sales@navo24.com` (routes client replies directly into Navo Sales inbox).
  * **CC List Rule:** Mirror the exact CC list from the incoming email (if the sender included colleagues in CC, preserve those exact addresses in CC; if incoming email had no CC, leave CC empty).
  * **Signature:** Official HTML signature with 1 blank line before and no top border line.
- **Strict Real Execution & Zero Mock Simulation Mandate**:
  * In automated outreach engines, cron scripts, and status reports, NEVER use synthetic mock logs or print placeholder progress claiming emails were sent or CRM records were created when no live HTTP POST requests or database mutations actually occurred.
  * Every outreach run must be backed by genuine API responses (e.g. Resend `200 OK` with returned message IDs, Airtable `200 OK` with returned record IDs).
- **Telegram Gateway Multi-User & Slash Command Access**:
  * Dual-layer authentication: update both `.env` (`TELEGRAM_ALLOWED_USERS`) and `config.yaml` (`platforms.telegram.allow_from`) with numeric Telegram user IDs and wildcard `*`.
  * Enable non-admin bot activation: explicitly specify `platforms.telegram.user_allowed_commands: ['start', 'help', 'status', 'new', 'clear']` so team members clicking the Telegram Start button do not get access denied errors.
- **Handling In-Depth B2B Replacement / Migration Inquiries (ex-SeaRates Evaluation)**:
  * When prospects actively choosing a replacement for SeaRates submit detailed technical/commercial questionnaires (e.g., coverage of niche lanes, index vs. bookable rates, LCL, free tier, SLAs, lineage):
    1. **Radical Honesty & Factuality**: Never make up coverage claims or promise bookable tariffs where only market indices exist. If a corridor (e.g., Venezuela feeder ports) or mode (LCL per CBM) is not published, state it directly in Point 1.
    2. **Component Role Separation**: Clearly separate **FreightRatesMCP** (weekly spot market index benchmark), **SchedulesMCP** (carrier transit times, cut-offs, vessel schedules across 5k+ lanes), and **TrackingMCP** (234 carriers, 4 AIS feeds, DCSA milestone events).
    3. **Enterprise Continuity & Lineage**: Highlight contractual deprecation notice periods (12 months), 99.9% SLA, full JSON/Webhook exportability, and transparent corporate background (Wemelogistics Ltd UK #14081751, 30 St Mary Axe London, co-founders Oleksii Shatunov & Stefan Rogovskiy).
- **Signature, CC & Resend Outreach Rules**:
   - **Strict Execution on Recipient Directives (No Speculative Debating)**: When the user requests specific recipients in `To`, `CC`, or `Reply-To` (e.g. `To: [Client]`, `CC: sales@navo24.com` or `CC: support@navo24.com`, `Reply-To: sales@navo24.com`), execute the exact configuration without philosophical debates or over-explaining mail client display behaviors.
   - **Resend Gateway CC vs Reply-To De-duplication Rule**:
     * In Resend / AWS SES, when `From` or `Reply-To` uses the identical local-part as `CC` (e.g., `From: sales@...`, `Reply-To: sales@...`, and `CC: sales@...`), the SMTP engine de-duplicates the identical mailbox entity and suppresses rendering of the `Cc:` MIME header.
     * To ensure 100% clean CC rendering across all email clients (Spark, Outlook, Gmail, Apple Mail), maintain distinct functional addresses:
       - `From:` `Richard Marlowe <rich@e.navo24.com>` (Sender)
       - `CC:` `support@navo24.com` (or individual team inboxes)
       - `Reply-To:` `sales@navo24.com` (Inbound Sales routing)
   - **Mass Customer Broadcast via Excel (`Customers.xlsx`) Workflow**:
     * **Environment**: Always execute mass outreach scripts using the active virtualenv python (`/opt/hermes/hermes-agent/venv/bin/python3 script.py > outreach.log 2>&1`) in the background.
     * **Rate & Interval**: Send with a 0.8s–1.0s delay between emails (well under Resend's 10 req/s cap) to ensure smooth delivery of 700+ emails in ~10–12 minutes without rate limit errors.
     * **Personalization Parsing**:
       - Name present -> `Dear [Name],`
       - Name missing -> `Dear Partner,`
     * **Standard Headers**: Include RFC 8058 `List-Unsubscribe` for inbox deliverability.
   - **SeaRates Portfolio Transition & Navo24 Migration Broadcast Template**:
     * Highlights corporate decisions on the suspension of SeaRates and DFA digital brand portfolio.
     * Recommends active paid subscribers contact respective SeaRates refund team as noted in their SeaRates login banner.
     * Introduces Navo24 founded by core SeaRates leadership team with AI logistics technology and developer portal link (`https://navo24.com/developers/`).
     * Directs demo inquiries and replies to `sales@navo24.com` with Richard Marlowe's official signature.
   - **HTML Layout**: Clean, responsive, readable typography (15px `#1e293b`, 1.6 line height), callout box for critical refund/action items, and standard Richard Marlowe HTML signature with 1 blank line before signature and no top horizontal rule.
