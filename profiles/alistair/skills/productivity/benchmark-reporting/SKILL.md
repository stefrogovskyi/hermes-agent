---
name: benchmark-reporting
description: "Use for benchmark reports and comparative data audits."
version: 1.0.0
author: Alistair Sterling
license: MIT
metadata:
  hermes:
    tags: [Benchmark, Reporting, Audit, Data]
    related_skills: [xlsx, grounded-citations]
---

# Benchmark Reporting & Comparative Audits

## When to Use

Use when generating comparative benchmark reports, API performance comparisons, tracking data audits, or multi-provider evaluation reports.

## Guidelines

1. **No Canned Conclusions:**
   - Never write static or hardcoded summary claims (e.g. "100% match", "X% faster") in executive summaries or chat captions unless those exact numbers are calculated directly from the current dataset.

2. **Ground Summaries in Table Evidence:**
   - If the detailed comparison rows show time deltas, location mismatches, or missing metadata (like IMO numbers or container identifiers), the summary section (Key Findings / Verdict) must explicitly highlight those discrepancies.
   - Suppressing noise (e.g. known API errors like DSSA / ДССА) must be stated clearly, but factual discrepancies in timestamps or status codes must be reflected in match accuracy percentages.

3. **Multi-Tab Excel Standard (5-Tab Structure for Ocean Tracking):**
   - **`Overview`**: Metadata, dataset parameters, query gap, purpose, and Key Findings table (#, Finding, Evidence).
   - **`Event Comparison`**: Event-by-event milestone audit (SR Code, Location, Time, Transport vs TM/Navo Code, Location, Time, Transport, Match [highlighted green `#E2EFDA` / red `#FCE4D6`], Difference/Comment).
   - **`Container Timestamps`**: Per-container breakdown of Discharge, Gate-out, Empty return, `events_mirrored` flags, and demurrage exposure gap analysis (+N days).
   - **`Structure & Metadata`**: Payload structure validation (Master status, `is_status_from_sealine`, Vessel IMO/MMSI, Voyage, AIS status, quota reporting).
   - **`Route & Geometry`**: POL/POD coordinates accuracy, port centroid distance deltas, rail/sea path resolution, and maritime geometry points.

4. **Telegram Delivery & Group Orchestration:**
   - Format chat captions with HTML (`<b>`, `<code>`).
   - Explicitly tag designated team members/bots in captions (e.g., `@thegaffermcp_bot` for Gaffer in Navo Tech geeks).
   - Deliver the `.xlsx` report as an active `MEDIA:` attachment path.

5. **Dynamic Sampling for Recurring Cron Benchmarks:**
   - For recurring (e.g., 48-hour) cron benchmarks, randomly sample track IDs from a master registry workbook (e.g., 20,000-row dataset) to maintain fresh, un-cached API test coverage across lines.

6. **Strict Alignment Between Message Caption and Report Content:**
   - Never hardcode optimistic statuses (e.g. `LIVE & ACTIVE`, default remaining quota numbers) in message summaries or caption templates as fallbacks.
   - If an API returns an error, auth failure (e.g. `API_KEY_WRONG`), or empty payload, the delivery caption must directly and truthfully report the exact error status (`❌ SeaRates API Status: ERROR (API_KEY_WRONG)`), remaining 100% consistent with the generated `.xlsx` report.

7. **Asynchronous Tracking Pipeline Resolution (Polling Protocol):**
   - When querying container tracking APIs that return asynchronous job statuses (e.g. `HTTP 202 Accepted`, `TRACKING_IN_PROGRESS`, `retry_after_seconds`), do NOT stop after the first request and ask the user if they want to poll again.
   - Proactively resolve the task: either poll the endpoint in a bounded loop or launch an autonomous background poller (`terminal(background=true, notify_on_complete=true)`) to wait for carrier data resolution and automatically deliver the final resolved tracking result directly into the chat when ready.

8. **Multi-Stage Pipeline Latency & SLA Monitoring (Navo Pipeline Standard):**
   - When auditing or benchmarking tracking systems (e.g., Navo Tracking vs SeaRates), break down latency across the full multi-stage architecture:
     1. **Carrier / SCAC Detection & Classification**: Identifying line and entity (BL, booking, container).
     2. **Checkpoint 1 (Inbound DB Log)**: Logging the incoming query to the database.
     3. **Line Scrape & Vessel DB Query**: Carrier parser call and internal vessel database lookup (visible on administrative dashboards).
     4. **Checkpoint 2 (Raw Parser DB Write)**: Storing raw line output before enrichment.
     5. **AIS Enrichment**: Polling and querying external AIS providers (MarineAsia, MarineTraffic, VesselFinder).
     6. **Consolidation & Normalization**: Standardizing payload format (`compat` vs `native`).
     7. **Checkpoint 3 (Client DB Write)**: Saving the finalized payload for client access.
     8. **Client Delivery (SLA Verification)**: Response delivery evaluated against the strict **≤ 60 seconds** SLA (operating across reserved fleet of 20 dedicated machines).
   - Reports must explicitly separate Line Parse Latency ($T_{parse}$), AIS Latency ($T_{ais}$), and Database Persistence Overhead ($T_{db}$) rather than reporting a single black-box response time.
9. **Multi-Provider Benchmark Architecture (12-Provider Standard):**
   - Involve both Enterprise visibility suites (Project44, Terminal49, OpenTrack, SeaRates) and Web aggregators (ShipsGo, GoComet, Track-Trace, VesselFinder, 17TRACK, Ship24, ParcelsApp).
   - Exclude direct clients (e.g., Portcast, MarineTraffic) from public benchmark evaluations.
   - Include PM GAP analysis identifying areas of improvement (US drayage/terminal gate status, Class-1 inland rail integration, AIS ping frequency in choke points).
10. **Authoritative Portal Verification vs Staging Endpoints:**
   - When evaluating carrier coverage or competitor parity, always inspect the live authoritative public portal (e.g. `navo24.com/developers/coverage/tracking/`) rather than internal/staging slices or incomplete sub-endpoints.
   - Account for naming aliases and SCAC variations (e.g., `11DX` vs `CNC`, `HALU` vs `11QU`, forwarder entries without 4-letter SCACs) before determining missing lines.
11. **Freight Rates Aggregation & Multi-Modal Standardization (SeaRates v3 + Navo):**
   - For instant rate queries (FCL, LCL, Road, Rail, Air), use asynchronous multi-source polling (<5s target).
   - Standardize outputs to SeaRates Logistics Explorer v3 format (`transportType`, `carrier`, `routing`, `pricing`, `breakdown`, `validity`, `terms`) enriched with Navo's `reliability_score`, `freeDays`, and `co2_emissions_kg` (GLEC v3).
   - **Market Sanity & Live Grounding:** Never output outdated pre-crisis baseline freight figures (e.g. $2k-$2.5k for Asia-Europe) without accounting for active geopolitical surcharges (Cape of Good Hope rerouting, PSS, EOS, ETS/EU carbon surcharges pushing spot rates to $6k-$8.5k). Verify real live quotes via headless browser / live API before returning rates.
   - **SeaRates Web Architecture Quirks:** SeaRates Logistics Explorer renders rates inside a Shadow DOM (`#shadow-wrapper-le`), enforces guest session rate limits (`API_KEY_LIMIT_REACHED` on `/access/check`), and requires platform tokens (`s-token`) or live UI search clicks (`button.ux0rsv`).


## Reference Documentation
- For exact SeaRates v3 endpoint parameters, query structures, and response error codes, see `references/searates_container_tracking_api.md`.
