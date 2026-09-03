import re
import json

title = "SeaRates Week 35: Air Cargo, Tracking, and API Updates"
meta_title = "SeaRates Product Release Notes: Week 35, 2024 Updates"
meta_description = "SeaRates Week 35 updates include support for 8 new airlines in Air Cargo Tracking, updated autodetection APIs, and 3D Load Calculator enhancements."

body_markdown = """SeaRates Week 35 updates bring tracking additions across air and sea freight, API routing adjustments, and tool upgrades.

### Air Cargo Tracking

Eight new airlines are now supported in Air Cargo Tracking:
- Air Madagascar
- LAM Mozambique Airlines
- Nauru Airlines
- Air Austral
- MIAT Mongolian Airlines
- US-Bangla Airlines
- Canadian North
- Global Air

Data processing and provider integrations were also refined for ten existing carriers: Atlas Air, Singapore Airlines, United Airlines, Qatar Airways, Finnair, Emirates, TAP Portugal, Air China Cargo, Air India, and Southwest Airlines.

### Tracking System and Schedules

API autodetection now uses updated logic for identifying shipment types, determining shipping lines, and routing freight.

Provider handling was enhanced for nine ocean container lines:
- CMA CGM
- Pan Continental Shipping
- Yang Ming
- Ocean Network Express (ONE)
- Hapag-Lloyd
- Orient Overseas Container Line (OOCL)
- COSCO
- Evergreen
- Hyundai Merchant Marine (HMM)

In Ship Schedules, provider connections were updated for Namsung and Evergreen 'by Points'.

### Load Calculator and Logistics Explorer

The Load Calculator now features a loading animation. Users can step through the visualization using Play and Pause controls. Cargo names now appear directly inside the 3D calculation view.

Logistics Explorer now calculates CO2 emissions across all transport modes. The Booking API received an update, and a new request structure was added for Logistics Explorer API Version 3. Detailed documentation is published on the Developer Portal.

### General Updates and Announcements

Platform updates include:
- Help Center: simplified category and question layout.
- Contact Us Form: added an option to request a phone callback by clicking buttons across website pages.
- API Upgrades: updated Contact Us API and Ship Schedules API.
- New Web Pages: added dedicated Vendors - Shipping Lines and Affiliate Program pages.

Current tool and API versions:
- Geocoding API / Autocomplete service Version 0.8
- New Version of Route Planner API
- 'Transport' tab in the Logistics Map tool
- Freight Index 1.0
- Mobile App Version 1.2 with Request System feature
- Load Calculator Version 2.2
- Booking System Version 1.1
- Parcel Tracking API
- Rail Tracking API
- Rail Tracking Web on LandRates.com
- Map platform"""

# 1. Em-dash check
full_text = f"{title}\n{meta_title}\n{meta_description}\n{body_markdown}"
em_dashes = full_text.count("—") + full_text.count("--")
print(f"EM-DASH COUNT: {em_dashes}")

# 2. Length check
print(f"TITLE LENGTH: {len(title)} (Max 60)")
print(f"META_TITLE LENGTH: {len(meta_title)} (Max 60)")
print(f"META_DESCRIPTION LENGTH: {len(meta_description)} (Max 155)")

# 3. 6-gram overlap check against original
with open('/opt/hermes/profiles/archie/original_article_clean.txt', 'r') as f:
    orig_text = f.read()

def normalize_and_tokenize(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    tokens = text_clean.split()
    return tokens

orig_tokens = normalize_and_tokenize(orig_text)
rewrite_tokens = normalize_and_tokenize(body_markdown)

orig_6grams = set(tuple(orig_tokens[i:i+6]) for i in range(len(orig_tokens)-5))
rewrite_6grams = [tuple(rewrite_tokens[i:i+6]) for i in range(len(rewrite_tokens)-5)]

matching_6grams = []
for gram in rewrite_6grams:
    if gram in orig_6grams:
        matching_6grams.append(" ".join(gram))

print(f"MATCHING 6-GRAMS COUNT: {len(matching_6grams)}")
if matching_6grams:
    print("Matching 6-grams examples:")
    for m in matching_6grams[:10]:
        print(" -", m)

# Save result for DOCX generation
data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body_markdown": body_markdown
}
with open('/opt/hermes/profiles/archie/final_article.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
