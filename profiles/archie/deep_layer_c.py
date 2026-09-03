import re

draft = """
When global supply chains face sudden geopolitical disruptions, natural catastrophes, and rapid trade reconfigurations, static operational models quickly collapse. Logistics executives need actionable strategies, not abstract theories. From November 18 to 20, 2024, the Global Freight Summit 2024 gathers over 5,000 top experts from 155+ countries at Expo City, Dubai. Organised by DP World under the theme "Acting on the Opportunities of a Changing World," this landmark gathering directly addresses the commercial realities of international trade, reaching a global audience of 150 million.

Modern logistics demands immediate operational adaptability. At the summit, participants evaluate six interconnected focus areas designed to solve pressing supply chain bottlenecks.

Dynamic international trade changes require robust crisis management frameworks. Industry leaders analyze volatile trade corridors and share proven contingency plans to keep freight moving when conventional routes encounter friction.

In digital freight forwarding, theoretical promises give way to operational deployment. Technical sessions present real cases of AI and blockchain integration, detailing specific adaptation steps while outlining the practical operational risks companies must manage.

Building supply chain resilience and adaptability is essential as geopolitical shifts and natural catastrophes alter traditional lanes. Discussions center on engineering flexibility into global networks before unforeseen shocks disrupt fulfillment schedules.

Meeting strict environmental requirements while maintaining core business margins requires disciplined execution. Practical green logistics cases showcase how forward-thinking operators implement carbon reduction targets without sacrificing operational efficiency.

Expanding operations into emerging regional markets brings distinct regulatory and logistical hurdles. Experienced operators offer clear guidance on managing supply chains in fragile environments, establishing reliable protocols for regional expansion.

Sustained growth across international freight depends on strategic partnership. Agenda sessions outline collaborative models where organizations participate in infrastructure and technology sharing to solve shared industry challenges.

To help forwarders stay ahead of future trends, the summit delivers targeted learning formats:
* Dynamic panel discussions with thought leaders debating capital allocation, route management, and regulatory compliance.
* Targeted workshops on freight logistics challenges offering hands-on problem-solving with senior practitioners.
* Live showcases of startup innovations demonstrating functional technology solutions for freight operations.
* Broad networking forums connecting global professionals and industry leaders to build long-term commercial relationships.

The operational teams from SeaRates and the Digital Freight Alliance (DFA) will attend the event in Dubai across all three days. They will engage directly with participants to share specialized trade insights, review digital tools, and discuss expansion strategies.

Maria Salabenko, Head of DFA, emphasized the summit's unique commercial value: "GFS stands out as the premier platform for our clients to forge new connections..."

Whether you aim to refine your crisis response playbook, evaluate artificial intelligence tools, or secure strategic partnerships, the DP World freight summit Dubai provides direct access to the decision-makers shaping modern logistics.

Register for the Global Freight Summit 2024 today to meet the SeaRates Digital Freight Alliance team in Expo City, Dubai, and position your organization at the center of international trade.
"""

# Split into sentences
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', draft) if s.strip()]

print(f"Total sentences: {len(sentences)}\n")

print("--- Sentence Analysis ---")
for i, sent in enumerate(sentences, 1):
    words = sent.split()
    print(f"{i:02d}. [{len(words)} words] {sent}")

print("\n--- Transition Words Check ---")
transitions = [
    'furthermore', 'in conclusion', 'moreover', 'additionally', 'consequently',
    'in summary', 'firstly', 'secondly', 'finally', 'therefore', 'thus', 'however', 'nevertheless'
]
for sent in sentences:
    for t in transitions:
        if t in sent.lower():
            print(f"Found transition '{t}': {sent}")

print("\n--- Contrastive Negation Check (Limit 1) ---")
# Looking for "not X, but Y" or "X, not Y" or similar
contrastive_matches = []
for sent in sentences:
    if 'not' in sent.lower():
        print(f"Sentence with 'not': {sent}")

print("\n--- Short/Aphoristic Sentences (<12 words, sweeping/generalized statements) ---")
for sent in sentences:
    words = sent.split()
    if len(words) <= 12:
        print(f"[{len(words)} words]: {sent}")

