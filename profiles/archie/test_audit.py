import re

def audit_text(title, meta_title, meta_desc, body):
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    errors = []
    
    # Rule 1: No em-dashes
    if "—" in full_text or "--" in full_text:
        errors.append("Rule 1 VIOLATION: Em-dash or double dash found!")
        
    # Rule 2: AI clichés
    cliches = [
        "crucial aspect", "in today's fast-paced world", "dive into", 
        "game-changer", "integral part", "it's not just", "in conclusion", 
        "it is important to note", "crucial", "testament", "delve", 
        "fostering", "tapestry", "seamlessly", "beacon", "landscape",
        "revolutionary", "at your fingertips", "smooth, efficient and profitable",
        "let's take a look", "let's explore", "transform your business"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Rule 2 VIOLATION: AI cliché '{c}' found!")
            
    # Check length limits
    if len(title) > 60:
        errors.append(f"Title too long: {len(title)} chars (max 60)")
    if len(meta_title) > 60:
        errors.append(f"Meta Title too long: {len(meta_title)} chars (max 60)")
    if len(meta_desc) > 155:
        errors.append(f"Meta Description too long: {len(meta_desc)} chars (max 155)")
        
    # Check rule-of-three balanced lists (A, B, and C)
    rule_of_three_pattern = r'\b\w+,\s+\w+,\s+(?:and|or)\s+\w+\b'
    matches = re.findall(rule_of_three_pattern, body, re.IGNORECASE)
    if matches:
        errors.append(f"Rule 4 WARNING: Rule-of-three list pattern found: {matches}")
        
    # Check contrastive negation ("not X, but Y", "X, not Y", "It isn't X", "rather than")
    cn_pattern = r'\b(not\s+[^,.]+(?:,|\s+)but|isn\'t\s+[^,.]+(?:,|\s+)it\'s|is\s+not\s+[^,.]+(?:,|\s+)it\s+is|rather\s+than)\b'
    cn_matches = re.findall(cn_pattern, body, re.IGNORECASE)
    if len(cn_matches) > 1:
        errors.append(f"Rule 7 VIOLATION: Too many contrastive negations/rather-than ({len(cn_matches)}): {cn_matches}")
        
    # Check symmetric antithesis pairs (Rule 10)
    antithesis_pairs = [
        r'\bglobal\s+(?:and|or)\s+local\b',
        r'\blocal\s+(?:and|or)\s+global\b',
        r'\bsmall\s+(?:and|or)\s+large\b',
        r'\blarge\s+(?:and|or)\s+small\b',
        r'\bpublic\s+(?:and|or)\s+private\b',
        r'\binternal\s+(?:and|or)\s+external\b',
        r'\bexternal\s+(?:and|or)\s+internal\b'
    ]
    for ap in antithesis_pairs:
        if re.search(ap, body, re.IGNORECASE):
            errors.append(f"Rule 10 VIOLATION: Symmetric antithesis pair found: {ap}")

    # Check required keywords
    keywords = [
        "digital transport management system (TMS)",
        "real-time fleet visibility & logistics map",
        "virtual office freight management",
        "structural quotes logistics marketplace",
        "digital freight forwarding asset tracking"
    ]
    for kw in keywords:
        if kw.lower() not in full_text.lower():
            errors.append(f"Missing required keyword: '{kw}'")

    return errors

title = "SeaRates Fleet Management via Virtual Office and Map"
meta_title = "Virtual Office Freight Management on SeaRates Logistics Map"
meta_desc = "List transport units in SeaRates Virtual Office, set custom rates, filter fleet on Logistics Map, and connect with Structural Quotes leads."

body = """## Asset Creation inside the Virtual Office

A scattered fleet on paper hardens into rigid operational delay, but structured digital listings turn raw transport capacity into reachable commercial routes. Inside the SeaRates platform, virtual office freight management starts under the Activity section on the left sidebar menu. Selecting the Transport tab opens the primary asset control panel where current listings remain indexed.

Clicking Add Transport or New Transport pulls up the main data entry interface. Fields adapt dynamically based on the selected transport category across road and sea routes as well as air or rail services. Standard form inputs capture transport names, models, registration numbers, vehicle types, and specified carriers. Popular transport classifications display at the top of category selection menus to simplify entry.

Carriers designate specific loading origins, adjacent loading zones, and operational parameters for each unit. Pricing structure setup allows direct input of rates with custom currency choices and contractual terms. Supplemental documentation and images upload directly into the entry form, creating an operational profile for fleet organization or client presentation.

## Real-Time Fleet Visibility & Logistics Map Setup

Finding available capacity requires precise filtering rather than manual calls. Within the real-time fleet visibility & logistics map feature set, the Transport tab functions as a searching and promotional board for shippers and carriers.

The Filter tab uses an Autocomplete input service to map specified pickup and delivery locations. Search parameters isolate vehicles by search radius around a location, targeted loading dates, unloading windows, unique ID numbers, or specific marked transport units. Users filter through single vehicle selections or tick checkboxes across equipment categories.

Rate configurations on the map adjust across several billing models: cost per kilometer, hourly or daily rates, flat fees, metric ton calculations, cubic meter metrics, kilogram rates, and fixed prices.

Switching between My Transport and My Company Transport toggles the display between individual user submissions and fleet units uploaded across associated company accounts. This setup supports digital freight forwarding asset tracking across regional or international routes.

## Shipper Search and Direct Rate Requests

Shippers submit transport needs through the Request a Quote form, which publishes their requirements into the global tool for carrier review. Alternatively, cargo owners browse vehicle markers across the interactive map or filter listing cards to evaluate carrier prices, pickup availability, and equipment details.

The system handles standard freight along with consolidated cargo and oversized shipments across ocean and air routes or road and rail legs.

Primary shipper actions include:
- Viewing unit locations, technical specifications, and planned routes
- Inspecting transport card details or map overlays
- Filtering listings by location radius, vehicle type, and pricing range
- Copying direct links to specific transport unit listings
- Sending configuration requests with target routes and proposed pricing
- Communicating directly with designated account managers through integrated chat

## Ecosystem Integration and Carrier Lead Matching

Carriers and freight forwarders, including DF Alliance members, list fleet inventory on the Transport tab to display available routes and spot tariffs. Sharing specific card links allows direct distribution of equipment availability to external clients and trading partners.

This transport panel operates alongside the broader digital transport management system (TMS) offered by SeaRates. Listings link into the structural quotes logistics marketplace, where carriers and DFA Premium Members view active shipper requests. Providers submit breakdown or lumpsum quotations directly against open shipping leads, matching available fleet capacity with real-time cargo demand across ocean shipping and air freight alongside trucking and rail transport.

Digital Freight Alliance Premium Members exchange equipment listings without moderation steps or listing fees. Integrated live chat within the DF Alliance framework allows members to handle inquiries, discuss terms, and finalize bookings directly."""

errs = audit_text(title, meta_title, meta_desc, body)
print("Errors found:", errs if errs else "NONE")
