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

# Split into paragraphs
paragraphs = [p.strip() for p in rewrite.split('\n\n') if p.strip()]

# Filter metadata (Title, Meta-Title, Meta-Description)
body_paras = []
for p in paragraphs:
    if p.startswith("Title:") or p.startswith("Meta-Title:") or p.startswith("Meta-Description:"):
        continue
    if p.startswith("Body:"):
        p = p[5:].strip()
    body_paras.append(p)

print(f"Total Body Paragraphs: {len(body_paras)}")

print("\n--- 1. Paragraph Length Breakdown (Staircase / Uniformity check) ---")
for i, p in enumerate(body_paras, 1):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    words = p.split()
    print(f"Para {i}: {len(words)} words | {len(sentences)} sentences | Words per sentence: {[len(s.split()) for s in sentences]}")

print("\n--- 2. Explicit Connectors Check ---")
connectors = ["that's why", "which is why", "that is why", "which is reason why", "furthermore", "moreover", "additionally", "in addition", "consequently", "thus", "therefore", "hence", "as a result"]
for conn in connectors:
    matches = re.findall(rf'\b{re.escape(conn)}\b', rewrite, re.IGNORECASE)
    if matches:
        print(f"Connector found: '{conn}' x{len(matches)}")

print("\n--- 3. Contrastive Negation Check ---")
# Examples: "X, not Y", "not X, but Y", "instead of", "rather than", "not only... but also"
neg_patterns = [
    r'\binstead of\b',
    r'\brather than\b',
    r'\bnot only\b',
    r'\bnot just\b',
    r'\b,\s*not\s+\b',
    r'\bnot\s+[\w\s]+,\s*but\b'
]
for pat in neg_patterns:
    matches = re.findall(pat, rewrite, re.IGNORECASE)
    if matches:
        print(f"Contrastive negation pattern '{pat}': {matches}")

print("\n--- 4. Aphoristic Endings Check ---")
# Check the last sentence of each paragraph for aphoristic/preachy/moralistic or summary claims
for i, p in enumerate(body_paras, 1):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    last_s = sentences[-1]
    print(f"Para {i} last sentence: \"{last_s}\"")

print("\n--- 5. Parallel Twin Sentences / Sentence Patterns ---")
# Check if sentences within a paragraph start with similar structures
for i, p in enumerate(body_paras, 1):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    first_words = [s.split()[0] if s.split() else '' for s in sentences]
    print(f"Para {i} sentence starters: {first_words}")

