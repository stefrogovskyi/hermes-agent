import re
from verify_rewrite import body

paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]

all_sentences = []
for p in paragraphs:
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    all_sentences.append(sents)

print("PARAGRAPHS AND SENTENCES:")
for i, sents in enumerate(all_sentences):
    print(f"\n--- Paragraph {i+1} ({len(sents)} sentences) ---")
    for j, s in enumerate(sents):
        print(f"  [{j+1}] ({len(s.split())} words) {s}")
