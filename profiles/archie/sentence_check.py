import re

with open('/opt/hermes/profiles/archie/test_article.py') as f:
    content = f.read()

# Extract body text from test_article.py
match = re.search(r'body = """(.*?)"""', content, re.DOTALL)
if match:
    body = match.group(1)

# Break body into paragraphs and sentences
paragraphs = body.split('\n\n')

print("--- Paragraph Sentence Analysis ---")
for i, p in enumerate(paragraphs):
    p_clean = p.strip()
    if not p_clean or p_clean.startswith('#'):
        continue
    # Simple sentence split
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p_clean) if s.strip()]
    print(f"Paragraph {i+1} ({len(sents)} sentences):")
    for s in sents:
        print(f"  - {s}")
    print()
