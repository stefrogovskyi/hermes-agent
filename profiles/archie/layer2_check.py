import re

rewrite = """Title: Fixing European Port Congestion in 2025
Meta-Title: European Port Congestion 2025: Delays & Routes
Meta-Description: Handle European port congestion 2025. Find Rotterdam and Antwerp freight alternatives, manage Rhine barge water levels, and check container tracking API.

Body:
When the tide turns against Europe's biggest harbors, supply chains learn how thin their safety margins really were.

June 2025 brought unprecedented delays across Northern Europe. Vessels lined up outside Rotterdam and Antwerp facing waits of 48 to 72 hours. Some ships waited days for a berth. Summer container demand surged while operational constraints and staff strikes reduced port capacity. High cargo volumes overburdened modern port infrastructure.

Rotterdam and Hamburg usually process ships within 8 to 12 hours. Backlogs are pushing cargo to smaller facilities. Smaller ports operate with less equipment and fewer workers, so waits of 10 to 30 hours are standard there during peak summer months.

Managing Northern European port delays in 2025 requires shifting cargo away from overloaded hubs. Rotterdam and Antwerp freight alternatives offer clearer pathways into the continent. Hamburg and Bremerhaven handle large volumes with fewer delays than Rotterdam and Antwerp. Shippers moving goods through Northern Europe can look to Felixstowe, where waiting times hold between 10 and 30 hours due to lower congestion. Stockholm and Tallinn cover Baltic entries, while Liverpool serves southwestern approaches. Gdansk processes arrivals in 24 to 48 hours for Central and Eastern European destinations. Trieste provides a 20 to 40 hour wait, linking sea routes directly to rail and road networks across Central Europe.

Shipping lines are adjusting their networks. MSC extended transit times on two major routes due to port bottlenecks and market conditions. Asian carriers including HMM reported Hamburg delays reaching up to six days. Data from Lloyd's List Intelligence and Drewry showed average waits in Antwerp rising from 32 hours in early April to 44 hours by late May, a 37 percent increase. Delays are expected to last through the peak season in August 2025.

Maersk restructured trade routes by dropping Rotterdam from certain loops and prioritizing Hamburg. In May 2025, Maersk introduced a domestic transshipment fee of EUR 10 per TEU for road, rail, barge, or intermodal transport serving Rotterdam and Antwerp. The fee protects long-distance land transportation capacity.

Shippers can compare rate breakdowns across reliable carriers in Logistics Explorer to secure freight rates. Comparing sailing schedules helps identify smaller ports with faster cargo processing. Booking freight in advance offsets potential schedule disruptions.

Inland waterways face operational limits this season. Drought reduced Rhine barge water levels and affected nearby rivers, lowering cargo capacity on inland waterways. Barge operators are increasing cargo volume per voyage and scheduling shipments early before water levels drop. For high-priority cargo on intra-European routes, rail and truck transport serve as backup options.

Tracking tools provide visibility when schedules change. Container Tracking by SeaRates updates status via container numbers, bills of lading, or booking references from over 200 shipping lines and leasing companies. The tool delivers predictive ETA data, route changes, customs events, and voyage information while managing up to 25 shipment exceptions. Connecting these feeds through a container tracking API supplies real-time alerts when carriers alter schedules."""

ai_words = [
    "delve", "delving", "tapestry", "landscape", "pivotal", "paramount", "testament",
    "fostering", "foster", "seamless", "seamlessly", "vital", "crucial", "beacon",
    "game-changer", "gamechanger", "realm", "harness", "harnessing", "unravel",
    "navigate", "navigating", "robust", "synergy", "underscores", "underscore",
    "spearhead", "nestled", "intricate", "vibrant", "holistic", "empower",
    "empowering", "elevate", "transformative", "unprecedented", "beacon", "catalyst",
    "leverage", "leveraging", "multifaceted", "proactive", "proactively",
    "burgeoning", "plethora", "myriad", "topography", "synergistic", "cornerstone",
    "orchestrate", "orchestrating", "embark", "navigating"
]

cliches = [
    "when the tide turns", "thin safety margins", "clearer pathways", "at the end of the day",
    "in today's world", "it's important to remember", "a double-edged sword", "the tip of the iceberg"
]

print("--- Word-Level AI Tells Check ---")

# Check em-dashes
em_dashes = len(re.findall(r'—|--', rewrite))
print(f"Em-dashes count: {em_dashes}")

# Check AI filler words
found_ai_words = {}
for word in ai_words:
    m = re.findall(rf'\b{re.escape(word)}\b', rewrite, re.IGNORECASE)
    if m:
        found_ai_words[word] = len(m)

print("AI Filler Words found:", found_ai_words)

# Check clichés
found_cliches = {}
for phrase in cliches:
    m = re.findall(rf'\b{re.escape(phrase)}\b', rewrite, re.IGNORECASE)
    if m:
        found_cliches[phrase] = len(m)

print("Clichés found:", found_cliches)

