import re

orig = """We are deeply grateful for your ongoing support of SeaRates. Our team is pleased to announce enhancements and changes designed to meet your trading and logistics requirements.

You’re always invited to discover our recent updates to remain informed about the newest changes.

What’s new for week 5:

Tracking System improvements: We are pleased to announce added support for 2 more shipping lines, namely Kanway Line and Sidra Line, bringing the total number to 182.
Furthermore, for the API, we have improved the auto-detection logic for shipping lines.
Finally, we have made enhancements to our collaboration with shipping lines and leasing companies, including Econship, Tailwind Shipping Lines, Seatrade, Emirates Shipping Line, and DSV Ocean Transport.

Air Cargo Tracking updates: Our integration with providers such as China Southern Airlines, Juneyao Airlines, Delta Air Lines, China Cargo Airlines, EVA Air, Challenge Airlines, ANA Cargo, Malaysia Airlines, and others has been further improved to deliver more accurate and timely tracking information.

Ship Schedules enhancements: We have improved our support for providers, namely for Swire Shipping, Evergreen, Econship, Kambara Kisen, Eukor, Sinotrans, and KMTC by Points.

Other updates:
For the Geocoding API, we have improved output data results.
Finally, we have created Individual Quotes API and Search Filter landing pages, as well as updated content for Freight Index and Carbon Emissions Calculator tools."""

draft = """Title: SeaRates Week 5 Updates: Tracking API & Schedules
Meta-Title: SeaRates Week 5 Updates | Container & Air Tracking API
Meta-Description: SeaRates Week 5, 2025 updates: added Kanway and Sidra lines, updated air cargo tracking integration, vessel schedules, and logistics rate tools.

Body Text:
Moving goods across borders relies on raw data moving just as fast.

SeaRates released several platform updates during the fifth week of 2025. These changes focus on tracking capabilities, schedules, and developer resources.

#### Container and Ocean Freight Updates
The SeaRates real-time container tracking API now includes support for Kanway Line and Sidra Line. This addition brings the total number of supported ocean carriers to 182. Along with expanded carrier coverage, the system features improved carrier auto-detection logic for shipping lines, assisting with vessel schedule auto-detection.

SeaRates also updated data integrations for five shipping lines and leasing companies:
- Econship
- Tailwind Shipping Lines
- Seatrade
- Emirates Shipping Line
- DSV Ocean Transport

#### Air Cargo and Schedules
Air cargo tracking integration received performance updates across eight airlines:
- China Southern Airlines
- Juneyao Airlines
- Delta Air Lines
- China Cargo Airlines
- EVA Air
- Challenge Airlines
- ANA Cargo
- Malaysia Airlines

These changes deliver more accurate and timely tracking information for air shipments.

For sea freight planning, vessel schedule support was updated for Swire Shipping, Evergreen, Econship, Kambara Kisen, Eukor, Sinotrans, and KMTC by Points.

#### Developer Tools and Site Pages
Geocoding API output data results were improved. SeaRates also published new dedicated landing pages for the Individual Quotes API and the Search Filter feature.

Finally, content was refreshed for two core logistics rate management tools: the Freight Index and the Carbon Emissions Calculator. Together, these updates deliver broader multimodal freight visibility for daily supply chain operations."""

def get_words(t):
    return re.findall(r'\b[\w\-]+\b', t)

ow = get_words(orig)
dw = get_words(draft)

print("Original word count:", len(ow))
print("Draft word count:", len(dw))

# 6+ word overlaps
overlaps = []
for n in range(6, 15):
    for i in range(len(dw) - n + 1):
        gram = dw[i:i+n]
        gram_lower = [w.lower() for w in gram]
        # check if gram_lower in orig
        for j in range(len(ow) - n + 1):
            if [w.lower() for w in ow[j:j+n]] == gram_lower:
                overlaps.append((n, ' '.join(gram)))

print("Overlaps found:")
for n, phrase in overlaps:
    print(f"[{n} words] {phrase}")
