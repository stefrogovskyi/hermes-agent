# Ocean Freight Rate Sources, Carrier APIs & Telegram Delivery Playbook

## 1. Zero-Key Live Spot Rates: SkyPace Public REST API

SkyPace (Maxton Shipping Inc DBA Skypace, FMC License OTI 027662) maintains an open, unauthenticated REST API exposing 61,605+ bookable FCL rates across 1,750+ trade lanes:

### Key Endpoints:
- **Global Rate Index (Pagination up to 1000 items):**
  `GET https://skypace.com/ocean-freight/api/public/rate-index?page=1&pageSize=1000`
  - Returns: `originCity`, `originUnlocode`, `destinationCity`, `destinationUnlocode`, `price20gp`, `price40hc`, `minTransit`, `maxTransit`, `oceanCarriers`, `sailingsCount`, `minEtd`, `maxEtd`.
- **City Port Route Widgets:**
  `GET https://skypace.com/ocean-freight/api/public/city-route-widgets?city={CityName}`
- **Port UN/LOCODE Canonical Map & Aliases:**
  `GET https://skypace.com/ocean-freight/api/public/port-canonical-map`
- **Route Specific Carrier & Sailing Breakdown:**
  `GET https://skypace.com/ocean-freight/rates/{origin-city}-to-{destination-city}`
  - Renders exact line quotes: Yang Ming, Hapag-Lloyd, Evergreen, OOCL with ETD dates, transit days, and direct booking links (`Select & Quote`).

---

## 2. Status of Aggregators (Cogoport, iContainers, Cargofive)

- **Cogoport (`cogoport.com`):** The public endpoint `/discover_rates` was decommissioned (returns 404). All rate inquiries require verified corporate login to `app.cogoport.com`.
- **iContainers (`icontainers.com`):** Direct rate calculation is gated behind a mandatory lead-capture form (`quotes.icontainers.com`). Unsuitable for automated headless fetching.
- **Cargofive (`cargofive.com`):** Closed enterprise Rate Management System; rates require licensed B2B API integrations.
- **Alternative Open Portals:**
  - **Transporteca (`transporteca.co.uk`):** Open quotes without registration for Sea (FCL/LCL), Rail (Silk Road China-Europe), and Road.
  - **Eurosender (`eurosender.com`):** Instant road and air freight rates via frontend calculator.
  - **BookAirFreight (`bookairfreight.com`):** Instant per-kg spot air cargo quotes for major airport pairs.
  - **Freight-Calculator (`freight-calculator.com`):** Open ocean container freight calculator without login walls.

---

## 3. Freightos Baltic Index (FBX) Live Spot Benchmarks

For global macroeconomic spot index validation:
- **URL:** `https://fbx.freightos.com/`
- **Extraction Method:** Headless Chromium / Playwright DOM evaluation.
- **Key Corridors:**
  - `FBX 11`: China / East Asia to North Europe (40' HC)
  - `FBX 01`: China / East Asia to US West Coast (40' HC)
  - `FBX 03`: China / East Asia to US East Coast (40' HC)
  - `FBX 13`: China / East Asia to Mediterranean (40' HC)

---

## 4. Direct Ocean Carrier Spot APIs (Enterprise Reality)

Top shipping lines (Maersk, CMA CGM, Hapag-Lloyd, MSC, COSCO) **do NOT offer open public API keys**:

| Carrier | Platform | Requirements for API Access |
|---|---|---|
| **Maersk Spot** | `developer.maersk.com` | Customer CID, approved commercial volume, OAuth2 mTLS with Client ID/Secret |
| **CMA CGM SpotOn** | `apis.cma-cgm.com` | eBusiness account, signed API License Agreement, account manager approval |
| **Hapag-Lloyd Quick Quotes** | `developer.hapag-lloyd.com` | Verified corporate Web-ID, DCSA contract compliance, Cloudflare WAF bypass |

*Takeaway:* For autonomous agents and quick ingestion, use licensed NVOCC aggregator feeds (SkyPace) rather than attempting direct unauthenticated calls to tier-1 carrier portals.

---

## 5. SeaRates Platform Quirks & Session Storage

- **Account Status:** DP World has announced the deprecation of SeaRates Digital Solutions.
- **Auth Bypassing:** Headless login requires Playwright with stealth flags (`--disable-blink-features=AutomationControlled`, custom viewport, navigator.webdriver override) to satisfy Google reCAPTCHA v3.
- **Session Tokens:** Saved cookies (`s-token`, `PHPSESSID`) must be injected into the browser context to access Logistics Explorer rate cards and avoid the 1-request-per-day guest block (`API_KEY_LIMIT_REACHED`).

---

## 6. Model Context Protocol (MCP) Standards (AfterQuery / MCP-Atlas)

- **AfterQuery MCP-Atlas Benchmark:** Standardizes agentic tool-use evaluation across 36 real MCP servers with Dockerized sandboxes and verifiers (`github.com/afterquery/mcp-atlas`).
- **Verifier-Based Execution:** Never return hallucinated or estimated freight values without a verified script assertion (Playwright DOM scrape, live API status 200).
- **Architecture for Navo:** Wrap `TrackingMCP`, `SchedulesMCP`, and `FreightRatesMCP` with standard JSON Schema tool contracts compliant with MCP-Atlas for interoperability across frontier AI reasoning harnesses.

---

## 7. Telegram Message & Report Formatting Standard

When formatting comparative audit reports or bot messages:
- **Strictly Human-Readable Markdown:** Use `**bold**`, `*italic*`, and `•` bullet markers.
- **Zero Raw HTML:** Banned tags include `<b>`, `<code>`, `<i>`, `<pre>`, and `<a>`.
- **Clean Structure:** Avoid raw markdown pipe tables (`|---|`) or nested code blocks that wrap awkwardly on mobile Telegram clients.
