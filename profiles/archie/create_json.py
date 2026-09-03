import json

data = {
  "title": "SeaRates Week 47 Updates: Tracking, Schedules & APIs",
  "meta_title": "SeaRates Week 47 Updates | Logistics & Tracking Tools",
  "meta_description": "Discover SeaRates Week 47 updates: container tracking, air cargo coverage, ship schedules, API enhancements, and global land freight rate search.",
  "body_markdown": """## Ocean and Air Tracking Upgrades

Managing freight across global routes requires clear, immediate details. In the web version of the Tracking System, new logo tooltips display carrier names on hover, paired with an updated Filter to sort active shipments quickly. Direct data collaboration has also expanded across four ocean carriers: Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL. Teams using supply chain visibility tools gain immediate clarity on active legs.

Air transport coverage broadens as well. Air cargo tracking integrations now include Azerbaijan Airlines and Air Arabia Abu Dhabi, pulling direct flight status updates into the main dashboard.

## Expanded Vessel Schedules and API Logic

Planning sea routes depends on reliable departure and arrival timelines. Vessel sailing schedules automation now covers KambaraKisen, Culines, and Sinokor by Vessel, along with KambaraKisen by Port.

On the developer side, Parcel Tracking for the API version features upgraded autodetect logic. The system identifies tracking number formats automatically, streamlining data retrieval for teams running a real-time container tracking API interface.

## Interface Fine-Tuning and Land Freight Options

Small workflow adjustments improve daily site navigation and rates discovery:

* Search Filter customization now includes a button hover color option for tailored visual styling.
* Container Tracking, Distance & Time, and Load Calculator pages now feature dedicated FAQ sections.
* LandRates.com added a Special Offers section to its main page, giving shippers a direct tool for land freight rate search and comparison worldwide.

## Upcoming Platform Features and Releases

Development continues across several core modules, with upcoming releases including:

* Calendar tab in the Tracking System tool
* New Version of Route Planner API
* Freight Index 1.0
* Mobile App Version 1.2 with Request System feature
* Load Calculator Version 2.2
* Booking System Version 1.1
* Map platform"""
}

with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

print("Wrote output.json")
