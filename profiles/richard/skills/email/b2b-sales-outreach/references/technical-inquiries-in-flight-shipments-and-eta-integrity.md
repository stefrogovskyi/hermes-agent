# Technical Inquiry & Objection Playbook: In-Flight Shipments, ETA Integrity & Full Lifecycle vs Legacy Models

This reference captures real field patterns, objections, edge cases, and technical resolutions encountered when transitioning enterprise logistics clients from legacy providers (like SeaRates) to Navo24.

---

## 1. Full Lifecycle Pricing vs Legacy Monthly Recurring Billing (The Math)

### Client Objection:
*"Your price is higher than SeaRates ($1.00 vs $0.80/container). We need a lower rate."*

### Field Argument & Breakdown:
* **The Legacy Trap (SeaRates):** Billed on a *per-calendar-month* basis. If a shipment is in transit across typical long-haul trade lanes (e.g. Asia → Latin America / Europe, taking 45–65 days), SeaRates consumes **2 to 3 monthly credits for that single container**. An apparent $0.80/month rate actually ends up costing **$1.60 – $2.40 per completed shipment**.
* **Navo24 Full Lifecycle Model:** The client pays **strictly once per unique container** from initial Gate-in / Empty Pickup all the way to final Empty Return at destination, whether the journey takes 15 days or 75 days. Zero recurring monthly deductions, zero re-polling penalties.
* **Result:** In real operational TCO (Total Cost of Ownership), Navo24's unit price is significantly lower per completed shipment.

---

## 2. In-Flight Shipments & Migration Allowances (Grandfathering)

### Client Objection / Blocker:
*"We already track 300+ containers through SeaRates that are mid-transit. If we switch to Navo, our script will re-query all 300 and we will be double-charged on day one."*

### Field Resolution:
1. **Migration Bonus (Grandfathering):** Offer a one-time complimentary credit allowance (e.g., +350 free container tracking credits upon activation) to absorb all active in-flight containers without double-charging.
2. **Re-polling Safety:** Reassure the client that in Navo24, once a container is registered, re-polling it across its lifecycle does not consume additional container credits.
3. **Temporary Test Cushion:** Provide a temporary credit buffer (e.g., 1,000 credits for 72 hours) during sandbox testing so batch polling scripts (e.g., querying 300 boxes in a single loop) do not trip low-balance exceptions.

---

## 3. Truthful ETA Principle & Transshipment Suppression

### Client Bug Report:
*"Your ETA field returns a date weeks too early (e.g. 7 September instead of late October) because it takes the intermediate transshipment hub arrival."*

### Technical Context & Architecture:
* **Carrier Payload Reality:** Carriers (such as COSCO on Caribbean feeders or MSC at transshipment hubs like Caucedo or Rodman) often publish the final feeder leg as an empty shell (`vsl None | dep None | arr None`, `destination_unlocode = NULL`).
* **The Flawed Fallback:** Naive algorithms take the latest future arrival estimate anywhere on the route (the transshipment hub) and publish it as the shipment ETA, corrupting downstream CRMs.
* **Navo24 Solution (Truthful ETA):** 
  - Suppress intermediate hub arrival dates when the final leg lacks confirmed carrier dates.
  - Return `null` / empty rather than a misleading date (*"No ETA rather than a wrong ETA"*).
  - Inject the future arrival date once the carrier allocates the feeder schedule, publishing it both to root `eta` and as an `estimated_arrival` event in the `events` array.

---

## 4. Bulk Uploads & Consolidated Report Composition

### Client Frustration:
*"When I upload 22 containers and 14 are already tracked, the report only gives me 8 rows. We use this file for our daily/weekly sync and need all 22 rows every time!"*

### Workflow Expectation:
* Clients use bulk upload not just to add new shipments, but as a **recurring batch reporting tool**.
* **Fix:** The export must return **100% of submitted references in the file** (e.g., 22 out of 22), with an explicit status column: `newly added`, `already tracked`, or `invalid`.
* **Terminology:** Never use "skipped" (clients read it as "you ignored my shipment"). Use *"already tracked — included in report"*.
* **Multi-Container Delimiters:** Ensure parsers handle and split cells containing multiple container numbers separated by commas (e.g. `TCLU8633826, BMOU6978247`).

---

## 5. Stale Carrier Cache vs AIS Pin Misalignment

### Anomaly / Client Inquiry:
*"The container was discharged at Rodman on 30 August, but the map pin is in the ocean near Ecuador, and the status says IN_TRANSIT."*

### Root Cause:
* The mother vessel (`MSC JUDITH`) discharged the container and departed, continuing its rotation southward.
* The AIS feed follows the vessel coordinates, while the container is grounded at the transshipment terminal awaiting connection (`status: NOT_ON_BOARD`).
* If the carrier's onward feeder leg (`MSC DARIEN`) hasn't updated in the cached feed, the map pin can erroneously follow the departed vessel.
* **Resolution:** Reconcile map pins for grounded containers to the terminal location (`lat/lng` of the discharge port), and trigger a manual carrier re-poll / cache bypass to ingest the onward transshipment events.

---

## 6. Transient Statuses: `AUTO_CANT_FIND_INFO` & Discovery Sweeps

### Client Question:
*"We received `AUTO_CANT_FIND_INFO` on fresh MSC/CMA CGM bills. Does this mean the system failed?"*

### Explanation:
* `AUTO_CANT_FIND_INFO` is a **transient in-progress state**, not a permanent failure.
* Occurs on:
  1. Newly issued bills where the carrier's EDI has not yet published physical milestones.
  2. Generic leasing container prefixes (`FFAU`, `TLLU`, `TEMU`, `TCLU`, `TXGU`, `TCNU`) requiring an automated discovery sweep across lines (resolves in 20–90 seconds).
* **Automated Action:** The engine places the reference into an active retry queue and re-polls the carrier up to 4 times within 24 hours. No manual intervention required from the client.
