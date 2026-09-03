import re

rewrite = """TITLE (H1): SeaRates Product Updates: Week 42, 2024
META TITLE: SeaRates Updates Week 42: Rail Tracking and API Upgrades
META DESCRIPTION: SeaRates launched web rail tracking on LandRates.com, AIS predictive ETA, 8 new airlines, expanded shipping line integrations, and Virtual Office embeds.

BODY:
LandRates.com now features a web version of Rail Tracking. Cargo owners can trace rail shipments using a tracking number to inspect real-time logistics events, route history, equipment details, and status updates on an interactive world map. Shipment cards can be copied directly for instant sharing with partners and customers.

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

original = """What’s new for week 42:

We are glad to introduce the Rail Tracking Web version on LandRates.com. Access an advanced solution to trace your rail cargo just by tracking number. Receive real-time logistics insights and details on events, route, history, equipment, status, and so on. Explore your current cargo location visualized on the world map and copy the shipment card for easy sharing with your partners and customers.

Parcel Tracking enhancements: For the API, we have added departure/arrival dates to the response (estimated and actual).

We have implemented smart Autodetect services and added an ‘AUTODETECT_CANT_DETECT_PARCEL_COMPANY’ status code to the API response.

Furthermore, we have added the list of supported carriers to the Developer Portal.

Air Cargo Tracking updates: We are glad to announce the support for 8 airlines: Air Moldova, Mahan Air, Transcarga International Airways, Vietravel Airlines, Lion Airlines, Super Air Jet, Thai Lion Air, and Wings Air.

For the API, we have improved location tracking and implemented the generation logic of extensive descriptions for logistics events to provide wide data for your air shipments.

Finally, we have enhanced our work with providers, including SAS Cargo, Malaysia Airlines, FedEx Express, Cargolux Airlines International, Cargolux Italia, British Airways, Cargolux, and Emirates.

Tracking System enhancements: We have enhanced the determination logic for container’s current location and updated routing for the API.

Also, we have implemented a new algorithm for predictive ETA determining based on AIS data.

Moreover, we have enhanced our work with providers, including Avana Global FZCO (BALAJI), CK Line, Atlantic Container Line (ACL), Wan Hai, BAL Container Line, Pan Continental Shipping, Yang Ming, Mediterranean Shipping Company (MSC), Dsv Ocean Transport, CMA CGM, PSL Navegacao, Hoegh Autoliners.

Geocoding API/Autocomplete service improvements: The Geocoding API beta is available now. Explore the documentation in the Developer Portal.

Distance & Time enhancements: For the API Version 3.0, we have added the option to specify IATA and ICAO codes in the queries for departure and arrival locations.

Kindly check out the updated documentation in our Developer Portal.

Ship Schedules updates: We have enhanced our work with providers, including KMTC for ‘by Vessel’, as well as PIL and Dong Young for ‘by Port’.

Load Calculator enhancements: For the web-integrated version, we have updated design. Explore the integration capabilities of our smart tool for efficient loading & stuffing.

Virtual Office enhancements: We are proud to announce the Virtual Office integration release. Receive instant access to the Virtual Office with the ability to authorize and register right on your website. Integrate the handy Dashboard and provide this ultimate interface to your customers. Start Virtual Office integration with the code on the Developer Portal.

Moreover, in the Dashboard, you can directly go to the suitable booking or request via points on the world map.

For the ‘Counterparties’ panel, we have added an option to display users registered on the platform in the general list.

Other updates:

We have created Demurrage & Storage Calculator Web integration page and updated content for the SeaRates Help page, as well as for Tracking API section on the Developer Portal for related documentation on APIs.

Also, we have improved content for the Find a Tool page to streamline your searching for the SeaRates digital solutions for logistics & trading. From now on, you can easily filter the tools by Web Access, Web Integration, and API to request the appropriate solution for your needs.

Finally, for LandRates.com, we have updated content and design for the Home page."""

# Check phrase overlap excluding proper nouns, carrier lists, standardized technical feature lists
# Let's inspect all sentences in rewrite and find where terms come from
lines = rewrite.split('\n')
for line in lines:
    line = line.strip()
    if not line: continue
    print(f"\nChecking line: {line[:60]}...")
    # check 6-gram matches in this line
    words = re.findall(r'[A-Za-z0-9_]+', line)
    orig_words = re.findall(r'[A-Za-z0-9_]+', original)
    for n in range(6, len(words)+1):
        for i in range(len(words)-n+1):
            phrase = " ".join(words[i:i+n])
            # search in original
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            if pattern.search(" ".join(orig_words)):
                print(f"  FOUND {n}-gram match: '{phrase}'")

