# Agentic AI Workflows & Early-Stage Platform Sales Strategy

Playbook for handling two high-converting deal types at Navo24:
1. **Early-stage software platforms & proprietary startup developers** (Design-in strategy).
2. **AI platforms & Enterprise Agentic Workflows** (MCP-native positioning).

---

## 1. Early-Stage Software Platforms & Startup Developers (The Design-In Wedge)

When negotiating with founders or CTOs of proprietary software platforms (e.g. Tendency / Katio Landi) who currently move very low volume (0–5 containers/month):

### Core Principles:
- **Design-In Over Immediate Revenue:** In B2B SaaS, getting your API into the codebase of a proprietary logistics/freight software platform before its public launch creates a permanent, high-switching-cost integration. As their users scale, our volume automatically scales with them.
- **The $0 Free Tier Wedge:**
  - Emphasize the **Free Tier ($0, up to 5 active containers, 100 calls/month, no credit card required)**.
  - Position it as zero-risk development runway: during low months (0–3 shipments) it costs them nothing.
  - Transparent upgrade path: $50/month (up to 25 containers, ~$2/container) or $450/year (25% discount, $37.50/month).
- **Handling Language & Call Anxiety:**
  - If a foreign founder expresses hesitation over spoken English ("my English is terrible"), **never force a video/phone call**.
  - Immediately validate their preference: agree to keep everything over written email/chat.
  - Offer to communicate in their native language (e.g. Spanish, German, Italian, Russian) to remove communication friction.
- **Quote & Rates Digitization (FreightRates & Schedules API Bundling):**
  - Clarify whether "quotes/rates" means subscription tier pricing or freight rate data feeds.
  - If they want to digitize live ocean rates (e.g. China → Europe), confirm that **FreightRatesMCP** (live spot rates for 20'/40'/40HC) and **SchedulesMCP** (72,000+ sailings) operate via the same unified API key.
  - Provide free sandbox requests during their development phase so their engineers can build quoting features without paying data fees before launch.
- **Trial Pacing & Check-In Cadence:**
  - **Day 0:** Deliver clear pricing and docs link; invite them to share their registered signup email.
  - **Day 1–2 (24–48h):** Check-in on registration and documentation review. Offer direct developer-to-developer support for webhook/payload questions.
  - **Day 4–5:** Developer unblocking touch if they haven't sent test API calls.

---

## 2. Positioning Navo24 for Agentic AI & Supply Chain LLMs

When engaging AI supply chain platforms, thought leaders, or enterprise builders (e.g. Dr. Muddassir Ahmed / SCM Sensei AI):

### Value Proposition:
- **MCP-Native Architecture (Model Context Protocol):** Unlike legacy monoliths (project44, Descartes, SeaRates), Navo24 components are built natively as MCP servers for autonomous agents (Claude, LangChain, CrewAI, AutoGen, OpenAI function calling) with structured JSON schemas and DCSA events.
- **Observed Truth Over Carrier Marketing:** Separates static carrier schedule dates from actual satellite AIS positions and real berth timestamps across 255 ports.

### The 3 Core Agentic Workflows:

1. **Autonomous Demurrage & Exception Agent:**
   - *Workflow:* Agent continuously ingests container milestones and AIS coordinates via `TrackingMCP`.
   - *Autonomous Action:* Detects schedule slips and port congestion threatening free time, computes demurrage risk, recalibrates ETA, and drafts exception notifications or ERP tickets 48 hours before detention penalties accrue.

2. **Multi-Carrier Procurement & Reliability Copilot:**
   - *Workflow:* Agent evaluates carrier booking allocations using `SchedulesMCP` (72,000+ sailings, 60+ carriers) and `FreightRatesMCP` (live spot rates ex-Asia).
   - *Autonomous Action:* Cross-checks carrier spot rates against observed historical reliability (actual berth times at discharge ports) to recommend optimal cost-versus-delay tradeoffs.

3. **Natural Language Visibility Copilot:**
   - *Workflow:* Conversational interface inside enterprise Slack/Teams or ERP.
   - *Autonomous Action:* Translates plain-language procurement questions ("Which boxes for PO #4182 are delayed?") into live API queries across 241 ocean carriers, returning hallucination-free container states.

### Enterprise AI Call to Action:
Always propose a dedicated **PoC Sandbox API key** for their engineering team to test within their agentic loops, paired with a brief technical sync between lead architects.

---

## 3. Handling Skepticism, Anti-AI Slop & The "Reverse Pitch" Trap

### A. Overcoming the "ChatGPT-Fluff" Objection (Anti-AI Slop Standard)
When an AI founder, engineer, or executive flags your draft as generic marketing slop (*"This is a good response from ChatGPT, but I asked for real examples"*):
1. **Disarm with Humor & Radical Transparency**: Never defend the marketing jargon. Own it immediately:
   * *"Fair point, you caught me! Guilty of letting an LLM polish the draft — quite ironic when emailing the founder of an AI platform."*
2. **Anchor on Real, Verifiable References with Live Links**:
   * Cite real platform integrations: e.g. **Shipzy** (`https://shipzy.com`) for ERP timeline milestone ingestion.
   * Provide open developer portal links: `https://navo24.com/developers/`, `https://navo24.com/developers/reference/tracking/`.
   * Reference the official **Model Context Protocol** specification (`https://modelcontextprotocol.io`).
3. **Be Radically Honest About Market Maturity**:
   * State plainly: *"The freight industry hasn't yet put autonomous cargo-rebooking agents into production. Anyone claiming that today is selling marketing slideware."*
   * Re-frame where AI actually sits today: LLM Copilots (Claude, Cursor, LangChain) querying MCP servers for deterministic container states and D&D risk alerts.

### B. Detecting & Handling the "Disguised Vendor / Reverse Pitch" Pattern
When an industry figure, consultant, or competitor-partner (e.g. partnered with project44) probes under the guise of exploring your API, dismisses real ERP integrations, and pivots to pitching their own service:
* *The Signal:* *"Unless there is a clear AI use case, we will not be utilizing your APIs... Alternatively, we could provide the [Platform] API to Navo24 to help you build context-aware applications. I would be happy to discuss this with your CEO/CTO."*
* *The Diagnosis:* **Disqualified.** They are not a prospect; they are fishing for executive intros, vendor sales, or consulting engagements.
* *The Action:* Stop investing outbound sales effort immediately. Never argue or escalate to founders for sales exploration.
* *The Graceful Exit Template:*
  ```text
  Dear [Name],

  Thank you for the candid note and the pointer to your program with [Partner/Competitor] — impressive work.

  We already develop our own internal agentic and LLM reasoning stack, so integrating third-party AI wrapper APIs isn't on our immediate product roadmap right now.

  We appreciate the offer, and should our leadership see an opportunity for an ecosystem partnership or joint research down the road, we’ll certainly be in touch.

  Wishing you continued success with [Platform]!

  Best regards,
  [Sender Name]
  Navo24
  ```

