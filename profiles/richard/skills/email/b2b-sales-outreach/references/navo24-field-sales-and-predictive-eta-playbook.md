# Navo24 Field Sales Playbook: Predictive ETA & Outreach Best Practices

Proven sales methodology and field insights from Navo24 senior account executives.

## 1. Core Value Proposition: Real Map Location & Predictive ETA

Shipping lines (MSC, Maersk, CMA CGM, Hapag-Lloyd, etc.) frequently show static or optimistic schedule ETAs that fail to reflect actual transit disruptions.

### How Navo24 Calculates Predictive ETA:
1. **Live Satellite AIS Feeds (110,000+ vessel positions)**: Real-time vessel coordinates, actual cruising speed, heading, and route deviations.
2. **Port Congestion & Anchorage Waiting Times**: Live monitoring of vessel queues at transshipment and destination ports.
3. **Carrier Historical Delays & Schedule Reliability**: Algorithmic scoring of line performance on specific port pairs.
4. **Transshipment Rollovers**: Instant detection of missed feeder connections at hub ports.

---

## 2. Touch #1 Email Structure: Problem Container Hook

### Rules for Cold Outreach:
- **Immediate Value Hook**: Challenge the reliability of carrier schedule ETAs and offer an immediate test for delayed/troubled containers.
- **No Cross-Selling in Touch #1**: Do not dilute the message with 3D Loading, Schedules, or Freight Rates. Maintain 100% focus on container tracking and ETA prediction.
- **Self-Serve Signup**: Never offer manual API key creation. Direct prospects to self-serve onboarding at `navo24.com` (5 active containers / 100 API calls free per month with no credit card required).
- **Target Audience Expansion**:
  - Freight Forwarders & NVOCCs.
  - Logistics IT, TMS developers, Supply Chain SaaS, and freight analytics platforms.
  - Decision Makers: CTOs, Heads of Product, Product Owners, Business Development Directors, Operations Directors, and functional mailboxes (`info@`, `pricing@`, `ops@`).
- **Strict Container ICP**: Disqualify non-container businesses (bulk/breakbulk, heavy project cargo, chartering without containerized freight like refractory manufacturers). Focus exclusively on FCL/LCL ocean containerized logistics.

---

## 3. LinkedIn Executive Outreach Rules

1. **Role Prioritization**: Focus primarily on **CTO, Head of Engineering, Product Owners, and Heads of Product** for software/IT integration.
2. **Language & Phrasing Standards**:
   - **STRICT BAN on "Are you guys"**: Replace with direct, professional questions (e.g. "Do you currently connect directly to carrier APIs...?").
   - **No "Scraping" Terminology**: Emphasize **direct official API connections across 239 ocean carriers + live satellite AIS tracking**.
   - **Extreme Simplicity**: Eliminate jargon (`MCP-native orchestration`, `data syndication`, `benchmarking feeds`). Write as a peer in a messaging app.
   - **No Email Signatures in DMs**: Never include `Best, Nikita \n Navo24`. Keep LinkedIn DMs in pure chat format (35-45 words).
3. **Bulletproof LinkedIn Search Links (Company Pages & Google X-Ray)**:
   - **Never use bare keyword search URLs** (e.g. `keywords=Company`): they frequently yield empty search results, wrong regional branches, or random people with similar words in their bio.
   - **Verified Company Page Link**: Extract the exact company slug from the website or LinkedIn directory (`https://www.linkedin.com/company/<company-slug>`) so reps can view the active **People / Employees** tab in 1 click.
   - **Google X-Ray Search URL**: Embed precision X-Ray search links (`https://www.google.com/search?q=site:linkedin.com/in/+"Company"+("CTO"+OR+"Head+of+Logistics"+OR+"VP+Operations")`) to instantly surface verified employee profiles in Google without LinkedIn search limits.

---

## 4. Lead Data Hygiene & Domain Pre-Flight Verification

- **Eliminate Mail Provider Domain Typos & Free Services**: Strip out mistyped domains (`gmauil.com`, `gmil.com`, `post.com`) and consumer/regional free mail services (`rediffmail.com`, `live.nl`, `web.de`, `libero.it`).
- **Pre-Flight DNS MX Resolution**: Programmatically verify that every prospect domain has valid active MX mail exchangers (`dns.resolver.resolve(domain, 'MX')`) before loading into sales spreadsheets.
- **Strict Name Normalization (Title Case Mandate)**: Cleanse raw inbound logs: convert ALL-CAPS names (`EMAD`, `MARC`) and lowercase names to proper Title Case (`Emad`, `Marc`, `Ferdinand`). Never address a prospect with placeholder text (`Hi Decision Maker`, `Hi Company`).

---

## 5. Multi-Channel WhatsApp Strategy

- Extract verified international phone numbers.
- Provide direct `Click-to-Chat (wa.me)` links with pre-filled conversational messages.
- Message format: 2-3 sentences max, personal greeting, direct mention of live vessel map tracking and free test for delayed containers.
