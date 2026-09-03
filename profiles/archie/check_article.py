import re

text = """Title: How to Take Your Trucking Company Global
Meta-Title: How to Expand Your Trucking Fleet Internationally
Meta-Description: Grow your trucking business across borders by securing funds, meeting regulations, building local partnerships, and adapting to target markets.

In 2023, the global trucking industry market reached $2656.87 billion. Pursuing cross-border road freight expansion opens up new revenue streams, fresh markets, and broader operations. Moving beyond domestic borders requires careful preparation and strategic decisions based on local laws and foreign market trends.

### Funding Strategy for International Scaling

Entering new international markets demands significant capital. Money is needed to acquire additional vehicles, hire staff, and upgrade operational technology to coordinate logistics across borders. Purchasing an established business in your target market offers an immediate footprint, supplying ready infrastructure, a client base, and active revenue.

Securing transport equipment financing provides loans or leasing options specifically for acquiring trucks, trailers, and heavy-duty gear. This approach expands your fleet without a large upfront cash outlay, preserving working capital for other growth costs. Carriers should also evaluate commercial loans, lines of credit, and government grants created to help small and medium businesses expand internationally.

### Navigating Regulatory Frameworks

Operating in foreign jurisdictions brings unique compliance demands. Non-compliance risks severe fines, shipping delays, or a complete shutdown of operations.

A thorough review of international customs compliance, transportation costs, and licensing rules for drivers and vehicles is essential before sending rigs across borders. Certain nations enforce strict safety or environmental criteria, while others set specific weight and size limits. International trade agreements affect tariffs, taxes, and overall border crossing expenses. Consulting legal professionals or hiring a regulatory compliance officer helps navigate these requirements.

### Building Strategic Regional Partnerships

Carriers do not need to execute an overseas rollout alone. Building strong relationships with established local firms provides invaluable knowledge about regional distribution networks and operating norms.

Working with freight forwarders, customs agents, and local transport companies streamlines cargo movements, customs clearances, and final-stage delivery. Teaming up with logistics tech providers grants access to fleet telematics and route optimization tools. These tools track shipments in real time and maintain clear communication between internal teams and international clients.

### Aligning Operations with Local Expectations

Grasping cultural differences is critical when entering new regions. Methods of doing business vary across borders, so companies must adjust their operational tactics, marketing, and customer support.

Proper local market adaptation requires thorough research into customer needs. Regional preferences influence delivery timelines, payment options, and the types of cargo moved. Communication expectations also differ across borders. Regular business English practice helps teams interact effectively with foreign clients. Translating websites, marketing materials, and service channels into local dialects builds client trust and distinguishes your business from competitors.
"""

# Check 1: Em-dashes, en-dashes, double hyphens
dashes = re.findall(r'[—–]|--', text)
print("Dashes found:", dashes)

# Check 2: Forbidden words/phrases
forbidden = [
    "crucial role", "in today's world", "delve", "important to note", "dive into",
    "seamlessly", "game-changer", "testament to", "landscape", "tapestry", "realm",
    "beacon", "foster", "elevate", "unlock", "pivotal", "vital", "it's not just",
    "not only", "furthermore", "additionally", "moreover", "consequently", "thus",
    "in conclusion", "to sum up"
]

found_forbidden = []
for word in forbidden:
    if word.lower() in text.lower():
        found_forbidden.append(word)
print("Forbidden words found:", found_forbidden)

# Check meta lengths
lines = text.strip().split('\n')
title = lines[0].replace('Title: ', '')
meta_title = lines[1].replace('Meta-Title: ', '')
meta_desc = lines[2].replace('Meta-Description: ', '')

print(f"Title len ({len(title)}): {title}")
print(f"Meta-Title len ({len(meta_title)}): {meta_title}")
print(f"Meta-Description len ({len(meta_desc)}): {meta_desc}")

# Check trend keywords
keywords = [
    "cross-border road freight expansion",
    "transport equipment financing",
    "international customs compliance",
    "fleet telematics and route optimization",
    "local market adaptation"
]

for kw in keywords:
    print(f"Keyword '{kw}': {'FOUND' if kw.lower() in text.lower() else 'MISSING'}")

