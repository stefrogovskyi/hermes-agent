import json
import re

output = {
  "title": "SeaRates Freight Logistics Updates: Week 1, 2025",
  "meta_title": "SeaRates Freight Logistics Updates: Week 1, 2025",
  "meta_description": "SeaRates Week 1 2025 freight logistics updates cover real-time container tracking, air cargo integration, and ship sailing schedules.",
  "body_markdown": """The first platform release of 2025 expands carrier connectivity and updates core tools across ocean, air, and land freight workflows.

## Ocean and Air Cargo Tracking

Data integrations have been updated to support real-time container tracking and air cargo tracking integration across several major global lines.

Ocean carriers with updated tracking feeds:
* Kuehne + Nagel (KN)
* Ignazio Messina
* Hyundai Merchant Marine (HMM)
* Maersk

Air freight tracking updates cover three air carriers: DHL Aviation, Silk Way West Airlines, and China Southern Airlines.

## Ship Sailing Schedules

Vessel routing feeds for ship sailing schedules received specific updates across three carriers:
* Yang Ming: updated data handling under the 'by Points' tab.
* Namsung: refreshed route feeds under the 'by Vessel' tab.
* PIL: revised schedules under the 'by Vessel' tab.

## Web Tools and Platform Roadmap

Recent development work includes updates to public web tools and system integrations:

* Load Calculator Web 3.0: released with a new layout and updated calculation features.
* AirRates App: launched for mobile access to air freight services.
* CO2 Calculator: integrated with SeaRates Autocomplete for faster location lookup.
* Request a Quote Form: streamlined field entry for price inquiries.
* Logistics Map and Map Platform: updated map layers and location displays.
* Unified Tracking System and Parcel Tracking Web: core infrastructure maintenance for multi-modal tracking.

These changes form part of ongoing efforts to improve supply chain visibility 2025 for shippers and freight forwarders."""
}

json_str = json.dumps(output, indent=2)

# Verify valid JSON
parsed = json.loads(json_str)

# Assertions
assert len(parsed["title"]) <= 60
assert len(parsed["meta_title"]) <= 60
assert len(parsed["meta_description"]) <= 155

# Check zero em-dashes
full_text = parsed["title"] + parsed["meta_title"] + parsed["meta_description"] + parsed["body_markdown"]
assert "—" not in full_text
assert "--" not in full_text

print("JSON payload validation passed successfully!")
print("JSON Output:")
print(json_str)
