import json

with open("/opt/hermes/profiles/archie/draft_rewrite.json") as f:
    draft = json.load(f)

body = draft["body_markdown"]

# Apply targeted replacements
replacements = [
    (
        "The upgraded Find a Tool page lists SeaRates digital tools and accepts direct IT quote requests for Web Access, Web Integration, or API integrations.",
        "The refreshed Tool Finder directory displays SeaRates digital products and takes direct custom IT quotes covering Web Access, Web Integration, or API connectivity."
    ),
    (
        "open vehicle unit cards and vehicle list cards under the Transport tab now display the carrier's name and logo.",
        "open vehicle unit cards and vehicle list cards under the Transport tab now display carrier branding alongside the company name."
    ),
    (
        "Distance and Time API V. 3.0 allows developers to specify IATA and ICAO codes in queries for departure and arrival locations, with updated documentation posted on the Developer Portal.",
        "Distance and Time API V. 3.0 lets developers include IATA and ICAO location identifiers when querying departure or arrival points, supported by refreshed Developer Portal documentation."
    ),
    (
        "For API integrations, developers can pass a `cache_expires` parameter and utilize new logic that generates extensive descriptions for logistics events.",
        "For API integrations, developers can pass a `cache_expires` parameter and utilize new logic that generates detailed event summaries across shipment milestone logs."
    ),
    (
        "Processing logic for predictive ETA estimation in the Tracking History API has also been updated.",
        "Response handling algorithms for calculated arrival estimates in the Tracking History API have also been refined."
    ),
    (
        "the main menu adds Map, Notifications, Analytics, and Calendar tabs.",
        "the main navigation bar incorporates dedicated tabs for Map, Notifications, Analytics, and Calendar."
    )
]

for old_str, new_str in replacements:
    if old_str in body:
        body = body.replace(old_str, new_str)
    else:
        print("WARNING: Could not find substring to replace:", old_str[:40])

draft["body_markdown"] = body

with open("/opt/hermes/profiles/archie/draft_rewrite.json", "w") as f:
    json.dump(draft, f, indent=2, ensure_ascii=False)

print("Fixes applied to draft_rewrite.json.")
