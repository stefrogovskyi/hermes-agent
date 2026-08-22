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

## Reference Documentation
- For exact SeaRates v3 endpoint parameters, query structures, and response error codes, see `references/searates_container_tracking_api.md`.
