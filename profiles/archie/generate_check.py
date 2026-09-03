import json
import re

title = "SeaRates Update: Expanded Tracking and API Tools"
meta_title = "SeaRates Updates Week 42: New Carriers and API Features"
meta_description = "Discover SeaRates Week 42 updates with 218 supported container lines, improved Geocoding API, air tracking tweaks, and upcoming tools."

body = """Freight data moves best when software gets out of its own way.

We hit a minor milestone in week 42 with three new ocean lines added to container tracking: Danmar Lines, Ti2 Container Lines, and Famous Pacific Shipping. That brings our coverage count to 218 ocean carriers. On the API side, response handling for cached queries got a systematic tune-up, while the web interface now links directly with Route Planner to follow internal tracking numbers without manual cross-checking.

We also updated tracking mechanics across fifteen established container lines: Hapag-Lloyd, CMA CGM, Pan Continental Shipping, Medkon Lines, Maersk, Sealead Shipping, COSCO, CK Line, Admiral Container Lines, DHL Global Forwarding, Dole Ocean Cargo Express, T.S. Lines, Yang Ming, W.E.C. (West European Container) Lines, and Turkon. This work helps maintain standardized container event schemas across high-volume trade lanes, feeding clean telemetry into your multi-carrier tracking API integration.

Air cargo tracking saw parallel upgrades. API query logic for carrier servers and local caches was rewritten to cut latent calls, alongside routine maintenance for Air Canada, Delta Air Lines, and Smart Wings. Combining these legs into single monitoring pipelines advances ocean and air freight tracking consolidation for logistics operators managing multimodal supply chains.

Location routing relies on clear spatial data, which led to targeted improvements in geocoding location intelligence. The Geocoding API received stability patches for cross-platform deployment across the SeaRates suite. Developers can now filter queries specifically by seaports, airports, countries, or cities.

Schedules data received updates as well. Hoegh Autoliners added point-to-point routing support, while vessel tracking expanded for both Hoegh Autoliners and AEL. Integration protocols were refined for COSCO, Matson, and Interasia Lines across point and vessel queries.

In the top drop-down menu under References, users can find the Carrier Directory for quick access to transport providers.

Looking ahead, development continues on several upcoming projects:
- Unified Tracking System
- Logistics Map 'Warehouse' tab
- Load Calculator Web 3.0 featuring a revised interface
- Map Platform
- Geocoding API integration within Logistics Explorer
- Inbox integration spanning Logistics Explorer, Bookings, and Notifications

Real-time shipment milestone monitoring remains central to these toolsets as new releases roll out."""

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# 1. Em-dash / double hyphen
em_dashes = re.findall(r'—|--', full_text)
print("Em-dashes count:", len(em_dashes))

# 2. AI Clichés
cliches = [
    'crucial', 'pivotal', 'delve', 'testament', 'in today’s fast-paced world',
    'in today\'s fast-paced world', 'game-changer', 'seamlessly', 'in conclusion',
    'it’s not just', 'it is not just', 'unlock', 'landscape', 'beacon', 'realm', 'tapestry'
]
found_cliches = [c for c in cliches if c.lower() in full_text.lower()]
print("Found clichés:", found_cliches)

# 3. Required keywords
keywords = [
    "multi-carrier tracking API integration",
    "standardized container event schemas",
    "ocean and air freight tracking consolidation",
    "real-time shipment milestone monitoring",
    "geocoding location intelligence"
]
missing_keywords = [kw for kw in keywords if kw.lower() not in full_text.lower()]
print("Missing keywords:", missing_keywords)

# 4. Contrastive negations check
# Look for "not", "instead", "rather than", "isn't"
negations = re.findall(r'\b(not|instead of|rather than|isnt|isn\'t|wasnt|wasn\'t)\b', full_text, re.IGNORECASE)
print("Negation occurrences:", negations)

# Print sentence structures
sentences = [s.strip() for s in re.split(r'[.!?]', body) if s.strip()]
print(f"Total sentences: {len(sentences)}")

# Length limits
print("Title len:", len(title), "valid:", len(title) <= 60)
print("Meta title len:", len(meta_title), "valid:", len(meta_title) <= 60)
print("Meta desc len:", len(meta_description), "valid:", len(meta_description) <= 155)

