import json
from check_rewrite import orig_text, tokenize, get_ngrams, check_text

data = {
    "title": "5 Digital Freight Forwarding Trends: Next 10 Years",
    "meta_title": "Freight Forwarding Trends & 10-Year Market Outlook",
    "meta_description": "Explore key digital freight forwarding trends over the next decade, including AI route planning, decarbonization reporting, and forwarder collaboration.",
    "body_markdown": """Global container shipping capacity is set to grow by roughly 4% near the end of 2024, with maritime transit demand projected to expand by 7% to 8%. Meanwhile, air cargo volumes grew by 9% in 2023, maintaining momentum into subsequent quarters. These indicators point to rapid evolution across multimodal transportation. Over the next decade, five key digital freight forwarding trends will reshape how goods move globally.

SeaRates delivers container shipping services and broader supply chain management tools to support this evolving market. Shippers can request customized quotes through our platform, while logistics providers can join our global service network.

### Adoption of Artificial Intelligence

Artificial intelligence has expanded well beyond basic content creation into daily logistics operations. Forwarding companies actively apply intelligent software to improve schedule generation, data processing, route planning, and cargo forecasting. Within the coming decade, automated systems across air and ocean freight will handle routine operational tasks with high efficiency.

Applying AI in ocean freight planning and multimodal route optimization helps streamline complex shipments. For instance, the SeaRates AI assistant allows users to search freight rates across all transport modes, track cargo movements, view port and vessel schedules, and resolve general logistics inquiries.

### Escalating Operational Complexity

Global shipping networks face persistent operational friction caused by geopolitical tensions and volatile environmental conditions. Border closures and regulatory sanctions force forwarders to establish alternative transit corridors to safeguard operating margins. 

Simultaneously, severe storms, volcanic events, hurricanes, and coastal surges disrupt regional drayage and maritime schedules. International forwarders must construct resilient operational plans that account for ongoing climate and geopolitical risks. 

To mitigate shipping disruptions, SeaRates provides interactive tools that determine route distances and estimated transit durations based on live carrier data. These insights help cargo teams maintain container tracking visibility and prevent transit delays.

### Industry Competition and Differentiation

Dozens of new entrants join air and sea freight forwarding markets annually, attracted by strong earnings and broader access to transport infrastructure. To retain clients, established forwarders build competitive advantages through specialized service add-ons, alternative routing strategies, and enhanced shipment monitoring.

Networking also provides a distinct market advantage. Forwarders can become members of the Digital Freight Alliance, an ecosystem uniting over 8,000 logistics firms globally. DFA participants exchange industry expertise, market freight rates, access partner tariffs, and provide digital tools to their client bases.

### Forwarder Collaboration

Heightened market competition and complex trade routes encourage increased cooperation among freight forwarders. Companies frequently partner to manage shared transport legs when cargo destinations align.

Less Container Load (LCL) consolidation offers an established framework for joint operations in container freight forwarding. For organizations seeking tailored digital tools, the SeaRates technical team provides customized software solutions and individual IT quotes to support collaborative logistics.

### Maritime Decarbonization and Compliance

International regulatory frameworks strictly control greenhouse gas output from commercial shipping. European authorities lead this transition by requiring ocean carriers and logistics providers to submit detailed reports on fleet technical conditions and vehicle emissions. Standardized maritime decarbonization reporting will soon become a mandatory global requirement.

SeaRates offers an integrated CO2 calculation tool accessible via API or white-label integration. The system computes carbon emissions across sea, air, and land routes, allowing forwarders to offer verifiable carbon offset options to clients.

### Adapting to Modern Logistics

Digital transformation remains the central force driving logistics over the next 10 years. Industry participants across trading, shipping, and freight management must adopt digital tools to stay competitive. The SeaRates team provides modern software solutions tailored to specific commercial requirements."""
}

title = data["title"]
meta_title = data["meta_title"]
meta_description = data["meta_description"]
body_markdown = data["body_markdown"]

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body_markdown}"

orig_tokens = tokenize(orig_text)
draft_tokens = tokenize(full_text)

orig_6grams = get_ngrams(orig_tokens, 6)

overlaps_6 = []
for i in range(len(draft_tokens)-5):
    gram = tuple(draft_tokens[i:i+6])
    if gram in orig_6grams:
        overlaps_6.append(gram)

overlaps, errors, neg_matches, missing_kw = check_text(title, meta_title, meta_description, body_markdown)

print("Check results:")
print("6-gram overlaps count:", len(overlaps_6))
print("Errors:", errors)
print("Negations:", neg_matches)
print("Missing keywords:", missing_kw)
print("Title len:", len(title))
print("Meta title len:", len(meta_title))
print("Meta desc len:", len(meta_description))

if len(overlaps_6) == 0 and len(errors) == 0 and len(missing_kw) == 0:
    print("\nALL AUDIT CHECKS PASSED PERFECTLY!")
