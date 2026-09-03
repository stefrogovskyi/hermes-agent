import re
from audit import rewrite_text

title = "Title: US Reciprocal Tariffs Hit South Korea and Japan"
meta_title = "Meta-Title: US Reciprocal Tariffs: Impact on Korea and Japan"
meta_desc = "Meta-Description: A 25% US tariff on South Korea and Japan forces supply chain rerouting across transpacific trade routes starting August 1, 2025. Here is what to know."

body_text = """On July 7, 2025, Washington gave fourteen trading partners three weeks to rewrite their export math. Formal letters from the administration warned of new 25 percent reciprocal tariffs set to take effect on August 1, 2025. That date marks the deadline for nations seeking alternative bilateral trade agreements.

The primary targets include Japan and South Korea at 25 percent, alongside South Africa at 30 percent, Kazakhstan at 25 percent, Laos at 40 percent, Malaysia at 25 percent, Myanmar at 40 percent, Tunisia at 25 percent, Bosnia and Herzegovina at 30 percent, Indonesia at 32 percent, Bangladesh at 35 percent, Serbia at 35 percent, Cambodia at 36 percent, and Thailand at 36 percent. A broader list of affected countries will follow within a month.

The official notice leaves room for rate adjustments based on market access, bilateral concessions, and commitments to shift manufacturing onto American soil.

Legal authority for these measures faces immediate resistance. Congress holds constitutional authority over foreign commerce, but delegates specific emergency powers to the executive branch under the Trade Expansion Act of 1962 for national security threats and the Trade Act of 1974 for temporary 150-day tariffs up to 15 percent. In May 2025, the U.S. Court of International Trade ruled that using the International Economic Emergency Powers Act for these tariffs exceeded presidential power. The administration appealed, setting up a hearing before the U.S. Court of Appeals for the Federal Circuit on July 31, 2025. The final legal position remains unresolved.

These reciprocal tariffs clash directly with existing agreements like KORUS and the U.S.-Japan Trade Agreement. Both Asian partners have grounds to challenge the measures at the WTO or demand formal compensation.

Shifting goods across transpacific trade routes will trigger extensive supply chain rerouting. Global financial losses could reach 1.4 trillion dollars. For U.S. consumers, imported goods prices are projected to rise by 3 percent compared to early 2025 levels, while domestic goods rise 2 percent. The U.S. Treasury anticipates 300 billion dollars in tariff revenue for 2025, offset by domestic inflation and reduced consumer purchasing power. Gross domestic product could contract by 0.8 percent in Japan and 0.5 percent in South Korea.

Sector impacts vary widely across key industries:

* Automotive: Car prices could rise 25 percent, dampening overall vehicle demand by 10 to 15 percent with annual industry losses near 30 billion dollars. Japan exports 129 billion dollars in vehicles and parts to the U.S. annually, representing 3 percent of its economy. South Korea ships 28 billion dollars in auto components.
* Tech and Electronics: Costs across the supply chain may jump by 20 billion dollars annually, pushing retail prices up 10 to 15 percent. Samsung faces an estimated 30 billion dollar increase in production costs against its 210 billion dollar annual revenue. Semiconductor components, OLED display panels, and lithium batteries face 25 percent duty increases.
* Pharmaceuticals: Medical spending could increase by 51 billion dollars annually, with drug prices rising 12.9 percent. The Japanese pharmaceutical market stands at 82.27 billion dollars and South Korea's at 28.83 billion dollars.
* Power and Energy: Electrical components face 10 to 15 percent cost increases, raising electricity sector costs by up to 5 billion dollars annually and consumer rates by 5 to 7 percent.
* Fashion and Textiles: Price tags will climb 5 to 10 percent, creating 3 to 5 billion dollars in losses. South Korea exports 10.5 billion dollars in textiles annually.
* Chemicals: Japanese chemical exports reach 45 billion dollars annually. The industry expects 2 to 4 billion dollars in added costs, with product prices rising 8 to 12 percent.
* Aviation and Logistics: Aircraft components shipped from Japan and South Korea total 25 billion dollars. Component costs will rise 8 to 10 percent, creating up to 2 billion dollars in total burden. Air freight rates are expected to climb 8 to 10 percent.
* Agriculture: U.S. food prices could rise 1 to 2 billion dollars annually as agricultural imports fall by 5 to 7 percent.

Washington frames these measures as an attempt to shrink trade deficits with Seoul and Tokyo. The announcement also aligns with domestic political events, including upcoming elections in Japan and ongoing political transitions in South Korea.

Corporate responses are already moving. Toyota is pursuing a 13 billion dollar expansion of U.S. facilities, while Hyundai and Kia are increasing domestic U.S. investments. Companies are also shifting freight lines toward Southeast Asia and Europe.

Logistics teams face heightened freight rate volatility and stricter demands for customs compliance. Operational planning relies on short-term contracts running 3 to 6 months rather than annual commitments. Shippers are embedding tariff-indexed price clauses that trigger a 3 percent price adjustment for every 5 percent tariff rate hike. Indexation terms review raw material prices, freight indexes, and inflation every three months. Standard agreements now feature penalty-free volume adjustments alongside strict Certificate of Origin documentation to preserve trade agreement benefits. Real-time freight rate calculators, API connections, and transport software help track carriers across secondary ports for logistics risk mitigation."""

# 1. Em-dashes
em_dashes_title = len(re.findall(r'—|--', title))
em_dashes_mtitle = len(re.findall(r'—|--', meta_title))
em_dashes_mdesc = len(re.findall(r'—|--', meta_desc))
em_dashes_body = len(re.findall(r'—|--', body_text))

print(f"Em-dashes count: Title: {em_dashes_title}, Meta-Title: {em_dashes_mtitle}, Meta-Description: {em_dashes_mdesc}, Body: {em_dashes_body}, Total: {em_dashes_title + em_dashes_mtitle + em_dashes_mdesc + em_dashes_body}")

# 2. Cliché AI words
cliches = [
    'crucial', 'vital', 'delve', 'testament', 'realm', 'navigating', 'navigate', 
    'in conclusion', 'tapestry', 'beacon', 'paramount', 'pivotal', 'fostering',
    'foster', 'underscore', 'underscores', 'bolster', 'interconnected', 'landscape',
    'game-changer', 'game changer', 'unwavering', 'ever-evolving', 'seamless', 'seamlessly'
]

full_rewrite = f"{title}\n{meta_title}\n{meta_desc}\n{body_text}".lower()

found_cliches = {}
for word in cliches:
    cnt = len(re.findall(rf'\b{word}\b', full_rewrite))
    if cnt > 0:
        found_cliches[word] = cnt

print(f"Cliché AI words found: {found_cliches}")

