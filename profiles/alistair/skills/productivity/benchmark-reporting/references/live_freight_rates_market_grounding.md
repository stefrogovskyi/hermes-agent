# Live Freight Rates Market Grounding & Web Architecture

## 1. Asia ➔ Europe Spot Freight Reality (Post-Crisis Routing)
- **Rerouting via Cape of Good Hope:** Due to Red Sea / Bab al-Mandab security crisis, vessels detour around Africa (+3,500 nm, +10–14 days transit, 38–48 total days).
- **Rate Breakdown (40ft High Cube / 40HC):**
  - All-in Spot Market Corridor: **$6,000 – $8,500 / 40HC**.
  - Components: Base Ocean Freight (BAS: $2,800–$3,500) + Peak Season Surcharge (PSS: $1,500–$2,200) + Emergency Operations Surcharge (EOS/ERR: $1,200–$1,800) + EU ETS Carbon & BAF.
- **Sanity Check:** Reject any pre-crisis static benchmarks of $2,000–$2,500 for Asia-North Europe.

## 2. SeaRates Logistics Explorer Web Parser Architecture
- **Shadow DOM:** Root rendered in `<div id="shadow-wrapper-le">` with open shadow root.
- **Search Trigger:** Clicking search button `shadowRoot.querySelector('button.ux0rsv')`.
- **Session Tokens & Quotas:** Guest calls hit `API_KEY_LIMIT_REACHED` on `/access/check`. Production integrations require acquiring `s-token` via `/auth/platform-token` or parsing Freightos FBX / iContainers / Freight-Calculator directly.
