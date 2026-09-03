import re

cand_text = """Title: SeaRates Week 41, 2024: Logistics Map Updates & More
Meta Title: SeaRates Week 41 2024: Virtual Office Transport Management
Meta Description: Discover SeaRates Week 41 2024 updates with carrier logo SCAC tracking, freight quote nearest port selection, and Virtual Office transport management.

Body Markdown:
SeaRates rolled out its Week 41 updates for 2024, focusing on clearer visual identification, streamlined quotation workflows, and expanded Virtual Office controls.

Logistics Map updates bring carrier visual identities directly into vehicle tracking. Cards across both the vehicle list and open vehicle unit views now display the carrier name alongside their official logo. Confirmation emails sent after submitting requests now link directly to transport unit details within Logistics Map, allowing team members to jump straight from an inbox notification to live tracking data.

Data management inside Virtual Office received several functional adjustments. Transport records now support editing, swapping, or appending extra images during record updates. Shipping line logos automatically appear based on SCAC codes. In the Counterparties section, users can group multiple active filters together to narrow down records faster. Operations involving leasing companies and providers ('by Points') have been refined, including specific updates for OOCL and X-Press.

Quoting workflows now handle city-level origin and destination selections more intelligently. When requesting a sea freight quote with a City-type location and leaving the port field empty, the system automatically identifies and assigns the nearest port. Elsewhere in the platform, new content for the Smart Documents tool and the Smart Documents API landing page is now accessible under the Integration menu.

Looking ahead, several updates and tools are in active development or queued for upcoming releases:

* New features for Air Cargo Tracking Web Version
* Geocoding API / Autocomplete service Version 0.8
* New version of Route Planner API
* Freight Index 1.0
* Mobile App Version 1.2 featuring the Request System
* Load Calculator Version 2.2
* Booking System Version 1.1
* Rail Tracking API
* Rail Tracking Web on LandRates.com
* Map platform
* Unified Tracking System WEB"""

# Check Em-Dashes
em_dashes = cand_text.count('—') + cand_text.count('–')
print(f"Em-dashes count: {cand_text.count('—')}")
print(f"En-dashes count: {cand_text.count('–')}")

# Check Banned Cliché Words
# Common AI cliché words: delve, pivotal, seamless, landscape, tapestry, testaments, beacon, realm, vital, foster, elevate, game-changer, unlock, robust, leverage, paramount, multifaceted, dynamic, testament, digital landscape, look no further, etc.
banned_words = [
    'delve', 'pivotal', 'seamless', 'seamlessly', 'landscape', 'tapestry', 'testament', 
    'beacon', 'realm', 'vital', 'foster', 'elevate', 'game-changer', 'game changer', 
    'unlock', 'robust', 'leverage', 'paramount', 'multifaceted', 'dynamic', 'comprehensive',
    'revolutionize', 'ever-evolving', 'delving', 'subsequent', 'moreover', 'furthermore',
    'in conclusion', 'synergy', 'transformative', 'cutting-edge'
]

found_banned = []
for bw in banned_words:
    matches = re.findall(r'\b' + bw + r'\b', cand_text, re.IGNORECASE)
    if matches:
        found_banned.append((bw, len(matches)))

print("\n--- Banned AI Cliché Words Check ---")
print(found_banned if found_banned else "None found!")

