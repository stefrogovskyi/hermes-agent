import re
from audit_script import candidate

paragraphs = [p.strip() for p in candidate.split('\n\n') if p.strip()]

print("=== CANDIDATE PARAGRAPHS / STRUCTURE ===")
for idx, p in enumerate(paragraphs):
    print(f"--- P{idx+1} ---")
    print(p)

# Check contrastive negations: 'X, not Y', 'instead of'
contrastive_neg = re.findall(r'\b(?:not|instead of)\b', candidate, re.IGNORECASE)
print(f"\nContrastive negations / 'instead of' count: {len(contrastive_neg)} -> {contrastive_neg}")

# Check transition connectors at sentence/paragraph start
transitions = ['moreover', 'furthermore', 'however', 'additionally', 'in addition', 'consequently', 'therefore', 'thus', 'further', 'overall']
found_trans = []
for word in transitions:
    m = re.findall(rf'\b{word}\b', candidate, re.IGNORECASE)
    if m:
        found_trans.append((word, len(m)))
print(f"Transition connectors: {found_trans}")

# Break into sentences
sentences = re.split(r'(?<=[.!?])\s+', candidate)
print(f"\nTotal sentences in Candidate: {len(sentences)}")

