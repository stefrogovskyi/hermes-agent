import json
from audit_script import audit_json, banned_words, banned_connectors, trend_keywords

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

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

errors = audit_json(data)
print("Errors found:", errors)

# Save JSON output to verify
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved result.json successfully.")
