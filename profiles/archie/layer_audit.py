import json
import re

with open("result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

text = f"{data['title']}\n{data['meta_title']}\n{data['meta_description']}\n{data['body']}"

# Layer A: Overlap
# Checking non-exempt N-grams (>6 consecutive words from source prompt)
# Source prompt strings to check:
source_phrases = [
    "On July 12, 2025, Donald Trump announced a new wave of tariffs",
    "undermining American industry",
    "dependence on drug trafficking",
    "trade imbalances",
    "Covers all product categories universally",
    "half a month window to prepare trade agreements and logistics",
    "raising effective import costs to 30% - 55%",
    "requiring reformulated customs valuations/transfers prior to",
    "False tariff exposure if origin for every SKU is not documented",
    "high legal risk on fixed door-to-door terms without revision clauses"
]

overlap_hits = []
for sp in source_phrases:
    if sp.lower() in text.lower():
        overlap_hits.append(sp)

print("Layer A (Plagiarism / Direct Overlap Hits):", len(overlap_hits), overlap_hits)

# Layer B: Word/Phrase Tells
banned_words = [
    "delve", "testament", "beacon", "pivotal", "landscape", "realm", 
    "game-changer", "transformative", "seamlessly", "harness", "fostering", 
    "paramount", "underscores", "tapestry", "unlock", "vital", "undoubtedly", "crucial"
]
banned_connectors = [
    "Furthermore", "Moreover", "In addition", "Consequently", "On the other hand", 
    "It is important to note that", "In summary", "Additionally"
]

word_tells = []
if "—" in text or "--" in text:
    word_tells.append("Em-dash present")

for bw in banned_words:
    if re.search(r'\b' + re.escape(bw) + r'\b', text, re.I):
        word_tells.append(f"Banned word: {bw}")

for bc in banned_connectors:
    if re.search(r'\b' + re.escape(bc) + r'\b', text, re.I):
        word_tells.append(f"Banned connector: {bc}")

print("Layer B (Word/Phrase Tells Hits):", len(word_tells), word_tells)

# Layer C: Structural Tells
# Count "that's why", "which is why", "which explains why"
causal_connectors = re.findall(r"\bthat's why\b|\bwhich is why\b|\bwhich explains why\b", text, re.I)

# Count contrastive negations
contrastive_negations = re.findall(r"\bnot\b.*?\bbut\b|\binstead of\b", text, re.I)

print("Layer C (Causal Connectors):", len(causal_connectors), causal_connectors)
print("Layer C (Contrastive Negations):", len(contrastive_negations), contrastive_negations)

# Layer D: Facts Check
facts_check = {
    "July 12, 2025": "July 12, 2025" in text,
    "August 1, 2025": "August 1, 2025" in text or "August 1" in text,
    "Donald Trump": "Donald Trump" in text,
    "30%": "30%" in text,
    "30% and 55%": "30% and 55%" in text or "30% - 55%" in text or ("30%" in text and "55%" in text),
    "62.5 percent": "62.5 percent" in text or "62.5%" in text,
    "5% to 10%": "5% to 10%" in text or "5%-10%" in text,
    "10%": "10%" in text,
    "Mexico": "Mexico" in text,
    "European Union / EU": "European Union" in text or "EU" in text,
    "EXW": "EXW" in text,
    "DDP": "DDP" in text,
    "USMCA": "USMCA" in text,
    "SeaRates": "SeaRates" in text,
    "sales@searates.com": "sales@searates.com" in text
}

print("Layer D (Factual Check Results):")
for k, v in facts_check.items():
    print(f"  - {k}: {'PASS' if v else 'FAIL'}")

if all(facts_check.values()) and len(overlap_hits) == 0 and len(word_tells) == 0 and len(contrastive_negations) <= 1:
    print("\nFINAL 4-LAYER AUDIT VERDICT: PERFECT PASS!")
else:
    print("\nFINAL AUDIT VERDICT: REQUIRES ATTENTION")
