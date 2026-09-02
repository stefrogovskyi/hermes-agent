# SeaRates Logistics Explorer v3 API Standard & Multi-Modal Freight Rate Schema

## Rate Schema Reference (FCL, LCL, Road, Rail, Air)

### Core Response Fields
- `transportType`: `fcl` | `lcl` | `road` | `rail` | `air`
- `carrier`:
  - `name`: Carrier brand name (e.g., `MSC`, `CMA CGM`, `Turkish Cargo`)
  - `scac` / `iata`: Standard 4-letter SCAC or 2-letter IATA code
  - `code`: System alias
- `routing`:
  - `origin`: `{ name, unlocode, country }`
  - `destination`: `{ name, unlocode, country }`
  - `transitTimeDays`: Transit duration in integer days
  - `etd` / `eta`: Standard ISO 8601 date strings (`YYYY-MM-DD`)
  - `vessel` / `voyage` / `flightNumber`: Specific transport asset identification
- `pricing`:
  - `totalAllIn`: Total all-inclusive spot amount
  - `currency`: ISO currency code (`USD`, `EUR`)
  - `breakdown`: Array of charge items (`BAS`, `BAF`, `THC`, `ISPS`, `LSS`, `Tolls`, `Screening`)
  - `validity`: `{ from: "YYYY-MM-DD", to: "YYYY-MM-DD" }`
- `terms`: Standard Incoterms / ocean delivery terms (`CY/CY`, `CFS/CFS`, `Door-to-Door`, `Airport-to-Airport`)

### Navo Enhancements
- `reliabilityScore`: On-time arrival percentage based on historical AIS port calls (e.g., `94.5%`).
- `freeDays`: `{ origin: N, destination: N }` for demurrage & detention risk mitigation.
- `co2EmissionsKg`: Standardized carbon footprint calculation under GLEC Framework v3.
