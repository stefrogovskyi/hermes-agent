import re

orig = """Shippers find transport units for shipping or backhauls right by their requirements, while carriers and asset owners promote their available fleet and get direct booking requests. How does this scenario sound to you?

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

The Logistics Map API allows you to have fleet data and request synchronization, create your application, and automate the entire workflow. The process is two-way: shippers gather transport offers, while carriers promote assets and advertise their services.
- Upload of shipping requests/transport units
- Leads generation and filtering into your ERP/TMS
- Management of dynamic freight pricing

Request the API demo and access from our team, and sync with systems like SAP or custom dashboards. For advanced access and custom integrations, drop us a line at it.sales@searates.com."""

rewrite = """Title: SeaRates Logistics Map: Transport Sourcing & Fleet Map
Meta Title: SeaRates Logistics Map Transport Guide
Meta Description: Book freight or list available trucks, vessels, railcars, and aircraft on SeaRates Logistics Map Transport with real-time fleet visibility.

Body:
Freight moves on clear information, but matching empty transport units with available cargo across global trade lanes often stalls in email chains.

The Transport tab inside SeaRates Logistics Map provides a live view of global freight activity. The tool adapts to cargo owners searching for space and fleet operators listing available capacity.

Carriers post equipment ready for loading, while shippers post active freight requests. The live map updates continuously. A user zooming into Rotterdam sees available trucks; shifting to the U.S. Midwest shows refrigerated trailers; focusing on the Black Sea displays Ro-Ro capacity near Istanbul. This gives operators real-time fleet visibility across international shipping corridors.

## Cargo Sourcing for Shippers and Forwarders

Shippers and freight forwarders find transport through two main workflows on the map: submitting a request form or applying filters to existing transport listings.

The Request a Quote form collects operational parameters:
* Cargo category and details
* Transportation mode
* Container type and quantity
* Weight
* Departure and arrival route points
* Ready to load date
* Freight Basis terms
* Associated services and extra notes

Submitting the form automatically posts the request onto Logistics Map Transport. Incoming quotes land in the Virtual Office Dashboard within minutes. Each quote displays carrier details, transport unit specifications, price (fixed or per kilometer), and terms for booking. Shippers can accept an offer with one click, receive booking confirmation, and track the shipment.

Users searching existing market offers enter departure and arrival points or filter transport cards by:
* Location
* Ready-to-load and unloading dates
* Transport ID
* Transport asset type
* Price structure (per kilometer, flat rate, or daily rate)

Supported equipment types cover five transport modes:
* **Containers:** Standard, High Cube, Refrigerated, Open Top, Flatrack, Bulk, Tank, Platform, Pallet Wide, and related types.
* **Trucks:** Custom truck, Tilt, Mega, Jumbo, Dry van, Metal body truck, Van, Conestoga, Isoterm truck, Isoterm van, Refrigerator, Refrigerator van, Dump truck, Tank truck, Grain carrier, Car carrier (Autocart), Logging & pipes truck, Drop-side platform, Open platform, Flatbed truck, Lowboy truck (Heavy loader), Cattle truck, and Coil carrier.
* **Vessels:** Bulk carrier, Containership, General cargo vessel, Barge, Product tanker, Crude carrier, Asphalt carrier, Chemical tanker, Gas carrier, Heavy-lift, Livestock, Refrigerated, Ro/Ro, and Wood chip.
* **Wagons:** Custom, Covered, Freight semi-wagon, Hopper, Flat, Container platform, High side wagon, Side dump wagon, and Tank wagon.
* **Aircraft:** Custom aircraft, Airbus, Boeing, McDonnell Douglas, Eurocopter, Mi’s, YAK, and charter flights.

Carrier listings pull from distinct databases: SeaRates for containers and vessels, LandRates for trucks and wagons, and AirRates for aircraft.

Each transport card displays an image, route location, container type, carrier name, ready date, cubic capacity, carrying capacity, volume, and rate. Users can copy direct card links to share with partners or save for later.

To secure equipment, shippers open a transport card, enter their destination and target price, and apply. This digital freight matching process lets cargo owners review 10 to 50 organized quotes in one dashboard instead of calling multiple providers individually.

## Fleet Management and Lead Generation for Carriers

Carriers and asset owners list available capacity through the Virtual Office Profile under Activity, in the Transport tab.

Clicking Add Transport or New Transport opens the listing form:
* **General information:** Unit category, transport name, type, model, number, and carrier name.
* **Parameters:** Cubic capacity and carrying capacity (mandatory); length, width, and height (optional).
* **Location:** Loading location and ready-to-load date.
* **Preferred destination (optional):** Intended unloading route and date for gathering LCL cargo.
* **Price (optional):** Fixed or minimum rate, downtime fees for loading or discharging, currency, and payment methods.
* **Additional information (optional):** Service description, equipment photos, and extra operational notes.

Saving the form publishes the asset to Logistics Map Transport immediately. Updates made in the Virtual Office update automatically on the public map. Fleet managers can filter by My transport or My company's transport to verify how listings appear to shippers.

Direct booking inquiries arrive under the Requests tab in the Virtual Office Dashboard. Operators reply with customized offers, lump-sum quotes, itemized breakdowns, or Structural Quotes.

Promoting available equipment helps carriers secure backhaul capacity, fill empty runs, gather FCL or LCL shipments, and sell equipment in international markets. Direct map placement improves overall asset utilization and eliminates empty miles on return legs.

## Web Integration and API Synchronization

Companies can embed this white-labeled tool into their own websites. Cargo owners gain a custom tender platform, while transport providers create a branded map for fleet promotion and lead generation. Integration demos are available upon request.

The Logistics Map API synchronizes fleet listings and freight requests with external software. Key capabilities include:
* Uploading shipping requests and transport units
* Exporting filtered leads into ERP or TMS platforms
* Managing dynamic freight pricing

The API connects with enterprise systems like SAP or custom internal dashboards. Integration access and technical documentation are available by contacting it.sales@searates.com."""

# Sentence level comparison
def get_sentences(text):
    return [s.strip() for s in re.split(r'[\.\n\*\-\•]', text) if len(s.strip().split()) >= 6]

orig_sents = get_sentences(orig)
rewrite_sents = get_sentences(rewrite)

def clean_seq(text):
    return re.sub(r'[^a-z0-9 ]', '', text.lower()).split()

for rs in rewrite_sents:
    rw = clean_seq(rs)
    for i in range(len(rw) - 5):
        ngram = rw[i:i+6]
        # check if ngram appears in orig
        ngram_str = " ".join(ngram)
        # see if in orig
        orig_clean = " ".join(clean_seq(orig))
        if ngram_str in orig_clean:
            print(f"Match: '{ngram_str}' in sentence: '{rs}'")

