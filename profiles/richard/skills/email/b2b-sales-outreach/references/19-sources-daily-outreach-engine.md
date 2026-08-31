# 19-Source B2B Daily Online Outreach Engine Architecture

## 1. Scope & Daily Quotas
- **Target Volume**: 95 verified personal executive emails per morning run (19 sources x 5 leads).
- **Cadence**: Monday through Friday at 07:00 Kyiv time (`0 4 * * 1-5` UTC).
- **Target Audience**: BCOs, Freight Forwarders, Trading Houses, Importers/Exporters (Head of Logistics, VP Supply Chain, Ocean Freight Director, C-Level).
- **Strict Anti-Generic Policy**: Never send to generic department mailboxes (`info@`, `sales@`, `pricing@`, `ops@`, `export@`, `ocean@`, etc.). Filter strictly using `is_personal_decision_maker_email()`.

## 2. 19 Active Lead Ingestion Sources
1. **Digital Freight Alliance (DFA)**: High-quality member directory (`/opt/hermes/profiles/richard/cache/dfa_members.xlsx`).
2. **Hunter.io BCO / Commodity Houses**: Global trading conglomerates (Trafigura, Glencore, ADM, Bunge, Geodis, CEVA).
3. **Freightnet Directory**: International forwarders by trade lane and service code.
4. **CIFFA**: Canadian International Freight Forwarders Association directory.
5. **ThomasNet**: US industrial manufacturers, exporters, and logistics service providers.
6. **Global Logistics Network (GLN)**: Independent forwarders network.
7. **Snov.io API**: Decision maker discovery by logistics domain.
8. **Prospeo API**: Name and domain verified email enrichment.
9. **Apollo API**: BCO and enterprise shippers discovery.
10. **ImportYeti**: US Customs bill of lading shippers and importers.
11. **Kompass**: Global freight forwarding and trade listings.
12. **WCA World**: Worldwide freight forwarding network directory.
13. **JCtrans Network**: Asian and global logistics directory.
14. **Volza**: Global trade customs intelligence.
15. **FIATA**: International Federation of Freight Forwarders Associations.
16. **Freightos**: Digital freight marketplace forwarders.
17. **Lognet Global**: Project cargo and freight forwarders.
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
