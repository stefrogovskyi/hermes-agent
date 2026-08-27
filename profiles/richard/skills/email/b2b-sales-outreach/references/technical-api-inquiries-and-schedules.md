# Technical API Inquiries: Tracking & Vessel Schedules Architecture

Guidelines for answering prospective clients and technical evaluators regarding Navo24 REST API capabilities, error handling, billing logic, and comparison with legacy platforms (SeaRates).

---

## 1. Tracking API Reference Validation & Billing Architecture

### A. Identifier Types & Auto-Resolution
- **Container Numbers (`container_id`)**: Auto-resolved across 234 carriers via standard BIC prefixes (e.g. `MSKU`, `COSU`, `MEDU`) with ISO 6346 check digit validation. No SCAC hint required.
- **Master Bills of Lading (`bill_of_lading`)**: Resolved automatically when following carrier master formats, or when paired with an optional `carrier_code` (SCAC) hint.
- **House Bills of Lading (HBL)**: Forwarder internal job numbers (e.g., `BMIIST26-88608`, `DEN/26/0182-D`) are not indexed by ocean carriers. If submitted without the Master BL or container number, the system answers `404 REFERENCE_NOT_RESOLVABLE`.

### B. Error Envelopes & Quota Protection
- Unrecognized or invalid references return `404 REFERENCE_NOT_RESOLVABLE` (or `400 VALIDATION_ERROR` for malformed payloads).
- **Billing Rule**: Container quotas and API credits are **ONLY consumed upon successful shipment registration into active tracking**. Failed, invalid, or unresolvable lookups incur **zero charges** and do not deduct from free-tier or paid quotas.

---

## 2. Request Structure & SeaRates Migration

### A. Single vs. Batch Lookups
- **Registration**: 1 reference per API call (`POST /v1/containers`).
- **Portfolio Retrieval**: Query the entire active fleet via `GET /v1/containers` with filters and pagination.
- **Real-Time Push**: Webhooks (`POST /v1/webhooks`) push event payloads on milestone changes, discharge, and predictive ETA movements, removing the need for batch polling workers.

### B. Drop-In SeaRates Compatibility
- Navo provides a native compatibility endpoint: `GET https://api.trackingmcp.com/compat/searates/tracking?api_key=tmcp_KEY&number=...&type=BL`.
- Outputs the exact SeaRates JSON envelope while utilizing Navo's 234-carrier connector engine and multi-source AIS redundancy.

---

## 3. Vessel & Ship Schedules REST API (SchedulesMCP)

### A. Protocol Support
Every Navo component is dual-protocol: **MCP-native** for LLM agents and **HTTPS RESTful JSON** for legacy TMS/CRM integrations.

### B. Vessel-First Architecture
Schedules are grouped around the physical hull rather than duplicating identical sailings for every slot-sharing carrier.

### C. Key Endpoints & Returned Data Fields
- `GET /public/schedules/cards?origin=UNLOCODE&destination=UNLOCODE` (Vessel-first cards)
  - **Vessel Data**: Name, IMO number, build year, flag, dimensions, and live AIS coordinates (`lat`, `lng`, `speed_knots`, navigation status).
  - **Timelines**: Published ETD/ETA, schedule revision history, and **Predictive ETA / Delay hours** from observed historical delays.
  - **Routing & Transshipment**: `is_transshipment`, `transship_via`, `leg_count`, intermediate port rotations.
  - **Slot Partners & Alliances**: Partner list with SCACs, service names, and specific CY/DOC/VGM cut-off deadlines.
- `GET /public/reliability/lanes?origin=UNLOCODE&destination=UNLOCODE`
  - On-time arrival percentage and average delay hours per carrier on the specific corridor.
- `GET /public/ports/search?name=port_name`
  - UN/LOCODE resolver (e.g. `rotterdam` -> `NLRTM`).

---

## 4. Bilingual Communication Protocol for Team Review
When formulating technical replies for colleagues or team members (e.g. Stefan, Ekaterina):
1. Provide the **ready-to-send English email draft** (structured with subject, clear headings, JSON examples, and documentation links).
2. Always attach the complete **Russian translation** (`🇷🇺 Русский перевод черновика`) underneath to facilitate rapid internal review.
