import json
import re

article = {
  "title": "April 2025 Trump Tariffs: Global Supply Chain Risks",
  "meta_title": "April 2025 Trump Tariffs: Supply Chain Impact",
  "meta_description": "April 2, 2025 US tariff changes trigger reciprocal duties and HTS reclassification. Master ICS2 compliance and blank sailings.",
  "body_markdown": """On April 2, 2025, a broad tariff wave hit U.S. import channels. Framed as "Liberation Day," the policy aims to curb American industrial reliance on foreign goods. For freight forwarders, cargo owners, and ocean carriers, the sudden duty shifts force immediate revisions to customs filings, sailing routes, and landed cost models.

### Tariff Rates Implemented on April 2

The U.S. established a 10% baseline import duty across all incoming goods. Specific country and commodity duties enacted on April 2 include:

- 25% on foreign-made automobiles
- 25% on Canadian and Mexican imports
- 34% on Chinese goods
- 20% on imports from European Union countries
- 46% on Vietnamese goods
- 32% on Taiwanese imports
- 24% on Japanese goods
- 25% on South Korean imports
- 36% on Thai goods
- 31% on Swiss imports
- 32% on Indonesian goods
- 24% on Malaysian imports
- 49% on Cambodian goods
- 10% on United Kingdom imports
- 30% on South African goods

Additional rate proposals target specific sectors:
- Proposed 25% tariff on nations importing Venezuelan oil
- Digital Service Taxes (DSTs)
- Copper imports
- Timber and lumber

### HTS Reclassification and Customs Compliance Disruption

Country-of-origin rules drive these reciprocal duties, demanding swift HTS classification updates across international inventories. Over 18,000 commodity items under international HS codes require alignment with U.S.-specific HTS codes. Mismatches between domestic and global databases trigger entry rejections, cargo delays, manual clearance holds, and demands for supplemental paperwork.

Cross-border regulatory shifts add further operational friction. Effective April 1, the European Union tightened rules for filing Entry Summary Declarations (ENS) under its ICS2 system for non-EU imports. Logistics managers must satisfy EU ICS2 requirements while simultaneously complying with U.S. tariffs governed by IEEPA (International Emergency Economic Powers Act).

Established Electronic Data Interchange (EDI) channels for bills of lading, commercial invoices, import summaries, and classification data frequently fail under the updated duty schedule. Outdated HS codes cause automated rejections in the CBP ACE (Automated Commercial Environment) system. Inconsistencies between pre-tariff invoice values and new import declarations lead to entry refusals, particularly for freight from China, the EU, and Latin America. Gaps in reciprocal tariff databases produce incorrect duty calculations, fines, and cargo detentions.

### Industry Cost Increases and Repricing Pressures

Country-specific duty rates directly alter pricing structures, freight quotes, and cost calculations across key commercial sectors:

- **Apparel:** China and Vietnam shipped $14 billion in clothing to the U.S. last year as the two main supply sources. Secondary suppliers including Indonesia, India, Cambodia, and Bangladesh now face duties from 26% to 49%, raising landed costs for importers.
- **Electronics:** China, Vietnam, and Taiwan delivered $47.2 billion in laptops and tablets to U.S. buyers last year. Taiwan leads global microchip and semiconductor production. Increased duty expenses affect home appliances, medical equipment, automotive components, spare parts, light bulbs, and Wi-Fi routers. A separate 25% tariff on semiconductors was proposed, though a White House fact sheet noted semiconductor duties will not be added on top of reciprocal duties.
- **Footwear:** China and Vietnam produced 70% of U.S. footwear imports in 2024, totaling $18.5 billion.
- **Toys:** Toy shipments from China and Vietnam reached $15 billion in 2024, with China supplying 77% of U.S. toy sales. Under a 54% duty on Chinese goods, retail toy prices are projected to rise 30% by fall 2025.

### Vessel Schedule Adjustments and Port Rerouting

Ocean carriers are altering sailing schedules to avoid congested ports and high-duty entry points. Rerouting decisions cause blank sailings and unplanned schedule changes. Canadian ports have become alternative gateways for carriers moving cargo from China and the EU into North America.

### Action Plan for Logistics Service Providers

Logistics companies must execute practical steps to navigate customs friction and maintain cargo flow:

- **Ensure Classification Accuracy:** Prepare for higher entry denial rates, manual processing, double documentation, and audit risks in U.S. and EU systems. Audit all shipment records to match current regulations.
- **Work with Trusted Customs Brokers:** Secure real-time status updates and establish pre-submission audit checkpoints for customs declarations.
- **Review Service Level Agreements:** Adjust commercial contracts to build flexibility during periods of tariff shifts.
- **Provide Direct Client Communication:** Identify potential delay risks from HTS reclassification or ICS2 holds. Warn customers early regarding shifting lead times, recommend carrier diversification, bundle compatible shipments, and assist with alternative sourcing options such as value-added processing in transit. Document all delays and maintain clear charge records.
- **Digitalize Operations:** Centralize the management of more than 25 exceptions at once to recover faster from delays. Use tracking systems to adapt supply chains around empty sailings and maintain cargo visibility for rerouting.
- **Integrate Freight APIs:** Deploy tracking system web integrations and APIs for real-time visibility across global freight routes.

*By Sophia Shkuro.*"""
}

with open("final_article.json", "w", encoding="utf-8") as f:
    json.dump(article, f, ensure_ascii=False, indent=2)

print("Saved final_article.json")
