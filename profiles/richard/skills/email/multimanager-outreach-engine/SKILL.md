---
name: multimanager-outreach-engine
description: Use when launching team B2B email campaigns from Sheets.
---

# Multi-Manager B2B Outreach Engine (Navo24)

Execute high-converting B2B cold email sequences from Google Sheets or CRM databases on behalf of any Navo24 sales executive (Nikita, Richard, Oleg, Alyona, Kate, etc.).

## Mandatory Pre-Launch Protocol

Whenever Stefan or a team member asks to launch an outbound campaign:

1. **Clarify Key Campaign Parameters (Do NOT launch blindly):**
   - **Spreadsheet / Source:** Verify the Google Sheet URL, sheet tab name, and target row range.
   - **Sender Profile:** Confirm Manager Name, `From` address (`<name>@e.navo24.com`), `Reply-To` (`<name>@navo24.com`), and `CC` list (`<manager>@navo24.com, stefan@navo24.com`).
   - **Signature Spec:** Name, Title (e.g. Account Executive / Connections Manager), Phone number, Email, Address.
   - **Sequence Touch:** Which step to send (Touch #1, Touch #2 Follow-up, Touch #3, Touch #4 Breakup).

2. **Mandatory Pre-Flight Test to Stefan:**
   - **ALWAYS** render the exact 1-on-1 HTML email with the configured signature and send a live test to `Stefan Rogovskiy <stefan@navo24.com>` via Resend REST API.
   - Wait for Stefan's explicit review and confirmation ("Да", "Запускай", "OK") before sending to external leads.

3. **Batch Execution & Status Sync:**
   - Send via Resend REST API (`https://api.resend.com/emails`) with 0.3–0.5s polite rate-limiting.
   - Automatically batch update Google Sheets:
     - `Status` -> `contacted_pending`
     - `Touch X Date` -> `YYYY-MM-DD`
     - `Next Follow-up` -> `YYYY-MM-DD` (+3 days)
     - `Current Step` -> `Touch #X (Sent)`
   - Record in Airtable CRM / log results.

## Reusable Signature Template

```html
<div style="margin-top: 24px; font-family: Tahoma, Arial, sans-serif; font-size: 13px; color: #334155; line-height: 1.4; text-align: left;">
  <b>{MANAGER_FULL_NAME}</b><br>
  <b>{MANAGER_JOB_TITLE}</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics & Trade<br>
  {MANAGER_PHONE}<br>
  <a href="mailto:{MANAGER_EMAIL}" style="color: #2563eb; text-decoration: underline;">{MANAGER_EMAIL}</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #2563eb; text-decoration: underline;">www.navo24.com</a>
</div>
```

## Known Team Presets

- **Nikita Kurudzhy:**
  - Name: `Nikita Kurudzhy`
  - Title: `Account Executive`
  - Email: `nikita@navo24.com` (From: `nikita@e.navo24.com`)
  - Phone: `+380932285150`
- **Richard Marlowe:**
  - Name: `Richard Marlowe`
  - Title: `Connections Manager`
  - Email: `rich@navo24.com` (From: `rich@e.navo24.com` / `rich@navo24.com`)
  - Phone: `+44 203 440 9800` / `+44 7360 065904`
- **Oleg Chervinskyi:**
  - Name: `Oleg Chervinskyi`
  - Title: `Account Executive / Freight Visibility Desk`
  - Email: `oleg.chervinskyi@navo24.com`
- **Alyona Holubova:**
  - Name: `Alyona Holubova`
  - Title: `Account Executive`
  - Email: `alyona.holubova@navo24.com`
