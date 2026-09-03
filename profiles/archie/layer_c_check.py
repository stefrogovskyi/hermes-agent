import re

rewrite = """Title: SeaRates Fleet Management via Virtual Office and Map
Meta Title: Virtual Office Freight Management on SeaRates Logistics Map
Meta Description: List transport units in SeaRates Virtual Office, set custom rates, filter fleet on Logistics Map, and connect with Structural Quotes leads.

## Asset Creation inside the Virtual Office

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

# Sections breakdown
sections = re.split(r'##\s+', rewrite)[1:] # Skip title/meta part
for i, sec in enumerate(sections):
    lines = sec.strip().split('\n')
    heading = lines[0]
    body = '\n'.join(lines[1:])
    words = len(body.split())
    paras = [p for p in body.split('\n\n') if p.strip()]
    print(f"Section {i+1}: '{heading}' | Total Words: {words} | Paragraphs/lists count: {len(paras)}")
    for j, p in enumerate(paras):
        p_words = len(p.split())
        print(f"   P{j+1}: {p_words} words")

print("\n--- Sentences structure check ---")
all_paras = [p.strip() for p in rewrite.split('\n\n') if p.strip() and not p.strip().startswith('Title:') and not p.strip().startswith('Meta') and not p.strip().startswith('##')]

for idx, p in enumerate(all_paras):
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    print(f"\nParagraph {idx+1} ({len(sents)} sentences):")
    for s_idx, s in enumerate(sents):
        print(f"  S{s_idx+1}: {s}")
