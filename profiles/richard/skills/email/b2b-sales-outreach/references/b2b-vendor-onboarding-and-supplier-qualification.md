# B2B Vendor Onboarding & Supplier Qualification Records

This reference guides the completion of enterprise client procurement documents, including **New Vendor Setup Forms** (Excel) and **Supplier Qualification Records / Vendor Questionnaires** (PDF/DOCX) for **Wemelogistics Ltd (trading as navo24)**.

---

## 1. Official Corporate & Legal Entity Data

* **Legal Entity Name:** Wemelogistics Ltd (trading as navo24)
* **Company Registration Number:** `14081751` (Registered in England & Wales at Companies House)
* **Date of Incorporation / Establishment:** `03 May 2022` (`03/05/2022`)
* **Registered Office & Operating Address:**
  * Address Line 1: `1 Robin Hood House`
  * Address Line 2: `Kingston Vale`
  * City / Postcode: `London SW15 3AL`
  * Country: `United Kingdom`
* **Nature of Business / SIC:** 
  * `62012 - Business and domestic software development`
  * `50200 - Sea and coastal freight water transport`
  * `52290 - Other transportation support activities`
* **Supplier Type / Classification:** `Service Provider` / `Non-Trade` (Software, API, MCP, and Digital Logistics Intelligence). NOT Manufacturer, Trader, or Physical Goods Distributor.
* **Product Brand:** Navo24 (`TrackingMCP`, `SchedulesMCP`, `LoadingMCP`, `FreightRatesMCP`, `AirCargoMCP`)
* **Website:** `https://navo24.com` (Developer Portal: `https://navo24.com/developers/`)

---

## 2. Executive Leadership & Key Contacts

* **Chief Executive / Director:** Oleksii Shatunov (Director & Co-founder)
* **Managing Director:** Stefan Rogovskiy (Co-founder & MD) — `stefan@navo24.com`, `+44 7554 565992`
* **Senior Sales & Account Representatives:** 
  * Richard Marlowe (Senior B2B Sales Manager) — `rich@navo24.com`, `+44 7360 065904`
  * Liliia Kuba (Account Representative) — `lilia.k@navo24.com`
  * Nikita Kurudzhy (Account Executive) — `nikita@navo24.com`, `+380932285150`
* **Finance & Accounts Contact:** 
  * Name: Stefan Rogovskiy (Director / Finance)
  * Email: `billing@navo24.com`
  * Telephone / Mobile: `+44 7554 565992`

---

## 3. Tax, Financial & Operational Terms

* **Tax ID / Company Number:** `14081751`
* **VAT / GST:** 
  * Not registered for VAT/GST in local overseas buyer jurisdictions (e.g. Malaysia, Singapore, US). Mark as `N/A (Overseas UK Supplier / Non-resident)`.
  * UK VAT: Unset / Not currently VAT registered.
* **Payment / Credit Terms:** `Net 14` (standard) or `Net 30` (enterprise agreement).
* **Billing Currency:** `USD` (primary international), `EUR`, `GBP`, `AED`.
* **HS / Tariff Code:** `N/A` (Digital services / cloud software).
* **Delivery Lead Time:** `Immediate` (Cloud SaaS provisioning, API key issuance within minutes of onboarding).
* **Paid-Up Capital:** `GBP 10,000` (or `GBP 10.00` nominal capital as per Companies House initial filing).
* **Turnover:** Commercial in confidence or `USD 500,000+`.
* **Market Share / Capacity:**
  * Manufacturing / Physical Capacity: `N/A` (Software / Cloud scalable architecture).
  * Malaysia / Regional Market Share: `N/A` (Global cloud service provider).
* **Target / Major Customers:** Global freight forwarders, shipping lines, BCOs, commodity traders, and multinational manufacturers.

---

## 4. Multi-Currency Banking Details (Revolut & HSBC UK)

Revolut is the primary multi-currency receiving bank for international wire transfers:

* **Bank Name:** Revolut
* **Account Name:** `Wemelogistics Ltd`
* **Company Reg No.:** `14081751`
* **IBAN:** `GB97 REVO 2301 6390 1552 22`
* **SWIFT / BIC:** `REVOGB21`
* **Intermediary BICs (Correspondent Banks for SWIFT):**
  * **USD:** `CHASGB2L` (JPMorgan Chase Bank N.A., London)
  * **EUR:** `CHASDEFX` (J.P. Morgan SE, Frankfurt)
  * **GBP (Faster Payments):** Sort Code `23-01-63`, Account No. `90155222`
  * **AED:** `BARCGB22` (Barclays Bank PLC)
* **Secondary / Alternative UK Bank (HSBC UK):**
  * Bank: HSBC UK
  * Sort Code: `40-05-20` | Account No.: `42304546`
  * IBAN: `GB44 HBUK 4005 2042 3045 46` | SWIFT: `HBUKGB4B`

---

## 5. Compliance, Standards & Certifications for SaaS / IT Vendors

When forms list industrial/manufacturing certifications (ISO 9001, ISO 14001, DOE, DOSH, SAMM, etc.):
* Mark physical manufacturing standards as **`No`**.
* In **"Others" / Additional Standards**, enter:
  `UK GDPR Compliant / DCSA Aligned / SOC 2 Type II Aligned / Cloud Security Standards`
* **Social Accountability Compliance:** Mark **`Yes`** (strict compliance with UK Modern Slavery Act, labor standards, and anti-bribery policies).

---

## 6. Technical Execution: Form Filling Best Practices

### A. Excel Forms (`.xlsx`)
Use `openpyxl`:
```python
import openpyxl
from openpyxl.styles import Alignment, Border, Font, Side

wb = openpyxl.load_workbook(input_path)
ws = wb.active

font_navy = Font(name='Arial', size=9, bold=True, color='0C2A5E')
align_left = Alignment(horizontal='left', vertical='center')
thin_border = Border(
    top=Side(style='thin'),
    bottom=Side(style='thin'),
    left=Side(style='thin'),
    right=Side(style='thin'),
)

# Populate cells preserving layout
ws['C5'] = 'Wemelogistics Ltd (trading as navo24)'
ws['C5'].font = font_navy
ws['C5'].alignment = align_left
ws['C5'].border = thin_border
wb.save(output_path)
```

### B. Static PDFs (No Interactive AcroForm Fields)
Use `pymupdf` (`fitz`):
1. Locate underlying table lines or coordinate bounding boxes via `page.get_drawings()`.
2. Overlay text at baseline coordinates using `page.insert_text(fitz.Point(x, y), text, fontsize=size, color=NAVY)`.
3. For multiple-choice selections (`Yes / No`), draw neat vector ovals around the desired choice using `page.draw_oval(fitz.Rect(x0, y0, x1, y1), color=NAVY, width=1.2)`.
4. Leave internal buyer evaluation sections (e.g. Page 2 "Qualification Assessments of New Supplier", "Evaluation done by Purchaser, R&D, QA, CFO approval") blank.
