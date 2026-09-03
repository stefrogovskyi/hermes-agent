import re

original = """May 2025 Development Release: Empowering Business Users

The SeaRates team appreciates your ongoing assistance and input. We update our digital ecosystem with new features and improvements every month, and this month is no exception. We want to highlight the accomplished products we have enhanced. Subscribe to our SeaRates newsletter, and we'll notify you of any updates.

Explore our new features for May and check out the most recent updates for the previous month.

Facilities Management System
The SeaRates team is proud to announce that our 'Facilities' management panel is available in your Virtual Office profile. Handle any type of warehouse assets in one place: Add, edit, import, and fully account for facilities and offered services you’d like to promote.
Share access with customers and partners to book your warehouse services. Start to streamline your warehouse management, and stay tuned for the upcoming improvements!

SeaRates Pricing
We are glad to present the newly added Pricing pages for a set of our products. Find your tool and choose the right package tailored to your logistics needs:
Air Tracking, Freight Index, CO2 Calculator, Ship Schedules, DFA Membership.

Terminal API
Our team is proud to announce Terminal Tracking API documentation on our Developer Portal. Connect to our database of worldwide terminals for effortless and wide coverage tracking.

Road Tracking
We’re glad to inform you about the added support for 1 more carrier: Kuehne + Nagel (KN). Find the list of supported carriers via API by following the link.

Container Tracking
We are glad to present a range of improvements for the 'Exceptions' tab in the Container Tracking tool, namely:
- Optimized logic for processing all 25 exception types
- Added the field with color markers for 'positive' (green mark for earlier arrival) and 'negative' (orange mark for delays) changes with new dates
For API, we have improved the logic for the detection of a container's type and size by description from the shipping line.
Finally, the Predictive ETA logic has also been updated.

Air Tracking
Our team is happy to announce added support for 2 airlines: My Indo Airlines and Thai Vietair, bringing the total number of supported airlines to 446.

Ship Schedules
We have updated the credit display in the tool and added a Pricing link to quickly continue your subscription.

Carbon Emissions Calculator
We have added a subscription button to easily check your credit limits and upgrade your plan for smooth usage of the CO2 Calculator.
Moreover, for API, we have added calculation by Coordinates as an alternative option if there are no results by Carrier.

Other updates
We are proud to announce the implementation of our own language model for SeaRates AI, as well as improved results processing for freight rate requests with a direct link to the Logistics Explorer.
For the Rate Management System, we have made a range of improvements for the following capabilities:
- Add your tariffs for FCL and FTL by 3 options: ‘Flat’ (full cost), ‘per km’, and ‘flat + per km’;
- Choose between ft³ and m³ for LCL type;
- Add air tariffs for D2P, D2D, and P2D types;
- Make groups of container types simultaneously (e.g., group 20: 20ST, 20HC, 20REF, etc.);
- Check added tooltips for the columns in the tariff table.
Finally, for Geocoding & Autocomplete, we have made translations into 8 major worldwide languages for 217 capitals, 35,000 seaports, and the top 100 world seaports, as well as improved data search for the top 200+ world seaports.

You’re always welcome to reach out to us for customized digital solutions for logistics via the Request an IT Quote form or by contacting us anytime."""

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

orig_words = re.findall(r'\b\w+\b', original)
draft_words = re.findall(r'\b\w+\b', draft)

orig_words_lower = [w.lower() for w in orig_words]
draft_words_lower = [w.lower() for w in draft_words]

# Find all 6+ word sequences
matches = []
n1 = len(orig_words_lower)
n2 = len(draft_words_lower)

for i in range(n1):
    for j in range(n2):
        k = 0
        while i+k < n1 and j+k < n2 and orig_words_lower[i+k] == draft_words_lower[j+k]:
            k += 1
        if k >= 6:
            matches.append((k, i, j, " ".join(draft_words[j:j+k])))

# Deduplicate
matches.sort(key=lambda x: x[0], reverse=True)
filtered = []
seen_ranges_draft = set()

for length, i, j, text in matches:
    draft_range = range(j, j+length)
    if not any(j in seen for seen in seen_ranges_draft):
        filtered.append((length, i, j, text))
        seen_ranges_draft.add(tuple(draft_range))

for length, i, j, text in filtered:
    orig_snippet = " ".join(orig_words[max(0, i-2):min(n1, i+length+2)])
    draft_snippet = " ".join(draft_words[max(0, j-2):min(n2, j+length+2)])
    print(f"Match length {length}: '{text}'")
    print(f"  Orig:  {orig_snippet}")
    print(f"  Draft: {draft_snippet}\n")

