# Competitor Intelligence Radar, Weekly Sales Loops, Telephony Voice AI & WhatsApp Gateway

## 1. Weekly Sales Team Testimonial & Customer Win Loop

### Objective & Schedule
- **Schedule:** Every Monday at 08:00 Kyiv time (`0 5 * * 1` UTC).
- **Target:** `To: Navo Sales Team <sales@navo24.com>`, `CC: Stefan Rogovskiy <stefan@navo24.com>, Alexei Shatunov <lxxmng@navo24.com>`.
- **Sender:** `From: Richard Marlowe <rich@e.navo24.com>`, `Reply-To: sales@navo24.com`.
- **Script:** `/opt/hermes/profiles/richard/scripts/send_weekly_sales_testimonial_reminder.py`.

### Dynamic Rotation & Content Rules
1. **Inspiring Business Aphorisms:**
   - Rotates authoritative quotes from Buffett, Bezos, Gates, Godin, Ziglar, and Kaufman on customer delight, reputation, and social proof.
2. **Dynamic 18+ Trigger Pool Across All Navo24 Products & Customer Delight:**
   - Every week picks a fresh mix of 3 distinct angles from 8 core categories:
     * *General Customer Delight & Ease of Use:* Intuitive UI, responsive human partnership, seamless migration from legacy systems.
     * *Customer Care & Support:* Lightning-fast support reaction ("Wait... you've already fixed it?!"), bespoke custom setups.
     * *Tracking & D&D Prevention:* 234-carrier coverage, observed ETAs preventing costly demurrage/detention fees, live AIS ocean maps.
     * *Schedules & Route Optimization:* 255 ports, 72,000+ sailings, avoiding transshipment bottleneck delays.
     * *FreightRates Spot Benchmarks:* Live ex-Asia market rates without hidden surcharges, 30-day trend analytics.
     * *Loading 3D Optimization:* IMO/ILO/UNECE CTU Code compliance, saving container space and preventing cargo damage.
     * *AirTracking API:* Single-window visibility across 80+ airlines alongside ocean freight.
     * *Developer Experience & MCP:* 5-minute setup, Free Tier onboarding (5 containers, 100 calls), Claude/Cursor/n8n MCP connections.
3. **Temporal Wording Mandate:**
   - ALWAYS use "недавно" (recently) instead of rigid "на этой неделе" or "на прошлой неделе".
4. **Friction-Free Client Ask Script:**
   - Provides sales reps with a ready-to-use message draft offering to pre-write a 2-3 sentence draft testimonial for the client's quick approval.

---

## 2. Competitor Intelligence & Benchmark Radar Engine

### System Architecture
- **Seed Base:** 96+ curated logistics tech competitors in `/opt/hermes/profiles/richard/cache/competitors_seed_list.json`.
- **Execution Script:** `/opt/hermes/profiles/richard/scripts/competitor_intelligence_engine.py`.
- **Schedule:** Daily at 11:00 Kyiv time (`0 8 * * *` UTC).
- **Chronology & Live Google Sheet:** `https://docs.google.com/spreadsheets/d/1z6O6-IkUUntnXnqTj66TwbMtU9UwzN3y0RVBbiY-uPI/edit`.

### 3-Tier Competitor Classification Framework
1. 🎯 **TIER 1 — Direct Peers (Deep Monitoring Focus):**
   - *Key Players:* Terminal49, project44, Vizion, SeaRates (DP World), Freightify, Cargofive, Container xChange, Portrix, Netpas.
   - *Metrics:* API rate limits, pricing models, carrier coverage, DCSA compliance, D&D algorithms, widget UX.
2. 🤝 **TIER 2 — Systems for Integration (Sales Outreach Targets):**
   - *Key Players:* CargoWise (WiseTech), Logisuite, Magaya, Infor Nexus, Soloplan, Kuebix.
   - *Metrics:* Legacy tracking weaknesses, opportunities to sell Navo24 Tracking & Schedules API plugins to their user base.
3. 🗑️ **TIER 3 — Legacy Directories, Defunct Crypto & Niche Portals (Archived/Filtered):**
   - *Key Players:* Pier2Pier (static link list), 300cubits (defunct 2018 blockchain), uShip (furniture reverse-auction).
   - *Handling:* Excluded from daily alert chatter to maintain high signal-to-noise ratio.

### Strict 3-Part Analytical Output Format (Zero-Boilerplate Mandate)
Every competitor breakdown MUST follow this 3-part concrete structure:
- `• Продукт и ЦА:` What specific software/service they sell, target persona (BCOs, SMB forwarders, carriers), tech architecture.
- `• Слабые места:` Proprietary lock-in, legacy client-server tech, manual data entry, high transaction commissions, lack of open DCSA APIs.
- `• Сравнение с Navo24 & Коммерческая выгода:` Exact technical superiority of Navo24 and tactical pitch for our sales team to win their clients.

### Anti-Boilerplate & Dynamic Generation Rules
1. **Zero Cookie Banner / Nav Scraping:** Never extract raw menu headers, cookie notices, or generic marketing fluff.
2. **WAF & Login Wall Accuracy:** Never output false "VPN/Offline" claims when server-side scrapers hit social media login walls (Facebook, LinkedIn).
3. **Dynamic Deduplicated Top-5 Proposals:** Rotate feature and sales engineering proposals dynamically using a deduplication history cache (`/opt/hermes/profiles/richard/cache/proposed_ideas_history.json`). Never output identical static lists.

---

## 3. Telephony & Voice AI Pipeline (Twilio + British Persona)

### Outbound Caller ID Integration (+44 7360 065904)
- **Twilio Verification:** Existing UK mobile numbers are authorized via Twilio `Verified Caller IDs` API / Console (`PN637a106ac9f7c9b55afe339b111a430e`) without requiring new number purchases.
- **Outbound Dispatch:** Python scripts call Twilio REST API with `from_="+447360065904"` and webhook URL pointing to the Voice Media Stream.
- **Trust Hub / KYC Prerequisite:** Outbound calls via Twilio REST API require an approved Customer Profile in Twilio Trust Hub. If Twilio returns `HTTP 401: Primary compliance profile is not approved`, inspect the KYC bundle in Trust Hub and submit company details for verification.
- **Inbound vs Outbound Routing Architecture:** A Verified Caller ID allows outbound calling with the custom number as caller ID. For inbound call reception by AI, route calls via unconditional call forwarding from the SIM card to a Twilio UK number/SIP URI, purchase a direct Twilio UK number (`+44 20...`), or deploy a WebRTC voice calling widget on the website.

### Voice Engine Configuration (Zero-External-Key Setup)
- **Telephony TTS:** Twilio built-in Amazon Polly Neural voices (**`Polly.Brian-Neural`** or **`Polly.Arthur-Neural`**) provide natural British Business English without external ElevenLabs API subscription overhead.
- **Telegram Voice Bubbles:** Hermes Edge TTS configured with **`en-GB-RyanNeural`** (English) and **`ru-RU-DmitryNeural`** (Russian) to maintain an identical vocal timbre across phone calls and chat voice notes.
- **Ultra-Low Latency (<400ms):** Twilio Media Streams (8kHz μ-law WebSockets) + Deepgram Nova-2 (STT) + Fast LLM + Streaming TTS with natural barge-in interruption support.

---

## 4. WhatsApp Multi-Device Gateway & Inbound Triage (+44 7360 065904)

### Service Architecture
- **Dedicated Port:** Port `3060` (`/opt/hermes/profiles/richard/services/whatsapp-gateway/`).
- **Auth & Session Directory:** `auth_info_richard/`.
- **Pairing Methods:** 
  * 8-digit Pairing Code (`POST /request-pairing-code` with `phone: "447360065904"`).
  * Direct QR Code scan (`GET /status` -> base64 PNG).

### Inbound Message Triage & Draft Approval Flow
1. **Message Interception:** Gateway receives inbound client messages via `sock.ev.on('messages.upsert')`.
2. **Telegram Notification to Stefan (`chat_id: 330656040`):**
   * Sender identity, company name, and phone number.
   * Full client message text + complete Russian translation.
   * Prepared AI draft reply from Richard Marlowe (English/Chinese/Russian as appropriate).
3. **Approval Mandate:** On Stefan's confirmation ("Да", "Отправляй", "OK"), dispatch reply via `POST http://localhost:3060/send-message`.
