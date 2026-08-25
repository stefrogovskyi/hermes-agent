---
name: b2b-saas-contract-review
description: "Review B2B SaaS contracts, MSAs, SLA and terms redlines."
version: 1.0.0
author: Harrison Croft, Navo Legal Counsel
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Legal, Contracts, B2B, SaaS, MSA, SLA, Redlines, Compliance]
    related_skills: [document-to-action-items, docx, pdf]
---

# B2B SaaS Contract Review & Special Conditions Drafting

A structured workflow for legal counsels and deal desks to audit incoming contract markups, redlines, and Special Conditions for enterprise SaaS, API, and data subscriptions without unnecessarily reopening baseline terms.

## When to Use

- Customer requests amendments to standard Terms of Service (TOS), Master Services Agreements (MSA), or Commercial Offers.
- Drafting binding Special Conditions (Order Form overrides) under English or common law.
- Formulating SLA / Support schedules for enterprise API / data services.
- Evaluating commercial and liability risks on deal redlines.

## Core Operational Workflow

### 1. Order of Precedence & Insertion Mechanism
Instead of amending public baseline Terms of Service (which triggers version control overhead), draft amendments as **Special Conditions** attached to the signed Commercial Offer / Order Form.
* Ensure the baseline TOS contains an **Order of Precedence clause** (e.g. *Order Form / Special Conditions > Service Agreement > Website Terms*).
* Include an explicit conflict-override preamble in the Special Conditions:
  > *"These Special Conditions amend and supplement the standard Terms and Conditions. In the event of any conflict or inconsistency between these Special Conditions and the Terms, these Special Conditions shall prevail."*

### 2. Standard Enterprise Clause Audit Matrix

| Clause / Domain | Typical Customer Request | Risk Rating | Provider Counter-Strategy & Safe Harbour |
|---|---|---|---|
| **Data Licensing & Permitted Use** | Right to display data to downstream clients and through customer APIs | **MEDIUM** | Grant commercial licence to integrate and display data **only** to specific downstream customers related to their shipments/accounts. **Strictly prohibit raw, standalone data reselling/scraping**. |
| **Variation of Terms** | Disallow unilateral changes by provider | **LOW** | Accept. Enterprise customers require mutual written consent for any changes during the active term. |
| **Price Protection & Escalation** | Lock subscription fees for initial term | **LOW** | Accept 12-month fee freeze. Require 60-day notice prior to renewal with reasonable increases. |
| **Termination for Convenience** | Remove 30-day provider termination right | **VERY LOW / FAVORABLE** | Accept. Locks in 12-month committed revenue (ARR/MRR) while preserving immediate termination for material breach/insolvency. |
| **Payment Terms** | Extend payment from 10 days to Net 30 from receipt of invoice | **LOW** | Accept Net 30 from date of receipt of valid VAT invoice. |
| **SLA & Uptime** | Demand availability commitment and penalties | **MEDIUM** | Offer 99.5% Monthly Uptime Target. **Exclude upstream third-party/carrier downtime**, planned maintenance, and Force Majeure. |
| **Data Quality / Accuracy** | Request warranties on external raw data feeds | **HIGH** | Exclude strict accuracy warranties for third-party/carrier feeds. Commit to reasonable diligence in connector maintenance and multi-source failover. |
| **Enterprise Procurement / Supplier Terms** | Customer insists on incorporating their standard Supplier / Purchase Terms | **CRITICAL** | **Never concede full precedence.** Supplier terms designed for procurement/consulting impose unlimited liability and breach warranties on third-party carrier data. **Solution:** Accept compliance clauses (Bribery, Modern Slavery, Sanctions, GDPR) in an Annex, but keep SaaS Special Conditions prevailing for all IP, liability, and data delivery terms. |

### 3. SLA & Support Incident Classification Standard

When an enterprise customer requests an SLA, define standard severity tiers:

* **Severity 1 (Critical):** Core API / service totally down across all routes. *Target response: < 2 hours (24/7), continuous fix effort.*
* **Severity 2 (Major):** Specific connector down or major feature impaired affecting high volume. *Target response: < 4 business hours, resolve in 1 business day.*
* **Severity 3 (Minor / Data Anomaly):** Single record discrepancy, cosmetic or edge-case schema issue. *Target response: < 1 business day, resolve in 2–3 business days.*

*Maintenance Window Rules:* Schedule planned maintenance during off-peak hours (e.g. 22:00–06:00 UK time or weekends) and commit to at least 48 hours advance notice.

### 4. Output Checklist

- [ ] Clear Risk Rating (Low / Medium / High / Critical) provided for each client point.
- [ ] Side-by-side comparative diff / audit matrix clearly formatted.
- [ ] Ready-to-use contractual drafting in clear, legally enforceable English.
- [ ] IP / raw data reselling boundaries explicitly safeguarded.
- [ ] SLA exclusions for third-party carrier/upstream systems clearly stated.
- [ ] Constructive Executive / Legal Cover Letter drafted (see `templates/enterprise_redline_cover_letter_template.md`) explaining the commercial rationale to customer procurement without antagonism.
- [ ] Actionable next steps outlined for sales and executive leadership.
