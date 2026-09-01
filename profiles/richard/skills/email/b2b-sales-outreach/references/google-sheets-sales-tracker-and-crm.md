# Google Sheets Sales Activity Tracker & Real-Time Sync Guide

Guidelines and code patterns for managing personalized Google Sheets activity trackers, deal pipelines, and outreach sequences for Navo24 sales representatives (e.g. Nikita).

## 1. Service Account & Authentication Setup

The Google Service Account JSON key is stored at:
`/opt/hermes/profiles/richard/google_service_account.json`

Client Email: `richard-bot@navo-sales-sheets.iam.gserviceaccount.com`

To grant Richard write access to any sales spreadsheet, the user shares the sheet with `richard-bot@navo-sales-sheets.iam.gserviceaccount.com` as **Editor**.

## 2. Standard Sheet Architecture

Each sales representative's Google Spreadsheet is structured into clean, styled tabs:
1. **`📌 Легенда & Правила`**:
   - Status color coding table with HEX codes and usage descriptions.
   - Quality markers (`🔥` High Volume/Priority, `⚡` Active Free Tier Trial, `⚠️` Warning/Duplicate, `❌` Invalid/Bounced).
   - 5 Golden Rules of Navo24 B2B Sales.
2. **`📧 Цепочка писем (Sequence)`**:
   - Comprehensive 4-touch outreach sequence playbook with timing, subject lines, value hooks, and CTAs.
   - Core delivery guidelines (timing, threading via `Re:`, personalization, prompt CRM status shifts).
3. **`👔 LinkedIn Decision Makers & DMs`**:
   - Multi-channel LinkedIn tracking targeting 1–3 decision-makers per target company.
   - Live pre-built LinkedIn search queries, tailored Connect Notes (<= 300 chars), and 1st Direct Messages (DMs).
4. **`📊 Monthly Dashboard`**:
   - 3 separate inbound/outbound streams: **Email Outreach (19 sources)**, **LinkedIn Outreach**, **Inbound & Website**.
   - Funnel metrics: `Found ➡️ Sent ➡️ Replied ➡️ Reply % ➡️ Trials ➡️ Closed Won ($)`.
   - Dynamic Excel formulas using `=IFERROR(D5/C5, 0)` for conversion percentages and sum aggregations across months.
5. **Operational Lead Sheets (by ICP)**:
   - `🎯 Forwarders & NVOCC` (DFA, CIFFA, WCA, GLN)
   - `💻 Tech Platforms & AI` (TMS, SaaS, AI agents)
   - `🚢 BCO & Shippers` (ThomasNet, ImportYeti, Kompass)
   - `🔄 Follow-ups & Active Trials` (Active trials and stalled deals)

## 3. Operational Columns Contract (15-Column Standard)

All operational lead sheets strictly adhere to the enhanced 15-column format with interactive controls:
1. `№` (Row index)
2. `Status (Статус)` — Dropdown + Conditional color fill
3. `🔥` (Priority indicator)
4. `Company (Компания)`
5. `Website (Сайт)`
6. `Contact Person (ЛПР)`
7. `Job Title (Должность)`
8. `Personal Email (Email ЛПР)`
9. `Product Focus (Продукт)`
10. `Current Step (Этап)` — Dropdown (`Touch #1 (Day 0)`, `Touch #2 (Day +3)`, `Touch #3 (Day +7)`, `Touch #4 (Day +14)`)
11. `Touch 1 Date`
12. `Next Follow-up`
13. `Subject Line (Тема)`
14. `Original Pain / Context (Контекст запроса)`
15. `Tailored Pitch Strategy / Action (Действие)`

## 4. Status Workflow & Color Palette

| Status ID | State Description | Hex Code |
|---|---|---|
| `not_attempted` | Lead queued, awaiting first touch | `#E0E0E0` (Grey) |
| `contacted_pending` | First touch sent (Email/Invite), awaiting reply | `#FCE5CD` (Peach) |
| `connected_no_msg` | Invite accepted / contact verified, drafting message | `#CFE2F3` (Light Blue) |
| `messaged_no_reply` | Pitch / offer sent, follow-up scheduled | `#FFF2CC` (Yellow) |
| `replied_warm` | Reply received, active dialogue / product interest | `#D9EAD3` (Green) |
| `trial_testing` | Free tier trial activated on navo24.com (5 cnt / 100 calls) | `#D0E0E3` (Cyan/Aqua) |
| `closed_won` | Deal won — paid commercial subscription active | `#B6D7A8` (Dark Green) |
| `closed_lost` | Deal lost / unresponsive / competitor chosen | `#F4CCCC` (Red/Rose) |

## 5. UI/UX Formatting & Styling Best Practices

1. **Header Styling**:
   - Dark Slate Blue (`#0F172A`) header fill with bold white text (`#FFFFFF`), centered vertical/horizontal alignment, and text wrapping enabled.
2. **Freeze Panes & Auto-Filters**:
   - Set `frozenRowCount: 1` on operational sheets and `frozenRowCount: 4` on the Dashboard.
   - Install `setBasicFilter` on operational sheets for 1-click filtering by Status, Step, or Company.
3. **Data Validation Dropdowns**:
   - Set `setDataValidation` with condition `ONE_OF_LIST` on column B (`Status`) and column J (`Current Step`).
4. **Column Width Optimization**:
   - Explicitly assign column widths: `№` (45px), `Status` (140px), `🔥` (40px), `Company` (150px), `Website` (170px), `Contact` (160px), `Job Title` (180px), `Email` (230px), `Product` (160px), `Step` (150px), `Dates` (105px), `Subject` (280px), `Context` (320px), `Action` (260px).
5. **Conditional Formatting**:
   - Apply `addConditionalFormatRule` using `TEXT_EQ` condition matching `not_attempted`, `contacted_pending`, `replied_warm`, `trial_testing`, etc., to color-code rows instantly.

## 6. Outreach Sequence Playbook (4 Touches)

- **Touch #1 (Day 0) — Authority Hook & Free Tier**:
  - *Subject:* `{FirstName}, direct ocean tracking & carrier feeds for {Company} — Navo24`
  - *Angle:* SeaRates founding team pedigree + 234 carriers + DCSA milestones + Free Tier (5 containers / 100 calls/mo) on `navo24.com`.
  - *CTA:* 10-minute introductory sync or direct self-serve test.
- **Touch #2 (Day +3) — D&D Penalty Pain Killer**:
  - *Subject:* `Re: {FirstName}, direct ocean tracking & carrier feeds for {Company}`
  - *Angle:* Automated Demurrage & Detention (D&D) free-time calculation across ocean lines + observed AIS ETAs to avoid carrier demurrage fines.
  - *CTA:* Test on 2-3 live MSC/Maersk/CMA CGM container numbers.
- **Touch #3 (Day +7) — Cross-Product Synergies**:
  - *Subject:* `Quick question regarding {Company}'s ocean schedules & load planning`
  - *Angle:* Schedules API (72k+ sailings, 255 ports) + 3D Container Loading (CTU Code / IMDG compliance).
- **Touch #4 (Day +14) — Breakup & Open API Sandbox**:
  - *Subject:* `Permission to close file for {Company} / Free API access`
  - *Angle:* Polite sign-off leaving active self-serve API test credentials open for future evaluation without sales pressure.

## 7. SeaRates Archive Ingestion & Team Ownership Ethics

1. **Large Archive Downloads via Google Drive API**:
   - For archives > 20 MB where Telegram direct upload fails, ingest via Google Drive API `drive_service.files().get_media(fileId=...)` using `/opt/hermes/profiles/richard/google_service_account.json`.
2. **HTML Telegram Export Fast Parsing**:
   - Parse `MSG SeaRates` and `Requests SeaRates` using regex-based extraction (`[CONTACT US]`, `From:`, `Phone:`, `Subject:`, `Message:`).
   - Filter out generic prefixes (`info@`, `sales@`, `support@`, `ops@`, `pricing@`, `dispatch@`) and free email domains (`gmail.com`, `yahoo.com`, `mail.ru`) to isolate high-value corporate decision-makers with concrete operational requests.
3. **Team Account Ownership & Re-activation Ethics**:
   - **No Permanent Monopoly**: Leads marked by past managers with no active sales pipeline are not permanently blocked.
   - **3+ Months Inactivity Rule**: Prospects with no touchpoints for 3+ months or 1+ year are open for re-activation.
   - **Team Transparency Protocol**: Before starting intensive re-engagement of an account with a prior assigned manager, notify the team group: *"Colleagues, no activity on [Company/Domain] for >3 months. If no active talks, taking into outreach re-activation."*

## 8. Deep Inbound Request Hyper-Personalization (Anti-Generic Mandate)

NEVER send generic boilerplate emails to inbound or re-activation prospects who submitted a specific inquiry. Always parse `Original Pain / Context` and customize:
1. **Pricing / Usage Inquiries** (*"pay for number of times", "flat rate"*): Focus on Navo's flexible Pay-As-You-Go model with zero monthly retainers + 5 free containers/mo.
2. **Software & Customs Inquiries** (*"customs software", "manifests", "API"*): Focus on developer-first MCP architecture, DCSA event normalization, and webhook milestones.
3. **Digital Forwarder Inquiries** (*"DFA", "digital forwarder"*): Highlight instant schedules (72k+ sailings) and tracking API to eliminate manual carrier web scraping.
4. **Rate Transparency Inquiries** (*"rates to Colombo/China", "spot prices"*): Highlight FreightRatesMCP daily spot indexes + SchedulesMCP transit reliability.
5. **Visibility & Tracking Inquiries** (*"lock track", "container status", "demurrage"*): Highlight DCSA events, observed AIS ETAs, and automated D&D free-time calculation.

## 9. Multi-Channel LinkedIn Executive Outreach Protocol

1. **Targeting Multi-Persona Decision-Makers (1–2 per account)**:
   - **Primary DM**: *VP of Logistics / Operations Director / Head of Ocean Freight*.
   - **Secondary DM**: *CTO / Head of Product* (for software/platform accounts) or *Supply Chain & Procurement Director* (for trading/BCO accounts).
2. **Connect Note Formula (<= 300 chars, Human & Low-Friction)**:
   - *Example:* `Hi {FirstName}, saw your logistics focus at {Company}. We build MCP-native ocean tracking & schedules API (ex-SeaRates team). Would love to connect here!`
3. **1st LinkedIn DM (Post-Acceptance, 3–4 sentences, Conversational)**:
   - Thank for connecting ➡️ Reference SeaRates engineering heritage ➡️ Highlight killer feature (234 carriers + automated D&D calculation + free tier) ➡️ Ask open question about their multi-carrier milestone workflows.
