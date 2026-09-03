import re

title = "SeaRates Week 24, 2025 Release Notes"
meta_title = "SeaRates Week 24 2025 Product Updates"
meta_desc = "Discover SeaRates Week 24, 2025 updates with DB Schenker road tracking and carbon emissions route mapping for multimodal supply chain visibility."

body = """SeaRates Week 24, 2025 release notes cover updates across API integrations and platform management.

Road and Ocean Tracking Upgrades

Adding DB Schenker road tracking brings our supported road carriers on the real-time freight tracking API to 4. Road Tracking API requests now accept the 'cargo_units' field, capturing container numbers, ULD (Unit Load Device) data, or other cargo details.

For ocean freight, our container tracking API enhances coverage for four shipping lines:
- Orient Overseas Container Line (OOCL)
- COSCO
- Hapag-Lloyd
- Maersk

Vessel Tracking API v1.0 improves vessel search logic alongside AIS vessel tracking data acquisition. Terminal Tracking API expands global location support with the addition of Nhava Sheva Freeport Terminal.

Air Shipping and Multimodal Routes

Air Tracking API improves integration across Cathay Pacific Airways, SpiceJet, Singapore Airlines, and other airlines.

To improve multimodal supply chain visibility, the Distance and Time API introduces the 'sections' field. Designed for ferry transport, this field describes each route segment and specifies transport type as either truck or ferry. Each section details distance, transit time, plus average speed metrics.

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

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== VERIFICATION ===")
print("Title length:", len(title), "(< 60)")
print("Meta title length:", len(meta_title), "(< 60)")
print("Meta desc length:", len(meta_desc), "(< 155)")

# Dashes check
em_dash = "—" in full_text or "\u2014" in full_text
double_hyphen = "--" in full_text
en_dash = "–" in full_text or "\u2013" in full_text
print("Em-dash present:", em_dash)
print("Double-hyphen present:", double_hyphen)
print("En-dash present:", en_dash)

# Regex rule-of-three detector
three_items = re.findall(r'\b[\w\s\(\)\'-]+,\s+[\w\s\(\)\'-]+,?\s+and\s+[\w\s\(\)\'-]+\b', full_text)
print("Rule-of-three matches found:", three_items)

# Keywords
keywords = [
    "real-time freight tracking API",
    "multimodal supply chain visibility",
    "AIS vessel tracking data",
    "DB Schenker road tracking",
    "container tracking API",
    "carbon emissions route mapping"
]
for kw in keywords:
    print(f"Keyword '{kw}':", kw.lower() in full_text.lower())

# Facts
facts = [
    "DB Schenker", "cargo_units", "sections", "Nhava Sheva Freeport Terminal",
    "Orient Overseas Container Line", "OOCL", "COSCO", "Hapag-Lloyd", "Maersk",
    "Cathay Pacific", "SpiceJet", "Singapore Airlines",
    "AirRates", "CO2 Calculator", "Ship Schedules", "Freight Index", "DFA Membership",
    "Unified Tracking System", "Warehouse", "Load Calculator Web 3.0", "Map Platform", "Logistics Explorer"
]
for f in facts:
    if f.lower() not in full_text.lower():
        print(f"MISSING FACT: {f}")
print("Fact check complete.")
