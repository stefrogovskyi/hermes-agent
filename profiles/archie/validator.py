import json
import re

banned_words = [
    "delve", "testament", "tapestry", "beacon", "pivotal", "realm", "crucial role", 
    "game-changer", "seamless", "unlock", "landscape", "spearhead", "navigate", 
    "foster", "ever-evolving", "paramount", "robust", "multifaceted", "imperative", 
    "underscore", "embark", "vibrant", "elevate", "harness", "demystify", "dive into", 
    "in summary", "in conclusion", "to sum up", "vital role", "testament to", 
    "leverage", "paradigm shift"
]

banned_connectors = [
    "furthermore", "moreover", "in addition", "additionally", "consequently", 
    "on the other hand", "it is important to note", "that being said", "in fact", 
    "as a result", "therefore"
]

keywords = [
    "digital logistics software",
    "supply chain tracking tools",
    "inventory management software",
    "mobile barcode scanning"
]

def check_rules(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_description = data.get("meta_description", "")
    body = data.get("body", "")

    all_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

    print("=== CHARACTER LIMIT CHECKS ===")
    print(f"Title length: {len(title)} (max 60) -> {'PASS' if len(title) <= 60 else 'FAIL'}")
    print(f"Meta Title length: {len(meta_title)} (max 60) -> {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
    print(f"Meta Description length: {len(meta_description)} (max 155) -> {'PASS' if len(meta_description) <= 155 else 'FAIL'}")

    print("\n=== RULE 1: DASH CHECKS ===")
    dashes = ["—", "–", "--"]
    dash_found = False
    for d in dashes:
        if d in all_text:
            print(f"FAIL: Found dash '{d}' in text")
            dash_found = True
    if not dash_found:
        print("PASS: No em-dashes, en-dashes, or double-hyphens found.")

    print("\n=== RULE 4: BANNED CONNECTORS CHECKS ===")
    connector_found = False
    all_lower = all_text.lower()
    for conn in banned_connectors:
        if re.search(r'\b' + re.escape(conn) + r'\b', all_lower):
            print(f"FAIL: Found banned connector '{conn}'")
            connector_found = True
    if not connector_found:
        print("PASS: No banned connectors found.")

    print("\n=== RULE 9: BANNED WORDS CHECKS ===")
    word_found = False
    for bw in banned_words:
        if re.search(r'\b' + re.escape(bw) + r'\b', all_lower):
            print(f"FAIL: Found banned word/phrase '{bw}'")
            word_found = True
    if not word_found:
        print("PASS: No banned AI vocabulary found.")

    print("\n=== RULE 6: PARAGRAPH SENTENCE COUNTS ===")
    # Split body into paragraphs
    paragraphs = [p.strip() for p in body.split('\n') if p.strip()]
    for idx, p in enumerate(paragraphs):
        if p.startswith('#'): # header
            continue
        # Split paragraph into sentences
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        if len(sentences) < 2 or len(sentences) > 4:
            print(f"WARNING/CHECK: Paragraph {idx+1} has {len(sentences)} sentences: '{p[:60]}...'")
        else:
            print(f"PASS: Paragraph {idx+1} has {len(sentences)} sentences.")

    print("\n=== RULE 7: PARALLEL TWIN-SENTENCE STRUCTURES ===")
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', body) if s.strip() and not s.startswith('#')]
    for i in range(len(sentences) - 1):
        first_word1 = sentences[i].split()[0].lower() if sentences[i].split() else ""
        first_word2 = sentences[i+1].split()[0].lower() if sentences[i+1].split() else ""
        if first_word1 and first_word1 == first_word2:
            print(f"FAIL: Consecutive sentences start with same word '{first_word1}':\n  1: {sentences[i]}\n  2: {sentences[i+1]}")

    print("\n=== KEYWORDS CHECK ===")
    for kw in keywords:
        if kw.lower() in all_lower:
            print(f"PASS: Keyword '{kw}' found.")
        else:
            print(f"MISSING: Keyword '{kw}' NOT found.")

if __name__ == "__main__":
    with open("draft.json") as f:
        check_rules(json.load(f))
