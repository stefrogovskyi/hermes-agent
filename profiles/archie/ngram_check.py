import re

source = """We value your continued support of SeaRates and always excited to provide you with additional services that will exceed your expectations. Improving the quality of our services is a top priority for us.
Please refer to our earlier publications for the most up-to-date information.

What’s new for week 52:
We are glad to announce a new version of the Route Planner API. Create, review, edit, and manage your custom routes with unique ID numbers to track them in the Tracking System and share them with your customers and partners. Generate your route options and add all key details: locations with types (seaport, airport, road/rail terminal) and logistics events for each of them, and transport types in detail.
The new version of the Route Planner API completes routing and adds information about each location if needed automatically. Kindly check the API documentation in our Developer Portal.

Tracking System updates:
We have upgraded how we work with providers, including ZIM, Yang Ming, Blue Water Lines (BWL), Swire Shipping, Interasia Lines, and Route Planner.

Air Cargo Tracking enhancements:
We have improved how we work with providers, including Air Canada and DHL Aviation.

Demurrage & Storage Calculator updates:
We have added the option to choose cost calculations for import and export modes. The mode you selected will be displayed in the downloaded file.

Ship Schedules improvements:
We are glad to announce we have added support to Pacific Forum Line by Port.
Moreover, we have added the option to request schedules by alternative SCAC values.
Finally, we have improved how we work with providers, including Arkas and PIL by Points and Ignazio Messina by Vessel.

Other updates:
We have updated the tooltip for transport type to display a full description, e.g., "40'Standard On terminal" for the Logistics Map tool.
Also, we have created a For Tracking Companies landing page and FAQs sections on the CO2 Calculator and Route Planner tools’ pages.
Finally, we have updated the design and content for Uncollected or abandoned cargoes, SeaLine Explorer, World Sea Ports, and Shipping in 10-foot containers pages.

Announcements:
AirRates app release
Logistics Map integration
Request a Quote form improvements
SeaRates Autocomplete integrated with CO2 Calculator
Unified Tracking System
Parcel Tracking Web
Load Calculator Web 3.0 (new design and features)
Map Platform"""

rewrite = """Title: SeaRates Week 52 2024 Updates: Route API & Tracking
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

# Let's find longest matching substrings between source and rewrite (case-insensitive)
def find_matching_substrings(s1, s2, min_len=20):
    s1_lower = s1.lower()
    s2_lower = s2.lower()
    
    # split into sentences or chunks and check
    import difflib
    matcher = difflib.SequenceMatcher(None, s1_lower, s2_lower)
    blocks = matcher.get_matching_blocks()
    
    matches = []
    for b in blocks:
        if b.size >= min_len:
            sub1 = s1[b.a:b.a+b.size]
            sub2 = s2[b.b:b.b+b.size]
            matches.append((b.a, b.b, b.size, sub1, sub2))
    return matches

matches = find_matching_substrings(source, rewrite, min_len=15)
print("Substrings matching len >= 15:")
for m in matches:
    print(f"Len {m[2]}: SRC: {repr(m[3])} | REW: {repr(m[4])}")
