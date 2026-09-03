import json
import re

# Original draft from prompt context
original_draft = """Title: SeaRates Updates: Week 39 Freight Tooling Enhancements
Meta Title: SeaRates Updates: Week 39, 2025 Platform Enhancements
Meta Description: Explore SeaRates Week 39 updates, including De Well Group tracking, Rate Management upgrades, carrier filters, and new schedule integrations.

Body:
## Container Tracking Upgrades

The Container Tracking tool now supports De Well Group, bringing the platform total to 215 supported shipping lines.

On the web version at searates.com/container/tracking/, importing a bulk Excel file of tracking numbers automatically generates shipment cards in your Dashboard. Free subscription users can now view their daily and monthly usage limits directly within the interface. Additionally, we updated the response formation logic for the History API.

We also refined data integration and collaboration with 21 ocean carriers: Maersk, Hapag-Lloyd, Interasia Lines, SITC Container Lines, DHL Global Forwarding, Swire Shipping, Orient Overseas Container Line (OOCL), Turkon, Wan Hai, Ocean Network Express (ONE), CEVA Logistics, COSCO, Yang Ming, Sealead Shipping, Sinokor, Samudera Shipping Line, Mediterranean Shipping Company (MSC), National Shipping of America, UWL, Trans Asian Shipping Services, and Wallenius Wilhelmsen.

## Air Tracking and Ship Schedules Updates

Air Tracking API expanded carrier support, adding integrations for Etihad Cargo and United Airlines.

Ship Schedules improved collaboration with three shipping lines. Integrations with Sinotrans and Crowley now operate by Points, while Ignazio Messina updates by Vessel.

## Rate Management System Enhancements

We released an updated version of the Rate Management System for FCL and LCL tariffs. Users can create multiple tariff types across multiple ports, selecting whether tariffs apply to import, export, or both direction options.

Tariffs now include an explicit validity period. We also added a dedicated Directory section listing all available tariffs for quick reference.

## Logistics Map Transport Options

Logistics Map Transport added a new Carrier filter. You can select one or multiple carriers from the dropdown list to isolate their active transport offers on the map.

We also added a 'To be nominated' filter option. This displays all transport entries on the map that have not yet been assigned to a specific carrier.

## Upcoming Releases

Our engineering team is actively working on several updates scheduled for future rollouts:

- Unified Tracking System
- Logistics Map 'Warehouse' tab
- Load Calculator Web 3.0 with an updated design and expanded features
- Map Platform
- Geocoding API integrated into Logistics Explorer
- Inbox integration connecting Logistics Explorer, Bookings, and Notifications"""

# Candidate Remediated Content
remediated_title = "SeaRates Updates: Week 39 Freight Tooling Enhancements"
remediated_meta_title = "SeaRates Updates: Week 39, 2025 Platform Enhancements"
remediated_meta_description = "Explore SeaRates Week 39 updates, including De Well Group tracking, Rate Management upgrades, carrier filters, and new schedule integrations."

remediated_body = """## Container Tracking Upgrades

The Container Tracking tool now supports De Well Group, bringing the platform total to 215 supported shipping lines.

Within the Container Tracking web interface, importing a bulk Excel file of tracking numbers automatically generates shipment cards in your Dashboard. Free subscription users can now view their daily and monthly usage limits directly within the interface. System updates also refined response formation logic for the History API.

Data integration and collaboration were enhanced across 21 ocean carriers. Supported global ocean lines include MSC, Maersk, Ocean Network Express (ONE), COSCO, Hapag-Lloyd, and OOCL. Logistics and transport providers include DHL Global Forwarding, CEVA Logistics, and Yang Ming. Regional ocean services span Turkon, Swire Shipping, Wan Hai, SITC Container Lines, and Interasia Lines. Additional carrier integrations feature Wallenius Wilhelmsen, Samudera Shipping Line, Sinokor, UWL, Sealead Shipping, Trans Asian Shipping Services, and National Shipping of America.

## Air Tracking and Ship Schedules Updates

Air Tracking API expanded carrier support, adding integrations for Etihad Cargo and United Airlines.

Ship Schedules improved collaboration with three shipping lines. Integrations with Sinotrans and Crowley now operate by Points, while Ignazio Messina updates by Vessel.

## Rate Management System Enhancements

We released an updated version of the Rate Management System for FCL and LCL tariffs. Users can create multiple tariff types across multiple ports, selecting whether tariffs apply to import, export, or both direction options.

Tariffs now include an explicit validity period. A dedicated Directory section lists all available tariffs for quick reference.

## Logistics Map Transport Options

Logistics Map Transport added a new Carrier filter. You can select one or multiple carriers from the dropdown list to isolate their active transport offers on the map.

A 'To be nominated' filter option displays all transport entries on the map that have not yet been assigned to a specific carrier.

## Announcements

New features and platform announcements include:

- Upgraded Unified Tracking System
- Logistics Map with new 'Warehouse' tab functionality
- Next generation Load Calculator Web 3.0 featuring a modernized interface and expanded tools
- Enhanced Map Platform capabilities
- Geocoding API fully integrated into Logistics Explorer
- Centralized Inbox connecting Logistics Explorer, Bookings, and Notifications"""

full_remediated = f"{remediated_title}\n{remediated_meta_title}\n{remediated_meta_description}\n{remediated_body}"

def get_words(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text_clean.split() if w]

orig_words = get_words(original_draft)
rem_words = get_words(full_remediated)

print("Checking ALL 6+ word n-gram matches between full remediated text and original draft...")
matches_6_plus = []
for n in range(6, 20):
    for i in range(len(rem_words) - n + 1):
        gram = rem_words[i:i+n]
        gram_tuple = tuple(gram)
        # check if in orig_words
        for j in range(len(orig_words) - n + 1):
            if tuple(orig_words[j:j+n]) == gram_tuple:
                matches_6_plus.append((n, " ".join(gram)))

print(f"Total overlapping 6+ word n-grams with original draft: {len(matches_6_plus)}")
unique_matches = set([m[1] for m in matches_6_plus])
for m in sorted(unique_matches):
    print("  Match:", m)

