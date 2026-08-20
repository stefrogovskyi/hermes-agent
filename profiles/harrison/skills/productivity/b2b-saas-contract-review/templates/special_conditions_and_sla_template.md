# SPECIAL CONDITIONS & SLA SCHEDULE TEMPLATE

## SPECIAL CONDITIONS AND SCHEDULES

These Special Conditions amend and supplement the Navo24 Terms and Conditions (Version 2.0) ("Terms"). In accordance with Clause A5, in the event of any conflict between these Special Conditions and the Terms, these Special Conditions shall prevail.

### 1. Permitted Commercial Use and Data Licence (Amending Clause A8)
1.1. Navo24 (WEMELOGISTICS LTD) hereby grants to Client a non-exclusive, worldwide, non-transferable (except in connection with an assignment of the Agreement) licence during the Term to access and use the TrackingMCP data obtained from Navo24 for commercial purposes through integration into the Client platform.
1.2. Client may surface, display, and distribute such data to Client’s customers within the Client application and via Client’s customer-facing API, provided that:
    (a) such data is made available only to the specific Client customer to whose shipments the data relates; and
    (b) Client shall not resell, sublicense, or distribute raw Navo24 API data on a standalone basis as a competing raw tracking data feed without value-add integration into Client's services.

### 2. Variation of Terms (Amending Clause A6)
Clause A6 of the Terms shall not apply. The Terms, this Commercial Offer, and any attached Schedules governing Client’s use of the Services may only be amended, modified, or varied by mutual written agreement signed by authorized representatives of both Parties.

### 3. Price Protection and Fee Adjustments (Amending Clause B2.5)
Clause B2.5 of the Terms shall not apply. The Charges stated in this Commercial Offer shall remain fixed for the Initial 12-Month Term. Navo24 may review Charges for any subsequent Renewal Term by providing Client with written notice of any proposed adjustment at least sixty (60) days prior to the expiration of the then-current Term. Any increase shall be reasonable and subject to mutual agreement; if the Parties fail to agree on revised Charges, the Agreement shall expire at the end of the current Term.

### 4. Fixed Term & Termination (Amending Clause B9.2)
The provision in Clause B9.2 permitting either Party to terminate for convenience on thirty (30) days' notice shall not apply. The Agreement shall remain in force for the full Initial Term (and any Renewal Term), save that either Party may terminate the Agreement immediately for cause pursuant to Clause B9.2 (material breach not remedied within 30 days, or insolvency).

### 5. Payment Terms (Amending Clause B2)
Invoices shall be payable by Client within thirty (30) calendar days from the date of receipt of a valid VAT invoice by Client (Net 30).

### 6. Term and Auto-Renewal (Amending Clause B9.1)
6.1. The Initial Term shall be twelve (12) months commencing on the date API credentials/access are provisioned to Client.
6.2. Following the Initial Term, this Agreement shall automatically renew for successive twelve (12) month periods ("Renewal Term(s)") unless either Party provides written notice of non-renewal to the other Party at least thirty (30) days prior to the expiration of the then-current Term.

---

### 7. SERVICE LEVEL AGREEMENT (SLA) & SUPPORT SCHEDULE

#### 7.1. Service Availability Target
Navo24 targets a Monthly Uptime Percentage of at least **99.5%** for the API ("Uptime Target"), calculated as total minutes in a calendar month less Downtime, divided by total minutes.
* **Exclusions from Downtime:** Downtime shall not include:
  (a) Scheduled Maintenance communicated in advance;
  (b) Upstream carrier portal/EDI/API downtime, network latency, or carrier-side data unresponsiveness outside Navo24’s reasonable control;
  (c) Force Majeure events (Clause B8);
  (d) Issues caused by Client’s systems, network, or third-party integrations.

#### 7.2. Scheduled Maintenance
Navo24 shall use reasonable endeavours to schedule standard maintenance during off-peak hours (between 22:00 and 06:00 UK time or weekends). Navo24 will notify Client of planned maintenance requiring downtime at least **forty-eight (48) hours** in advance via email or status dashboard.

#### 7.3. Support Response & Incident Management
Client may report technical issues, connector anomalies, or data errors by emailing **support@navo24.com** or via dedicated communication channels.

| Severity Level | Definition | Target First Response | Target Resolution / Workaround |
|---|---|---|---|
| **Severity 1 (Critical)** | Core API is completely unavailable or returning critical system errors across all carriers. | **< 2 hours** (24/7/365) | Continuous effort until service restored |
| **Severity 2 (Major)** | Major functionality impaired, or specific carrier connector down affecting high volume. | **< 4 Business Hours** | Within 1 Business Day |
| **Severity 3 (Minor / Data Anomaly)** | Single container discrepancy, minor edge-case schema parsing issue, or general technical query. | **< 1 Business Day** | Within 2–3 Business Days |

*Business Hours: 09:00 to 18:00 UK Time (GMT/BST), Monday through Friday, excluding UK Public Holidays.*

#### 7.4. Data Integrity & Carrier Limitations
Navo24 continuously normalises and validates incoming milestone and AIS data to standard schemas through multi-source fallback connectors. While Navo24 guarantees the diligent operation and maintenance of its data connectors, Client acknowledges that the underlying timeliness and substantive accuracy of carrier-reported milestones depend on the respective ocean/air carriers and terminal operators.
