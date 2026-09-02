# Live Freight Rate Sources & Web Ingestion Playbook

## 1. Verified Public Freight Rate Sources (Zero Hallucination)

### A. Global Ocean Freight Indices (FBX - Freightos Baltic Index)
- **URL:** `https://fbx.freightos.com/`
- **Method:** Headless Chromium / Playwright (`page.goto('https://fbx.freightos.com/', wait_until='networkidle')`).
- **Data Extracted:**
  - `FBX 01`: China / East Asia to North America West Coast
  - `FBX 03`: China / East Asia to North America East Coast
  - `FBX 11`: China / East Asia to Northern Europe (e.g. $7,621 / 40HC)
  - `FBX 13`: China / East Asia to Mediterranean (e.g. $4,800 / 40HC)
- **Characteristics:** 100% public, updated daily, IOSCO-compliant benchmark reflecting actual market rates (including Cape of Good Hope rerouting, PSS, BAF).

### B. Shanghai & Ningbo Containerized Freight Indices (SCFI / NCFI)
- **URLs:** `https://www.chineseshipping.com.cn/`, `https://www.ncfi.com.cn/`
- **Method:** Lightweight HTTP GET via `aiohttp` / `requests`.
- **Data Extracted:** Base spot rates per TEU / FEU from Chinese ports to European base ports (Rotterdam, London, Antwerp, Hamburg).

### C. European Road Freight (Eurosender & ClickTrans)
- **URLs:** `https://www.eurosender.com/`, `https://clicktrans.com/`
- **Method:** Direct frontend calculation endpoints (by postal codes / city pairs).
- **Data Extracted:** FTL, LTL, and Van Express rates with transit times and distance breakdown.

---

## 2. Technical Scraping Protocols & Anti-Bot Bypasses

### SeaRates Logistics Explorer (`searates.com/logistics-explorer/`)
1. **Shadow DOM Structure:** The rate calculator is encapsulated within `#shadow-wrapper-le`.
2. **Accessing DOM:** Must access via `document.getElementById('shadow-wrapper-le').shadowRoot`.
3. **Triggering Query:** Parameterized URLs preload form values, but require triggering the search button: `shadowRoot.querySelector('button.ux0rsv').click()`.
4. **Session Limitation:** Unauthenticated guest queries hit `API_KEY_LIMIT_REACHED` on `/access/check` (1 query/day). To fetch live multi-carrier cards, provide a platform session token (`s-token`) in `localStorage`.

---

## 3. Grounding Rule for Navo Database Ingestion
- Never record estimated or synthetic freight rates into Navo databases.
- Every database write must be backed by an executed network payload, verified HTTP status code, timestamp, and source URL.
