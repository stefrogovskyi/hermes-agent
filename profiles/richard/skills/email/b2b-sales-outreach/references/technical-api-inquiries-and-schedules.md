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

## 6. Commercial Negotiation: Budget Matching & Unit Price Defense

### A. Proportional Volume Adjustment Rule
- When a prospect requests a lower annual budget (e.g. $1,200/yr vs proposed $2,400/yr for 1,000 req/mo), **do not discount the unit rate ($0.20/req)**.
- **Action**: Scale down monthly volume proportionally (e.g. offer **500 requests/month for $1,200/year**).
- **Benefits**:
  1. Matches client's exact approved budget.
  2. Defends core unit price ($0.20/call).
  3. Creates a natural upgrade trigger as usage grows.

### B. Offer Cleanliness
- Avoid bundling unrequested free products (e.g. free tracking) if it risks devaluing that product line or complicating contract terms. Focus strictly on closing the requested component.

---

## 7. Bilingual Communication Protocol for Team Review
When formulating technical replies for colleagues or team members (e.g. Stefan, Ekaterina):
1. Provide the **ready-to-send English email draft** (structured with subject, clear headings, JSON examples, and documentation links).
2. Always attach the complete **Russian translation** (`🇷🇺 Русский перевод черновика`) underneath to facilitate rapid internal review.
