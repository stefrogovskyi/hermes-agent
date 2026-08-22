# Competitive Battlecard: Navo vs SeaRates vs Internal Development (Key Selling Points & Continuity Guarantees)

## 1. Core Technical Differentiators (Navo vs SeaRates & In-House Development)

1. **DCSA Data Model Standardization (Digital Container Shipping Association)**:
   - *SeaRates / In-House Flaw*: Fragmented, carrier-specific JSON structures and scraped HTML fields requiring custom scrapers/parsers per carrier on the client side. High ongoing maintenance when carriers alter portals.
   - *Navo Advantage*: All 234 ocean carriers normalized to official DCSA standards (unified milestone codes, standardized event schemas). Integrate once for all carriers.

2. **Real-Time AIS Telemetry & AI Predictive ETA (0–5 Min Freshness)**:
   - *SeaRates Flaw*: Infrequent static position pings; ETA timestamps remain stale if the shipping line delays updating portal data.
   - *Navo Advantage*: Live AIS fused from 4 satellite/terrestrial feeds (110,000+ vessels) with AI predictive ETA models calculating true arrival based on vessel speed, nautical routes, and anchorage wait times.

3. **Event-Driven Signed Webhooks (HMAC-SHA256)**:
   - *SeaRates Flaw*: High API polling overhead; clients must continuously ping endpoints to discover status changes.
   - *Navo Advantage*: Real-time push webhooks signed with HMAC-SHA256 headers (`X-CargoPulse-Signature`) delivering instant milestone events directly to client backends/TMS.

4. **Demurrage & Detention (D&D) Free-Time Risk Tracking**:
   - *SeaRates Flaw*: Only shows raw milestone strings without commercial context or storage calculations.
   - *Navo Advantage*: Automated risk engine comparing actual vessel discharge timestamps against published carrier free-time, firing proactive risk alerts before detention/demurrage fees accrue.

5. **Port Congestion & Terminal Dwell Times**:
   - *SeaRates Flaw*: No terminal or port operational metrics.
   - *Navo Advantage*: Live dwell and berth congestion metrics across 255+ key ports worldwide.

6. **Unified MCP-Native Ecosystem (4 Components under 1 Key)**:
   - *SeaRates Flaw*: Fragmented legacy tools; no native support for AI assistant frameworks.
   - *Navo Advantage*: Model Context Protocol (MCP) native for LLMs/AI agents, plus instant unified access to Tracking, Schedules (72k+ sailings), 3D Container Loading optimization (CTU/IMDG compliance), and Spot Freight Rates.

---

## 2. Continuity, SLA & Long-Term Availability Guarantees

1. **Enterprise 99.9% SLA & Contractual Protections**:
   - Contractually guaranteed 99.9% uptime SLA backed by Enterprise Master Services Agreement (MSA) governed under UK Law (London HQ: 30 St Mary Axe), including defined service credit remedies.

2. **12-Month Deprecation & Sunset Notice Policy**:
   - Contractual commitment to provide at least 12 months' prior written notice before deprecating any API version or endpoint.
   - First-class maintenance of the **SeaRates Compatibility Endpoint** for 6–12+ months as a zero-friction drop-in bridge.

3. **Multi-Source Redundancy (No Single Point of Failure)**:
   - Ingestion engine aggregates across 121 direct carrier connectors, DCSA gateways, and 4 independent AIS providers with automated Cloudflare Edge failover. Not a re-seller or scraper dependent on a single upstream provider.

4. **Dedicated Data-First Company**:
   - Navo is a specialized logistics data infrastructure provider. API data feeds are our primary core product, not a secondary side project of a freight forwarding brokerage.
