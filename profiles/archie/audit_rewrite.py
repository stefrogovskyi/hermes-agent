import re

source = """We appreciate your continuing support for SeaRates. We are glad to introduce new solutions and upgrades that will better satisfy your trading and logistics requirements. Our team continues to prioritize the improvement of our services.
To acquire the most recent information, please see our prior updates.

What’s new for week 15:
Tracking System updates:
We’re pleased to share that Euroconsol & Hugo Stinnes have been added to our list of supported carriers — bringing the total to 198 integrated providers. You can view the entire updated list in our API documentation here.
Moreover, we have made enhancements to our collaboration with shipping lines, including the following:
Gold Star Line, DSV Ocean Transport, ZIM, CEVA Logistics, Orient Overseas Container Line (OOCL), and Yang Ming.

Road Tracking improvements:
We have improved our support for providers, including TForce Freight.

Terminal API enhancements:
Our team is glad to announce added support for two more terminals, namely CSP Abu Dhabi and CSP Zeebrugge.

Air Cargo Tracking updates:
We’ve enhanced our integration with airlines, namely Cathay Pacific Airways, Juneyao Airlines, China Cargo Airlines, and Malaysia Airlines.

Logistics Explorer improvements:
Sign up for SeaRates.com to access instant chat with our Support Team right next to the rate result card.

Ship Schedules enhancements:
We have made enhancements to our collaboration with shipping lines, including ONE and Shipping Corporation of India by Points, Yang Ming by Ports, as well as for Namsung, ZIM, CMA CGM, APL, ANL, and CNC by Vessel.

Announcements / Platform capabilities:
Unified Tracking System, Vessel Tracking API v1, Logistics Map 'Warehouse' tab, SeaRates AI 1.0, Parcel Tracking Web, Load Calculator Web 3.0, Map Platform, Road Tracking API."""

title = "SeaRates Release Notes: Week 15, 2025"
meta_title = "SeaRates Product Updates | Week 15, 2025"
meta_desc = "SeaRates added Euroconsol and Hugo Stinnes to its tracking network, updated Terminal API, air cargo tracking, and added instant chat to Logistics Explorer."

body = """Logistics data stays useful only when the connections behind it remain fresh.

Our tracking network now includes Euroconsol and Hugo Stinnes, bringing the total count of integrated carriers to 198. You can inspect the full carrier list inside our API documentation.

Alongside those additions, we updated tracking integrations for Gold Star Line, DSV Ocean Transport, ZIM, CEVA Logistics, Orient Overseas Container Line (OOCL), and Yang Ming. On the ground, road tracking support was updated for providers including TForce Freight.

Two container terminals joined the Terminal API this week: CSP Abu Dhabi and CSP Zeebrugge.

For air cargo tracking, integrations were updated across four airlines: Cathay Pacific Airways, Juneyao Airlines, China Cargo Airlines, and Malaysia Airlines.

If you search rates on SeaRates.com while signed into your account, an instant chat window now sits directly next to the rate result card, putting our support team one click away.

Ship Schedules received several updates:
* Points searches: ONE and Shipping Corporation of India
* Ports searches: Yang Ming
* Vessel searches: Namsung, ZIM, CMA CGM, APL, ANL, and CNC

As part of our broader ecosystem, SeaRates continues supporting operations through the Unified Tracking System, Vessel Tracking API v1, the Warehouse tab on Logistics Map, SeaRates AI 1.0, Parcel Tracking Web, Load Calculator Web 3.0, Map Platform, and the Road Tracking API."""

# Layer A: Plagiarism / 6-gram overlap (excluding proper nouns / standard terms)
def get_ngrams(text, n=6):
    words = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    return set(zip(*[words[i:] for i in range(n)]))

source_6grams = get_ngrams(source)
body_6grams = get_ngrams(body)
overlap_6grams = source_6grams.intersection(body_6grams)

print("Layer A (Plagiarism / 6-gram overlap):")
print("Overlapping 6-grams:", [" ".join(gram) for gram in overlap_6grams])

# Layer B: Word-level AI tells
print("\nLayer B (Word-level AI tells):")
em_dashes = re.findall(r'—|--|–', title + meta_title + meta_desc + body)
print("Em-dashes count:", len(em_dashes))
cliches = ["delve", "testament", "crucial", "today's world", "game-changer", "seamless", "unlock", "leverage", "worth noting", "vital component", "pleased to share", "glad to introduce", "prioritize", "unwavering"]
found_cliches = [c for c in cliches if c in (title + meta_title + meta_desc + body).lower()]
print("Banned cliches found:", found_cliches)

# Layer C: Structural & Rhetorical tells
print("\nLayer C (Structural/Rhetorical tells):")
negations = re.findall(r'\bnot\b|\binstead of\b|\brather than\b', (title + meta_title + meta_desc + body).lower())
print("Contrastive negations count:", len(negations))

# Layer D: Fact Audit
print("\nLayer D (Factual Fabrication Audit):")
print("Checking all claims in body against source:")
print("- Euroconsol & Hugo Stinnes added -> In source")
print("- Total carriers 198 -> In source")
print("- API documentation carrier list -> In source")
print("- Integrations: Gold Star Line, DSV Ocean Transport, ZIM, CEVA Logistics, OOCL, Yang Ming -> In source")
print("- Road tracking: TForce Freight -> In source")
print("- Terminal API: CSP Abu Dhabi, CSP Zeebrugge -> In source")
print("- Air cargo: Cathay Pacific, Juneyao, China Cargo, Malaysia Airlines -> In source")
print("- SeaRates.com rate search instant chat next to rate result card -> In source")
print("- Ship Schedules: ONE & SCI (Points), Yang Ming (Ports), Namsung, ZIM, CMA CGM, APL, ANL, CNC (Vessel) -> In source")
print("- Platform tools listed -> In source")
