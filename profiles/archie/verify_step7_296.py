import json
import re

refined_data = {
  "title": "How Language Tools Improve Freight Software Communication",
  "meta_title": "Language Tools for Freight Shipping & Logistics Systems",
  "meta_description": "Discover how paraphrasing and grammar tools boost clear communication, bill of lading accuracy, and customs invoice clarity in freight shipping platforms.",
  "body": """Modern freight shipping software serves as the structural foundation of logistics operations. Dispatchers and forwarding teams rely on digital platforms to coordinate international movement, manage carrier relationships, and track cargo movements. While these platforms process operational data efficiently, human clarity remains central to every transaction. Teams send hundreds of status updates, customs notes, and email messages every day. Poorly phrased messages or minor grammatical errors can delay ocean containers, create invoice disputes, or confuse overseas partners.

## Refining Freight Communication with Paraphrasing Systems

Logistics managers handle technical details about port congestion, customs clearance, and vessel schedules. Explaining these concepts to external stakeholders requires clear language adapted to the recipient. Paraphrasing tools assist operators by converting informal draft notes into concise, professional updates.

When dispatchers communicate with international clients, clear phrasing ensures instructions are understood across language boundaries. Text rephrasing tools generate polished email responses in seconds. Logistics teams reduce drafting time on repetitive client inquiries, allowing managers to spend more time resolving operational bottlenecks on the ground.

## Eliminating Errors in Core Shipping Documentation

Grammar refinement tools provide essential oversight for written records across logistics platforms. Critical documents such as bills of lading, customs declarations, and commercial invoices require exact phrasing to pass regulatory review.

Mistakes in documentation can lead to costly customs holds or financial discrepancies between shippers and carriers. Integrated grammar tools verify text accuracy across emails and formal reports. These tools also manage regional localization standards, adjusting terms between UK English and US English spelling to match regional customs standards.

For teams managing high-volume freight accounts, automated email drafting tools turn simple operational inputs into complete, accurate client updates. Forwarders can integrate these writing solutions alongside digital logistics tools and workflow integrations to maintain clear, proactive updates across account management operations.

## Streamlining Logistics Systems Integration

Connecting text optimization tools directly into freight management platforms strengthens team productivity. Forwarding operations can connect communication tools through API integrations or automated workflow channels to format shipment milestone notices before they reach customers.

Combining bill of lading accuracy, customs invoice clarity, and automated text checking ensures that internal notes and external correspondence meet professional standards. Companies using SeaRates tools and integrated language utilities maintain clear documentation, minimize delivery misunderstandings, and build stronger relationships across global logistics networks.

To explore options tailored to your logistics operations, contact the SeaRates team to learn more about freight software tools."""
}

title = refined_data["title"]
meta_title = refined_data["meta_title"]
meta_desc = refined_data["meta_description"]
body = refined_data["body"]

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== STEP 7 PROGRAMMATIC VERIFICATION ===")

# 1. Em-dash / En-dash / Double hyphen count
dashes = re.findall(r'[—–]|--', full_text)
print(f"1. Dash count (em-dash, en-dash, --): {len(dashes)}")

# 2. Lengths
print(f"2. Title length: {len(title)} (max 60) -> {'OK' if len(title) <= 60 else 'EXCEEDED'}")
print(f"   Meta Title length: {len(meta_title)} (max 60) -> {'OK' if len(meta_title) <= 60 else 'EXCEEDED'}")
print(f"   Meta Description length: {len(meta_desc)} (max 155) -> {'OK' if len(meta_desc) <= 155 else 'EXCEEDED'}")

# 3. N-gram 6-gram overlaps
with open('/opt/hermes/profiles/archie/clean_article_296.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

orig_6grams = set(get_ngrams(orig_text, 6))
rewrite_6grams = get_ngrams(body, 6)

overlaps = [g for g in rewrite_6grams if g in orig_6grams]
print(f"3. 6-gram Overlaps Count: {len(overlaps)}")
if overlaps:
    print("   Overlaps:", overlaps)

# 4. Sentence-starting connectors
banned_starters = [
    "Furthermore", "Moreover", "In addition", "However", "Therefore",
    "That's why", "Which is why", "Consequently", "Additionally",
    "As a result", "Hence", "Thus", "Because of this"
]
found_starters = []
for line in body.split('\n'):
    line_clean = line.strip()
    if not line_clean or line_clean.startswith('#'):
        continue
    for sentence in re.split(r'(?<=[.!?])\s+', line_clean):
        for starter in banned_starters:
            if re.match(r'^' + re.escape(starter) + r'[\s,]', sentence.strip(), re.IGNORECASE):
                found_starters.append((starter, sentence.strip()))
print(f"4. Banned Sentence Starters: {len(found_starters)}")

# 5. Banned AI Clichés
banned_words = [
    r'\bdelve\b', r'\bseamless\b', r'\bseamlessly\b', r'\bunlock\b',
    r'\bgame-changer\b', r'\bgame changer\b', r'\btestament\b', r'\btapestry\b',
    r'\bpivotal\b', r'\belevate\b', r'\bcutting-edge\b', r'\bfostering\b',
    r'\bvibrant\b', r'\blandscape\b', r'\brealm\b', r'\bharness\b', r'\bempower\b'
]
found_cliches = []
for bw in banned_words:
    m = re.findall(bw, full_text, re.IGNORECASE)
    if m:
        found_cliches.extend(m)
print(f"5. Banned AI Clichés: {len(found_cliches)}")

# 6. Contrastive Negation Count
contrastive_patterns = [r'\binstead of\b', r'\brather than\b', r'\bnot only\b.*\bbut\b', r'\bX,\s*not\s*Y\b']
contrast_count = sum(len(re.findall(p, full_text, re.IGNORECASE)) for p in contrastive_patterns)
print(f"6. Contrastive Negations: {contrast_count} (max 1)")

# Save final clean JSON
with open('/opt/hermes/profiles/archie/final_data_296.json', 'w', encoding='utf-8') as f:
    json.dump(refined_data, f, indent=2, ensure_ascii=False)

print("Final JSON data saved to /opt/hermes/profiles/archie/final_data_296.json")
