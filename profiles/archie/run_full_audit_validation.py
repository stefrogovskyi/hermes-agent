import json
import re

title = "SeaRates Updates: Week 39 Freight Tooling Enhancements"
meta_title = "SeaRates Updates: Week 39, 2025 Platform Enhancements"
meta_description = "Explore SeaRates Week 39 updates, including De Well Group tracking, Rate Management upgrades, carrier filters, and new schedule integrations."

body = """## Container Tracking Upgrades

The Container Tracking tool now supports De Well Group, bringing the platform total to 215 supported shipping lines.

Within the Container Tracking web interface, importing a bulk Excel file of tracking numbers automatically generates shipment cards in your Dashboard. Free subscription users can now view their daily and monthly usage limits directly within the interface. Response formation logic for the History API has also been updated.

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

Platform updates and new feature announcements include:

- Upgraded Unified Tracking System
- Logistics Map with new 'Warehouse' tab functionality
- Next generation Load Calculator Web 3.0 featuring a modernized interface and expanded tools
- Enhanced Map Platform capabilities
- Geocoding API fully integrated into Logistics Explorer
- Centralized Inbox connecting Logistics Explorer, Bookings, and Notifications"""

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

def get_words(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text_clean.split() if w]

# Finding 1: Carrier List Check
orig_carrier_phrase = "Maersk, Hapag-Lloyd, Interasia Lines, SITC Container Lines, DHL Global Forwarding, Swire Shipping, Orient Overseas Container Line (OOCL), Turkon, Wan Hai, Ocean Network Express (ONE), CEVA Logistics, COSCO, Yang Ming, Sealead Shipping, Sinokor, Samudera Shipping Line, Mediterranean Shipping Company (MSC), National Shipping of America, UWL, Trans Asian Shipping Services, and Wallenius Wilhelmsen."
orig_carrier_words = get_words(orig_carrier_phrase)
body_words = get_words(body)

matches_carrier_6plus = []
for n in range(6, 15):
    for i in range(len(body_words) - n + 1):
        gram = body_words[i:i+n]
        gram_tuple = tuple(gram)
        for j in range(len(orig_carrier_words) - n + 1):
            if tuple(orig_carrier_words[j:j+n]) == gram_tuple:
                matches_carrier_6plus.append((n, " ".join(gram)))

print("=== FINDING 1 CHECK ===")
print("Carrier list 6+ word matches with original carrier list:", len(matches_carrier_6plus))
assert len(matches_carrier_6plus) == 0, "Finding 1 failed!"

# Finding 2: Announcements List Check
verbatim_12_word = "Unified Tracking System, Logistics Map 'Warehouse' tab, Load Calculator Web 3.0"
print("\n=== FINDING 2 CHECK ===")
print("12-word verbatim match present:", verbatim_12_word.lower() in full_text.lower())
assert verbatim_12_word.lower() not in full_text.lower(), "Finding 2 failed!"

# Finding 3: Fabricated URL Check
print("\n=== FINDING 3 CHECK ===")
print("searates.com URL present:", "searates.com" in full_text.lower())
assert "searates.com" not in full_text.lower(), "Finding 3 failed!"

# Finding 4: Upcoming Releases Header and Intro Check
print("\n=== FINDING 4 CHECK ===")
print("## Upcoming Releases present:", "## upcoming releases" in body.lower())
print("engineering team present:", "engineering team" in body.lower())
print("scheduled for future rollouts present:", "scheduled for future rollouts" in body.lower())
assert "## upcoming releases" not in body.lower(), "Finding 4 failed (header)!"
assert "engineering team" not in body.lower(), "Finding 4 failed (intro)!"
assert "scheduled for future rollouts" not in body.lower(), "Finding 4 failed (intro)!"

# Finding 5: Repetitive Transition Starters Check
print("\n=== FINDING 5 CHECK ===")
we_also = re.findall(r'\bwe also\b', full_text, re.IGNORECASE)
additionally = re.findall(r'\badditionally\b', full_text, re.IGNORECASE)
print("'We also' occurrences:", len(we_also), we_also)
print("'Additionally' occurrences:", len(additionally), additionally)
assert len(we_also) == 0, "Finding 5 failed ('We also')!"
assert len(additionally) == 0, "Finding 5 failed ('Additionally')!"

# Finding 6: Em-dashes and Double-hyphens Check
print("\n=== FINDING 6 CHECK ===")
em_dashes = full_text.count('—')
double_hyphens = full_text.count('--')
print("Em-dashes count:", em_dashes)
print("Double-hyphens count:", double_hyphens)
assert em_dashes == 0, "Finding 6 failed (em-dashes)!"
assert double_hyphens == 0, "Finding 6 failed (double-hyphens)!"

# Finding 7: Lengths Check
print("\n=== FINDING 7 CHECK ===")
print(f"Title length: {len(title)} (limit < 68)")
print(f"Meta Title length: {len(meta_title)} (limit <= 60)")
print(f"Meta Description length: {len(meta_description)} (limit <= 155)")
assert len(title) < 68, "Finding 7 failed (title)!"
assert len(meta_title) <= 60, "Finding 7 failed (meta_title)!"
assert len(meta_description) <= 155, "Finding 7 failed (meta_description)!"

print("\nALL 7 AUDIT CHECKS PASSED PERFECTLY!")

# Output JSON
result_json = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

with open("final_output.json", "w") as f:
    json.dump(result_json, f, indent=2)

