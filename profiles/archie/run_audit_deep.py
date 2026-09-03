import re

orig_text = """
Title: Moving to Singapore? Average Container Rates & What to Consider

Planning a move to Singapore? If you're relocating for work, family, or a fresh start in one of Asia's most exciting cities, managing the logistics of an overseas move can be overwhelming, and not least when it comes to shipping your goods. One of the biggest costs to factor in is your container shipping cost. Here's the inside scoop on what you need to know before making the move.

Average Container Shipping Rates to Singapore
Depending on where you're shipping from, here are the ballpark figures:
- 20-foot container: USD $2,000–$4,000
- 40-foot container: USD $3,500–$6,500

These prices include ocean freight but may exclude additional charges such as packing, insurance, local port fees, or last-mile delivery in Singapore.

Rates vary widely depending on:
- Point of origin (e.g., shipping from the U.S. or Europe is more expensive than from Malaysia or Indonesia)
- Type of container (Full Container Load vs. Less-than Container Load)
- Seasonality
- Shipping company or freight forwarder

What Affects the Cost of Shipping to Singapore?

1. Distance & Shipping Route
The further your items need to travel, the more you’ll pay. Popular routes from major cities like London, New York, or Sydney are generally more affordable and faster than lesser-used routes.

2. Container Type: FCL vs. LCL
- FCL (Full Container Load): Best for full-house moves. You pay a flat rate for the whole container, regardless of how much space you use.
- LCL (Less-than Container Load): Ideal for smaller moves. You share a container and pay only for the volume you use.

3. Time of Year
Moving in peak months (June–August and December–January) can result in higher rates due to demand surges. Booking early can save you both time and money.

4. Customs Clearance & Duties
Singapore has efficient and transparent customs procedures. Although household effects are duty-free if used and declared correctly, restricted items (e.g., alcohol, medication, or electronics) may be levied a charge or require permits.

5. Insurance & Packing Services
International moves often feature professional packing, inventory reports, and transit insurance. While they add to the cost, they're worthwhile — especially for fragile or high-value items.

Sea Freight vs. Air Freight: Which One to Choose?

Sea Freight:
- Delivery Time: 3–6 weeks
- Cost: Budget-friendly, especially for full households
- Best for: Furniture, kitchenware, books, and personal belongings

Air Freight:
- Delivery Time: 5–10 days
- Cost: 3–5x more expensive than sea freight
- Best for: Urgent items, small shipments, valuables

Some families choose a hybrid solution — sending essentials by air and the rest by sea.

Tips for a Smooth Move to Singapore
- Compare quotes from 2–3 reputable international movers. Look for companies experienced with Southeast Asia and transparent pricing.
- Understand what's included in your quote. Does it include door-to-door service, customs clearance, and unpacking?
- Prepare a detailed inventory. It will speed up customs clearance and help with insurance claims if needed.
- Label and number all boxes clearly. This helps you track your items and unpack efficiently when you arrive.
- Check Singapore’s import regulations. Certain goods (e.g., chewing gum, controlled drugs, some supplements) are strictly regulated or banned.

Final Thought
Singapore offers an incredible mix of efficiency, opportunity, and quality of life — but international moving takes planning. By understanding your container shipping options and preparing accordingly, you’ll set yourself up for a smooth transition into life in the Lion City.
If you're considering using an unsecured loan to finance your move to Singapore, explore platforms such as ROSHI to secure the lowest rates and competitive terms.
Start early, stay organized, and enjoy the journey ahead. Welcome to Singapore!
"""

rewrite_text = """
TITLE: Container Shipping Costs to Singapore: Rates and Rules
META_TITLE: Singapore Relocation Container Costs and Rates Guide
META_DESCRIPTION: Compare international container shipping rates to Singapore, FCL vs LCL options, sea freight delivery timelines, customs duty-free import rules, and costs.

BODY:
Relocating across an ocean settles into a cold equation of box counts, port tariffs, and transit days. Base international container shipping rates to Singapore average USD $2,000 to $4,000 for a 20-foot container. Larger moves requiring a 40-foot container generally cost between USD $3,500 and $6,500. These baseline quotes cover ocean freight, though packing services, transit insurance, local port fees, and last-mile delivery within Singapore often incur extra charges. Shipments originating from distant regions like Europe or North America carry higher baseline prices than regional runs from Malaysia or Indonesia. High-density ocean routes out of major transport hubs such as London, New York, or Sydney remain cheaper and faster than obscure secondary lanes.

Container selection splits between Full Container Load (FCL) and Less-than Container Load (LCL). FCL charges a single flat rate for the entire container regardless of occupied space, fitting full-house relocations. LCL fits smaller moves by grouping multiple shipments inside shared space where you pay strictly for the volume used. Pricing fluctuates across the year. Peak shipping surges hit between June and August, then return from December through January. Booking moves months ahead of these windows reduces baseline costs. For transit timelines, sea freight household goods Singapore shipments require 3 to 6 weeks. Air freight cuts transit time to 5 to 10 days, but expenses jump to 3 to 5 times the price of ocean transport. Many households use a hybrid plan: air cargo carries immediate essentials, while sea vessels handle furniture, kitchenware, books, and bulk items.

Singapore customs duty-free household import regulations apply to personal belongings that are already used and declared properly upon arrival. Restricted goods like alcohol, prescription medications, and consumer electronics may require permits or import tariffs. Chewing gum, controlled drugs, and specific dietary supplements face strict import bans or heavy regulations. International movers operating in Southeast Asia should provide transparent door-to-door quotes specifying whether customs clearance and unpacking are included. Obtaining quotes from 2 to 3 international movers helps benchmark true market rates. Detailed, numbered box inventories accelerate clearance at port checkpoints and substantiate transit insurance claims for fragile goods. Financing an overseas move using an unsecured loan can be evaluated through comparison platforms like ROSHI to compare interest rates and loan terms.
"""

print("=== LAYER A: PLAGIARISM / N-GRAM SIMILARITY ===")

def get_words(text):
    return re.findall(r'\b\w+\b', text.lower())

orig_words = get_words(orig_text)
rewrite_words = get_words(rewrite_text)

# Check 6+ consecutive words overlap
for n in range(6, 12):
    orig_ngrams = set(" ".join(orig_words[i:i+n]) for i in range(len(orig_words)-n+1))
    rewrite_ngrams = [" ".join(rewrite_words[i:i+n]) for i in range(len(rewrite_words)-n+1)]
    matches = [g for g in rewrite_ngrams if g in orig_ngrams]
    print(f"Exact {n}-word overlaps: {len(matches)}")
    for m in matches:
        print(f"  - {m}")

# Check 5-gram and 4-gram overlaps for interest
for n in range(4, 6):
    orig_ngrams = set(" ".join(orig_words[i:i+n]) for i in range(len(orig_words)-n+1))
    rewrite_ngrams = [" ".join(rewrite_words[i:i+n]) for i in range(len(rewrite_words)-n+1)]
    matches = [g for g in rewrite_ngrams if g in orig_ngrams]
    print(f"Exact {n}-word overlaps: {len(matches)}")
    for m in matches[:10]:
        print(f"  - {m}")


print("\n=== LAYER B: WORD/PHRASE-LEVEL AI TELLS ===")

# Check em-dashes
em_dashes_unicode = len(re.findall(r'—', rewrite_text))
em_dashes_ascii = len(re.findall(r'--', rewrite_text))
en_dashes = len(re.findall(r'–', rewrite_text))
hyphens = len(re.findall(r'-', rewrite_text))

print(f"Em-dashes (—): {em_dashes_unicode}")
print(f"Double hyphens (--): {em_dashes_ascii}")
print(f"En-dashes (–): {en_dashes}")

# AI clichés & slop list
cliches = [
    "important to note", "in today's world", "key aspect", "delve", "integral part",
    "unique balance", "it's not just", "not only", "in conclusion", "it should be noted",
    "crucial role", "testament to", "game changer", "tapestry", "beacon", "realm",
    "nestled", "fostering", "seamless", "paramount", "pivotal", "boasts", "vibrant",
    "inside scoop", "set yourself up for", "enjoy the journey"
]

found_cliches = []
for c in cliches:
    matches = re.findall(r'\b' + re.escape(c) + r'\b', rewrite_text, re.IGNORECASE)
    if matches:
        found_cliches.append((c, len(matches)))

print(f"AI Clichés found: {found_cliches}")

# Empty intro/outro filler check
print("Intro sentence:", rewrite_text.strip().split('\n')[0])
lines = [l.strip() for l in rewrite_text.strip().split('\n') if l.strip()]
print("Outro sentence:", lines[-1])


print("\n=== LAYER C: STRUCTURAL / RHETORICAL AI TELLS ===")

# Explicit connectors
connectors = ["that's why", "which is why", "that is why", "that's a sign of", "which explains why"]
found_connectors = []
for conn in connectors:
    m = re.findall(r'\b' + re.escape(conn) + r'\b', rewrite_text, re.IGNORECASE)
    if m:
        found_connectors.append((conn, len(m)))
print(f"Explicit connectors: {found_connectors}")

# Contrastive negation
contrastive_patterns = [
    r'\bnot\b.*?\bbut\b',
    r'\binstead of\b',
    r'\bnot a\b',
    r'\bnot just\b',
    r'\bnot only\b'
]
print("Checking contrastive negation (' not ', 'instead of', 'X, not Y'):")
for p in contrastive_patterns:
    matches = re.findall(p, rewrite_text, re.IGNORECASE)
    print(f"  Pattern '{p}': {len(matches)} matches -> {matches}")

# Check general occurrences of 'not' and 'instead'
not_matches = re.findall(r'\bnot\b', rewrite_text, re.IGNORECASE)
instead_matches = re.findall(r'\binstead\b', rewrite_text, re.IGNORECASE)
print(f"Total 'not': {len(not_matches)}, Total 'instead': {len(instead_matches)}")

# Sentences analysis
body_match = re.search(r'BODY:\s*(.*)', rewrite_text, re.DOTALL)
body_text = body_match.group(1).strip() if body_match else rewrite_text

paragraphs = [p.strip() for p in body_text.split('\n\n') if p.strip()]
print(f"Total paragraphs in BODY: {len(paragraphs)}")
for idx, p in enumerate(paragraphs, 1):
    sentences = re.split(r'(?<=[.!?])\s+', p)
    print(f"\nParagraph {idx} ({len(sentences)} sentences, {len(p.split())} words):")
    for s_idx, s in enumerate(sentences, 1):
        print(f"  [{s_idx}] {s}")

