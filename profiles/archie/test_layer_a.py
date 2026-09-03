import re

orig = """We are truly grateful for your continued loyalty and confidence in working with SeaRates. It is our pleasure to offer you innovative solutions that address all your logistics and trade requirements. We are dedicated to refining our services and adapting to your evolving needs.

Please refer to our earlier updates for the most up-to-date information.

What’s new for week 24:

Road Tracking updates: Our team is proud to announce added support for a new carrier to the Road Tracking API — DB Schenker, bringing the total number to 4.

Moreover, we have added the 'cargo_units' field for broader cargo details (container numbers, ULD (Unit Load Device), or other data).

Distance and Time enhancements: For the API , we have added the 'sections' field to facilitate transportation by ferry, which includes a description of each section of the route and specifies the type of transport—either truck or ferry. Distance, transit time, and average speed are also indicated for each section.

Terminal Tracking improvements: For API, we have updated our support of worldwide terminals , namely NHAVA SHEVA FREEPORT TERMINAL.

Vessel Tracking enhancements: For the API (version 1.0), we improved the logic of vessel search and AIS data acquisition.

Container Tracking improvements: For API , we have improved our support of shipping lines, namely Orient Overseas Container Line (OOCL), COSCO, Hapag-Lloyd, and Maersk.

Air Tracking updates: For API , our team has enhanced support of airlines, including Cathay Pacific Airways, SpiceJet, Singapore Airlines, and others.

Carbon Emissions Calculator updates: We have included route display on the map for land and sea shipping.

Rate Management System : For the owner of a company in your own Virtual Office , we have added the ability to review all rates placed by your employees from their profiles under your account.

AirRates improvements: We are gladly announcing the addition of the CO2 Calculator , Ship Schedules , Freight Index , and DFA Membership to the AirRates Pricing page .

Announcements:
Unified Tracking System
Logistics Map ‘Warehouse’ tab
Load Calculator Web 3.0 (new design and features)
Map Platform
Logistics Explorer in the Mobile App"""

rewrite = """TITLE: SeaRates Week 24, 2025 Release Notes
META_TITLE: SeaRates Week 24 2025 Product Updates
META_DESCRIPTION: Discover SeaRates Week 24, 2025 updates with DB Schenker road tracking and carbon emissions route mapping for multimodal supply chain visibility.

BODY:
SeaRates Week 24, 2025 release notes cover updates across API integrations and platform management.

Road and Ocean Tracking Upgrades

Adding DB Schenker road tracking brings our supported road carriers on the real-time freight tracking API to 4. Road Tracking API requests now accept the 'cargo_units' field for detailed cargo specifications like container numbers and ULD (Unit Load Device) entries.

For ocean freight, our container tracking API enhances coverage for four shipping lines:
- Orient Overseas Container Line (OOCL)
- COSCO
- Hapag-Lloyd
- Maersk

Vessel Tracking API v1.0 improves vessel search logic alongside AIS vessel tracking data acquisition. Terminal Tracking API expands global location support with the addition of Nhava Sheva Freeport Terminal.

Air Shipping and Multimodal Routes

Air Tracking API improves integration across Cathay Pacific Airways, SpiceJet, Singapore Airlines, and other airlines.

To improve multimodal supply chain visibility, the Distance and Time API introduces the 'sections' field. Designed for ferry transport, this field describes each route segment and specifies transport type as either truck or ferry. Each section details transit duration and distance covered alongside average speed metrics.

Carbon Emissions and Account Management

For environmental tracking, the Carbon Emissions Calculator displays carbon emissions route mapping directly on the map for land and sea shipping.

In Virtual Office, company owners can review freight rates placed by employees directly from profile views under their account.

AirRates Pricing Page Additions

Four features have been added to the AirRates Pricing page:
- CO2 Calculator
- Ship Schedules
- Freight Index
- DFA Membership

Announcements

Recent platform additions include:
- Unified Tracking System
- Logistics Map 'Warehouse' tab
- Load Calculator Web 3.0 with new design and features
- Map Platform
- Logistics Explorer in the Mobile App"""

# Detailed tokenization that keeps exact words
orig_words = re.findall(r'[a-zA-Z0-9_]+', orig)
rewrite_words = re.findall(r'[a-zA-Z0-9_]+', rewrite)

def find_exact_ngrams(w1, w2, min_len=6):
    w1_lower = [w.lower() for w in w1]
    w2_lower = [w.lower() for w in w2]
    
    matches = []
    for i in range(len(w2_lower)):
        for j in range(len(w1_lower)):
            k = 0
            while (i + k < len(w2_lower) and j + k < len(w1_lower) and w2_lower[i+k] == w1_lower[j+k]):
                k += 1
            if k >= min_len:
                # check if this match is a sub-match of an already recorded longer match or previous iteration
                phrase = " ".join(w2[i:i+k])
                matches.append((i, j, k, phrase))
    
    # Deduplicate / filter maximal matches
    maximal = []
    for m in matches:
        # check if m is contained in any other match with larger k or different starting point covering it
        is_sub = False
        for o in matches:
            if o != m:
                if o[0] <= m[0] and (o[0] + o[2]) >= (m[0] + m[2]) and o[2] > m[2]:
                    is_sub = True
                    break
        if not is_sub and m not in maximal:
            maximal.append(m)
    return maximal

matches = find_exact_ngrams(orig_words, rewrite_words, 6)
print(f"Maximal 6+ word overlaps found: {len(matches)}")
for m in matches:
    print(f"Length {m[2]}: '{m[3]}'")
