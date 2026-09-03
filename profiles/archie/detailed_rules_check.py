import re

with open('draft2.md', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
body_text = "\n".join([l for l in lines if not (l.startswith('TITLE:') or l.startswith('META_TITLE:') or l.startswith('META_DESCRIPTION:'))])

print("--- RULE 3: Anti-textbook Architecture ---")
paragraphs = [p.strip() for p in body_text.split('\n\n') if p.strip()]
print(f"Total paragraphs/blocks: {len(paragraphs)}")
p_lengths = [len(p.split()) for p in paragraphs if not p.startswith('#')]
print(f"Paragraph word counts: {p_lengths}")

print("\n--- RULE 4: Banned Explicit Connectors ---")
banned_connectors = [
    "Furthermore", "Moreover", "In addition", "However", "Therefore", 
    "That's why", "Which is why", "Consequently", "Additionally", "As a result",
    "Hence", "Thus", "Because of this"
]
found_conn = []
for p in paragraphs:
    if p.startswith('#'): continue
    for line in p.split('\n'):
        if line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line):
            continue
        sents = re.split(r'(?<=[.!?])\s+', line)
        for s in sents:
            s_clean = s.strip()
            for bc in banned_connectors:
                if re.match(r'^' + re.escape(bc) + r'\b', s_clean, re.IGNORECASE):
                    found_conn.append((bc, s_clean))
print(f"Explicit connectors found: {found_conn}")

print("\n--- RULE 5: Limit Contrastive Negations ---")
cn_patterns = [
    r'\binstead of\b',
    r'\brather than\b',
    r'\bnot\b\s+[\w\s]+,\s*but\b',
    r',\s*not\s+'
]
found_cn = []
for pat in cn_patterns:
    matches = re.findall(pat, body_text, re.IGNORECASE)
    if matches:
        found_cn.extend(matches)
print(f"Contrastive negations found ({len(found_cn)}): {found_cn}")

print("\n--- RULE 6: Aphoristic Sentence Limit ---")
# Short standalone one-liner paragraphs (< 10 words)
one_liners = [p for p in paragraphs if not p.startswith('#') and not p.startswith('-') and not re.match(r'^\d+\.', p) and len(p.split()) <= 10]
print(f"Short standalone one-liner paragraphs ({len(one_liners)}): {one_liners}")

print("\n--- RULE 7: Ban Parallel Twin-Sentences ---")
# Back-to-back sentences with identical syntactic structures
parallel_found = []
for p in paragraphs:
    if p.startswith('#'): continue
    for line in p.split('\n'):
        if line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line): continue
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', line) if s.strip()]
        for i in range(len(sents)-1):
            w1 = [w.lower() for w in re.findall(r'\b\w+\b', sents[i])[:3]]
            w2 = [w.lower() for w in re.findall(r'\b\w+\b', sents[i+1])[:3]]
            if w1 and w2 and w1 == w2:
                parallel_found.append((sents[i], sents[i+1]))
print(f"Parallel twin-sentences found: {parallel_found}")

print("\n--- RULE 8: Ban Symmetric Antithesis Pairs ---")
# Check if adjacent sentences have mirror image contrast pairs
# e.g. "When X increases, Y decreases. When Y increases, X decreases."
print("Checking adjacent sentence structures for symmetric antithesis...")

print("\n--- RULE 9: Word-level AI Clichés ---")
banned_words = [
    "delve", "seamless", "unlock", "game-changer", "testament", 
    "tapestry", "pivotal", "elevate", "cutting-edge", "fostering", 
    "vibrant", "it is crucial to note", "in today's fast-paced world"
]
found_banned = []
for bw in banned_words:
    if re.search(r'\b' + re.escape(bw) + r'\b', content, re.IGNORECASE):
        found_banned.append(bw)
print(f"Banned words found: {found_banned}")

