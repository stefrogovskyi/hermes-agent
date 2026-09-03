import json
import re

# Refined rewrite addressing all audit feedback
title = "SeaRates at LISW25: Takeaways from London Shipping Week"
meta_title = "SeaRates at LISW25: London Shipping Week Highlights"
meta_description = "SeaRates recap from LISW25 at IMO Headquarters in London, covering maritime decarbonization, S-100 standards, and end-to-end supply chain visibility."

content = """During the week of September 15 through 19, 2025, SeaRates participated in London International Shipping Week (LISW25) at the IMO Headquarters in London. The event focused on the central theme of The Management of Paradox in Global Shipping, addressing trade-offs between growth, emissions reduction, vessel speed, safety, regulation, and technical innovation.

The week opened officially at the London Stock Exchange and covered key tracks including maritime decarbonization, digital transformation, supply chain resilience, and regulatory compliance. On September 16, DNV presented its Maritime Forecast to 2050 at IET London. The UKHO also hosted its "S-100 in focus" panel, examining new navigation and mapping standards. The S-100 framework is central to digital ecosystems, vessel safety, and standardized port operations.

Throughout the event, we met with clients, ocean carriers, and technology partners to demonstrate how SeaRates software supports daily logistics operations. Our team showcased live instant freight calculators, container tracking, air shipment visibility, carbon footprint estimators, and tailored enterprise IT integrations designed for operational cost control and transparency.

Four core operational developments defined discussions across the week. Decarbonization strategies are actively turning into practical deployment, moving beyond preliminary efficiency measures into alternative fuel trials monitored by regulators and financial stakeholders.

At the same time, structured data is becoming the baseline for maritime digital transformation. Frameworks like S-100 establish shared protocols across navigation and digital port services, giving organizations that standardize data and adopt open integrations a distinct edge in speed and operational security.

In parallel, shippers and 3PL providers are prioritizing end-to-end supply chain visibility, predictive risk assessment, and dynamic route adjustments to keep freight networks resilient.

Finally, persistent maritime labor shortages alongside updated safety mandates are directing capital into crew support, specialized training, and human-guided digital workflows.

We thank the LISW25 team and the IMO for convening industry leaders around sustainable growth. To discuss custom logistics software or event insights, reach out to our team at it.sales@searates.com or contact Kateryna Komarova or Lilia Khovrak directly."""

print("Title length:", len(title))
print("Meta title length:", len(meta_title))
print("Meta description length:", len(meta_description))

# Check em-dashes
em_dashes = len(re.findall(r'—|--', title + meta_title + meta_description + content))
print("Em-dash count:", em_dashes)

# Save JSON
article_data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "content": content
}

with open("/tmp/final_article.json", "w", encoding="utf-8") as f:
    json.dump(article_data, f, ensure_ascii=False, indent=2)

print("Saved /tmp/final_article.json successfully.")
