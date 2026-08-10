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

1. **Client Language Matching**: Always match the language of the prospect. If a Chinese client replies in Chinese (e.g. 陈先生 from Qiaoye Logistics), translate questions and draft responses into clear, professional B2B Chinese.
2. **Direct Execution on Feedback**: When the user approves draft direction (e.g., "Billy text is good - translate to Chinese and send") or tells you to stop ("Стоп"), execute the translation, draft, or answer directly without embarking on unnecessary exploratory tool searches or file queries.
3. **Inbound Replies vs. Mass Cold Outreach**:
   - **Inbound Replies (1-on-1)**: Handled via `check_inbound.py` poller (3m interval). User approves/modifies drafts before sending.
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
   - **Mass Cold Outreach (Batches of 500)**: B2B campaigns across Airtable bases (`CN FF 1`: `appdWYgvtQR2Fgaeq` / `CNFF-1`, `CN FF 2`: `appa1AH0vV4fl1BVQ` / `CNFF-2`, `CN FF 3`: `appVItBOee1awOPHh` / `CNFF-3`) with 1m sending interval, CCing `lxxmng@navo24.com` & `stefan@navo24.com`. Update `Stage` and `status` to `"Contacted"` via Airtable PATCH API strictly record-by-record AFTER each email is sent.
   - **Plain Text Body + HTML Signature Only**: Cold outreach emails MUST use a natural human plain-text body (or simple HTML text). DO NOT send full HTML email newsletter templates, which look like automated marketing blasts. ATTACH ONLY the official HTML signature at the bottom (Richard Marlowe, Senior Sales Manager, domain links).
   - **Verification before Confirming Launch**: Never report a mass outreach batch as "launched/running" based on text alone. Verify that the necessary credentials (full Airtable PAT format `pat<id>.<secret>`, SMTP credentials, or local script) are present and actually executed.
4. **Airtable PAT Authentication & Base Mapping**:
   - Airtable Personal Access Tokens use the full format `pat<id>.<secret>` (e.g. `patzjFlOTnLygbDs0.64e5...`). Single `pat<id>` prefixes will return 401 Unauthorized.
   - Base mapping for Chinese Freight Forwarder outreach:
     * `CN FF 1` = Base ID `appdWYgvtQR2Fgaeq` (Table `CNFF-1`)
     * `CN FF 2` = Base ID `appa1AH0vV4fl1BVQ` (Table `CNFF-2`)
     * `CN FF 3` = Base ID `appVItBOee1awOPHh` (Table `CNFF-3`)

## Pitfalls & Common Mistakes

- **CRITICAL: Premature CRM Status Updates**: Never bulk-update Airtable records from `Lead` to `Contacted` in advance or without actually dispatching the emails. Sending a batch of 500 emails with a 1-minute interval physically takes **~8.3 hours** — updating Airtable in seconds without real SMTP/API dispatch corrupts lead tracking and creates false completion reports. Always update Airtable status record-by-record AFTER each email is actually sent.
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
