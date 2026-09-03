# Navo24 Ideal Customer Profile (ICP) & Sales Handbook

Practical guide for Navo24 sales representatives and account executives on audience segmentation, decision-makers, core pains, qualification, and objection handling.

---

## 1. Navo24 Positioning & Value Proposition

Navo24 (navo24.com) is a developer-first data infrastructure provider founded by the original core engineering and product leadership behind SeaRates (10+ years developing freight intelligence).

Unlike heavy legacy monoliths (project44, Descartes, legacy SeaRates) requiring $30k+ annual commitments, Navo24 provides composable, lightweight MCP-native components (Model Context Protocol) and clean JSON REST APIs:
- **TrackingMCP**: 241 ocean carriers (132 direct connectors, 109 partner lines), 0–5 minute freshness, DCSA milestones, automated D&D free-time calculation, 4 live AIS feeds (110,000+ vessels), port congestion alerts.
- **SchedulesMCP**: 5,000+ lanes, 255 global ports, 72,000+ live sailings with observed carrier reliability.
- **FreightRatesMCP**: Daily verified spot rates ex-Asia (20'/40'/40'HC) and container freight indices.
- **LoadingMCP**: 3D container & truck loading optimization compliant with CTU Code, IMDG, EN 12195, and Center of Gravity (CoG).
- **AirTracking API**: Real-time AWB tracking across 100+ global airlines.
- **Self-Serve Free Tier**: 5 active containers and 100 API calls/month forever (zero upfront commitment, no credit card required).

---

## 2. Core ICP Segmentation Matrix

### ICP 1: Freight Forwarders & NVOCCs (Independent Forwarders)
- **Profile**: Medium to large independent forwarders (20–500 employees, 500–50,000 TEU/year). Members of WCA World, JCtrans, CIFFA, FIATA, GLN, DFA.
- **Key Decision-Makers**: CEO / Managing Director, VP / Head of Ocean Freight, Operations Director, Pricing Manager.
- **Core Pains**:
  1. Manual website checking across 10–15 shipping lines with CAPTCHAs (2–3 hours/day per logistics operator).
  2. Severe demurrage & detention (D&D) penalties due to unmonitored container discharge and free-time expiration.
  3. Client dissatisfaction and constant phone calls asking "Where is my shipment?".
- **Navo24 Solution**: Unified API across 241 lines, white-label client notifications, automated D&D calculation by port/line, instant schedules for spot quotation.
- **Target Products**: Tracking API + Schedules API.
- **Pricing**: $50/mo starter (up to 25 shipments) to scalable enterprise tiers.

### ICP 2: Beneficial Cargo Owners (BCOs) & Importers
- **Profile**: Large commodity traders, retailers, industrial manufacturers, agro-exporters (Bunge, ADM, Cargill, Wayfair, Target, Walmart logistics). 100–10,000+ TEU/year. Sources: ImportYeti, ThomasNet, Volza, US Customs.
- **Key Decision-Makers**: VP of Supply Chain, Director of Global Logistics, Inbound Freight Manager, Head of Procurement.
- **Core Pains**:
  1. Opaque supply chains: carrier reports container "arrived" while vessel is anchored on roadstead for 5 days.
  2. Factory/warehouse downtime and supply chain disruptions due to false carrier schedule ETAs.
  3. Hidden markups and freight surcharges from freight forwarding intermediaries.
- **Navo24 Solution**: Independent AIS-observed ETAs (grounded in satellite telemetry, not liner PR schedules), predictive port congestion alerts, verified ex-Asia spot rate benchmarking.
- **Target Products**: Tracking API + FreightRates API + Loading 3D.

### ICP 3: Logistics Tech, TMS/ERP Vendors & AI Platforms
- **Profile**: B2B SaaS logistics startups, Transportation Management Systems (TMS), SAP/Oracle/Dynamics integrators, autonomous AI agent builders.
- **Key Decision-Makers**: CTO, Head of Product, Lead Solutions Architect, AI Engineering Lead.
- **Core Pains**:
  1. Enormous expense ($200k+/year) maintaining internal carrier scrapers that break on website changes.
  2. Legacy competitors (project44, Descartes) impose ancient SOAP/XML interfaces, inflexible contracts, and months of onboarding.
  3. Total lack of native MCP (Model Context Protocol) support for LLMs and AI workflows.
- **Navo24 Solution**: MCP-native out of the box, clean OpenAPI REST JSON, 99.9% uptime SLA, instant developer signup and testing.
- **Target Products**: All 4 MCP components.

### ICP 4: Multimodal & Air Cargo Forwarders
- **Profile**: Express logistics, air cargo forwarders, cross-border e-commerce fulfillment.
- **Key Decision-Makers**: Air Freight Manager, Operations Lead.
- **Core Pains**: Fragmented AWB tracking across 100+ separate airline portals.
- **Navo24 Solution**: AirTracking API by Master AWB number with standardized milestones.

---

## 3. Categorical Anti-ICP (Never Waste Sales Time)

1. **B2C Private Individuals**: People looking for personal parcels, luggage, or AliExpress packages.
2. **Trucking-Only Carriers**: Domestic trucking without ocean or air freight legs.
3. **Physical Forwarding & Customs Requests**: Prospects asking Navo24 to physically book vessels, provide customs clearance, or haul cargo. We are an IT data infrastructure provider, NOT a freight broker.
4. **Custom Software Development**: Prospects demanding custom monolithic ERP development from scratch.

---

## 4. Discovery Script & Qualifying Questions (BANT)

**Golden Rule**: *Never pitch features abstractly. Ask the prospect for a real troubled/active container or booking number during the call. Look it up live on navo24.com/track — seeing actual AIS vessel location and D&D free-time closes the sale immediately.*

1. **Volume**: "How many ocean containers or bookings do you actively manage in transit each month?" (Qualifies pricing tier).
2. **Carrier Fit**: "Which shipping lines carry the majority of your volume — top carriers or regional feeder lines?" (Confirms 241 carrier coverage).
3. **Workflow Pain**: "How do your operators currently track shipment milestones — manual portal checking or direct system feeds?" (Identifies operator routine).
4. **Financial Impact**: "Have you incurred demurrage or detention charges over the past 6 months because free-time expiration was missed?" (Pinpoints immediate ROI).
5. **Authority**: "If our API automates status feeds and cuts demurrage risk to zero, who handles technical integration and vendor sign-off?"

---

## 5. Objection Handling Playbook

- **"We already use project44 / Vizion / SeaRates"**:
  *"Great platforms. However, Navo24 was founded by the original core team who built SeaRates for 10+ years. We created Navo24 specifically to fix the bloat of legacy monoliths: we provide lightweight, MCP-native components with direct carrier connectors (132 lines), 0–5 min latency, and a free tier. Let's test 5 of your active containers in parallel — compare our observed ETAs and update speed side-by-side."*
- **"Carrier websites are free"**:
  *"True, but when tracking 30+ containers across 6 lines, operators spend 2+ hours daily entering CAPTCHAs and chasing updates. Navo24 automates the entire process, provides webhooks, and alerts you to demurrage risks BEFORE penalties accrue ($1,500+). Preventing one demurrage invoice pays for Navo24 for months."*
- **"We have no budget right now"**:
  *"That is exactly why we built our permanent Free Tier: 5 active containers and 100 API calls per month, completely free without a credit card. You can start getting live data today with zero budget approval."*
- **"We don't have developers to integrate an API"**:
  *"No coding is required! You can use our ready web interface at navo24.com, export Excel tracking reports, or connect our MCP connector directly to your corporate AI assistant in 2 clicks. Let me show you on a 5-minute demo."*

---

## 6. Onboarding Collateral Generation (.docx)

For new sales representatives and onboarding materials, use `/opt/hermes/profiles/richard/scripts/generate_icp_docx.py` to compile the complete ICP matrix, discovery script, objection handling bank, and email templates into a formatted Word handbook:
- File Output: `/opt/hermes/profiles/richard/Navo24_Ideal_Customer_Profile_Guide.docx`
- Built using `python-docx` with professional typography, corporate navy styling (`#1B365D`), table formatting, and callout blocks.
- Synchronized with verified carrier metrics (241 ocean carriers, 132 direct connectors).
