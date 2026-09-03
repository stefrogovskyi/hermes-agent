import re

meta_title = "SeaRates Updates Week 42: Rail Tracking and API Upgrades"
meta_desc = "SeaRates launched web rail tracking on LandRates.com, AIS predictive ETA, 8 new airlines, expanded shipping line integrations, and Virtual Office embeds."

article_title = "# SeaRates Product Updates: Week 42, 2024"

article_body = """LandRates.com now features a web version of Rail Tracking. Cargo owners can trace rail shipments using a tracking number to inspect real-time logistics events, route history, equipment details, and status updates on an interactive world map. Shipment cards can be copied directly for instant sharing with partners and customers.

### Parcel Tracking API and Developer Portal

The Parcel Tracking API now returns estimated and actual departure and arrival dates. Smart Autodetect services identify parcel carriers automatically, returning the status code `AUTODETECT_CANT_DETECT_PARCEL_COMPANY` when a carrier cannot be matched. A complete list of supported carriers is now published in the Developer Portal.

### Air Cargo Tracking Expansion

Support is live for eight additional airlines: Air Moldova, Mahan Air, Transcarga International Airways, Vietravel Airlines, Lion Airlines, Super Air Jet, Thai Lion Air, and Wings Air.

The Air Cargo Tracking API features enhanced location tracking and logic that generates detailed event descriptions. Integration performance was upgraded across eight key providers: SAS Cargo, Malaysia Airlines, FedEx Express, Cargolux Airlines International, Cargolux Italia, British Airways, Cargolux, and Emirates.

### Tracking System and Predictive ETA

Container location determination logic and API routing received system updates. A new predictive ETA algorithm processes live AIS data to project arrival times.

Provider integrations were strengthened for twelve ocean carriers and logistics providers: Avana Global FZCO (BALAJI), CK Line, Atlantic Container Line (ACL), Wan Hai, BAL Container Line, Pan Continental Shipping, Yang Ming, Mediterranean Shipping Company (MSC), Dsv Ocean Transport, CMA CGM, PSL Navegacao, and Hoegh Autoliners.

### Geocoding, Schedules, and Distance API v3.0

The Geocoding API beta is live, complete with documentation in the Developer Portal.

Distance & Time API Version 3.0 allows developers to query departure and arrival locations using standard IATA and ICAO codes.

Ship Schedules tracking was updated for KMTC for vessel searches, alongside PIL and Dong Young for port searches.

### Virtual Office, Tools, and Portal Upgrades

The Virtual Office integration package allows businesses to embed authorization, registration, and the customer Dashboard directly onto their own websites using code from the Developer Portal. Within the Dashboard, interactive map points link directly to specific bookings and requests, while the Counterparties panel offers an option to display platform-registered users in the general list.

The Load Calculator web integration features a redesigned interface for cargo loading and stuffing planning. A new web integration page is available for the Demurrage & Storage Calculator.

The Find a Tool page added filtering by Web Access, Web Integration, and API. Documentation updates are published across the SeaRates Help page and the Tracking API section on the Developer Portal. LandRates.com launched an updated homepage design and content layout."""

print(f"Meta Title ({len(meta_title)} chars): {meta_title}")
print(f"Meta Desc ({len(meta_desc)} chars): {meta_desc}")

# Full string check
full_str = f"{meta_title}\n{meta_desc}\n{article_title}\n{article_body}"

# Check 1: Dash check
dashes = ['—', '–', '--']
for d in dashes:
    if d in full_str:
        print(f"FAIL: Dash '{d}' found")

# Check 2: Explicit connectors
connectors = [
    r'\bfurthermore\b', r'\bmoreover\b', r'\bin addition\b',
    r'\bcrucially\b', r'\bthat\'s why\b', r'\bultimately\b',
    r'\bimportantly\b', r'\bit is worth noting that\b'
]
for conn in connectors:
    m = re.search(conn, full_str, re.IGNORECASE)
    if m:
        print(f"FAIL: Connector '{m.group(0)}' found")

# Check 3: Cliché words
cliches = [
    "delve", "tapestry", "testament", "beacon", "landscape", "pivotal",
    "game-changer", "fostering", "unlock", "seamless", "elevate",
    "cutting-edge", "realm", "ever-evolving", "paramount", "spearhead", "boasts"
]
for c in cliches:
    m = re.search(r'\b' + re.escape(c) + r'\b', full_str, re.IGNORECASE)
    if m:
        print(f"FAIL: Cliché word '{m.group(0)}' found")

# Check 4: Textbook intro/outro
for t in ["in conclusion", "in summary", "overall"]:
    if t in full_str.lower():
        print(f"FAIL: Textbook phrase '{t}' found")

# Check 5: Character limits
if len(meta_title) > 60:
    print("FAIL: Meta title > 60 chars")
if len(meta_desc) > 155:
    print("FAIL: Meta desc > 155 chars")

print("Verification script finished.")
