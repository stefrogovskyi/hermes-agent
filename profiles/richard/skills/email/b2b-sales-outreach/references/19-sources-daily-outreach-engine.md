# 19-Source B2B Daily Online Outreach Engine Architecture

## 1. Scope & Daily Quotas
- **Target Volume**: Up to 95 verified personal executive emails per morning run (19 sources x strictly 5 leads each).
- **Strict Per-Source Quota (Zero-Monopoly Rule)**:
  * Hard limit of **maximum 5 leads per source** (`MAX_PER_SOURCE = 5`).
  * **No Backfilling**: If a scraper or API returns fewer than 5 (or 0), do NOT backfill the difference from DFA or any other source.
  * In-memory pre-dispatch counter strictly drops any candidate leads exceeding 5 for any single source platform.
- **Cadence**: Monday through Friday at 07:00 Kyiv time (`0 4 * * 1-5` UTC).
- **Target Audience**: BCOs, Freight Forwarders, Trading Houses, Importers/Exporters (Head of Logistics, VP Supply Chain, Ocean Freight Director, C-Level).
- **Strict Anti-Generic Policy**: Never send to generic department mailboxes (`info@`, `sales@`, `pricing@`, `ops@`, `export@`, `ocean@`, etc.). Filter strictly using `is_personal_decision_maker_email()`.

## 2. 19 Active Lead Ingestion Sources & 2-Step Enrichment Architecture
Directory sources often show generic contact emails or web forms. To ensure all 19 sources yield verified personal decision-makers:
- **Phase 1 (Directory Scraping)**: Extract company legal name, website/domain, and target geography (focus on Americas).
- **Phase 2 (B2B Executive Enrichment)**: Query B2B APIs (Prospeo, Hunter.io, Snov.io) for verified personal executive emails (`VP of Logistics`, `Director of Ocean Freight`, `Head of Supply Chain`, `CEO`).
- **Phase 3 (DNS/MX Verification)**: Validate recipient mailserver via `validator.py`.

### Source Breakdown:
1. **Digital Freight Alliance (DFA)**: High-quality member directory (`/opt/hermes/profiles/richard/cache/dfa_members.xlsx`).
2. **Hunter.io BCO / Commodity Houses**: Global trading conglomerates (Trafigura, Glencore, ADM, Bunge, Geodis, CEVA).
3. **Freightnet Directory**: International forwarders directory + Prospeo/Hunter domain enrichment.
4. **CIFFA**: Canadian International Freight Forwarders Association directory + executive enrichment.
5. **ThomasNet**: US industrial manufacturers, exporters, and logistics suppliers + domain enrichment.
6. **Global Logistics Network (GLN)**: Independent forwarders network + executive enrichment.
7. **Snov.io API**: Decision maker discovery by logistics domain.
8. **Prospeo API**: Direct B2B personal decision-maker search for ocean logistics directors.
9. **Apollo API**: BCO and enterprise shippers discovery.
10. **ImportYeti**: US Customs bill of lading shippers and sea container importers.
11. **Kompass**: Global freight forwarding and trade listings + domain enrichment.
12. **WCA World**: Worldwide freight forwarding network directory + executive enrichment.
13. **JCtrans Network**: Asian and global logistics directory + executive enrichment.
14. **Volza**: Global trade customs intelligence shippers.
15. **FIATA**: International Federation of Freight Forwarders Associations + domain enrichment.
16. **Freightos**: Digital freight marketplace forwarders.
17. **Lognet Global**: Project cargo and freight forwarders network.
18. **CargoNet**: Supply chain security and logistics network.
19. **Clay / Lusha / LinkedIn Logistics**: Enriched logistics decision-makers.

## 3. Pre-Send Quality & Deliverability Gates
1. **Cross-CRM Deduplication**:
   - Cross-check candidate emails across ALL 3 active Airtable bases before dispatch:
     * `Online Outreach` (`appdJR8VVczRxcVke` / Table `Outreach Leads`)
     * `Navo CRM` (`appbxvl9BBaTiLMlf` / Tables `Leads` & `Contacts`)
     * `Rich Outreach` (`appEoWQjvhgN8LIX7` / Table `Leads`)
   - Guarantee **0% duplicate outreach**.
2. **Pre-Send DNS & MX Verification**:
   - Verify recipient domain mail exchanger via `validator.py` (`socket.getaddrinfo(domain, 25)`).
3. **RFC 5322 Recipient Formatting**:
   - Format `To` header strictly as `f"{lead['name']} <{lead['email']}>"`.
4. **Dynamic AI Personalization & Combinatorics**:
   - Rotate 6+ subjects, 4+ introductory hooks citing the core founding team of SeaRates, and full 5-product portfolio list.
5. **Airtable CRM Real-Time Logging**:
   - Log each dispatched email immediately with `Stage: Contacted`, `First Email Sent At`, `Source Platform`, `Email Subject`, `Email Body Sent`, and Resend ID.
