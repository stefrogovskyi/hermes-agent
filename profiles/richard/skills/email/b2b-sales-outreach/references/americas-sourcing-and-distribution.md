# Americas Regional Sourcing & Lead Distribution Playbook

## 1. Verified Sources for North & South America

| Source | Region / Countries | Extraction Method | Entity Types |
|---|---|---|---|
| **DFA Americas** | US, CA, BR, AR, CL, CO, MX, PE, TT | `dfa_members.xlsx` (filtered by Continent/ISO) | Ocean Freight Forwarders, NVOCCs |
| **CIFFA** | Canada (CA) | `ciffa_scraper.py` / Member Directory | Canadian Freight & Trade Shippers |
| **Freightnet Directory** | US, MX, CA | `freightnet_scraper.py` | US Port Forwarders & Customs Brokers |
| **ThomasNet** | United States (US) | Industrial Importer Registry & Hunter/Snov | BCO Industrial Manufacturers & Importers |
| **Hunter.io B2B** | US, CA, BR, MX | Domain Search (`cargill.com`, `alcoa.com`, etc.) | Commodity Trading Houses & Corporate Giants |
| **Snov.io B2B** | United States (US) | Domain Search (`hubgroup.com`, `expeditors.com`) | US Transport & 3PL Logistics Leaders |

## 2. Strict Lead Distribution Rules

1. **Even Multi-Source Split**: When tasked with $N$ leads per source, extract $N$ from **Source 1**, $N$ from **Source 2**, etc., guaranteeing distinct companies for every slot.
2. **Explicit Country Tagging**: Always map ISO codes to full country names (`US` -> `United States`, `CA` -> `Canada`, `BR` -> `Brazil`, `AR` -> `Argentina`, `CL` -> `Chile`, `MX` -> `Mexico`).
3. **No "Global" Fallback on Regional Runs**: If a regional batch is requested, every single contact must have an explicit country belonging to that region.
4. **Full 5-Product Representation**: Ensure email templates present Tracking, Schedules, FreightRates, AirTracking, and Loading 3D.
