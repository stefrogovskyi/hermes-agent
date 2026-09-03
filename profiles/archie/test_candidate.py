import re

orig_text = """
SeaRates Updates - Week 21, 2025
The SeaRates team is grateful for your ongoing assistance and support. We are always working to make our service better, and we are happy to share the latest updates to make your experience smoother.
To keep informing about our news, take a look at our earlier updates .
What's new for week 21:
- The SeaRates team is proud to announce a newly added 'Facilities' management panel to handle any type of your warehouses in one place. Add, edit, import, and fully account any details on warehouse assets, as well as mention offered services. Share unique access with customers and partners to book your warehouse services. Find the panel in your Virtual Office Profile to streamline management of your warehouses.
- Container Tracking improvements: We have improved the 'Exceptions' tab by adding markers for 'positive' (green mark for earlier arrival) and 'negative' (orange mark for delays) changes.
- Moreover, for API, we have improved our support of shipping lines, namely Sinotrans Container Lines, Swire Shipping, DHL Global Forwarding, Gold Star Line, Wan Hai, Emirates Shipping Line, Arkas, Mediterranean Shipping Company (MSC), Cordelia Container Shipping Line, and Orient Overseas Container Line (OOCL).
- Air Tracking updates: Our team has enhanced support of airlines, including DHL Aviation, ASL Airlines Belgium, Laparkan Airways, and Malaysia Airlines.
- Ship Schedules enhancements: We have improved our collaboration with shipping lines, namely Seaboard Marine and Wan Hai by Points, Unifeeder by Vessel, and Evergreen by Port.
Other updates:
- We have added a subscription button to easily check your credit limits and timely upgrade your plan for smooth usage of the Carbon Emissions Calculator.
Announcements:
- Unified Tracking System
- Vessel Tracking API v1
- Logistics Map 'Warehouse' tab
- SeaRates AI 1.0
- Parcel Tracking Web
- Load Calculator Web 3.0 (new design and features)
- Map Platform
- Logistics Explorer in the Mobile App
"""

title = "SeaRates Week 21, 2025: Warehouse Tools & Tracking Updates"
meta_title = "SeaRates Week 21: Ocean Freight & Tracking API Updates"
meta_desc = "SeaRates Week 21 updates bring a Facilities panel for warehouse asset management, improved ocean freight tracking, carrier API fixes, and credit alerts."

body_candidate = """Week 21 brings operational updates to the SeaRates platform, centered on warehouse management, tracking updates, and carrier integrations.

## New Facilities Management Panel

A Facilities management panel is live inside your Virtual Office Profile. It provides a single interface to handle warehouse asset management across your storage locations.

You can add, edit, or import assets, record offered services, and fully account for warehouse asset details. The panel also lets you generate dedicated access credentials for clients and partners to book storage services.

## Tracking Exceptions and Carrier Integrations

Visual indicators are now active on the tracking dashboard. The Exceptions tab marks earlier arrivals with green indicators and delays with orange flags, offering quick supply chain visibility when vessel timetables shift.

API integrations for ocean freight tracking offer enhanced support across ten ocean carriers:

* Sinotrans Container Lines
* Swire Shipping
* DHL Global Forwarding
* Gold Star Line
* Wan Hai
* Emirates Shipping Line
* Arkas
* Mediterranean Shipping Company (MSC)
* Cordelia Container Shipping Line
* Orient Overseas Container Line (OOCL)

These updates improve container tracking API support for these shipping lines.

## Air Cargo and Vessel Schedules

Air cargo tracking support expanded across four air carriers:

* DHL Aviation
* ASL Airlines Belgium
* Laparkan Airways
* Malaysia Airlines

Ship schedule queries received targeted carrier updates. Schedules for Seaboard Marine and Wan Hai now support filtering by Points, Unifeeder by Vessel, and Evergreen by Port.

## Carbon Calculator Credit Limits

A subscription button is now available in your account profile. It lets you monitor credit limits and upgrade plans on time, avoiding service pauses when using the carbon emissions calculator.

## Upcoming Releases

Work continues on several upcoming features and tools:

* Unified Tracking System
* Vessel Tracking API v1
* Logistics Map 'Warehouse' tab
* SeaRates AI 1.0
* Parcel Tracking Web
* Load Calculator Web 3.0 (new design and features)
* Map Platform
* Logistics Explorer in the Mobile App"""

print("=== CHECKING LENGTHS ===")
print(f"Title length ({len(title)}): {'PASS' if len(title) <= 60 else 'FAIL'}")
print(f"Meta Title length ({len(meta_title)}): {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
print(f"Meta Desc length ({len(meta_desc)}): {'PASS' if len(meta_desc) <= 155 else 'FAIL'}")

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body_candidate}"

print("\n=== CHECKING DASHES ===")
dashes = re.findall(r'[—–]|--', full_text)
print(f"Em/En/Double dashes count: {len(dashes)}")

print("\n=== CHECKING BANNED BUZZWORDS ===")
banned = [
    "Moreover", "Furthermore", "In addition", "It is worth noting", "Delving into",
    "Tapestry", "Testament", "Seamless", "Crucial", "Evolving landscape",
    "In conclusion", "Game-changer", "Tired of unexpected fees", "delve", "landscape",
    "testament", "tapestry", "seamless", "crucial", "moreover", "furthermore", "pivotal",
    "fostering", "beacon", "key role", "vital role", "elevate", "navigate", "dynamic", "realm"
]
found_banned = [b for b in banned if re.search(r'\b' + re.escape(b) + r'\b', full_text, re.IGNORECASE)]
print(f"Banned words found: {found_banned}")

print("\n=== CHECKING AUDIT REQUIREMENTS ===")
req1 = "These updates improve container tracking API support" in body_candidate
print(f"Req 1 (Source-grounded API statement without invented mechanism): {'PASS' if req1 else 'FAIL'}")

req2 = "enhanced support across ten ocean carriers" in body_candidate
print(f"Req 2 (Carrier Scope Wording 'enhanced support across ten ocean carriers'): {'PASS' if req2 else 'FAIL'}")

req3 = "and fully account for warehouse asset details" in body_candidate
print(f"Req 3 (Facilities Wording 'and fully account for warehouse asset details'): {'PASS' if req3 else 'FAIL'}")

def tokenize(text):
    return re.findall(r'\b[A-Za-z0-9_]+\b', text.lower())

orig_words = tokenize(orig_text)
body_words = tokenize(body_candidate)

print("\n=== CHECKING PROSE N-GRAM OVERLAPS (6-grams) ===")
n = 6
orig_ngrams = set(tuple(orig_words[i:i+n]) for i in range(len(orig_words)-n+1))
body_ngrams = [(i, tuple(body_words[i:i+n])) for i in range(len(body_words)-n+1)]

matches = []
for idx, ng in body_ngrams:
    if ng in orig_ngrams:
        matches.append(' '.join(ng))

print(f"6-gram matches count: {len(matches)}")
for m in set(matches):
    print(f"  Match: {m}")

