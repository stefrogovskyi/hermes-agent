import json
import re

title = "SeaRates Release Notes: Week 37 2024 Platform Updates"
meta_title = "SeaRates Updates: Week 37 2024 Tools and API Changes"
meta_description = "SeaRates Week 37 updates add a Transport tab to the Logistics Map, improve container load optimization, and expand multi-carrier tracking integration."

body_markdown = """# SeaRates Week 37 Development Update

Regular platform updates keep freight management tools aligned with operational requirements. In the Week 37 release, SeaRates expanded booking visibility within the Logistics Map interface, refreshed carrier tracking connections, and updated spatial parameters inside loading calculation tools.

## Transport Units on the Logistics Map

A new Transport tab adds dedicated visibility inside the Logistics Map tool. Users can now browse transport units available for booking, with details on equipment types, vehicle models, current locations, target destinations, rate quotes, and availability dates.

Data renders simultaneously in list view and on map pins. Selecting an entry opens detailed vehicle cards, where filters allow users to narrow results by location, transport type, or price range. Standard sharing links let teams copy exact unit listings. Shippers can also submit packing requests with specific routes and prices, or start a direct chat with account managers regarding selected units.

## Carrier Connections and Dashboard Tools

Air cargo tracking features enhanced integration with providers, including Air France. Maritime tracking underwent updates to refine tracking connections across lines including OOCL, Asyad Line, CMA CGM, Sarjak Container Lines, Maersk, Akkon Lines, Atlantic Container Line (ACL), and Grimaldi Deep Sea S.P.A.

On the web interface, open shipment cards now feature a Follow button for direct addition into the Dashboard.

Navigation additions include new top-menu links for Parcel Tracking API and Parcel Tracking Web. Explanatory content was refreshed on Container Tracking, Tracking System API, and For Carriers pages. SeaRates launched a Quotation System landing page. Airline vendor listings went live on AirRates.com, paired with railway operator directories on LandRates.com to expand coverage across global supply chains.

## Schedule Search Expansion

Searching vessel schedules by ship name now supports Pacific International Lines (PIL). For Ro-Ro transportation, Wallenius Wilhelmsen and Sallaum Lines now process point-to-point schedule searches.

## Load Calculator Spacing Adjustments

Updates to container load calculation focus on practical spacing parameters. The web calculator sets Height as a default third dimension under the Spacing settings section.

Box orientation control now includes Length and Width marks with checkboxes to flip positioning. For shipments containing uniform box dimensions, the step-by-step loading plan algorithm has been updated.

## Pipeline Projects

Upcoming releases will introduce new web features for air cargo tracking, Geocoding API autocomplete v0.8, a revised Route Planner API release, and Freight Index 1.0. Development continues on mobile app v1.2 with request system integration, Load Calculator v2.2, Booking System v1.1, parcel tracking interfaces, rail tracking on LandRates.com, standalone tracking APIs, mapping infrastructure, and unified web tracking environments."""

# Source text
source_text = """We sincerely appreciate your ongoing support and encouragement here at SeaRates. We are devoted to refining our service and are eager to highlight new features designed to make your experience more convenient.
Ensure you have the most recent details by looking at our previous updates.
What’s new for week 37:
We are glad to announce that SeaRates has added the ‘Transport’ tab into the Logistics Map tool. With this functionality, you promptly access to transports are available for bookings with all details on types, models, locations, desired destinations, prices, date of readiness, and much more.
We have implemented a wide range of features, including the following:
View the list of available transport units and visualize their location on the map;
View detailed information about the transport and its location or the desired transportation route;
Go to detailed information about the transport both from the list of cards and from the map;
Filter transport by location, type, price range, etc.
Copy a link to the selected unit of transport;
Send requests for transport packing, indicating the desired directions of transportation and prices;
Chat with the manager about the selected transport units.
Air Cargo Tracking improvements:
We have enhanced our work with providers, including Air France.
Tracking System updates:
For the web version, we have added the ‘Follow’ button to the open shipment card for the easiest adding into your Dashboard.
Finally, we have enhanced our work with providers, including Orient Overseas Container Line (OOCL), Asyad Line, CMA CGM, Sarjak Container Lines, Maersk, Akkon Lines, Atlantic Container Line (ACL), and Grimaldi Deep Sea S.P.A.
Ship Schedules enhancements:
We are pleased to present that we have added support for the PIL for schedules searching by Vessel, as well as Wallenius Wilhelmsen and Sallaum Lines for Ro-Ro transportation by Points.
Load Calculator improvements:
For the web version, we have added the default 'Height' parameter as the third dimension in the settings in the 'Spacing settings' section. To set the positioning of the box, you can flip it through the Length and/or Width marks and checkboxes.
Also, we have improved the algorithm for building a step-by-step loading plan in cases when a container is loaded with identical boxes.
Other updates:
We have added Parcel Tracking API and Parcel Tracking Web pages into the ‘Integrations’ top menu, updated the content for Container Tracking, Tracking System API, and For Carriers pages, as well as created the Quotation System landing page.
Finally, we have created Vendors – Airlines page for AirRates.com and Vendors – Railway Operators page for LandRates.com. With the triad of SeaRates, AirRates, and LandRates, you explore wider coverage of solutions for the supply chain to ensure a customized approach for your logistics and trading operations upon any needs your business has.
Announcements:
New features to the Air Cargo Tracking Web Version
Geocoding API / Autocomplete service Version 0.8
New Version of Route Planner API
Freight Index 1.0
Mobile App Version 1.2 with Request System feature
Load Calculator Version 2.2
Booking System Version 1.1
Parcel Tracking API
Rail Tracking API
Rail Tracking Web on LandRates.com
Map platform
Unified Tracking System WEB"""

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def get_ngrams(words, n=6):
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

def main():
    print("=== CHECK 1: EM-DASHES ===")
    em_dashes = []
    for field_name, val in [("Title", title), ("Meta Title", meta_title), ("Meta Description", meta_description), ("Body", body_markdown)]:
        cnt = val.count("—") + val.count("--")
        print(f"{field_name} em-dashes: {cnt}")
        if cnt > 0:
            em_dashes.append(field_name)

    print("\n=== CHECK 2: LENGTHS ===")
    print(f"Title len: {len(title)} (max 60)")
    print(f"Meta Title len: {len(meta_title)} (max 60)")
    print(f"Meta Description len: {len(meta_description)} (max 155)")

    print("\n=== CHECK 3: 6-GRAM OVERLAPS ===")
    source_words = normalize(source_text)
    body_words = normalize(body_markdown)
    source_6grams = get_ngrams(source_words, 6)
    body_6grams = get_ngrams(body_words, 6)

    overlaps = source_6grams.intersection(body_6grams)
    print(f"Total 6-gram overlaps: {len(overlaps)}")
    exempt_terms = [
        "orient overseas container line", "asyad line", "cma cgm", "sarjak container lines",
        "maersk", "akkon lines", "atlantic container line", "grimaldi deep sea",
        "container tracking tracking system api", "tracking system api and for carriers",
        "for carriers pages", "wallenius wilhelmsen and sallaum lines",
        "vendors airlines page for airratescom", "vendors railway operators page for landratescom",
        "container line acl and grimaldi"
    ]
    non_exempt = []
    for o in overlaps:
        is_exempt = any(term in o for term in exempt_terms)
        print(f" - '{o}' (Exempt: {is_exempt})")
        if not is_exempt:
            non_exempt.append(o)

    print(f"Non-exempt 6-gram overlaps count: {len(non_exempt)}")

    print("\n=== CHECK 4: CONTRASTIVE NEGATION & CONNECTORS ===")
    not_cnt = len(re.findall(r'\bnot\b', body_markdown.lower()))
    instead_cnt = len(re.findall(r'\binstead of\b', body_markdown.lower()))
    rather_cnt = len(re.findall(r'\brather than\b', body_markdown.lower()))
    print(f"'not' count: {not_cnt}, 'instead of' count: {instead_cnt}, 'rather than' count: {rather_cnt}")

if __name__ == "__main__":
    main()
