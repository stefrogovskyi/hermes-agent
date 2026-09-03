import json
import re

# Final revised data from Step 6
final_data = {
  "title": "SeaRates Week 23 Release: Vessel API, Geocoding & Rates",
  "meta_title": "SeaRates Week 23: Vessel Tracking API & Rate Updates",
  "meta_description": "SeaRates Week 23 updates bring a real-time vessel tracking API, Rate Management docs, expanded carrier coverage, and 140k seaport translations.",
  "body": """SeaRates released several platform updates during week 23 of 2025. This batch focuses on new API endpoints, documentation releases, and broader carrier coverage across ocean and air shipping modes.

## Real-Time Vessel Tracking API (Version 1)
Version 1 of the real-time vessel tracking API is live. Developers can access the documentation on the SeaRates Developer Portal to integrate live vessel positioning into their applications.

## Freight Rate Management API Documentation
We published new API documentation for the Rate Management System. Connecting your system directly to the API allows teams to standardise freight rate management and pricing workflows across their systems.

## Tracking Infrastructure Updates

### Container Tracking
Facility detection logic for the API was updated, and support was improved for the following shipping lines and forwarders:
* Wan Hai
* CMA CGM
* Hapag-Lloyd
* COSCO
* DHL Global Forwarding
* Volta Container Line
* Orient Overseas Container Line (OOCL)

### Air Cargo Tracking
Air cargo tracking via API enhanced support for airlines, including Sichuan Airlines, Air India, Challenge Airlines, and TAP Portugal.

### Vessel Schedules
Schedule integration was enhanced for Crowley, Seaboard Marine, and SM Line by Points, Vessel, and Port.

## Seaport Geocoding and Multilingual Support
Our team updated the seaport geocoding database by adding translations for over 140,000 seaports across eight major languages. Developers can pull these translations via the Geocoding/Autocomplete API.

## AirRates Subscription Pricing
AirRates introduced a dedicated Pricing Page. The page outlines subscription tiers and tools available for air logistics operational management.

## Platform Announcements
Upcoming features and platform announcements:
* Unified Tracking System
* Logistics Map Warehouse tab
* Parcel Tracking Web interface
* Load Calculator Web 3.0 (updated design and feature set)
* Map Platform
* Logistics Explorer inside the mobile app"""
}

# 1. Em-dash check
full_text = f"{final_data['title']}\n{final_data['meta_title']}\n{final_data['meta_description']}\n{final_data['body']}"
em_dashes = full_text.count("—") + full_text.count("--") + full_text.count("–")
print(f"1. Em-dash count: {em_dashes}")

# 2. Field length checks
print(f"2. Length checks:")
print(f"   Title: {len(final_data['title'])} chars (max 60) -> {'OK' if len(final_data['title']) <= 60 else 'EXCEEDED'}")
print(f"   Meta Title: {len(final_data['meta_title'])} chars (max 60) -> {'OK' if len(final_data['meta_title']) <= 60 else 'EXCEEDED'}")
print(f"   Meta Description: {len(final_data['meta_description'])} chars (max 155) -> {'OK' if len(final_data['meta_description']) <= 155 else 'EXCEEDED'}")

# 3. N-gram overlap check against original source
original_text = """Your support of SeaRates is appreciated. We are presently very excited about presenting fresh improvements that will better support your business needs. We continue to place a premium on enhancing our offerings. Check out the prior improvements if you're curious about the latest updates here.

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

def tokenize(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text_clean.split() if w]

orig_tokens = tokenize(original_text)
body_tokens = tokenize(final_data['body'])

def get_ngrams(tokens, n=6):
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))

orig_ngrams = get_ngrams(orig_tokens, 6)
body_ngrams = get_ngrams(body_tokens, 6)

inter = orig_ngrams.intersection(body_ngrams)
print(f"3. 6-gram overlaps found: {len(inter)}")
for idx, gram in enumerate(inter, 1):
    phrase = " ".join(gram)
    print(f"   [{idx}] {phrase}")

# Save final JSON
with open("/opt/hermes/profiles/archie/final_article.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)
