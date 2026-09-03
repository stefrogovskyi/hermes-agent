import re

title = "Wheel Stops and Bollards for Efficient Freight Docks"
meta_title = "Wheel Stops & Bollards: Freight Bay Risk Mitigation"
meta_description = "Simple tools like dock wheel stops and warehouse traffic control bollards protect infrastructure, guide vehicles, and prevent accidents in freight bays."

body = """Loading and unloading cargo remains a stubborn bottleneck across ports, rail terminals, and distribution centers. Minor driving miscalculations at the bay stall operations, damage freight, or cause costly structural repairs. Heavy vehicles and ground personnel share tight spaces. Physical safeguards prevent expensive disruptions.

## Wheel Stops for Bay Alignment and Worker Protection

A reversing trailer must hit the dock mark cleanly on the first try. Dock wheel stops and chocks act as solid physical barriers at the edge of loading bays and parking slots. Drivers feel the tire contact immediately. That physical signal stops overruns before a trailer collides with dock seals, equipment, or wall structures. Eliminating repeated pull-outs and repositioning saves driver minutes on every turnaround.

Unintended vehicle movement creates severe hazards for ground crews working nearby. A trailer drifting forward or rolling backward during pallet transfer can injure personnel working around the vehicle. Secured wheel stops anchor stationary trucks. They provide a final defense against vehicle movement while crews work inside and behind the trailer.

## Bollards for Facility Infrastructure Protection and Traffic Flow

Heavy machinery and trucks frequently clip building structures during tight turns. Warehouse traffic control bollards absorb or deflect vehicle strikes before an impact damages dock doors, walls, or building corners. Protecting these vulnerable areas maintains facility infrastructure protection, preventing site downtime and unexpected repair bills.

Beyond structural defense, these sturdy vertical posts establish orderly traffic lanes across crowded yards. Placed near entrances and bay perimeters, bollards mark clear routes for incoming drivers while blocking access to restricted zones. They also create designated pedestrian boundaries that separate worker pathways from moving vehicles, keeping staff safe from traffic.

## Combined Impact on Yard Operations

Wheel stops keep trucks positioned correctly at the bay. Bollards safeguard surrounding structures and guide yard movement. Together, these simple physical installations form an effective setup for loading dock safety equipment and freight bay risk mitigation. Preventing structural collisions keeps daily operations smooth, reducing insurance premiums and maintenance delays across the facility."""

print(f"Title length ({len(title)}): {title}")
print(f"Meta-Title length ({len(meta_title)}): {meta_title}")
print(f"Meta-Description length ({len(meta_description)}): {meta_description}")

# Check 1: Em-dashes
full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"
em_dashes = re.findall(r'—|--| - ', full_text)
print(f"Em-dashes count: {len(em_dashes)}")

# Check 2: Banned AI clichés
cliches = [
    "delve", "testament", "crucial role", "vital role", "integral role", "pivotal role",
    "in today's", "worth noting", "game-changer", "seamless", "landscape", "beacon",
    "foster", "tapestry", "nestled", "elevate", "ever-evolving", "paramount", "underscores",
    "vibrant", "realm", "pivot", "synergy", "furthermore", "moreover", "in addition",
    "additionally", "ensure", "ensuring", "plays a key role"
]
found_cliches = [c for c in cliches if c in full_text.lower()]
print(f"Banned AI clichés found: {found_cliches}")

# Check 6: Over-explaining connectors
connectors = ["that's why", "which is why", "that explains why", "this is because", "because of this", "this means that"]
found_connectors = [conn for conn in connectors if conn in full_text.lower()]
print(f"Connectors found: {found_connectors}")

# Check 7: Contrastive negation
negations = re.findall(r'\b(not X|instead of|rather than|X, not Y)\b', full_text, re.IGNORECASE)
print(f"Contrastive negations found: {negations}")

# Check 10: Symmetric antithesis
antithesis = re.findall(r'\b(not only|while .*?,|from .*? to)\b', body, re.IGNORECASE)
print(f"Antithesis found: {antithesis}")

# Check keywords
keywords = [
    "loading dock safety equipment",
    "warehouse traffic control bollards",
    "dock wheel stops and chocks",
    "facility infrastructure protection",
    "freight bay risk mitigation"
]
for kw in keywords:
    print(f"Keyword '{kw}' in text: {kw.lower() in full_text.lower()}")
