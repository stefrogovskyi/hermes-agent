import re

title = "SeaRates Release Notes: Week 37 2024 Platform Updates"
meta_title = "SeaRates Updates: Week 37 2024 Tools and API Changes"
meta_description = "SeaRates Week 37 updates add a Transport tab to the Logistics Map, improve container load optimization, and expand multi-carrier tracking integration."

body = """# SeaRates Week 37 Development Update

Shipping software changes fast, but quiet weekly iterations keep freight operations running without unnecessary friction. In the Week 37 release, SeaRates expanded booking visibility across road transit and refreshed tracking connectors while tweaking spatial calculations inside loading tools.

## Transport Units on the Logistics Map

A new Transport tab transforms the interface into a functional logistics map transport directory. Users can now browse transport units ready for booking, viewing specific equipment types, vehicle models, current locations, target destinations, rate quotes, and availability dates.

Data renders simultaneously in list view and on map pins. Selecting an entry opens detailed vehicle cards, where filters allow users to narrow results by location, vehicle type, or price range. Standard sharing links let teams copy exact unit listings. If a haulage scenario requires tailored setup, shippers can submit packing requests with specific routes and budget limits, or start a direct chat with account managers.

## Carrier Connections and Dashboard Tools

Air cargo tracking now includes deeper data feeds from Air France. Maritime tracking underwent updates to refine multi-carrier tracking integration across lines including OOCL, Asyad Line, CMA CGM, Sarjak Container Lines, Maersk, Akkon Lines, Atlantic Container Line (ACL), and Grimaldi Deep Sea S.P.A.

On the web interface, shipment cards now feature a Follow button for one-click transfers into the main Dashboard.

Navigation additions include new menu items for parcel tracking API integration and Parcel Tracking Web. Explanatory content was refreshed on Container Tracking, Tracking System API, and For Carriers pages. SeaRates launched a Quotation System landing page. Airline vendor listings went live on AirRates.com, paired with new railway operator directories on LandRates.com to expand coverage across transport modes.

## Schedule Search Expansion

Searching vessel schedules by ship name now supports Pacific International Lines (PIL). For heavy cargo and rolling stock, Ro-Ro vessel schedules under Wallenius Wilhelmsen and Sallaum Lines now process point-to-point route searches.

## Load Calculator Spacing Adjustments

Updates to container load optimization focus on practical loading parameters. The web calculator sets Height as a default third dimension under the Spacing settings tab.

Cargo orientation control now includes Length and Width marks with selection checkboxes to flip box positioning. For full container loads containing uniform box dimensions, the step-by-step loading algorithm was revised to render cleaner cargo placement sequences.

## Pipeline Projects

Upcoming builds will introduce web features for air tracking, Geocoding API autocomplete v0.8, a new Route Planner API release, and Freight Index 1.0. Development continues on mobile app v1.2 with request integration, Load Calculator v2.2, Booking System v1.1, a dedicated real-time freight tracking API, rail tracking on LandRates.com, and a unified web tracking interface."""

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# Check sentences
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', body) if s.strip() and not s.startswith('#')]
print(f"Total sentences in body: {len(sentences)}")

for idx, s in enumerate(sentences, 1):
    print(f"{idx}. {s}")

