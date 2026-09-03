import re

title = "US Trade Tariffs 2025 and Global Ocean Freight"
meta_title = "US Trade Tariffs 2025: Port Fees & Vehicle Duties"
meta_description = "New US trade tariffs in 2025 increase vehicle duties and shipping costs. Discover how higher container fees affect global supply chains and trade."

full_body_text = """In the spring of 2025, the United States introduced new customs policy changes affecting automotive and maritime logistics. Starting April 2, 2025, a 25% duty applies to vehicles and parts imported from Mexico and Canada. The US government expects these tariffs to boost domestic vehicle manufacturing and reduce reliance on foreign suppliers. However, American automakers Ford and General Motors anticipate car prices will rise by 10% due to the increased cost of imported components. In response to these tariff shifts, Volkswagen and Toyota are evaluating options to move portions of their production to the United States or Canada. Meanwhile, Ford plans to expand output at facilities in Canada and Mexico, while Volkswagen considers shifting certain European assembly lines to American plants. Overall, parts of the automotive supply chain will become more expensive, and manufacturers may discontinue some vehicle models in the US market.

Maritime trade faces additional expense under new administration initiatives that establish extra port fees for vessels sailing from China and ships built in Chinese shipyards. A single port call under this policy can incur up to $1.5 million in additional charges. As a result, shipping costs for goods moving from China to the United States are expected to rise by 20% to 30%, with California ports seeing a primary impact. These measures reduce the overall efficiency of supply chains between countries and prompt Chinese shipping lines to re-evaluate their trade routes. Higher import taxes in the United States also create potential risks of retaliatory tariffs from major trading partners, including South Korea and Japan.

US exporters also encounter higher operational expenses, as container transportation costs have risen from $600 to $800 per container. This increase directly impacts agricultural commodities such as corn, wheat, and soybeans, which generate the majority of farm income. Higher freight rates reduce the global competitiveness of American agricultural exports, creating risks of lower export volumes and potential market loss in key destinations like India and China. Internationally, European Union officials noted that the combination of vehicle tariffs and new transportation charges brings US-EU trade relations to an unfavorable level. The EU has pledged to engage international trade organizations, including the WTO, and has initiated direct negotiations with Washington to explore alternative solutions.

To maintain resilience amid evolving regulations and tariffs, shipping and trading businesses can implement several practical adjustments:

- Adjust supply chain strategies and explore new freight markets to maintain commercial competitiveness.
- Use a reliable freight rate calculator to account for unexpected increases in customs duties and transportation costs.
- Negotiate freight terms early to lock in transportation rates before new surcharges take effect.
- Source alternate suppliers from countries like Brazil, Vietnam, and India that do not face similar import restrictions.
- Prepare contingency plans for potential disruptions across food, energy, and transportation sectors.
- Maintain continuous, 24/7 shipment tracking to identify port delays early.
- Explore air transportation channels for high-value goods.
- Utilize customs-licensed warehouses to defer cost obligations and accelerate customs clearance.

The SeaRates Logistics Explorer tool helps traders and logistics providers adapt to global market challenges. Through this platform, users can compare transparent freight rates across sea, air, road, and rail, evaluate carrier options, and secure instant cargo bookings to lock in pricing. Designed for seamless planning, Logistics Explorer can also integrate into existing workflows via web tools and API connections. For custom logistics support and tailored supply chain solutions, contact sales@searates.com."""

print(f"Title length: {len(title)} (limit: 60) -> {'PASS' if len(title) <= 60 else 'FAIL'}")
print(f"Meta-Title length: {len(meta_title)} (limit: 60) -> {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
print(f"Meta-Description length: {len(meta_description)} (limit: 155) -> {'PASS' if len(meta_description) <= 155 else 'FAIL'}")

# Check em-dashes
full_content = title + "\n" + meta_title + "\n" + meta_description + "\n" + full_body_text
em_dashes = [m.start() for m in re.finditer(r'—|--', full_content)]
print(f"Em-dashes count: {len(em_dashes)} -> {'PASS' if len(em_dashes) == 0 else 'FAIL'}")

# Check specific audit requirements
checks = {
    "No 'bypass port congestion'": "bypass port congestion" not in full_content.lower(),
    "Separate supplier sourcing & disruptions": ("Brazil, Vietnam" in full_content) and ("food, energy, and transportation" in full_content) and ("Brazil, Vietnam, and India that do not face similar import restrictions" in full_content),
    "General supply chain efficiency (no 'Pacific trade corridors')": "pacific trade corridors" not in full_content.lower() and "efficiency of supply chains between countries" in full_content.lower(),
    "Retaliatory tariffs not 'already triggered'": "already triggered" not in full_content.lower(),
    "20-30% shipping costs phrasing": "shipping costs for goods moving from china to the united states are expected to rise by 20% to 30%" in full_content.lower(),
    "Discontinue probability phrasing": "may discontinue" in full_content.lower(),
    "No clichés ('harsh recalibration', 'grim financial tag', 'slap added port charges', 'feel the pinch')": not any(c in full_content.lower() for c in ["harsh recalibration", "grim financial tag", "slap added port charges", "feel the pinch"])
}

for name, res in checks.items():
    print(f"Audit Check - {name}: {'PASS' if res else 'FAIL'}")

