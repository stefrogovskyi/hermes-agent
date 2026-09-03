import json
import re

source_text = """
Title: Cut Carbon Costs & Boost Logistics Margins: CBAM & EU ETS Guide

Global initiatives to reduce greenhouse gas emissions are becoming inevitable, and businesses will no longer be able to ignore them without financial losses. Logistics companies are under double pressure: stricter regulations on the one hand and rising costs due to carbon pricing on the other.

Carbon taxes and restrictions are no longer the future — they are the present, determining who will stay in the market and who will be left behind. Let’s discover a clear strategy for adapting to new environmental standards so you do not risk losing competitiveness.

What regulations affect LSP?

EU Emissions Trading System (ETS): Key Takeaways
A central element of the EU's climate change policy is setting limits on overall greenhouse gas emissions and allowing companies to trade allowances for emissions from shipping, aviation, power plants, and industrial facilities.
- 100% of CO2 emissions for flights within the EU.
- 50% of emissions for flights between the EU and non-EU regions are subject to payment.
- Compliance costs are rising — carbon prices are set to reach €100 per ton of CO2 in 2023.
- Medium-Sized Bulk Carrier Example: Emissions ~16,000 tonnes CO2 annually. EU ETS Costs: At a carbon price of €100 per tonne, annual cost would be €1.6 million. Data based on a 10-year-old bulk vessel operating primarily between EU ports.

Carbon Border Adjustment Mechanism (CBAM)
- An import tax on emissions applied to steel, aluminum, cement, fertilizers, and electricity into the EU.
- CBAM certification linked to the EU ETS prices will have to be obtained by the importers.
- Costs are going up for non-EU suppliers, especially those depending on high-carbon production.
- Cement Imports from Turkey Example: Carbon intensity ~0.8 tonnes CO2 per tonne of cement. CBAM Surcharge: With EU ETS price of €75 per tonne CO2, CBAM surcharge would be €60 per tonne of cement (0.8 × €75). Impact: Could reduce competitiveness of Turkish cement in EU market, potentially leading to a decrease in imports.

Singapore's Carbon Tax: A Blueprint for Asia-Pacific
- Ramps up from S$5 to S$50-80 per tonne CO2 by 2030.
- Affects port operations and raises costs for maritime freight moving through Singapore.
- Port Facilities Increase Operational Costs: Airport/port terminals have immense electricity consumption. As tax rises, facilities bear increased operational costs, charging higher fees for docking and handling, increasing overall shipping price.
- Higher Bunker Fuel Prices: Bunker fuels fall under national carbon tax purview. Suppliers pass tax burden to shipping companies by raising fuel prices, directly pegging freight rates to higher fuel costs.
- Low-Carbon Shipping Incentives: Fee cuts offered for vessels using low- or zero-carbon fuels as part of Maritime Singapore Green Initiative operated by Maritime and Port Authority (MPA). Offsets tax burden partially by lower port taxes, encouraging green technology investments.

California's Cap-and-Trade Program
- Includes transportation fuels, making diesel and gas costs higher for freight operators.
- Effect per gallon: Increases retail gasoline prices in California by roughly $0.27 per gallon.
- Impact on Freight Operators: High fuel costs as diesel prices are similarly affected.
- Forecasted Long Term: By 2030, combined effects of California environmental programs (Cap-and-Trade and Low Carbon Fuel Standard) will increase prices per gallon of gasoline and diesel by $0.89-$2.10.
- Implication: Freight operators transfer cost burden to consumers.

Shipping routes optimization
- Use ETS-exempt transshipment hubs to reduce direct exposure to EU ETS.
- Shift from road to multimodal rail + sea to reduce emissions and fuel consumption.
- Reassess scheduling to integrate lower-emission traffic.
- LSPs should engage shippers in agreed sustainable aspirations for equitable cost-sharing and broader transparency.
- Make long-term contracts with fuel & carbon efficiency goals built-in.
- Give clear emissions tracking so customer matches their carbon reduction goals.

Low-emission vessel networks
- Methanol-powered Maersk vessels reduce emissions by up to 95%.
- CMA CGM's LNG-powered fleet reduces CO2 emissions by 20-30%.
- Battery-electric short-sea shipping emerging as zero-emission alternative.
- Pairing with low-emission carriers reduces long-term freight charges while ensuring compliance.

Low-carbon technologies investing
- Integrating alternative fuels and digital optimization tools brings down emissions and compliance spending.
- Adopt biofuels, hydrogen, and LNG.
- Scale up electric & hybrid last-mile logistics and urban freight.
- Use tools for freight planning and loading efficiency.

Do not lose your profit and cut carbon costs:
- Try the Carbon Emissions Calculator to maintain sustainability practices: calculate CO2 emissions based on shipment distances, transport modes, and cargo weight.
- Support multimodal transportation (sea, air, road, rail) for green/economical routes.
- Compare and apply low-carbon alternatives.
- Stay tuned with carbon taxation policies (EU ETS, CBAM, worldwide).
- Make detailed emission reports and enhance transparency with customers.
- CO2 Calculator web integration and API connection to keep pace with sustainable freight practices.
- Contact SeaRates team at sales@searates.com for customized logistics solutions.
"""

with open('/opt/hermes/profiles/archie/final_output.json', 'r') as f:
    rewrite = json.load(f)

# Helper for text normalization
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

source_tokens = tokenize(source_text)

fields = ['title', 'meta_title', 'meta_description', 'body']
combined_rewrite = " ".join([rewrite.get(k, '') for k in fields])
rewrite_tokens = tokenize(combined_rewrite)

print("=== CHECK 1: Plagiarism (6+ consecutive word matches) ===")
# Generate 6-grams from rewrite and check if in source
source_6grams = set()
for i in range(len(source_tokens) - 5):
    source_6grams.add(" ".join(source_tokens[i:i+6]))

matches = []
for i in range(len(rewrite_tokens) - 5):
    gram = " ".join(rewrite_tokens[i:i+6])
    if gram in source_6grams:
        matches.append((i, gram))

print(f"Total 6-gram exact matches: {len(matches)}")
for m in matches:
    print(f"  Match at token index {m[0]}: '{m[1]}'")

print("\n=== CHECK 2: Em-dashes ===")
em_dash_patterns = [r'—', r'--', r'–']
for field in fields:
    val = rewrite.get(field, '')
    count = sum(len(re.findall(p, val)) for p in em_dash_patterns)
    print(f"  {field}: {count} em-dashes/dashes found")

print("\n=== CHECK 3: Common AI Cliché / Buzzword Check ===")
cliches = [
    "in today's fast-paced world", "vital role", "delve into", "testament to",
    "beacon of", "tapestry", "demystify", "game-changer", "unravel", "realm",
    "crucial role", "pivotal role", "landscape", "navigate", "imperative",
    "fostering", "spearhead", "multifaceted", "paramount", "synergy",
    "evolving landscape", "in conclusion", "furthermore", "moreover"
]

for c in cliches:
    cnt = len(re.findall(r'\b' + re.escape(c) + r'\b', combined_rewrite, re.IGNORECASE))
    if cnt > 0:
        print(f"  Found cliché '{c}': {cnt} occurrence(s)")

print("\n=== CHECK 4: Rhetorical / Structural checks ===")
# Connectors: "That's why", "Which is why"
connectors = len(re.findall(r'\b(that\'s why|which is why)\b', combined_rewrite, re.IGNORECASE))
print(f"  'That's why / Which is why': {connectors}")

# Contrastive negation: "instead of", "not X", etc.
negations = re.findall(r'\b(instead of|rather than|not only|x, not y)\b', combined_rewrite, re.IGNORECASE)
print(f"  Contrastive negations ('instead of', 'rather than'): {negations}")

# Let's search for " not " or negation patterns
not_patterns = re.findall(r'(\b\w+\b,\s+not\s+\b\w+\b)', combined_rewrite, re.IGNORECASE)
print(f"  'X, not Y' patterns: {not_patterns}")

print("\n=== CHECK 5: Numbers / Facts in Rewrite ===")
# Find all numbers/percentages/monetary values in rewrite
numbers = re.findall(r'\b(?:\d+[\d,.]*|\$\d+[\d,.]*|€\d+[\d,.]*|S\$\d+[\d,.]*|\d+%\s*|\d+\s*percent)\b', combined_rewrite)
print(f"  Numbers/amounts in rewrite: {set(numbers)}")

