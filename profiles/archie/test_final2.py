import json
import re

title = "SeaRates Release Notes: Week 31, 2025 Updates"
meta_title = "SeaRates Updates: Week 31, 2025 Release Notes"
meta_desc = "SeaRates Week 31, 2025 release notes cover tracking updates across 14 ocean lines and 4 airlines, schedule refinements, plus new platform tools."

body_text = """## Ocean Tracking Enhancements

SeaRates expanded ocean tracking coverage by integrating two additional shipping lines: Expressway Container Line and Fairfreight Lines. The platform now supports 209 shipping lines in total.

Tracking integrations were updated for 12 existing ocean carriers:
* Pan Continental Shipping
* Jin Jiang Shipping (SHJJ)
* Hapag-Lloyd
* Maersk
* Dachser
* Hede Shipping
* Wan Hai
* Mediterranean Shipping Company (MSC)
* SITC Container Lines
* Asyad Line
* Sealead Shipping
* Maritime Carrier Shipping (MACS)

These data updates improve real-time ocean freight visibility. SeaRates also revised internal status processing logic to determine DELIVERED cargo milestones more accurately.

## Air Tracking and Vessel Schedules

Air tracking improvements reached four airlines:
* Turkish Airlines
* Avianca
* LOT Polish Airlines
* ASL Airlines Belgium

These updates refine air cargo milestone updates for active shipments.

Vessel schedule intelligence was updated across four carrier data feeds:
* Points searches: Yang Ming, DSV Ocean
* Vessel searches: Emirates, Vertraco

## Landing Pages and New Feature Announcements

Content and layout revisions were completed for key product landing pages:
* Container Tracking API
* Container Tracking Web Integration
* Integrations landing page

These site updates clarify options for multi-carrier tracking API deployment and broader digital logistics platform integration.

SeaRates also announced several tools and integration projects:
* Unified Tracking System
* Logistics Map Warehouse tab
* Load Calculator Web 3.0 (redesigned with new features)
* Map Platform
* AI Assistant integrated with Ship Schedules
* Geocoding API integrated with Logistics Explorer
* Inbox integration linking Logistics Explorer, Bookings, plus Notifications"""

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_desc,
    "body_text": body_text
}

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body_text}"

print("=== CHECKING CONSTRAINTS ===")
print("1. Title length:", len(title), len(title) <= 60)
print("2. Meta Title length:", len(meta_title), len(meta_title) <= 60)
print("3. Meta Description length:", len(meta_desc), len(meta_desc) <= 155)

# Dash check
dashes = ["—", "–", "--"]
dash_found = any(d in full_text for d in dashes)
print("4. No dashes:", "PASS" if not dash_found else "FAIL")

# Cliches check
cliches = [
    "fast-paced", "worth noting", "game-changer", "seamless", "delve into", "testament",
    "elevate", "beacon", "landscape", "unwavering", "delighted", "thrilled", "steadfast",
    "excited", "stay tuned", "ever-changing", "cutting-edge", "state-of-the-art", "game changer"
]
cliche_found = [c for c in cliches if c.lower() in full_text.lower()]
print("5. No clichés:", "PASS" if not cliche_found else f"FAIL: {cliche_found}")

# Connectors check
connectors = ["that's why", "which is why", "this is a sign of", "this means that", "as a result"]
conn_found = [c for c in connectors if c.lower() in full_text.lower()]
print("6. No forbidden connectors:", "PASS" if not conn_found else f"FAIL: {conn_found}")

# Keyword check
keywords = [
    "real-time ocean freight visibility",
    "multi-carrier tracking API",
    "air cargo milestone updates",
    "vessel schedule intelligence",
    "digital logistics platform integration"
]
for kw in keywords:
    print(f"7. Keyword '{kw}':", "PASS" if kw.lower() in full_text.lower() else "FAIL")

# Rule of three check
rule_of_three = re.findall(r'\b[\w\s]+,\s+[\w\s]+,\s+and\s+[\w\s]+\b', full_text, re.IGNORECASE)
print("8. Rule-of-three matches:", rule_of_three)

# Contrastive negations check
cn_matches = re.findall(r'\b(not\s+[\w\s]+,\s*but|instead of|[\w\s]+,\s*not\s+[\w\s]+)\b', full_text, re.IGNORECASE)
print("9. Contrastive negation count:", len(cn_matches), cn_matches)

