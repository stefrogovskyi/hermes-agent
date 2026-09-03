import json
import re

title = "30% US Tariffs on Mexico & EU: Trade Plan for August 1"
meta_title = "US Mexico EU Import Tariffs 2025: August 1 Deadline"
meta_description = "Prepare for 30% US tariffs on Mexico and EU goods starting August 1, 2025. Learn INCOTERMS tariff risk mitigation and USMCA origin thresholds."

body = """Donald Trump announced a sweeping 30% tariff on all goods imported from Mexico and the European Union on July 12, 2025. The decision targets commercial trade deficits, drug trafficking, and domestic manufacturing decline. Unlike earlier measures that singled out automotive parts or farm produce, this duty applies across every single product category.

The implementation date is set for August 1, 2025. Shippers have less than three weeks to adapt.

### Cumulative Cost Adjustments

These duties stack directly onto existing trade barriers. Effective import taxes will climb to between 30% and 55% across affected sectors. The heaviest financial pressure falls on automotive manufacturers, machinery builders, agricultural exporters, and textile producers.

US Customs and Border Protection is altering entry protocols. Officers now require updated valuation reports before granting unloading permits. Importers should expect physical container inspections and significant LCL customs clearance delays at major ports.

### Supply Chain Risk Exposure

Shippers face operational friction on multiple fronts. Buyers in North America are already pausing orders or demanding immediate price concessions.

Fixed-price agreements like EXW and DDP are causing contract disputes. EXW assigns tariff expenses to the buyer. DDP requires the exporter to cover duty increases out of pocket. Freight forwarders face intense pressure to hold shipping prices static even as customs expenses escalate.

Mixed-origin shipments create hidden financial liabilities. Missing country-of-origin documentation for a single SKU can subject entire consignments to maximum duty rates. Rerouting European freight through third-country hubs like Canada, the UK, or the Middle East adds transit days and introduces compliance overhead.

### Action Plan Before August 1

Managing US Mexico EU import tariffs 2025 requires immediate operational adjustments across contracts, logistics, and customs filings.

1. **Audit Tariff Lines by SKU.** Map every harmonized system code against the new 30% surcharge. Identify low-margin product lines in agriculture, textiles, or machinery that cannot absorb the tax.
2. **Revise Trade Terms.** Implement INCOTERMS tariff risk mitigation by renegotiating fixed DDP terms. Shift toward flexible pricing clauses or insert a 5% to 10% tariff buffer.
3. **Route Through Secondary Hubs.** Divert Mexican or European shipments through Canada, the UK, or the Middle East while protecting origin verification records.
4. **Notify Trading Partners.** Reach out to buyers and suppliers two to three weeks before the August 1 deadline to establish clear cost-sharing terms.
5. **Verify USMCA Qualification.** Mexican exporters can reduce or eliminate duties if their goods meet the USMCA 62.5 percent origin threshold. Ensure origin documentation is verified before shipping.
6. **Update Contractual Protections.** Insert political force majeure clauses, tariff variation terms, and tariff and delay insurance into supply agreements.
7. **Re-evaluate Retail Pricing.** A 10% retail price hike can erode customer demand and erase operating margins. Recalculate landed costs for every product family.
8. **Audit Customs Documentation.** Inspect commercial invoices, waybills, CMRs, and certificates of origin for line-item accuracy. Misdeclarations trigger severe fines.
9. **Restructure 3PL Contracts.** Negotiate tiered agreements with freight forwarders, such as a base transport rate plus a 5% adjustment per duty threshold.
10. **Establish Staging and Automation.** Stage cargo in Canadian warehouses or temporary CFS/ICD facilities. Connect your system to the SeaRates freight rate recalculation API to adjust landed costs across sea, air, rail, and road routes.

### Execution Tools

SeaRates provides digital tools to handle shifting customs requirements and volatile freight markets.

The Logistics Explorer platform lets cargo owners calculate multimodal shipping rates in real time. Businesses can integrate these capabilities directly into their operational software using web APIs. For customized logistics strategies and contract reviews, contact sales@searates.com."""

# Check lengths
print("Title length:", len(title), "<= 60:", len(title) <= 60)
print("Meta Title length:", len(meta_title), "<= 60:", len(meta_title) <= 60)
print("Meta Description length:", len(meta_description), "<= 155:", len(meta_description) <= 155)

# Check em-dash and double dash
full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"
em_dash_count = full_text.count("—") + full_text.count("--")
print("Em-dash and double-dash count:", em_dash_count)

# Check 6-grams overlap with original text
with open('/opt/hermes/profiles/archie/original_post_202.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

def normalize_words(text):
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text.split() if w]

orig_words = normalize_words(orig_text)
rewrite_words = normalize_words(body)

orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(tuple(orig_words[i:i+6]))

matches = []
for i in range(len(rewrite_words) - 5):
    gram = tuple(rewrite_words[i:i+6])
    if gram in orig_6grams:
        matches.append(" ".join(gram))

print("6-gram overlap count:", len(matches))
if matches:
    print("Matches found:", matches)

# Save verified JSON
verified_data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body,
    "em_dash_count": em_dash_count,
    "ngram_overlap_count": len(matches),
    "title_len": len(title),
    "meta_title_len": len(meta_title),
    "meta_desc_len": len(meta_description)
}

with open('/opt/hermes/profiles/archie/final_verified_article.json', 'w', encoding='utf-8') as f:
    json.dump(verified_data, f, ensure_ascii=False, indent=2)

print("Saved final_verified_article.json successfully.")
