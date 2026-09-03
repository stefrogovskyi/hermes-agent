import re

draft = """
TITLE: Navigating Global Trade Volatility: Global Freight Summit 2024

META_TITLE: Global Freight Summit 2024 | DP World Dubai

META_DESCRIPTION: Join 5,000+ logistics experts at the DP World Global Freight Summit 2024 in Dubai, Nov 18-20. Connect with SeaRates and Digital Freight Alliance.

BODY:
When global supply chains face sudden geopolitical disruptions, natural catastrophes, and rapid trade reconfigurations, static operational models quickly collapse. Logistics executives need actionable strategies, not abstract theories. From November 18 to 20, 2024, the Global Freight Summit 2024 gathers over 5,000 top experts from 155+ countries at Expo City, Dubai. Organised by DP World under the theme "Acting on the Opportunities of a Changing World," this landmark gathering directly addresses the commercial realities of international trade, reaching a global audience of 150 million.

### Navigating Disruption Across Core Trade Pillars

Modern logistics demands immediate operational adaptability. At the summit, participants evaluate six interconnected focus areas designed to solve pressing supply chain bottlenecks.

#### 1. International Trade Shifts and Crisis Preparedness
Dynamic international trade changes require robust crisis management frameworks. Industry leaders analyze volatile trade corridors and share proven contingency plans to keep freight moving when conventional routes encounter friction.

#### 2. Practical Digital Transformation
In digital freight forwarding, theoretical promises give way to operational deployment. Technical sessions present real cases of AI and blockchain integration, detailing specific adaptation steps while outlining the practical operational risks companies must manage.

#### 3. Strengthening Supply Chain Resilience
Building supply chain resilience and adaptability is essential as geopolitical shifts and natural catastrophes alter traditional lanes. Discussions center on engineering flexibility into global networks before unforeseen shocks disrupt fulfillment schedules.

#### 4. Sustainable Logistics with Measured Efficiency
Meeting strict environmental requirements while maintaining core business margins requires disciplined execution. Practical green logistics cases showcase how forward-thinking operators implement carbon reduction targets without sacrificing operational efficiency.

#### 5. Strategic Entry into Emerging Regional Markets
Expanding operations into emerging regional markets brings distinct regulatory and logistical hurdles. Experienced operators offer clear guidance on managing supply chains in fragile environments, establishing reliable protocols for regional expansion.

#### 6. Collaborative Models and Shared Technological Infrastructure
Sustained growth across international freight depends on strategic partnership. Agenda sessions outline collaborative models where organizations participate in infrastructure and technology sharing to solve shared industry challenges.

### Maximizing Value for Attending Logistics Executives

To help forwarders stay ahead of future trends, the summit delivers targeted learning formats:
* Dynamic panel discussions with thought leaders debating capital allocation, route management, and regulatory compliance.
* Targeted workshops on freight logistics challenges offering hands-on problem-solving with senior practitioners.
* Live showcases of startup innovations demonstrating functional technology solutions for freight operations.
* Broad networking forums connecting global professionals and industry leaders to build long-term commercial relationships.

### Strategic Presence of SeaRates and Digital Freight Alliance

The operational teams from SeaRates and the Digital Freight Alliance (DFA) will attend the event in Dubai across all three days. They will engage directly with participants to share specialized trade insights, review digital tools, and discuss expansion strategies.

Maria Salabenko, Head of DFA, emphasized the summit's unique commercial value: "GFS stands out as the premier platform for our clients to forge new connections..."

Whether you aim to refine your crisis response playbook, evaluate artificial intelligence tools, or secure strategic partnerships, the DP World freight summit Dubai provides direct access to the decision-makers shaping modern logistics.

Register for the Global Freight Summit 2024 today to meet the SeaRates Digital Freight Alliance team in Expo City, Dubai, and position your organization at the center of international trade.
"""

forbidden_list = [
    'delve', 'testament', 'crucial', 'seamless', 'landscape', 'tapestry',
    'game-changer', 'beacon', 'pivotal', 'paradigm shift', 'realm',
    'ever-evolving', 'fostering', 'unlock', 'spearhead', 'harnessing',
    'paramount', 'cutting-edge', 'game changer', 'paradigm-shift',
    'ever evolving', 'cutting edge'
]

print("--- Forbidden AI Words Check ---")
found_words = False
for word in forbidden_list:
    matches = re.findall(r'\b' + re.escape(word) + r'\b', draft, re.IGNORECASE)
    if matches:
        print(f"FOUND: '{word}' (count: {len(matches)})")
        found_words = True

if not found_words:
    print("NO forbidden AI words detected!")

print("\n--- Punctuation Check ---")
em_dashes = re.findall(r'—|--', draft)
print(f"Em-dashes or '--' found: {len(em_dashes)}")

colons = re.findall(r':', draft)
print(f"Colons found: {len(colons)}")
for line in draft.split('\n'):
    if ':' in line:
        print(f"  Line with colon: {line.strip()}")

