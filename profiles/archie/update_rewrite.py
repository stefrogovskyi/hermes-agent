import json

data = {
  "title": "SeaRates Week 41, 2024: Logistics Map Updates & More",
  "meta_title": "SeaRates Week 41 2024: Virtual Office Transport Management",
  "meta_description": "Discover SeaRates Week 41 2024 updates with SCAC-based shipping line logo display, freight quote nearest port selection, and Virtual Office tools.",
  "body_markdown": """SeaRates rolled out its Week 41 updates for 2024, focusing on clearer visual identification, streamlined quotation workflows, and expanded Virtual Office controls.

Logistics Map updates bring carrier visual identities directly into vehicle tracking. Cards across both the vehicle list and open vehicle unit views now display the carrier name alongside their official logo. Confirmation emails sent after submitting requests now link directly to transport unit details within Logistics Map, allowing team members to jump straight from an inbox notification to live tracking data.

Data management inside Virtual Office received several functional adjustments. Transport records now support editing, swapping, or appending extra images during record updates. Shipping line logos automatically appear based on SCAC codes. In the Counterparties section, users can group multiple active filters together to narrow down records faster. Operations involving leasing companies and providers ('by Points') have been refined, including specific updates for OOCL and X-Press.

Quoting workflows now handle city-level origin and destination selections more intelligently. When requesting a sea freight quote with a City-type location and leaving the port field empty, the system automatically identifies and assigns the nearest port. Elsewhere on the platform, dedicated landing page documentation for both the Smart Documents application and its corresponding API has been added to the Integration menu.

Recent platform announcements also highlight updates across several tools and services:

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
}

with open('/opt/hermes/profiles/archie/final_rewrite.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
