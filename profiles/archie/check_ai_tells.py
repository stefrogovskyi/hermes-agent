source = """Title: SeaRates Week 52 2024 Updates: Route API & Tracking
Meta Title: SeaRates Week 52 2024 Updates | Logistics API & Tools
Meta Description: Explore SeaRates Week 52 2024 updates: new route planner API capabilities, carrier tracking fixes, demurrage calculation modes, and vessel schedule tools.

# SeaRates Week 52 2024 Updates: Route API & Tracking

The final shipping update of 2024 brings technical changes across SeaRates tools, expanding data access and refining carrier connections. Here is what changed in Week 52.

### Route Planner API Version Upgrade

A new version of the route planner API is live in the Developer Portal. Logistics teams can create, review, edit, and manage custom routes using assigned unique ID numbers. These ID numbers allow you to track custom routes inside the Tracking System or share route parameters with clients and logistics partners.

When generating route options, users can specify key details such as location types (including seaports, airports, and road or rail terminals), logistics events for each location, and transport types in detail. The updated API completes routing automatically and adds detailed information for each location whenever needed.

### Container & Air Cargo Tracking Systems

Data handling for the container tracking API received updates across several ocean carriers. Data processing routines were adjusted for ZIM, Yang Ming, Blue Water Lines (BWL), Swire Shipping, Interasia Lines, and Route Planner.

For air cargo tracking, service response handling was updated for Air Canada and DHL Aviation.

### Demurrage & Storage Calculator Modes

The demurrage and storage calculator now includes an option to choose cost calculations specifically for import or export modes. The selected calculation mode stays attached to the file and appears directly in downloaded reports.

### Vessel Schedules SCAC & Carrier Queries

Ship Schedules added search support for Pacific Forum Line by Port. Users searching for schedules can also request data using alternative vessel schedules SCAC codes.

Carrier data processing was improved for Arkas and PIL (searched by Points), alongside Ignazio Messina (searched by Vessel).

### Interface Tooltips, Landing Pages, & FAQ Additions

- The Logistics Map tooltip now displays complete transport type descriptions, such as 40'Standard On terminal.
- A dedicated landing page is live for tracking companies.
- FAQ sections were added to the tool pages for the CO2 Calculator and Route Planner.
- Page content and visual design were updated for Uncollected or abandoned cargoes, SeaLine Explorer, World Sea Ports, and Shipping in 10-foot containers.

### Announcements & Freight Logistics Automation

SeaRates continues updating its platform tools to support freight logistics automation, with recent developments and feature rollouts including:

- AirRates app release
- Logistics Map integration
- Request a Quote form improvements
- SeaRates Autocomplete integrated with CO2 Calculator
- Unified Tracking System
- Parcel Tracking Web
- Load Calculator Web 3.0 (new design and features)
- Map Platform"""

ai_words = [
    "delve", "testament", "tapestry", "realm", "beacon", "foster", "crucial",
    "paramount", "pivotal", "vital", "seamless", "seamlessly", "elevate", 
    "landscape", "game-changer", "transformative", "ever-evolving", "holistic",
    "unwavering", "spearhead", "nestled", "unveiled", "unveil", "boasts",
    "important to note", "it is worth noting", "it's worth noting", "notably",
    "furthermore", "moreover", "in conclusion", "to sum up", "as a result",
    "serves as", "stands as"
]

found = []
for w in ai_words:
    if w in source.lower():
        found.append(w)

print("Em-dashes count:", source.count("—") + source.count("--"))
print("AI clichés found:", found)
