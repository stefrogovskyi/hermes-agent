import json
import re

json_data = {
  "title": "SeaRates October 2024 Release Notes",
  "meta_title": "SeaRates Development Update: October 2024",
  "meta_description": "SeaRates October 2024 updates bring rail tracking to LandRates, 10 new airlines, predictive ETA algorithms, and Virtual Office web integration.",
  "body_markdown": """Monthly updates to the SeaRates platform bring practical features and performance tweaks requested by users. The October 2024 release expands carrier integrations, updates tracking logic across web and API tools, and introduces new setup options for Virtual Office. Signing up for the SeaRates newsletter keeps you notified about every monthly build.

### Rail and Air Cargo Tracking

Rail tracking is now active on LandRates.com. Users entering carrier tracking numbers can view real-time cargo locations, movement logs, shipment statuses, route details, and logistics events.

Air cargo tracking adds support for ten additional carriers: Air Moldova, Mahan Air, Transcarga International Airways, Vietravel Airlines, Lion Airlines, Super Air Jet, Thai Lion Air, Wings Air, Air Arabia Maroc, and Challenge Airlines Malta. Total airline coverage now reaches 435 carriers. For API integrations, developers can pass a `cache_expires` parameter and utilize new logic that generates extensive descriptions for logistics events.

### Tracking System and Parcel Services

The web tracking interface introduces Exceptions and Demurrage tabs inside the shipping card, while the main menu adds Map, Notifications, Analytics, and Calendar tabs. On the API side, determination logic for a container's current location has been updated. A new predictive ETA algorithm factors in AIS data alongside parameters for Storage, Demurrage, and Detention fees. Processing logic for predictive ETA estimation in the Tracking History API has also been updated.

Parcel Tracking API responses now include estimated and actual departure and arrival dates, a smart Autodetect service, and the `AUTODETECT_CANT_DETECT_PARCEL_COMPANY` status code. A complete list of supported parcel carriers is published on the Developer Portal.

### Schedules, Maps, and Geocoding

Ship Schedules for both "by Port" and "by Points" queries now support five new carriers: Hapag-Lloyd, CK Line, Dong Young, Culines, and Sinokor. A beta version of the Geocoding API is available in the Developer Portal along with technical documentation.

On the Logistics Map, open vehicle unit cards and vehicle list cards under the Transport tab now display the carrier's name and logo. Distance and Time API V. 3.0 allows developers to specify IATA and ICAO codes in queries for departure and arrival locations, with updated documentation posted on the Developer Portal.

### Mobile App and Virtual Office

Android users running the SeaRates mobile app can authenticate without being redirected to the SeaRates website. Android logins now support Google and Apple account authorization, and both the Profile and Settings sections have been refreshed.

Virtual Office web integration allows platform operators to embed registration and authorization directly on their own websites, giving clients interface access through a Dashboard. Integration code is available on the Developer Portal. Platform owners using the web-integrated version can view registered user profiles inside the Counterparties management panel.

On the main Virtual Office web interface, clicking map points on the Dashboard world map navigates directly to corresponding bookings or requests. The Transport tab now displays shipping line logos based on SCAC codes, with options to edit, add, or update photos when modifying transport unit data. The Counterparties section allows displaying registered platform users in a general list and applying multiple grouped filters simultaneously.

### Quoting and System Tools

Selecting a City location type on the Request a Quote form updates nearest port selection logic and provides a ZIP code field for shipping and warehousing options. The upgraded Find a Tool page lists SeaRates digital tools and accepts direct IT quote requests for Web Access, Web Integration, or API integrations."""
}

text_to_check = json.dumps(json_data)

# Rule 1: No em-dashes —, –, --
dashes = re.findall(r'[—–]|--', text_to_check)
print("Rule 1 Em-dashes found:", dashes)

# Rule 2: Forbidden clichés
cliches = [
    "delve into", "testament to", "crucial role", "in today's world", 
    "it is worth noting", "game-changer", "seamless", "landscape", 
    "beacon", "unlocking", "spearheading", "in conclusion", "important to note",
    "comprehensive", "robust", "empower", "elevate", "realm", "tapestry"
]
found_cliches = [c for c in cliches if c in text_to_check.lower()]
print("Rule 2 Clichés found:", found_cliches)

# Rule 5: Contrastive negation
negations = re.findall(r'\b(instead of|rather than|\bnot\b.*\bbut\b)', text_to_check.lower())
print("Rule 5 Negations found:", negations)

# Rule 9: Connectors
connectors = ["that's why", "furthermore", "in addition", "moreover", "additionally", "consequently", "therefore"]
found_connectors = [c for c in connectors if c in text_to_check.lower()]
print("Rule 9 Connectors found:", found_connectors)

# Check lengths
print("Title length:", len(json_data["title"]))
print("Meta title length:", len(json_data["meta_title"]))
print("Meta description length:", len(json_data["meta_description"]))

# Check single sentence paragraphs
paras = [p.strip() for p in json_data["body_markdown"].split("\n\n") if p.strip() and not p.strip().startswith("#")]
single_sent_paras = []
for p in paras:
    # sentence count
    sents = [s for s in re.split(r'[.!?]+', p) if s.strip()]
    if len(sents) < 2:
        single_sent_paras.append(p)

print("Single sentence paragraphs count:", len(single_sent_paras))

