import json
import re

with open('/opt/hermes/profiles/archie/final_output.json', 'r') as f:
    rewrite = json.load(f)

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

def clean(text):
    return re.sub(r'[^\w\s]', '', text.lower())

src_clean = clean(source_text)
rw_clean = clean(" ".join([rewrite.get(k, '') for k in ['title', 'meta_title', 'meta_description', 'body']]))

src_words = src_clean.split()
rw_words = rw_clean.split()

# Find longest matching substrings of words
def find_long_matches(src, rw, min_len=6):
    matches = []
    src_len = len(src)
    rw_len = len(rw)
    for i in range(rw_len):
        for j in range(src_len):
            k = 0
            while i + k < rw_len and j + k < src_len and rw[i + k] == src[j + k]:
                k += 1
            if k >= min_len:
                match_str = " ".join(rw[i:i+k])
                matches.append((k, i, j, match_str))
    # Deduplicate overlapping matches
    matches.sort(key=lambda x: x[0], reverse=True)
    unique_matches = []
    seen_indices = set()
    for m in matches:
        rw_indices = set(range(m[1], m[1] + m[0]))
        if not rw_indices.issubset(seen_indices):
            unique_matches.append(m)
            seen_indices.update(rw_indices)
    return unique_matches

long_m = find_long_matches(src_words, rw_words, min_len=6)
print(f"Unique matches of length >= 6:")
for m in long_m:
    print(f"Len {m[0]}: '{m[3]}'")

