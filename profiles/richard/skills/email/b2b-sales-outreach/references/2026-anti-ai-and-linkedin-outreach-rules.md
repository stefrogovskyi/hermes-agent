# 2026 B2B Cold Outreach & LinkedIn Executive Playbook

## Core Research Findings (Lavender, Belkins 5.5M emails, Gong 85M emails, Expandi, Lemlist)

### 1. B2B Cold Email 2026 Standards
- **Optimal Length**: 40–65 words. Emails under 75 words get 83% more replies than 120+ word emails.
- **Subject Lines**: 2–3 words, lowercase, internal colleague style (`company / topic`). Avoid capitalized product marketing subjects (`John, direct ocean tracking... — Navo24`) which drop open rates by 17.5%.
- **Zero AI Slop**: Remove all generic phrases ("I hope this email finds you well", "streamline workflows", "game-changer", "unifying seamless experience").
- **Zero Filler Openers**: Strict ban on "quick question", "quick note", "quick thought", "quick follow-up". Jump straight to the core point.
- **Zero Em-Dashes**: Strict ban on `—` and `–`. Use commas, colons, or clean direct clauses.
- **Zero-Friction CTA**: Do not ask for calls on touch #1. Ask low-friction interest questions ("Worth exploring if our free tier helps your ops team?").
- **Clean Copy-Paste Ready Email Text Standard**:
  - When outputting email drafts or final text for copy-pasting into Gmail/Outlook:
  - Remove all markdown bullet characters (`-`, `*`) and raw HTML tags inside text body lines.
  - Use clean standard numbered lists (`1.`, `2.`) and standard double line-breaks between paragraphs.

### 2. LinkedIn Executive Outreach 2026 Standards
- **Carrier Count**: TrackingMCP covers **239 ocean carriers** (with 121 direct connectors and 186 SCACs) and **97 airlines (AWB)**. SchedulesMCP covers 60+ lines with 72,000+ sailings.
- **Strict .ru / Russian Entity & Domain Exclusion**: Mandated by executive policy (Stefan): NEVER include `.ru`, `.su`, `.рф`, yandex/mail.ru domains, or Russian logistics entities in any outreach list, CRM, or campaign. Clean and replace with verified international forwarders immediately.
- **Name Sanitization & Title Case Normalization**: Raw database extracts often have all-caps names (`EMAD`, `MARC`). Always normalize to Proper Title Case (`Emad`, `Marc`, `Ferdinand`) and clean non-name tokens before generating email greetings or LinkedIn DMs to prevent sounding like an automated bot.
- **Address Real DM Humans by First Name**: ALWAYS address the real human decision maker by first name (`Hi {FirstName}`). NEVER address company names (`Hi Acme`), titles (`Hi Decision Maker`), or generic greetings (`Hi there`).
- **Messenger/Chat Style Only (Zero Email Artifacts)**: LinkedIn DMs are private chat messages, NOT email letters.
  - NEVER attach email signatures (`Best,\nNikita`, `Navo24`).
  - NEVER add formal closings or company sign-offs.
  - Keep it in direct conversational chat flow (like Telegram/WhatsApp/Slack).
- **Connection Notes**: Under 20 words, zero sales pitch, zero links. Gives 58–68% acceptance vs <21% for pitch notes.
  - Pattern: `Hi {FirstName}, saw your ocean freight focus at {Company}. Fellow logistics operator (ex-SeaRates team). Glad to connect!`
- **1st Direct Message (Post-Acceptance)**: Under 45 words, question-first into an operational pain point (D&D calculation, carrier website scraping, DCSA feed), zero links on touch 1.
  - Pattern: `Hi {FirstName}, thanks for connecting!\n\nHow much time is your ops team spending chasing carrier websites (MSC, Maersk, CMA CGM) for milestone updates right now?\n\nWe rolled out Navo24 to unify 239 carriers with live D&D countdowns. Let me know if you would like to test a live container number through it.`

### 3. Guaranteed Zero-404 LinkedIn URL Architecture & B2B Enrichment APIs
- **Zero Blind Speculative `/in/` Slugs**: Never guess personal LinkedIn profile slugs (e.g. `linkedin.com/in/atlas-trading` or `in/john-smith`). LinkedIn redirects unverified slugs to `404 This page does not exist`.
- **Direct Scraping Failure**: Direct headless browser visits from datacenter IPs hit Cloudflare/DataDome bot challenges or LinkedIn authwalls (`Sign In / Anmelden`).
- **Official B2B Enrichment API Pipeline (Hunter.io / Snov.io / Apollo.io)**:
  1. **Hunter.io API**:
     - Endpoint: `GET https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}&limit=10`
     - Returns verified executive names, roles, corporate emails, and exact personal LinkedIn URLs (`linkedin`) with full unique hashes.
  2. **Snov.io API**:
     - Auth: `POST https://api.snov.io/v1/oauth/access_token` with `client_id` and `client_secret` -> `Bearer {token}`
     - Endpoint: `GET https://api.snov.io/v2/domain-emails-with-info?domain={domain}&type=all&limit=10`
     - Extracts `socialLinks.linkedin`.
  3. **Apollo.io API**:
     - Header: `X-Api-Key: {APOLLO_API_KEY}` (Mandatory header format)
     - Endpoint: `POST https://api.apollo.io/v1/mixed_people/search` with `q_organization_domains` and `person_titles`.

### 4. Commercial Quoting & Honest Pricing Rules
- Never invent arbitrary unit prices (e.g. cents per container) unless explicitly approved.
- Official baseline structure:
  - **Free Tier**: €0 / 5 active containers + 100 API calls/mo (no credit card, never expires).
  - **Starter Plans**: From $49 / €49 per month (Pay-as-you-go, scalable, month-to-month, zero annual lock-in).
  - **Volume / Enterprise Plans**: Custom volume-based pricing with automatic scaling discounts; direct prospect to a brief 10-minute demo call or desk approval with Stefan (`stefan@navo24.com`).
  - **Coverage**: 239 ocean carriers, 97 airlines (AWB), satellite AIS, DCSA milestones, D&D free-time, Predictive ETA.

### 5. Sales Peer Review Template
```text
Могу ли я еще тебя помучать вопросами, пожалуйста? Хочу ответить лиду на запрос и хочу быть уверен что не отвечаю ерунду.

Запрос лида:
[Exact client inquiry text]

Мой предполагаемый ответ:
[Clean, point-by-point, professional response with no markdown artifacts]
```
