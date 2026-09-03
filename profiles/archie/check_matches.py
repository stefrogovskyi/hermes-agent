import re

original = """Your support of SeaRates is appreciated. We are presently very excited about presenting fresh improvements that will better support your business needs. We continue to place a premium on enhancing our offerings. Check out the prior improvements if you're curious about the latest updates here.

What’s new for week 23:
- We are glad to announce the launch of the Vessel Tracking API (Version 1). Find the API documentation on our Developer Portal and try real-time monitoring of vessels around the globe.
- Our team is proud to present newly added API documentation for the Rate Management System. Connect your system to the API for smooth control of your freight rates and pricing management.
- Container Tracking improvements: For API, we have updated detection logic for facilities. Also, we have improved our support of shipping lines, namely Wan Hai, CMA CGM, Hapag-Lloyd, COSCO, DHL Global Forwarding, Volta Container Line, and Orient Overseas Container Line (OOCL).
- Air Tracking updates: For API, our team has enhanced support of airlines, including Sichuan Airlines, Air India, Challenge Airlines, and TAP Portugal.
- Ship Schedules enhancements: We have improved our collaboration with shipping lines, namely Crowley and Seaboard Marine, as well as SM Line by Points, Vessel, and Port.
- Geocoding/Autocomplete improvements: We have added translation for more than 140,000 worldwide seaports into 8 major languages. Connect to the API to access our constantly growing database.
- AirRates updates: Finally, we are glad to present the Pricing Page for the AirRates platform. Choose the right tool and subscription plan for profitable management of your air logistics.

Announcements:
- Unified Tracking System
- Logistics Map ‘Warehouse’ tab
- Parcel Tracking Web
- Load Calculator Web 3.0 (new design and features)
- Map Platform
- Logistics Explorer in the Mobile App"""

rewrite = """Title: SeaRates Week 23 Release: Vessel API, Geocoding & Rates
Meta Title: SeaRates Week 23: Vessel Tracking API & Rate Updates
Meta Description: SeaRates Week 23 updates bring a real-time vessel tracking API, Rate Management docs, expanded carrier coverage, and 140k seaport translations.
Body:
"SeaRates released several platform updates during week 23 of 2025. This batch focuses on new API endpoints, documentation releases, and broader carrier coverage across ocean and air shipping modes.

## Real-Time Vessel Tracking API (Version 1)
Version 1 of the real-time vessel tracking API is live. Developers can access the documentation on the SeaRates Developer Portal to integrate live vessel positioning into their applications.

## Freight Rate Management API Documentation
We published new API documentation for the Rate Management System. Connecting an existing ERP or logistics platform directly to the API allows teams to standardise freight rate management and pricing workflows across their systems.

## Tracking Infrastructure Updates

### Container Tracking
The container tracking API received an update to its facility detection logic. Tracking performance and data mapping were updated for seven ocean carriers and forwarders:
* Wan Hai
* CMA CGM
* Hapag-Lloyd
* COSCO
* DHL Global Forwarding
* Volta Container Line
* Orient Overseas Container Line (OOCL)

### Air Cargo Tracking
Air cargo tracking support via API grew to cover four additional airlines: Sichuan Airlines, Air India, Challenge Airlines, and TAP Portugal.

### Vessel Schedules
Schedule integrations were expanded for Crowley, Seaboard Marine, and SM Line. Search functionality now handles data queries filtered by points, vessel, and port.

## Seaport Geocoding and Multilingual Support
Our team updated the seaport geocoding database by adding translations for over 140,000 seaports across eight major languages. Developers can pull these translations via the Geocoding/Autocomplete API.

## AirRates Subscription Pricing
AirRates introduced a dedicated Pricing Page. The page outlines subscription tiers and tools available for air logistics operational management.

## Platform Announcements
Work continues on several additional products and design upgrades across the platform:
* Unified Tracking System
* Logistics Map Warehouse tab
* Parcel Tracking Web interface
* Load Calculator Web 3.0 (updated design and feature set)
* Map Platform
* Logistics Explorer inside the mobile app" """

def tokenize(text):
    return re.findall(r'\b[\w\.]+\b', text)

orig_tokens = tokenize(original)
rew_tokens = tokenize(rewrite)

# Find longest matching substrings of tokens
from difflib import SequenceMatcher

sm = SequenceMatcher(None, [t.lower() for t in orig_tokens], [t.lower() for t in rew_tokens])
blocks = sm.get_matching_blocks()

print("Matching Blocks >= 5 tokens:")
for block in blocks:
    if block.size >= 5:
        orig_match = " ".join(orig_tokens[block.a : block.a + block.size])
        rew_match = " ".join(rew_tokens[block.b : block.b + block.size])
        print(f"Length {block.size}:")
        print(f"  Orig: {orig_match}")
        print(f"  Rew:  {rew_match}")
        print()

