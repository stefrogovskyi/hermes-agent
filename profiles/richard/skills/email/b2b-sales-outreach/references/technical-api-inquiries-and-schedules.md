# Technical API Inquiries: Tracking & Vessel Schedules Architecture

Guidelines for answering prospective clients and technical evaluators regarding Navo24 REST API capabilities, error handling, billing logic, and comparison with legacy platforms (SeaRates).

---

## 1. Tracking API Reference Validation & Billing Architecture

### A. Identifier Types & Auto-Resolution
- **Container Numbers (`container_id`)**: Auto-resolved across 239 carriers via standard BIC prefixes (e.g. `MSKU`, `COSU`, `MEDU`) with ISO 6346 check digit validation. No SCAC hint required.
- **Master Bills of Lading (`bill_of_lading`)**: Resolved automatically when following carrier master formats (e.g. 9-digit Maersk, 12-digit Evergreen `1496*`, `SHZ*` CMA CGM/CNC, `MEDU*` MSC, `HLCU*` Hapag-Lloyd), split-bill suffixes (`A`/`B`), or when paired with an optional `carrier_code` (SCAC) hint.
- **House Bills of Lading (HBL) & Non-BL Invoices**: Forwarder internal invoice numbers (e.g. `7555823083`, `BMIIST26-88608`) are not ocean carrier identifiers. If submitted without Master BL or container number, the system returns `404 REFERENCE_NOT_RESOLVABLE` or `AUTO_CANT_DETECT_SEALINE`.

### B. Error Envelopes & Quota Protection
- Unrecognized, invalid, or background-polling requests incur **zero quota deduction**.
- **Billing Rule**: Billed strictly per **unique tracked shipment per calendar month**. Querying the same reference 30 times in a month consumes exactly 1 shipment unit. Failed calls (4xx/5xx) never deduct quota.

---

## 2. Request Structure & SeaRates Migration

### A. Registration vs. Polling vs. Webhooks
- **Compatibility Endpoint (SeaRates Format)**:
  - **1 Single Call**: `GET /compat/searates/tracking?number=...&api_key=...`. Auto-registers and returns full payload directly.
- **Native API (`/v1/containers`)**:
  - **Direct POST (1 call)**: `POST /v1/containers` registers and returns resolved payload immediately.
  - **Polling (2 calls)**: `POST /v1/containers` returns `202 Accepted` + `id`; query `GET /v1/containers/{id}` for updates.
  - **Webhooks (Recommended - 0 polling)**: Register via POST, receive real-time push events on status/ETA changes.

### B. SeaRates Parity Parameters & Telemetry
- **Synchronous Execution**: Append `?wait=30` (or desired seconds) to hold connection until data resolves, avoiding polling loops.
- **Port Local Time vs UTC**: Pass `?dates=local` for port local timestamps (for Letter of Credit compliance), or default UTC.
- **Real-Time Quota Telemetry**: Delivered via HTTP headers on all requests (including trial keys):
  - `X-Usage-Used`, `X-Usage-Remaining`, `X-Usage-Limit`.
- **Field Additions**: `sealine_full_name` (e.g. "Mediterranean Shipping Company") alongside `sealine_name` ("MSC").

---

## 3. Georoute Construction, AIS Reconciliation & LOCODEs

### A. Real-World Routing vs Legacy Schedules
- During diversions (e.g. Cape of Good Hope around Africa vs static Suez Canal schedules), live AIS positions reflect true vessel coordinates.
- **New Validation Flags in Payload**:
  - `pin_reconciled` (`boolean`): `true` when vessel coordinate aligns with served route geometry.
  - `pin_route_distance_km` (`number`): Perpendicular distance in km between vessel pin and nearest route segment (allows client-side threshold filtering).

### B. LOCODE Canonicalization
- Carrier alias variants (e.g. `CNNBO` -> `CNNGB`, `MAPTG` -> `MAPTM`, `SGSNG` -> `SGSIN`) are mapped to canonical UN/LOCODEs, eliminating duplicate intra-port loops and ensuring feeder legs stay bounded within their corridor.

---

## 4. ETA Calculation Methodology & Line Discrepancies

### A. Dual ETA Exposure in `pod`
When carrier website and API differ, both are exposed:
- `carrier_eta`: Raw date published by the carrier API/EDI feed.
- `predictive_eta`: AI/AIS-calculated forecast factoring vessel speed over ground, transit hub congestion, and real routing.

### B. Explaining Web vs API Discrepancies to Clients
- Carrier public websites frequently cache optimistic/static schedules.
- Backend carrier APIs and AIS telemetry already account for transshipment delays and speed adjustments. The later date supported by satellite AIS is objectively closer to reality.

---

## 5. Vessel & Ship Schedules REST API (SchedulesMCP)

### A. Key Endpoints
- `GET /public/schedules/cards?origin=UNLOCODE&destination=UNLOCODE` (Vessel-first grouping with `partners` array, IMO, AIS, cut-offs, `transship_via`).
- `GET /public/schedules` (Flat list per carrier).
- `GET /public/reliability/lanes` (Historical on-time % and average delay).
- OpenAPI Spec: `https://schedulesmcp.com/openapi.json`.

### B. Current Capabilities & Limitations
- **Horizon**: Delivers all published sailings for 4–8+ weeks ahead in 1 call.
- **Client-Side Filtering**: Date ranges (`date_from`/`date_to`) and carrier filters are currently applied client-side from the complete forward payload.

---

## 6. Commercial Negotiation: Budget Matching, Levers & Objection Handling

### A. Proportional Volume Adjustment Rule
- When a prospect requests a lower annual budget (e.g. $1,200/yr vs proposed $2,400/yr for 1,000 req/mo), **do not discount the unit rate ($0.20/req)**.
- **Action**: Scale down monthly volume proportionally (e.g. offer **500 requests/month for $1,200/year**).
- **Benefits**:
  1. Matches client's exact approved budget.
  2. Defends core unit price ($0.20/call).
  3. Creates a natural upgrade trigger as usage grows.

### B. Offer Cleanliness
- Avoid bundling unrequested free products (e.g. free tracking) if it risks devaluing that product line or complicating contract terms. Focus strictly on closing the requested component.

### C. Startup Flexibility Bluff (Competitor Leverage & Non-Expiring Top-Up Wallet)
- **The Bluff**: Early-stage startups claim a regional competitor (e.g. Shipsgo in Turkey) offers "flexible per-shipment terms without commitment" and ask for post-paid per-shipment billing without deposits.
- **Tactical Response**:
  1. **Call the Competitor Calmly**: Acknowledge the regional competitor by name without fear ("Shipsgo is well known, but our enterprise data infrastructure and direct carrier connectors are built for production reliability").
  2. **Refuse Uncommitted Post-Paid Billing**: Protect engineering and infrastructure margins.
  3. **Present a Decisive 2-Option Fork**:
     - *Option A (Starter Subscription)*: 3-month commitment (e.g. 300 shipments/mo at $1.30 = $390/mo).
     - *Option B (Prepaid Flex / Top-Up Wallet)*: Upfront deposit of **$500** with **zero monthly expiration**. Deduct at a higher unit rate (**$1.40/shipment**). Next payment is required ONLY when the $500 balance is exhausted.

### D. Stepped Growth Incentive Model (Legacy SeaRates $0.80 Anchoring)
- **Scenario**: Mid-volume clients (e.g. 380 shipments/mo) demand legacy SeaRates pricing of **$0.80/container**, which normally opens at 1,000+ monthly shipments.
- **Counter-Strategy**:
  - Do NOT collapse the baseline contract to $0.80.
  - Offer a **Two-Tier Growth Structure**:
    1. *Baseline Package (up to 380/mo)*: Preferential base rate of **$1.10/shipment** ($5,000/year instead of $6,800).
    2. *Expansion Tier (all volume > 380/mo)*: Exactly **$0.80/shipment** for all growth volume.
  - Protects baseline ARR while unlocking the client's target unit economics for their expansion.

### E. Enterprise Capital-Efficiency Positioning (e.g. VesselFinder, MarineTraffic)
- **Scenario**: High-volume maritime data platforms previously paid large multi-year lump sums on SeaRates (e.g. $20,000 prepaid for 25,000 containers over 18 months at $0.80/container).
- **Counter-Strategy**:
  - Match their historical **$0.80/container** rate.
  - Frame Navo24 as **significantly more agile and capital-efficient**: offer a 12-month contract with a fraction of the upfront capital lock (e.g. **$4,000 for 5,000 shipments** or **$2,000 for 2,500 shipments** at $0.80 with fixed $0.80 overage).

---

## 7. Advanced Technical API Resolution & Milestone Precedence

### A. Same-Day Event Chronology & `order_id` (Date Only, No Time)
- When carriers report milestone dates without timestamps (`YYYY-MM-DD 00:00:00`), Navo24 enforces deterministic DCSA lifecycle precedence in the sequencing engine:
  - **Origin / POL**: `Gate In / Vanning` -> `Loaded on Vessel (LOAD)` -> `Vessel Departure (DEPT)`.
  - **Destination / POD**: `Vessel Arrival (ARRV)` -> `Discharged (DISC)` -> `Gate Out` -> `Empty Container Returned`.
- Guarantee to client: `order_id` strictly sorts Arrival before Discharge, and Loading before Departure, provided the carrier did not misreport the calendar dates.

### B. Leased Equipment Prefix Auto-Resolution (`RFSU`, `BEAU`, `SEGU`)
- Leased boxes belong to leasing companies (e.g. Beacon Intermodal, Triton), where equipment owner != operating ocean line.
- In multi-carrier cascade routing, ensure leased prefix resolvers probe dedicated line connectors (e.g. OOCL `OOLU`, Emirates `ESPU`) rather than timing out at parent alliance holding groups (e.g. COSCO).

### C. Carrier Parameter Parity in Compatibility Endpoint
- Legacy SeaRates query parameter was `sealine` (e.g. `&sealine=WHLC`), whereas some documentation examples show `carrier`.
- Ensure query resolvers accept both `sealine` and `carrier` as exact aliases and confirm to clients that both parameters resolve properly.

### D. ERP Gap Bridging & Web Access Positioning (e.g. Conexos, CargoWise)
- When a prospect lacks direct native integration with their local ERP (e.g. Conexos in Brazil):
  1. Confirm active ongoing negotiations/discussions with the ERP provider for native integration.
  2. Detail practical Web Access workflow (individual/batch CSV upload, unified status dashboard, interactive satellite AIS map, exportable reports).
  3. Close with a 15–20 minute live walkthrough demo invitation.

---

## 8. Bilingual Communication Protocol for Team Review
When formulating technical replies for colleagues or team members (e.g. Stefan, Ekaterina):
1. Provide the **ready-to-send English email draft** (structured with subject, clear headings, JSON examples, and documentation links).
2. Always attach the complete **Russian translation** (`🇷🇺 Русский перевод черновика`) underneath to facilitate rapid internal review.
