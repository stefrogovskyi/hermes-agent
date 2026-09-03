import re

title = "SeaRates at SCM Iberia 2025: Supply Chain Agility"
meta_title = "SeaRates at SCM Iberia 2025 | Event Recap & Insights"
meta_description = "SeaRates joined SCM Iberia 2025 in Madrid. Discover key takeaways on eCMR 2026 digital standards, real-time tracking, and Iberian logistics agility."

body = """Inside Sala Picasso at LOOM Azca on November 25, Madrid hosted the third edition of SCM Iberia 2025 under the theme "From Volatility to Agility: Reinventing the Iberian Supply Chain." Discussions started fast. Disruptions, inflation, and green regulations dominated every session, forcing shippers and carriers to turn agility into working practice.

Ramón García from CEL set the tone in his opening keynote on the 3 C's of sustainable supply chain. Immediately after, executives from Lactogal, KENVUE, Alloga, and Venture Vanguard took the stage for the roundtable "From Volatility to Agility," tackling how supply chain agility shifts from executive theory into daily freight movements.

Case studies replaced abstract talk. Nestlé and CHEP outlined their joint digital visibility roadmap. Generix demonstrated AI warehouse planning, while Arvato detailed broad systems integration. A dedicated Tech and Data panel examined eCMR 2026 digital standards, warehouse automation, and the friction point between executive gut feeling and algorithmic forecasting.

For the SeaRates team, these topics matched daily platform operations. Valeria Guliy, Logistics Account Manager at SeaRates, captured moments from the floor and shared her perspective in a post-event LinkedIn update, highlighting joint experiences alongside the Digital Freight Alliance. Throughout back-to-back meetings, SeaRates demonstrated platform features including instant rates, real-time tracking, and an integrated CO2 Calculator covering ocean, air, rail, and road transport. Attendees wanted tools capable of trimming costs and transit delays while maintaining environmental accountability.

Decarbonization took center stage in sustainability sessions led by Unilever and Luís Simões, who presented operational excellence metrics alongside Carboninsets decarbonization tools. Sustainability functioned as a firm KPI. Later, the closing roundtable "From Border to Bridges" brought together APOL, Combiberia, Logifrio, and Porto de Aveiro to explore regional integration. Unified port networks, rail corridors, and shared digital protocols are building cross-border visibility across the peninsula.

As SaaS supply chain platforms replace fragmented point tools, long-term scalability rests on combining skilled personnel with intelligent automation.

To evaluate your logistics operations or discuss insights from SCM Iberia 2025, reach out to sales@searates.com for tailored digital tools or an informal exchange of conference notes."""

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# 1. Em-dash check
em_dashes = re.findall(r'[—–]|--', full_text)
print("Em-dash count:", len(em_dashes))

# 2. Length checks
print(f"Title length: {len(title)} chars (limit 60)")
print(f"Meta-title length: {len(meta_title)} chars (limit 60)")
print(f"Meta-description length: {len(meta_description)} chars (limit 155)")

# 3. 6-gram overlap check against original
original_text = """On November 25, the third edition of SCM Iberia 2025, “From Volatility to Agility: Reinventing the Iberian Supply Chain” was welcomed in Madrid, Spain. One day at LOOM Azca – Sala Picasso turned into a manifesto full of messages: the future in a world of disruptions, inflation, and green pressure is for those who make agility out of volatility through collaboration, digitalization, and smart technology.
Opening keynote by Ramón García (CEL) on “The 3 C’s of sustainable supply chain”
Roundtable “From Volatility to Agility” with Lactogal, KENVUE, Alloga, and Venture Vanguard
Real-life cases: Nestlé + CHEP digital visibility roadmap, Generix AI warehouse planning, Arvato systems integration
Tech & Data panel on eCMR 2026, warehouse automation, and balancing gut feeling with algorithms
Sustainability talks: Unilever + Luís Simões operational excellence and Carboninsets decarbonization tools
Closing roundtable “From Border to Bridges” with APOL, Combiberia, Logifrio and Porto de Aveiro on Iberian integration
We spent the whole day in back-to-back meetings and demos that showed how our platform provides instant rates, live tracking, and a CO2 Calculator for ocean, air, rail, and road. The atmosphere was perfect—everyone was eager for the practical digital solutions that would not only reduce costs and delays but also be eco-friendly. The talks about eCMR and cross-border visibility were as if they were tailor-made for what SeaRates does every day.
Photos by Valeria Guliy, Logistics Account Manager, at the SCM Iberia 2025 in November 2025.
Moreover, Valeria Guliy shared her impressions of the conference speeches in her LinkedIn post. Learn more about the personal experience of the SeaRates and Digital Freight Alliance teams in the modern supply chain innovation world.
Digital platforms have conquered logistics and are now functioning as the new operating system — SaaS-style ecosystems outstripping point solutions invariably
Sustainability is not simply acknowledged; it is a tough KPI
Iberian collaboration (ports + rail + digital standards) is gradually turning into a competitive advantage
The combination of people and smart technology is the sole scaling formula
At SeaRates, we are heavily invested in the digitization of logistics in order to provide global transportation that is more efficient, predictable, and manageable. If you are re-evaluating your supply chain playbook based on these highlights, let’s get in touch. You can contact us at sales@searates.com for a quick chat about personalized digital solutions or simply to exchange notes from the conference."""

def tokenize(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text_clean.split() if w]

orig_tokens = tokenize(original_text)
body_tokens = tokenize(body)

def get_ngrams(tokens, n=6):
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))

orig_6grams = get_ngrams(orig_tokens, 6)
body_6grams = get_ngrams(body_tokens, 6)

overlap = orig_6grams.intersection(body_6grams)
print("\n6-gram overlaps found:", len(overlap))

allowed_proper_phrases = [
    "from volatility to agility reinventing the",
    "volatility to agility reinventing the iberian",
    "to agility reinventing the iberian supply",
    "agility reinventing the iberian supply chain",
    "lactogal kenvue alloga and venture vanguard",
    "valeria guliy logistics account manager at",
    "apol combiberia logifrio and porto de",
    "combiberia logifrio and porto de aveiro",
    "3 c s of sustainable supply",
    "c s of sustainable supply chain"
]

non_proper_overlap = []
for gram in overlap:
    phrase = " ".join(gram)
    if not any(allowed in phrase for allowed in allowed_proper_phrases):
        non_proper_overlap.append(phrase)

print("Non-proper 6-gram overlaps:", len(non_proper_overlap))
if non_proper_overlap:
    for gram in non_proper_overlap:
        print("  -", gram)
