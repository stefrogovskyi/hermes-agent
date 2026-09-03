import re
from collections import Counter

rewrite = """Title: Transport Logistic 2025: Key Takeaways from Munich
Meta Title: Transport Logistic 2025: SeaRates Highlights
Meta Description: SeaRates team members Lilia Khovrak and Oleksandr Grabarchuk joined Transport Logistic 2025 in Munich. Here is our event summary.
Body Text:
From June 2 to 5, 2025, global supply chain professionals gathered at Messe München in Germany for Transport Logistic 2025. Representing SeaRates, Digital Account Managers Lilia Khovrak and Oleksandr Grabarchuk spent four productive days connecting with clients, sharing operational insights, and presenting customized SeaRates logistics solutions.

## Key Themes Across 60+ Sessions

The conference schedule packed in over 60 individual sessions focused on practical technology and regulatory updates. Discussions centered around several core operational areas:

* Supply chain automation and warehouse robotics for handling daily tasks
* Big Data and Internet of Things (IoT) applications designed to optimize cargo tracking
* Practical implementation of AI to tackle routine workflow challenges
* Green logistics, energy-efficient solutions, and sustainable freight development
* Updated environmental rules and international transport safety standards
* Digital freight management systems and future technology trends

## Air Cargo and Aviation Initiatives

A significant portion of the agenda targeted air cargo digitalization and specialized transport management. Industry experts examined the intricacies of air logistics, highlighting modern digital tools for flight and cargo management. Presenters also highlighted cargo drones alongside new environmental standards aimed at lowering transport aviation emissions.

## Connect with the SeaRates Team

Throughout the event, Lilia Khovrak and Oleksandr Grabarchuk captured photos from the exhibition floor while meeting directly with long-standing partners and new contacts. To learn more about SeaRates freight services or follow up on conversations from Munich, contact Lilia Khovrak and Oleksandr Grabarchuk directly. You can send an email to sales@searates.com or reach out through the SeaRates chat room and official communication channels."""

words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', rewrite)]
counts = Counter(words)

cliches_to_check = [
    'delve', 'pivotal', 'testament', 'seamless', 'robust', 'landscape', 
    'game-changer', 'fostering', 'tapestry', 'beacon', 'key role', 'vital role',
    'revolutionize', 'spearhead', 'beacon', 'realm', 'vibrant', 'intricate', 
    'intricacies', 'multifaceted', 'paramount', 'ever-evolving', 'cornerstone',
    'holistic', 'interconnected', 'crucial', 'foster', 'underpins', 'transformative',
    'showcase', 'disrupt', 'synergy', 'navigating', 'dynamic', 'paradigm',
    'unwavering', 'plethora', 'myriad', 'testament', 'harness', 'harnessing',
    'game changer', 'fostered', 'delved', 'delving'
]

found = []
for word in counts:
    if word in cliches_to_check:
        found.append((word, counts[word]))

print("Found vocabulary AI clichés from list:", found)
