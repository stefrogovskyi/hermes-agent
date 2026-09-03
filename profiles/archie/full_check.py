import re

title = "SeaRates Week 52 2024 Updates: Route API & Tracking"
meta_title = "SeaRates Week 52 2024 Updates | Logistics API & Tools"
meta_desc = "Explore SeaRates Week 52 2024 updates: new route planner API capabilities, carrier tracking fixes, demurrage calculation modes, and vessel schedule tools."

body = """The final shipping update of 2024 brings technical changes across SeaRates tools, expanding data access and refining carrier connections. Here is what changed in Week 52.

### Route Planner API Version Upgrade

A new version of the **route planner API** is live in the Developer Portal. Logistics teams can create, review, edit, and manage custom routes using assigned unique ID numbers. These ID numbers allow you to track custom routes inside the Tracking System or share route parameters with clients and logistics partners.

When generating route options, users can specify key details such as location types (including seaports, airports, and road or rail terminals), logistics events for each location, and transport types in detail. The updated API completes routing automatically and adds detailed information for each location whenever needed.

### Container & Air Cargo Tracking Systems

Data handling for the **container tracking API** received updates across several ocean carriers. Data processing routines were adjusted for ZIM, Yang Ming, Blue Water Lines (BWL), Swire Shipping, Interasia Lines, and Route Planner.

For **air cargo tracking**, service response handling was updated for Air Canada and DHL Aviation.

### Demurrage & Storage Calculator Modes

The **demurrage and storage calculator** now includes an option to choose cost calculations specifically for import or export modes. The selected calculation mode stays attached to the file and appears directly in downloaded reports.

### Vessel Schedules SCAC & Carrier Queries

Ship Schedules added search support for Pacific Forum Line by Port. Users searching for schedules can also request data using alternative **vessel schedules SCAC** codes.

Carrier data processing was improved for Arkas and PIL (searched by Points), alongside Ignazio Messina (searched by Vessel).

### Interface Tooltips, Landing Pages, & FAQ Additions

- The Logistics Map tooltip now displays complete transport type descriptions, such as `40'Standard On terminal`.
- A dedicated landing page is live for tracking companies.
- FAQ sections were added to the tool pages for the CO2 Calculator and Route Planner.
- Page content and visual design were updated for Uncollected or abandoned cargoes, SeaLine Explorer, World Sea Ports, and Shipping in 10-foot containers.

### Announcements & Freight Logistics Automation

SeaRates continues updating its platform tools to support **freight logistics automation**, with recent developments and feature rollouts including:

- AirRates app release
- Logistics Map integration
- Request a Quote form improvements
- SeaRates Autocomplete integrated with CO2 Calculator
- Unified Tracking System
- Parcel Tracking Web
- Load Calculator Web 3.0 (new design and features)
- Map Platform
"""

def check_all():
    print("--- RUNNING DETAILED RULE CHECKS ---")
    
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    # Rule 1: Em-Dashes
    dashes = ["—", "--"]
    for d in dashes:
        if d in full_text:
            print(f"FAIL Rule 1: Found dash '{d}'")
            
    # Length checks
    print(f"Title len: {len(title)} (max 60) -> {'OK' if len(title)<=60 else 'FAIL'}")
    print(f"Meta Title len: {len(meta_title)} (max 60) -> {'OK' if len(meta_title)<=60 else 'FAIL'}")
    print(f"Meta Desc len: {len(meta_desc)} (max 155) -> {'OK' if len(meta_desc)<=155 else 'FAIL'}")
    
    # Rule 2: AI clichés
    cliches = [
        "important to note", "delve into", "in today's world", "testament to", 
        "game-changer", "key aspect", "not just", "in conclusion", "furthermore", 
        "moreover", "seamless", "robust", "leverage", "revolutionize", "tapestry",
        "beacon", "landscape", "unlock", "elevate", "cutting-edge", "game changer",
        "excited to announce", "pleased to announce", "thrilled"
    ]
    for c in cliches:
        if c in full_text.lower():
            print(f"FAIL Rule 2: Found cliché '{c}'")
            
    # Rule 6: Over-explaining connectors
    connectors = ["that's why", "which is why", "that's a sign of", "this is why", "this means that", "this ensures that"]
    for conn in connectors:
        if conn in full_text.lower():
            print(f"FAIL Rule 6: Found connector '{conn}'")
            
    # Keywords check
    keywords = [
        "route planner API", "container tracking API", "air cargo tracking", 
        "demurrage and storage calculator", "vessel schedules SCAC", "freight logistics automation"
    ]
    for kw in keywords:
        if kw.lower() in full_text.lower():
            print(f"Keyword present: '{kw}' -> OK")
        else:
            print(f"FAIL Keyword missing: '{kw}'")

check_all()
