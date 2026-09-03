import re

draft = """Title: SeaRates May 2025 Updates: Warehousing, Tariffs, Tracking
Meta Title: SeaRates May 2025 Product Release and Platform Updates
Meta Description: Explore May 2025 digital logistics platform updates: warehouse facilities management, 25 exception types, AI rate updates, and API additions.

Body:
## Virtual Office Warehouse Asset Handling

The Virtual Office profile now features a dedicated Facilities management panel. Logistical teams can add, edit, import, and account for warehouse assets alongside offered services from a single interface. External customers and business partners can receive shared access to inspect listed services and book warehouse capacity directly. This warehouse facilities management system expands internal operational visibility while providing a direct channel to market storage capacity.

## Upgraded Tracking for Road, Ocean, and Air

Our latest digital logistics platform updates expand visibility tools across sea, road, and air operations.

The Container Tracking tool received targeted container tracking exception management upgrades inside the Exceptions tab. Logic processing for all 25 exception types has been refined for higher precision. A new visual status field displays color-coded markers for timeline shifts: green indicators highlight earlier arrivals, while orange marks flag delays alongside revised dates. On the API side, container type and size detection logic now parses raw shipping line descriptions more effectively. The underlying predictive ETA shipping technology has also been updated to refine estimated delivery timelines.

For overland movement, our multimodal road tracking carrier integration now includes Kuehne + Nagel (KN). Developer Portal users can consult the API documentation for the full index of supported road carriers.

Air Tracking added coverage for 2 airlines: My Indo Airlines and Thai Vietair. These additions bring the total count of supported air carriers to 446.

Developers can now access complete terminal tracking API integration documentation on the Developer Portal. This endpoint links directly into our global database to support terminal tracking across worldwide port facilities.

## Rate Management and Custom AI Search

Rate management system tariff automation received multiple functional updates. Users can input FCL and FTL tariffs through three distinct structures: Flat (full cost), per km, or flat plus per km. For LCL shipments, users can select between ft³ and m³ measurement units. Air tariffs now support D2P, D2D, and P2D shipment routing types. Freight teams can group multiple container types simultaneously (such as 20ST, 20HC, and 20REF), while informative tooltips have been embedded across tariff table columns.

Rate requests handled by SeaRates AI now execute through a proprietary in-house language model. Output processing generates a freight rate calculator logistics explorer direct link for rapid booking navigation.

## Multi-Tool Usability and Geocoding Refinements

Product navigation and reference datasets across several platform tools received usability adjustments.

Dedicated Pricing pages have been launched for Air Tracking, Freight Index, CO2 Calculator, Ship Schedules, and DFA Membership, allowing teams to review subscription tiers for specific workflows.

Inside Ship Schedules, updated credit displays allow users to track remaining usage, paired with a direct Pricing link for subscription renewal.

The Carbon Emissions Calculator interface incorporates a dedicated subscription button for monitoring usage limits and upgrading plans. The CO2 Calculator API now supports calculation by Coordinates as an alternative option when Carrier queries return no result.

Geocoding & Autocomplete database expansions introduce multi-language translations in 8 worldwide languages across 217 capitals, 35,000 seaports, and the top 100 world seaports. Search functionality for the top 200+ world seaports has also been upgraded.

Teams requiring tailored enterprise setups can request custom software builds through the Request an IT Quote form or contact the SeaRates team directly."""

words = re.findall(r'\b\w+\b', draft.lower())

ai_words = [
    'crucial', 'delve', 'testament', 'seamlessly', 'seamless', 'game changer', 'game-changer',
    'in today', 'digital landscape', 'landscape', 'tapestry', 'foster', 'fostering',
    'elevate', 'elevating', 'realm', 'unlock', 'unlocking', 'empower', 'empowering',
    'beacon', 'demystify', 'spearhead', 'spearheading', 'paramount', 'pivotal',
    'robust', 'vital', 'synergy', 'transformative', 'cutting-edge', 'state-of-the-art',
    'revolutionize', 'ever-evolving', 'beacon', 'unwavering', 'plethora', 'myriad'
]

found = []
for w in ai_words:
    matches = re.findall(r'\b' + re.escape(w) + r'\b', draft, re.IGNORECASE)
    if matches:
        found.append((w, len(matches)))

print("AI Cliches found:", found)

# Em-dash check
em_dash_matches = re.findall(r'—|--|&mdash;|&#8212;', draft)
print("Em dash matches count:", len(em_dash_matches))

