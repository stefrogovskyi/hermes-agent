# Pipeline Segregation & Batch Outreach Standards (Navo24)

Guidelines for organizing multi-batch lead generation, segregating personal vs company pipelines, and maintaining single-sheet master lists for sales reps.

## 1. CRM & Dashboard Pipeline Segregation (Personal vs Company Routed)
Never combine personal rep outreach and company-wide broadcast inbound into a single undifferentiated number:
- **Personal Outbound Pipeline (AE-Specific)**: Emails/messages dispatched specifically under the sales rep's identity (`From: Name <rep@e.navo24.com>`, `Reply-To: rep@navo24.com`). Track Base, Sent, Replied, Reply Rate %, Trials Started separately.
- **Company Routed Inbound**: Inbound responses originating from global company broadcasts (`rich@e.navo24.com`) or website forms assigned to the sales rep by team leaders (Ekaterina / Stefan). Track as `Company Routed Leads` -> `Active Trials` -> `Closed Won ($)`.
- **CRM Attribution Field**: Every lead record on `Follow-ups & Active Trials` must carry an explicit `Lead Origin` tag (`🏢 Company Routed` vs `🎯 Personal Cold Email` vs `👔 Personal LinkedIn` vs `📱 WhatsApp Outbound`) and an `Assigned AE` field.

## 2. Single-Sheet Continuous Master List Mandate (No Fragmented Batch Tabs)
When generating new outreach batches (e.g. Batch 2: leads #101–#200, Batch 3: #201–#300):
- **DO NOT create separate fragmented worksheets** (like `Forwarders Batch 2 (101-200)`).
- **Append directly to the main worksheet (`🎯 Forwarders & NVOCC`)**:
  * Rows 1–100: Batch 1 (Status: `sent` / `Touch 1 Sent`).
  * Rows 101–200: Batch 2 (Status: `not_sent` / `Scheduled (Touch 1)`).
- Resize sheet rows automatically (`ws.resize(rows=N)`) so sales reps can scroll through one single continuous table without switching tabs.

## 3. Multi-Batch Forwarders Campaign Generation & Zero-Tolerance Filters
- **Cross-Batch Deduplication**: Always load existing domains and email sets from prior batches before compiling Batch 2 (#101–200), Batch 3, etc.
- **Zero-Tolerance Domain Filters**:
  - Exclude all `.ru`, `.by`, `.su`, `.рф`, and Russian mail services (`mail.ru`, `yandex`, `rambler`, `bk.ru`, `inbox.ru`).
  - Exclude free/public consumer email domains (`gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`, `icloud.com`). Only corporate forwarding / logistics domains.

## 4. Mandatory SeaRates Pedigree Hook & 2026 Touch #1 Architecture
In cold email Touch #1 for international freight forwarders and NVOCCs, ALWAYS include the SeaRates core team pedigree:
```text
Navo24 was founded by the original core team and engineering leadership behind SeaRates to provide direct tracking infrastructure across 239 ocean carriers. We calculate Predictive ETA using satellite AIS vessel tracking and live port congestion data (standard DCSA milestones and automated free-time calculation).
```
- **Why**: SeaRates is universally recognized among forwarders; citing the founding leadership instantly establishes high trust and overcomes cold outreach skepticism.
- **CTA**: Free test on 1-2 active or delayed containers at `https://trackingmcp.com/auth/signup` (5 active containers included every month, no credit card required).
- **Banned Formatting**: ZERO em-dashes (`—` / `–`). Use standard hyphens `-`, commas, or clean sentences. ZERO conversational filler ("quick question", "hope this finds you well").
