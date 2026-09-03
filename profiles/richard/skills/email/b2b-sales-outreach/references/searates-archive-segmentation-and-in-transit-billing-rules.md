# SeaRates Archive Segmentation, Month-Boundary Billing & Clean Team Communication Standards

## 1. SeaRates Client Archive Database Segmentation (Multi-Rep Distribution)

When distributing legacy SeaRates client pools across multiple Account Executives (e.g. Nikita, Elena/Lena, Oleg, Alona):
- **Nikita Kurudzhy Active Pipeline**:
  * Source: `/opt/hermes/profiles/richard/searates_archive/parsed_leads.json` (parsed from `messages*.html` SeaRates Inbound MSG).
  * Range: First ~350 records (filtered into clean Batches 1 & 2, leads #1–#200). Over 60,000 clean leads remain available.
- **Available Fresh Bases for New Reps (Elena/Lena & Others)**:
  * In `/opt/hermes/profiles/richard/searates_archive/Requests SeaRates/`:
    1. `Requests - 2026.xlsx` (3,344 rows) — Highest priority, most recent active inquiries. Completely untouched by Nikita.
    2. `Requests - 2025.xlsx` (7,852 rows) — Large warm client pool from the preceding year.
    3. `Requests - 2024.xlsx` (3,540 rows) — Mid-term historical inquiries.
  * **Rule**: Keep rep source files strictly segregated to guarantee zero lead overlap or duplicate cold touches.

---

## 2. Commercial Month-Boundary Billing vs Lifecycle Counting (Eugene Karavan Standard)

When prospects evaluate how unique shipments are counted across calendar month boundaries:
- **Strict Calendar-Month Counting**:
  * Accounting period is strictly calendar month based (1st to last day of the month).
  * Unique shipments are calculated per calendar month for each successful shipment reference queried.
  * **Boundary Crossing**: If a shipment is queried on August 30 and queried again on September 1, it counts as 1 unique shipment in August and 1 unique shipment in September.
- **Product Separation (Tracking vs Schedules)**:
  * Container Tracking and Ocean Schedules API are billed separately.
  * Starter Tracking Plan: USD 50/month (or USD 500/year) for up to 25 unique shipments and 750 API calls/month.
  * Schedules API: Billed separately based on expected monthly API requests. Always qualify request volume before quoting.
- **API Call Allowance Consumption**:
  * Every API call consumes allowance upon invocation regardless of HTTP response state.
  * Automated background rechecks and incoming webhook pushes do NOT consume API calls.
  * Lookups consume API calls, but repeated lookups for the same container within the same calendar month do not add another unique shipment count.

---

## 3. Operational Milestone Status: In-Transit Logic

When clients question why a shipment enters `in_transit` before the vessel departs:
- Under Navo24 tracking logic, **any confirmed operational event moves the transport cycle into `in_transit` status**.
- Specifically, an actual `Gate-out` event from a terminal/depot indicates that pre-carriage/intermodal execution has commenced.
- Equipment milestones (gate moves) and vessel departures (ocean legs) remain distinct events within the DCSA timeline, while the top-level status confirms that transport execution is underway.

---

## 4. Internal Team Communication & User Output Standards (No Meta-Preamble Rule)

- **CRITICAL: Strict Zero Meta-Preamble**: When the user requests a message, text, or draft ("напиши коротко", "составь ответ клиенту"), NEVER output introductory meta-sentences that announce the topic or state the obvious (e.g. "Остались ровно два вопроса:", "Вот готовый текст:", "Ниже приведен ответ:"). Output the substantive content DIRECTLY on line 1.
- **Zero Emotional Labels**: In internal team updates, never use emotional adjectives or demographic labels (avoid "жесткий разбор", "индус", "злой клиент"). State purely technical, dry facts, container IDs, error codes, and explicit prospect questions.
- **Internal Escalation Structure**:
  ```text
  Всем привет! Лид снова прислал разбор после тестов. Прикрепил логи с таймстемпами. 
  Вопросы такие:
  [Clean bullet points with shipment IDs, exact behavior, and what the client asked]
  ```

---

## 5. Outreach Cadence & Domain Safety Rules

- **Follow-up Timing (Touch 2)**: Never send a follow-up email after only 24 hours. The optimal window for Touch 2 is strictly **2–3 business days** (e.g., sent Wednesday -> follow up Friday or Monday) to prevent spam complaints.
- **Daily Sending Safety Cap**: For sales reps on warm-up subdomains (e.g. `e.navo24.com`), cap sending at strictly **95–100 emails/day** per sender address. Never dispatch 200+ cold emails in a single day from a single account.
