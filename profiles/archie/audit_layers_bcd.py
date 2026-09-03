import re

rewrite = """Title: How to Use the Demurrage & Storage Calculator
Meta Title: SeaRates Demurrage & Storage Calculator Guide
Meta Description: Calculate demurrage, detention, and storage costs with SeaRates. Get real-time carrier tariffs, compare rates, and prevent unexpected logistics penalties.

Body:
Unplanned demurrage, detention, and storage fees inflate logistics budgets quickly. Late fees accumulate when free days expire unmonitored. The SeaRates Demurrage & Storage Calculator provides instant cost estimates across ocean containers, FTL and LTL trucking, rail freight, air freight, and vessel downtime.

### Live Carrier Tariffs

Instead of contacting port or terminal operators individually, shippers and freight forwarders access live carrier data in one place. Using real-time container tracking & penalty forecasting gives teams early visibility before fees accrue.

### Manual Mode Setup

Review terms, disclaimers, and tooltips across Regime, Discharge date/Empty pick up, Gate out full, Gate in empty/Loading date, Storage, Demurrage, and Detention.

Select Import or Export in the Regime field, then enter dates for discharge or empty pickup. Input gate out full to mark when the full container leaves the terminal. Specify gate in empty or loading to set when the empty container returns. These inputs define the handling window.

Proper terminal storage surcharges & detention rate management requires choosing the right fee category:
- Demurrage applies to overtime at the terminal.
- Detention covers delays outside the terminal.
- Storage applies to extended holding fees.

Set carrier free days and pick a preferred currency. Click Calculate to view total cost breakdowns based on live major carrier tariffs.

### Automatic Mode Calculations

Automatic mode simplifies entries through drop-down menus.

Select Import or Export, pick a container type, specify the discharge port, and choose an available shipping line. Input discharge or empty pickup dates alongside gate out full and gate in empty or loading dates, then click Show tariffs.

Under the Storage section, adjust the Until day field and check currency. Click Calculate to view storage, demurrage, and detention rates converted into chosen local currency. Modifying parameters lets users compare options. Results can be named by container number or custom identifiers and downloaded for reports and analytics.

The tool incorporates automated free time tracking to highlight exact overrun days. FAQs and detailed benefit descriptions sit directly beneath the calculator.

### Integration Options

Freight forwarders, 3PLs, and e-commerce providers can add a white-label drayage and container cost estimator widget to their domain, allowing clients to calculate penalties and book shipments directly.

Software teams can implement TMS/ERP API integration for ocean freight to connect penalty data into internal systems. The API supports multi-level rate calculations, real-time total costs, automated notifications, and booking system connections. It covers major carriers, sea, road, rail, and air modes, alongside multi-currency support and high-volume authentication. Developers can access API documentation and sample requests, then request an access key from SeaRates."""

print("=== LAYER B: AI MARKERS / CLICHÉS ===")
cliches = [
    "in today's world", "vital role", "delve into", "seamlessly", "game-changer",
    "testament", "tapestry", "landscape", "beacon", "fostering", "elevate",
    "realm", "harnessing", "unravel", "demystify", "revolutionize", "pivotal",
    "paramount", "cutting-edge", "state-of-the-art", "game changer", "vital",
    "delve", "seamless", "unlock", "empower", "spearhead", "testament"
]
found_cliches = []
for c in cliches:
    matches = re.findall(rf'\b{c}\b', rewrite, re.IGNORECASE)
    if matches:
        found_cliches.append((c, len(matches)))
print("Found clichés:", found_cliches)

# Check em dashes
em_dashes = re.findall(r'—|--', rewrite)
print(f"Em-dashes count: {len(em_dashes)}")

print("\n=== LAYER C: STRUCTURAL / RHETORICAL AI TICS ===")

# 1. Section lengths
sections = re.split(r'###\s+', rewrite)[1:] # ignore preamble/body header
print(f"Number of sections (H3): {len(sections)}")
for i, s in enumerate(sections, 1):
    lines = s.strip().split('\n')
    title = lines[0]
    content = "\n".join(lines[1:])
    words = len(content.split())
    paras = [p for p in content.split('\n\n') if p.strip()]
    print(f"Section {i} ('{title}'): {words} words, {len(paras)} paragraphs/blocks")
    for j, p in enumerate(paras, 1):
        p_words = len(p.split())
        p_sents = len(re.split(r'[.!?]+', p.strip())) - 1
        print(f"   Para {j}: {p_words} words, {p_sents} sentences")

print("\n2. Causal Connectors ('That's why', 'Which is why', 'Therefore', etc.):")
causals = ["that's why", "which is why", "therefore", "thus", "hence", "as a result", "consequently", "because of this"]
found_causals = []
for c in causals:
    m = re.findall(rf'\b{c}\b', rewrite, re.IGNORECASE)
    if m:
        found_causals.append((c, len(m)))
print("Causal connectors:", found_causals)

print("\n3. Contrastive Negation ('X, not Y', 'instead of'):")
print("Matches for 'instead of':", re.findall(r'instead of\s+[^,.!?]+', rewrite, re.IGNORECASE))
print("Matches for ', not ':", re.findall(r',\s*not\s+[^,.!?]+', rewrite, re.IGNORECASE))

print("\n4. Aphoristic sentence closers / literary peak sentences / twin conclusions:")
# Print all section ending sentences
for i, s in enumerate(sections, 1):
    lines = s.strip().split('\n')
    title = lines[0]
    content = "\n".join(lines[1:])
    sents = [st.strip() for st in re.split(r'(?<=[.!?])\s+', content) if st.strip()]
    if sents:
        print(f"Section {i} last sentence: '{sents[-1]}'")

