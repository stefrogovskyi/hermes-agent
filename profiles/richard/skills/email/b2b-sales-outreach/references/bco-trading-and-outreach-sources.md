# BCO, Commodity Trading & Multi-Source Outreach Architecture

## 1. Target Audience Priority: High-Volume BCOs & Trading Houses

In addition to freight forwarders, high-margin enterprise prospects for Navo24 data components (TrackingMCP, SchedulesMCP, LoadingMCP, FreightRatesMCP) are **Beneficial Cargo Owners (BCOs)**, **Global Commodity Traders**, **Import/Export Houses**, and **Industrial Manufacturers** that manage and ship hundreds or thousands of containers independently.

### Key Target Sectors:
- **Agribusiness & Food Commodity Trading:** Bunge, ADM, Louis Dreyfus, Olam Group, Wilmar, Danone, Nestlé.
- **Chemicals & Plastics Exporters:** BASF, Dow Chemical, LyondellBasell, Sabic.
- **Metals, Mining & Energy Traders:** Trafigura, Glencore, Vitol, Gunvor, ArcelorMittal, Tata Steel.
- **Consumer Goods, Electronics & Retail Importers:** Large BCOs identified via US Customs Sea Manifests (ImportYeti / Volza).

### Target Decision-Maker Titles:
- `Head of Global Logistics` / `Director of Logistics`
- `VP Supply Chain` / `Director of Supply Chain`
- `Director of International Trade` / `Head of Global Trade`
- `Import / Export Director` / `Customs & Compliance Director`
- `Commercial General Manager`

---

## 2. 17-Source Outreach Directory Matrix

| Source Platform | Type | Primary Entity Scraped | Connection Method |
|---|---|---|---|
| **Digital Freight Alliance (DFA)** | Forwarder Alliance | 2,954 Verified global forwarders | File (`dfa_members.xlsx`) |
| **Hunter.io Enterprise** | B2B Domain Intelligence | BCO & Trading enterprise executives | API (`HUNTER_API_KEY`) |
| **Apollo.io Logistics & Trade** | B2B Directory & Intent | Trading houses (50+ employees) | API (`APOLLO_API_KEY`) |
| **Prospeo.io / Clay / Lusha** | Email Enrichment | Multi-modal logistics & trade executives | API |
| **ImportYeti** | US Customs Sea Manifests | Real BCO ocean importers by volume | Playwright Headless Chrome |
| **Volza** | Customs & Trade Intelligence | Global import/export companies | Session Cookies / Playwright |
| **CIFFA Directory** | Forwarders & Trade | Canadian logistics & customs brokers | REST / Scraper |
| **ThomasNet** | Industrial Directory | US manufacturers & equipment exporters | BeautifulSoup Scraper |
| **WCA World / JCtrans** | Freight Networks | Global independent forwarders & NVOCCs | Scraper |

---

## 3. Strict Pre-Send DNS & MX Validation Policy

To guarantee 100% genuine data and zero synthetic / dead domains:
1. **MX Record Verification:** Query DNS MX records on port 25 before saving to CRM or queuing emails (`validator.py`).
2. **Hard Deletion of Non-Existent Domains:** Immediately remove any unresolvable domain from the pipeline.
3. **Database Segregation:** Cold outreach leads live strictly in `Online Outreach` (`appdJR8VVczRxcVke` -> `Outreach Leads`). Qualified inbound replies move to `Navo CRM` (`appbxvl9BBaTiLMlf` -> `Leads`).
