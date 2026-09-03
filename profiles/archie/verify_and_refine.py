import re
import json

title = "SeaRates Logistics Map: Transport Sourcing & Fleet Map"
meta_title = "SeaRates Logistics Map Transport Guide"
meta_description = "Book freight or list available trucks, vessels, railcars, and aircraft on SeaRates Logistics Map Transport with real-time fleet visibility."

original_text = """
Shippers find transport units for shipping or backhauls right by their requirements, while carriers and asset owners promote their available fleet and get direct booking requests. How does this scenario sound to you?

This is not just a script but the principle of mutual benefits behind Logistics Map Transport, which we will explore in this article.

As from our previous guide of Logistics Map Cargoes, you can book the best shipping option from all available offers or promote your services and attract hot leads, all in one place. Ready to see how it works for transport units? Let’s put your trucks on the map or find the perfect vessel in seconds.

## Overview of the "Transport" tab

Open Logistics Map → find the “Transport” tab.

The tool adapts to your role (Shipper or Carrier), whether you're requesting a transport or offering shipping services.

Here, there is a live world map — current international freight market with:
- Available vehicles and equipment (posted by carriers)
- Active transport requests (posted by shippers/forwarders looking for specific units)

Everything updates in real time. Zoom in on Europe, and you’ll see hundreds of trucks in Rotterdam; switch to the U.S. Midwest and spot refrigerators ready for your shipments; jump to the Black Sea and find Ro-Ro capacity near Istanbul.

## For shippers & freight forwarders: Exact matches in minutes

Need a mega-trailer tomorrow from Hamburg to Milan?
- To place your inquiry, submit the Request a Quote form
- To quickly check available offers — use the Filter in Logistics Map Transport

Request a Quote form. Go to the following:
- Cargo category and details
- Transportation mode
- Container type and quantity
- Weight
- Route points (departure and arrival)
- Ready to load date
- Freight Basis terms
- Select Associated services and add extra details if needed
- Submit your request by clicking Send.

Find the detailed overview of the Request System here.

Voilà! Your request has been automatically posted on Logistics Map Transport. Carriers and transport owners will provide you with individual offers based on your requirements specified in the request.

Within minutes, you’ll see quotes flowing into your Virtual Office Dashboard. Each quote shows carrier details, transport unit specifications, price (fixed or per km), and other details to prepare for smooth shipping.

Compare and accept the best offer with one click and receive immediate booking confirmation, and proceed with tracking in real time.

How to find the currently available transport on the market?
- Enter the departure/arrival points of your route.
or
- Explore the Filter for sorting transport cards by location, ready-to-load and unloading dates, transport ID, transport asset type, and price (per km/flat/day).

Find your transport asset type:
- Containers: Standard, High Cube, Refrigerated, Open Top, Flatrack, Bulk, Tank, Platform, Pallet Wide, etc.
- Trucks: Custom truck, Tilt, Mega, Jumbo, Dry van, Metal body truck, Van, Conestoga, Isoterm truck, Isoterm van, Refrigerator, Refrigerator van, Dump truck, Tank truck, Grain carrier, Car carrier (Autocart), Logging & pipes truck, Drop-side platform, Open platform, Flatbed truck, Lowboy truck (Heavy loader), Cattle truck, Coil carrier, etc.
- Vessels: Bulk carrier, Containership, General cargo vessel, Barge, Product tanker, Crude carrier, Asphalt carrier, Chemical tanker, Gas carrier, Heavy-lift, Livestock, Refrigerated, Ro/Ro, Wood chip, etc.
- Wagons: Custom, Covered, Freight semi-wagon, Hopper, Flat, Container platform, High side wagon, Side dump wagon, Tank wagon, etc.
- Aircrafts: Custom aircraft, Airbus, Boeing, McDonnell Douglas, Eurocopter, Mi’s, YAK, charter flights, etc.

For each transport asset, we provide carrier selection: SeaRates carrier database for Containers and Vessels, providers for Trucks and Wagons by LandRates, and AirRates database of airlines for Aircrafts.

A closer look at the results: Each transport card has a transport image, route or location, container type, carrier’s name, and date of readiness to load, as well as many details such as cubic or carrying capacity, volume, price, and others.

Copy the link to any card to save for later or share with partners.

Open the transport card for details and Apply for the offered service within a few seconds. Just enter the preferred destination and price — no more efforts to fix appropriate transport for your logistics needs.

This way, the time you spend sourcing for transport is cut from days to minutes as it becomes tailored and highly targeted searching. And the most significant — you compare 10–50 quotes already in one place instead of calling 3-4 providers with a limited variety of routes, times, or types of transport.

## For carriers & asset owners

Own trucks, trailers, railcars, or vessels? You already know how shippers can find you via the Logistics Map Transport, so you need to place your service offer here.

Start with your Virtual Office Profile:
Go to the left side → the ‘Activity’ section → the ‘Transport’ tab. This is your panel for logistics asset management. Here, you see the empty space or transport list with units entered before.

Click ‘Add transport’ or ‘New Transport’ to complete the list. Then, fill out the form step by step for the transport unit you’d like to promote:

General information: Choose unit, transport name, type, model, number, and carrier. The fields are changed appropriately to the units you chose.
Parameters: Enter cubic and carrying capacity are mandatory. Length, width, and height are optional.
Location: Provides shippers with the place of loading and the ready-to-load date.
Preferred destination (optional): If you are transporting cargo by exact route and want to gather more LCL requests for this purpose, specify the preferred destination with the unloading date.
Price (optional): You can specify a fixed or minimal price for your transportation services, as well as include additional charges (downtime on loading or downtime on discharging). Choose preferred currency and payment methods.
Additional information (optional): Provide an extensive description for more info about your services or transport unit for shippers and freight forwarders. Upload photos or add notes to promote specific details or your service in general.

Click Save ... and that's it! You don't need anything else for the transport to appear automatically and be promoted to the SeaRates audience via Logistics Map.

At any time, you can return to your Virtual Office to view the list of transports and manage your entire fleet in one place and make changes to costs, routes, and other details, and it will automatically update for shippers on Logistics Map Transport.

To view, delete, or share the direct link to your transport cards, use the Filter and mark My transport and/or My company's transport to check how your potential customer sees it.

Now the main thing happens automatically: Shippers searching your area see your unit and can send direct booking requests.

You receive requests straight to your VO Dashboard under the Requests tab. Send customized offers and breakdown/lump sum quotes even with the Structural Quotes in your Profile.

Miles won’t ever run empty, as it was before when “nobody knew you were there”. You can always gather more FCL and LCL cargo on a specific route or fill backhauls, sell any kind of your equipment, and reach international markets.

## Web integration

There are more benefits to be gained by integrating this white-labeled tool into your site. You can manage freight requests depending on your position: shippers have their own tender platform, and carriers can set up a branded map for lead generation and fleet promotion. Check the documentation and ask our team for an integration demo.

## API connection

The Logistics Map API allows you to have fleet data and request synchronization, create your application, automate the entire workflow. The process is two-way: shippers gather transport offers, while carriers promote assets and advertise their services.
- Upload of shipping requests/transport units
- Leads generation and filtering into your ERP/TMS
- Management of dynamic freight pricing

Request the API demo and access from our team, and sync with systems like SAP or custom dashboards. For advanced access and custom integrations, drop us a line at it.sales@searates.com.
"""

# Now let's craft an improved, completely original version that addresses:
# 1. Zero 6-gram overlaps with source (reword all form lists, filter parameters, equipment options, and quote details).
# 2. Asymmetric, varied headings and sentence structures (no repetitive "X while Y", no formulaic H2s, no semicolon triadic cadence).
# 3. 0 em-dashes.
# 4. Strict factual accuracy (Rule 11).

revised_body = """Freight moves on clear information, but matching empty transport units with available cargo across global trade lanes often stalls in lengthy back-and-forth communication.

The Transport section inside SeaRates Logistics Map provides a live view of worldwide commercial movement. Cargo owners search here for vehicle space, and transport operators publish their available capacity.

Carriers list trucks, vessels, wagons, or aircraft ready for dispatched jobs. At the same time, shippers submit active transport inquiries. When exploring the map, zooming into Rotterdam highlights regional haulage units, checking the American Midwest shows refrigerated trailers awaiting loads, and shifting toward the Black Sea reveals Ro-Ro vessels near Istanbul. This grants dispatchers real-time fleet visibility across major trade corridors.

## How Cargo Owners Secure Equipment

Cargo owners and forwarders locate equipment on the map using two main methods: submitting a formal quote inquiry or filtering available market listings.

The quote submission form gathers necessary operational specifics:
* Freight classification and cargo characteristics
* Shipping mode selection
* Required container specification and volume
* Total payload mass
* Dispatch and destination locations
* Scheduled loading date
* Commercial freight terms
* Optional add-on services and instructions

Once submitted, the system publishes the inquiry directly to Logistics Map Transport. Quotes from fleet owners populate the Virtual Office Dashboard in real time. Individual quotes specify transport operator background, unit technical capacity, distance-based or fixed pricing, and booking conditions. Shippers accept preferred rates with a single click, obtain instant booking confirmation, and track cargo movements.

To browse pre-listed market capacity, users set origin and destination points or refine cards through specific filters:
* Operational area
* Target availability and discharge timing
* Unique unit identifier
* Asset classification
* Pricing structure (flat rate, distance pricing, or daily rental)

The platform supports diverse asset classifications across five transport modes:
* **Container Equipment:** Standard dry boxes, high cube, reefer units, open top, flat rack, bulk, tank, platform, and pallet wide variants.
* **Road Freight:** Standard trucks, tilt trailers, mega units, jumbo trailers, dry vans, metal body vehicles, vans, conestoga units, insulated transport, reefers, dump trucks, tank trailers, grain haulers, car carriers, timber trucks, drop-side platforms, open flatbeds, lowboys, livestock haulers, and coil units.
* **Maritime Fleet:** Bulk carriers, container ships, general cargo vessels, barges, product tankers, crude carriers, asphalt tankers, chemical vessels, gas carriers, heavy-lift ships, livestock carriers, reefers, Ro-Ro ships, and wood chip carriers.
* **Rail Fleet:** Standard covered wagons, semi-wagons, hoppers, flatcars, container platforms, high-side wagons, side dumpers, and tank cars.
* **Air Transport:** Cargo aircraft, passenger-freight conversions, Airbus models, Boeing freighters, McDonnell Douglas aircraft, Eurocopter units, Mi freighters, YAK freighters, and chartered flights.

Asset listings integrate with specialized databases: SeaRates for maritime shipping, LandRates for road and rail transport, and AirRates for aviation routes.

Every listing card displays vehicle imagery, route geography, container specs, carrier branding, availability dates, payload weight, cubic volume, and rate details. Users can copy direct card links to share across teams.

Selecting a card allows shippers to specify destination requirements and offer target prices. This digital freight matching framework lets cargo owners review between 10 and 50 organized proposals simultaneously rather than contacting individual suppliers manually.

## Capacity Promotion for Transport Operators

Asset owners publish available capacity through the Virtual Office Profile under the Activity area in the Transport tab.

Selecting the option to register transport opens a step-by-step entry form:
* **Primary Information:** Unit category, vehicle designation, model, registration identifier, and carrier entity.
* **Technical Parameters:** Required volume capacity and payload limit, along with optional dimensions.
* **Location:** Current positioning and earliest load date.
* **Target Route (Optional):** Intended discharge destination and arrival timing to gather less-than-container-load freight.
* **Pricing Terms (Optional):** Base charges, minimum rates, loading or discharge demurrage fees, currency preference, and payment terms.
* **Operational Notes (Optional):** Detailed service description, equipment photographs, and special handling capabilities.

Saving the entry automatically lists the vehicle on Logistics Map Transport. Adjustments made in the Virtual Office mirror instantly on the public map. Fleet managers select internal filters to inspect how listings appear to potential clients.

Direct booking inquiries arrive in the Virtual Office Dashboard under the Requests tab. Operators respond by providing customized pricing, lump-sum offers, itemized cost breakdowns, or Structural Quotes.

Listing available units helps carriers secure backhaul capacity, fill empty legs, collect FCL or LCL shipments, and expand international reach. Placing assets on the live map improves overall asset utilization and eliminates empty miles on return journeys.

## Site Integration & System API Connectivity

Businesses can embed this white-label tool onto their own web domains. Shippers establish branded procurement portals, while carriers present interactive capacity maps for lead generation. Demo access is available upon request.

The Logistics Map API synchronizes equipment availability and freight inquiries with enterprise management systems. Core functions include:
* Pushing shipment requests and vehicle listings
* Exporting filtered lead data into existing ERP or TMS platforms
* Managing dynamic freight pricing

The API integrates with software environments such as SAP or proprietary operational dashboards. Access credentials and technical documentation are available through it.sales@searates.com.
"""

def normalize_text(text):
    # Lowercase and keep only alphanumeric and spaces
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text.split()

def find_ngram_overlaps(orig_text, candidate_text, n=6):
    orig_words = normalize_text(orig_text)
    cand_words = normalize_text(candidate_text)
    
    orig_ngrams = {}
    for i in range(len(orig_words) - n + 1):
        ngram = tuple(orig_words[i:i+n])
        orig_ngrams[ngram] = orig_ngrams.get(ngram, 0) + 1
        
    matches = []
    for i in range(len(cand_words) - n + 1):
        ngram = tuple(cand_words[i:i+n])
        if ngram in orig_ngrams:
            matches.append(" ".join(ngram))
            
    return matches

def run_checks():
    full_candidate = f"{title}\n\n{meta_title}\n\n{meta_description}\n\n{revised_body}"
    
    # 1. Check Em-Dashes
    em_dashes = [m.start() for m in re.finditer(r'—|--', full_candidate)]
    
    # 2. Check Lengths
    t_len = len(title)
    mt_len = len(meta_title)
    md_len = len(meta_description)
    
    # 3. Check N-grams
    overlaps = find_ngram_overlaps(original_text, revised_body, n=6)
    
    # 4. Check Contrastive Negation
    negations = re.findall(r'\bnot\b|\binstead of\b', revised_body, re.IGNORECASE)
    
    print(f"Title length: {t_len} (max 60)")
    print(f"Meta Title length: {mt_len} (max 60)")
    print(f"Meta Description length: {md_len} (max 155)")
    print(f"Em-dashes count: {len(em_dashes)}")
    print(f"6-gram overlaps count: {len(overlaps)}")
    if overlaps:
        print("Overlaps found:", set(overlaps))
    print(f"Contrastive words count: {len(negations)}")

run_checks()
