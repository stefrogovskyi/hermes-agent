import json
import re

text = {
  "title": "SeaRates Platform Updates: Week 40, 2025",
  "meta_title": "SeaRates Week 40, 2025 Updates: Tracking & Rate Tools",
  "meta_description": "SeaRates Week 40, 2025 updates bring container tracking APIs, rate management system tools, air tracking upgrades, and geocoding database additions.",
  "body": """We appreciate your ongoing support of SeaRates and remain committed to refining our services to meet your operational needs. For earlier context, please refer to our previous update posts.

Here is what was updated during Week 40, 2025:

Container Tracking & Integration
Our History API now displays shipments marked with CANCELLED status. We also updated operational connections with several shipping lines and leasing companies: G2 Ocean, Sinokor, CMA CGM, T.S. Lines, Maersk, Hapag-Lloyd, Kuehne + Nagel (KN), Turkon, Independent Container Line (ICL), Kintetsu World Express, SAS Cargo, and Pacific International Lines (PIL).

Air Freight Tracking
We added direct tracking support for Air Corsica, Hong Kong Express, and Jazeera Airways. This brings our total to 445 supported airlines. Additionally, we updated integration for LATAM Cargo, Lufthansa Cargo, Singapore Airlines, Turkish Airlines, ASL Airlines Belgium, Shenzhen Airlines, YTO Cargo Airlines, FITS Aviation, and Air Canada.

Schedules, Rates & Platform Updates
Ship Schedules integration has been updated for Wan Hai and Hyundai across both Points and Vessel search functions. In our rate management system, users can now copy direct links to individual tariffs across all transport modes. We also added the option to sort port tariffs by the Pet lot parameter in the RMS. Elsewhere on the site, shipping line pages in the Carrier Directory feature a new layout, while our geocoding database has been updated with postal codes across multiple countries.

Announcements
Announcements:
- Unified Tracking System
- Logistics Map 'Warehouse' tab
- Load Calculator Web 3.0 (new design and features)
- Map Platform
- Geocoding API integrated with Logistics Explorer
- Inbox integration with Logistics Explorer, Bookings, and Notifications"""
}

# Check rule checks
body = text["body"]

# Check em-dashes
em_dashes = re.findall(r'—|--', body)
print("Em-dashes found:", em_dashes)

# Check contrastive negations
contrastive = re.findall(r'\b(rather than|instead of|not only|not just|not merely)\b', body, re.I)
print("Contrastive negations found:", contrastive)

# Check AI clichés
cliches = ['delve', 'testament', 'revolutionize', 'pivotal', 'beacon', 'realm', 'tapestry', 'transformative', 'game-changer', 'nestled', 'paramount', 'unwavering', 'furthermore', 'moreover', 'spearhead', 'underpins', 'seamlessly', 'cutting-edge', 'unleash', 'robust']
found_cliches = [c for c in cliches if re.search(r'\b' + c + r'\b', body, re.I)]
print("AI cliches found:", found_cliches)

