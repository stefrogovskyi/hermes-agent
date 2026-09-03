import json
import re

json_data = {
    "title": "SeaRates Week 41: Tracking Upgrades and Platform Updates",
    "meta_title": "SeaRates Week 41 Updates: Ocean & Air Tracking News",
    "meta_description": "SeaRates Week 41 updates expand ocean freight tracking, air cargo track and trace, ship schedules, and announce upcoming integrations.",
    "body_markdown": """Logistics works best when moving cargo feels simple, transparent, and connected. For week 41 of 2025, SeaRates brings another round of technical upgrades focused on keeping freight visibility clear and accessible across every leg of transit.

### Expanded Ocean Freight Tracking

Staying on top of cargo movements requires accurate ocean freight tracking that connects directly to the carriers managing your goods. We have updated our container tracking integrations across seventeen shipping lines and leasing companies:

* Marguisa Shipping Lines
* Asyad Line
* Maxicon Container Line (MCL)
* Ocean Network Express (ONE)
* Cordelia Container Shipping Line
* Maritime Carrier Shipping (MACS)
* Turkon
* Interasia Lines
* Hapag-Lloyd
* Crowley Maritime
* Arkas
* Mariana Express Lines (MELL)
* CMA CGM
* Maersk
* Yang Ming
* Evergreen
* Swire Shipping

These improvements give shippers and freight forwarders reliable real-time container visibility across global trade lanes.

### Air Tracking Enhancements

Air freight operations demand quick turnaround times and precise status updates. To keep your air cargo track and trace reliable, we have refreshed airline integration support for:

* Oman Air
* Delta Air Lines
* Turkish Airlines
* Swiss International Air Lines
* Smart Wings
* Etihad Cargo

### Ship Schedules Improvements

Schedules shift quickly in maritime transport. Better partner coordination helps maintain overall supply chain transparency when planning voyages ahead of time. Our team improved schedule integration data for:

* COSCO
* Maersk by Points

### Upcoming Announcements and Integrations

We are also moving forward with new system developments to strengthen our entire platform ecosystem:

* **Unified Tracking System:** Centralized monitoring across multiple transport modes.
* **Logistics Map 'Warehouse' tab:** Dedicated location mapping for storage facilities.
* **Load Calculator Web 3.0:** Fresh design and upgraded calculation features.
* **Map Platform:** Direct mapping tools built for route visualization.
* **Geocoding API:** Integrated into Logistics Explorer for precise location lookup.
* **Inbox Integration:** Streamlined communications linked with Logistics Explorer, Bookings, and Notifications.

Each update brings your everyday shipping tasks into a cleaner, single view."""
}

from verify import check_rules

errors = check_rules(json_data)
print("Errors found:", errors)
print("Title length:", len(json_data["title"]))
print("Meta Title length:", len(json_data["meta_title"]))
print("Meta Description length:", len(json_data["meta_description"]))
