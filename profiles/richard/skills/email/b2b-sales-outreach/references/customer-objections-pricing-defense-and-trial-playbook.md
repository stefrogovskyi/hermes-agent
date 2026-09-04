# Customer Objections, Pricing Defense & Trial Migration Playbook

This reference provides exact field-tested frameworks for handling key commercial and technical objections encountered during B2B sales cycles for Navo24 (Tracking, Schedules, Air Cargo, D&D).

---

## 1. Defending Price Against SeaRates & Low-Cost Aggregators

When a prospect states: *"Your prices are higher than SeaRates and older/newer competitors. Why?"*

### Core Value Pillars:
1. **Direct Connectors vs. Fragile Web Scraping**:
   - Legacy providers rely on HTML scraping of carrier web portals. When lines update UI, introduce CAPTCHAs, or throttle IPs, scraping breaks, causing silent tracking gaps (often 12–24+ hours stale).
   - Navo24 operates on **121+ direct carrier connectors and official DCSA-standardized feeds** across 234+ ocean lines with 0–5 minute data freshness.
2. **Truthful ETA & Smart Transshipment Suppression**:
   - Cheap aggregators routinely take the latest future timestamp in a feeder chain and publish intermediate transshipment hub arrivals (e.g. Caucedo) as the final destination ETA, corrupting the client's CRM/TMS.
   - Navo24 suppresses misleading intermediate dates when the final feeder leg lacks confirmed schedules.
3. **Integrated 4-Feed AIS & D&D Risk Engine**:
   - Competitors charge heavy enterprise add-on fees for vessel tracking and demurrage management.
   - Navo24 includes live 4-feed satellite/terrestrial AIS (110,000+ vessels) and automated Demurrage & Detention free-time monitoring against published line tariffs out of the box.
4. **Drop-in Compatibility (Compat Mode)**:
   - Zero-cost, zero-code migration: Navo24 provides a dedicated translation layer replicating the SeaRates API contract, allowing instant failover without rewriting client backends.

---

## 2. Full-Lifecycle Billing vs. Monthly Recurring Deductions

When a prospect argues: *"I have a budget of $1/container, and previously paid less per month"*:

### The Math:
* **Legacy Model (SeaRates / monthly recurring)**:
  - Billed per calendar month.
  - A shipment with a 45–60 day transit time (typical Asia → LatAm / Europe) consumes **2 to 3 monthly credits for that single container**.
  - An apparent $0.80/month rate actually costs the client **$1.60 – $2.40 per completed shipment**.
* **Navo24 (Full Lifecycle Pricing)**:
  - The client pays **strictly once per container** from Gate-In at origin all the way to Empty Return at destination (even if it takes 75 days).
  - No recurring monthly deductions, no per-call polling penalties.
  - Result: Lower Total Cost of Ownership (TCO).

---

## 3. Handling Trial Churn & Unreasonable Discount Requests (The 30% Trap)

When a trial client lists technical edge cases and demands an additional 30% discount before signing:

### Strategy:
1. **Do not concede base unit rates**: Conceding price during onboarding sets a toxic precedent where every edge case triggers discount demands.
2. **Diagnose before discounting**: In reality, 80%+ of "missing tracking" reports stem from:
   - Generic leasing prefixes (`FFAU`, `TLLU`, `TCLU`) undergoing a 20–88s discovery sweep.
   - Forwarder House Bills (HBLs) not issued by ocean carriers.
   - Carrier-side missing records (e.g., ZIM portal returning *"Oops... tracking information is not available"*).
   - Snapshot exports taken mid-flight while background workers are resolving.
3. **Risk Reversal Counter-Offer**:
   - Provide a **complimentary 2-week trial extension** to verify fixes.
   - Offer **Quarterly Billing** instead of upfront 12-month lock-in.
   - Offer a modest **10% onboarding discount for Q1 only**, resuming standard tier rates in Q2.
   - Offer **Monthly Billing until year-end**, locking in the agreed annual rate for the following year once performance is validated.

---

## 4. Bulk Upload & Reporting Workflow Expectations

Logistics operators do not treat bulk CSV/Excel uploads simply as an "add container" trigger; they treat it as an **operational sync and reporting tool**.

### Technical & UX Principles:
1. **Full Set Reporting**: The generated report must return **100% of uploaded rows** (e.g. 22 of 22), even if 14 were already tracked.
2. **Clear Row Status**: Distinguish rows clearly: `Newly added`, `Already tracked (included in report)`, `Invalid / No carrier record`.
3. **No "Skipped" Labels**: Never use the term "skipped" for active shipments—clients interpret it as "not monitored". Use `"Already tracked — active"`.
4. **Multi-Container Delimiters**: Ensure parser handles comma- or slash-separated containers in a single spreadsheet cell (`TCLU8633826, BMOU6978247`).
5. **On-Demand & Scheduled Re-exports**: Provide a saved working fleet list with a manual "Export All" button and automated weekly email delivery.

---

## 5. Explaining AIS vs. Carrier Fallback Fusion

When clients ask how Navo24 handles multi-layer data fusion:

* **Carrier EDI/DCSA Layer**: Authoritative for landside and terminal operations (`Gate-in`, `Loaded on vessel`, `Discharged`, `Gate-out`, `Empty Return`, and customs release).
* **AIS Telemetry Layer (Satellite + Terrestrial)**: Authoritative for open-ocean transit. Overrides carrier latency when carriers don't update for days; detects real-time berth and anchorage arrivals.
* **Truthful ETA Engine**: When a carrier's nominal schedule is physically broken (vessel delayed at intermediate port or reduced knots), predictive ETA calculates observed arrival based on live AIS kinematics and destination port congestion.

---

## 6. Real-World Objection Handling: ETA Accuracy & Transshipment Inconsistencies

### A. Answering "What is your percentage of ETA accuracy?"
* **The Pitfall**: Never claim a blind "99% accuracy" — ocean carriers themselves only achieve ~55–65% schedule reliability globally.
* **The Two-Tier Architecture Answer**:
  1. **Carrier Raw Schedule**: 100% faithful replication of carrier published milestones.
  2. **Navo Predictive ETA**: Achieves **88%–92% accuracy** within a 3–7 day arrival window by fusing 4 AIS feeds (110k+ vessels) with live port congestion statistics and vessel kinematics.
  3. **Truthful ETA Standard**: We suppress intermediate transshipment hub arrivals rather than falsely reporting them as destination arrival dates in the client's CRM.

### B. The "Vessel Departed but Container Discharged" Payload Anomaly
* **The Scenario**: The JSON response shows a map pin out at sea following a departed vessel, while the container was discharged days ago at an intermediate port (e.g. Rodman, Panama).
* **Root Cause**: The carrying vessel continued its rotation southward, while the container is dwelling at the terminal awaiting a feeder connection (`NOT_ON_BOARD`).
* **Sales Explanation**: Be transparent that the container is physically grounded in port waiting for on-carriage allocation, while map pin reconciliation pins the grounded container to the terminal rather than tracking the departed vessel.

---

## 7. Migration In-Flight Shipments & Quarterly Soft-Cap Billing

### A. Absorbing In-Flight Shipments from SeaRates
* When clients switch from SeaRates with 300+ active containers mid-transit and fear double billing:
  - Offer an immediate one-time **Migration Allowance / Bonus credits** (e.g. +350 free container slots) upon activating their plan so ongoing voyages are tracked at zero extra charge.
  - Temporarily grant 1,000 test credits for 48–72 hours so their legacy polling scripts can query the entire fleet uninterrupted during testing.

### B. Communicating Quarterly Billing without Hard Caps
* When splitting an annual volume (e.g. 5,000 shipments/yr) into quarterly invoices (1,250 shipments/quarter):
  - State clearly that the **entire 5,000 volume is available upfront with zero technical hard caps** to avoid operational disruptions during volume spikes.
  - The 1,250 number is strictly a **notional accounting milestone** aligned with quarterly invoicing.
  - Pacing: Next invoice is issued 2 weeks before quarter-end, or triggered early only if the notional milestone is consumed ahead of schedule.
