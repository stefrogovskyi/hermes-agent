import re
from audit_layer2 import body_text, title, meta_title, meta_desc

text = body_text

# 1. Causal connectors
causal_patterns = [
    r"\bthat's why\b", r"\bwhich is why\b", r"\bthat's a sign of\b", r"\bthis is why\b",
    r"\bthat is why\b", r"\bthis is a sign of\b"
]

causal_matches = []
for p in causal_patterns:
    m = re.findall(p, text, re.IGNORECASE)
    if m:
        causal_matches.extend(m)

print("Causal Connectors Found:", len(causal_matches), causal_matches)

# 2. Contrastive negation constructions ('X, not Y', 'It isn't X, it's Y', 'instead of', 'not X, but Y', 'rather than')
negation_patterns = [
    r"\binstead of\b",
    r"\brather than\b",
    r"\bnot\b[^\.\,\;]+?\,\s*but\b",
    r"\bisn't\b[^\.\;]+?\,\s*it's\b",
    r"\bis not\b[^\.\;]+?\,\s*it is\b"
]

negation_matches = []
for p in negation_patterns:
    for m in re.finditer(p, text, re.IGNORECASE):
        # print context
        start = max(0, m.start() - 30)
        end = min(len(text), m.end() + 30)
        negation_matches.append(text[start:end].replace('\n', ' '))

print("Contrastive Negation Matches:", len(negation_matches))
for nm in negation_matches:
    print("  ->", nm)

# 3. Check paragraph length uniformity (word count per paragraph)
paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
print("\nParagraph Word Counts:")
for i, p in enumerate(paragraphs):
    words = len(p.split())
    first_few = " ".join(p.split()[:5])
    print(f"  P{i+1}: {words} words | '{first_few}...'")

