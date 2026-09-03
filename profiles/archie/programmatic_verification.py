import json
import re

new_title = "SeaRates at SIL Barcelona 2025: Connect in Spain"
meta_title = "SeaRates at SIL Barcelona 2025: Logistics Event Guide"
meta_description = "Join SeaRates at SIL Barcelona 2025 from June 18-20 at Fira de Barcelona. Meet Valeriya Guliy and discover modern logistics supply chain technology."

body_text = """## Bringing Logistics Experts Together in Spain

The SeaRates team is heading to Barcelona this summer for SIL Barcelona 2025, taking place from June 18-20, 2025. Held at the Fira de Barcelona - Montjuïc Exhibition Center in Barcelona, Spain, this gathering brings industry professionals together to discuss practical ways to improve freight operations and supply chain management.

If you want to refine your shipping strategy or learn about new digital tools, we invite you to sit down with our team. We look forward to discussing your specific transport requirements and sharing clear steps to streamline your daily logistics processes.

## What to Expect on the Event Agenda

The three-day conference offers plenty of opportunity to gain practical industry insights. Across more than 70 sessions, over 350 experts will share their experience on key topics shaping global trade today:

* Technological innovations and Industry 4.0
* Artificial intelligence in road transport
* Sustainable development and decarbonization
* Robotization of the logistics industry
* Supply chain digitalization and automation
* Urban logistics and last-mile delivery practices
* Development of multimodal terminals

Two dedicated tracks add extra focus to the schedule:

* Tech by SIL (June 18): Highlights practical digital tools, Industry 4.0 applications, and green logistics practices.
* BWAW by SIL (June 19-20): Focuses on technology and inclusion, workforce equity, geopolitical trends, and building a sustainable future.

Attendees can also connect using dedicated networking spaces. The Startups Innovation Hub brings fresh ideas to the floor, while the SILvIA Platform provides a digital space for participants to message and coordinate meetings throughout the gathering.

## Connect with SeaRates in Barcelona

Valeriya Guliy will attend SIL Barcelona 2025 as the primary representative for SeaRates. Whether you want to expand your business network or resolve specific freight management challenges, our team is ready to talk through practical solutions.

To schedule a dedicated meeting during SIL Barcelona 2025 or ask questions about the gathering, contact our team directly at sales@searates.com. We look forward to meeting you in Barcelona this June."""

print("Length checks:")
print("new_title:", len(new_title), "chars (max 60)")
print("meta_title:", len(meta_title), "chars (max 60)")
print("meta_description:", len(meta_description), "chars (max 155)")

# Check em-dashes
full_text = f"{new_title}\n{meta_title}\n{meta_description}\n{body_text}"
em_dashes = full_text.count("—") + full_text.count("–") + full_text.count("--")
print("Em-dashes count:", em_dashes)

# Check 6-grams against original
with open('/opt/hermes/profiles/archie/original_article.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

def get_ngrams(text, n=6):
    words = re.sub(r'[^\w\s]', '', text.lower()).split()
    return set(" ".join(words[i:i+n]) for i in range(len(words)-n+1))

orig_ngrams = get_ngrams(orig_text, 6)
new_ngrams = get_ngrams(full_text, 6)

overlap = orig_ngrams.intersection(new_ngrams)
print("\n6-gram overlaps count:", len(overlap))
for o in overlap:
    print(" - Match:", o)
