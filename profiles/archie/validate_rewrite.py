import json
import re
import string

def validate_candidate(json_path, source_text_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_text", "")

    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    print("=== 1. LENGTH CHECKS ===")
    print(f"Title ({len(title)} chars, max 60): {'OK' if len(title) <= 60 else 'FAIL'}")
    print(f"Meta Title ({len(meta_title)} chars, max 60): {'OK' if len(meta_title) <= 60 else 'FAIL'}")
    print(f"Meta Description ({len(meta_desc)} chars, max 155): {'OK' if len(meta_desc) <= 155 else 'FAIL'}")

    print("\n=== 2. EM-DASH / EN-DASH / DOUBLE-HYPHEN CHECK ===")
    dashes = re.findall(r'[—–]|--|\s-\s', full_text)
    print(f"Forbidden dashes count: {len(dashes)}")
    if dashes:
        print(f"Matches: {dashes}")

    print("\n=== 3. AI CLICHES & SLOP WORDS CHECK ===")
    cliches = [
        "delve", "testament", "pivotal", "game-changer", "gamechanger", "in today's",
        "fast-paced", "crucial aspect", "seamlessly", "seamless", "in conclusion",
        "beacon", "realm", "tapestry", "landscape", "synergy", "transformative",
        "empower", "streamline", "leverage", "cutting-edge", "state-of-the-art",
        "unlock", "foster", "paradigm", "boasts", "vibrant", "robust", "revolutionize",
        "dive into", "explore how", "look no further", "let's explore", "let's dive",
        "ready to see", "harness", "elevate", "game changer", "crucial", "vital",
        "at your fingertips", "game-changing", "groundbreaking", "unleash",
        "optimize", "optimizing", "smoothly", "effortless", "effortlessly",
        "it's not just", "not just", "this isn't just", "a testament to", "pinnacle",
        "holistic", "spearhead", "ultimately", "in summary", "overall"
    ]
    found_cliches = []
    for c in cliches:
        m = re.findall(rf'\b{re.escape(c)}\b', full_text, re.IGNORECASE)
        if m:
            found_cliches.append((c, len(m)))
    print(f"Found cliches ({len(found_cliches)}): {found_cliches}")

    print("\n=== 4. CONNECTOR CHECK ===")
    connectors = [
        "that's why", "which is why", "this is why", "therefore", "as a result",
        "consequently", "for this reason", "thus", "hence", "furthermore",
        "moreover", "in addition", "that's a sign of", "this is a sign of"
    ]
    found_conn = []
    for conn in connectors:
        m = re.findall(rf'\b{re.escape(conn)}\b', full_text, re.IGNORECASE)
        if m:
            found_conn.append((conn, len(m)))
    print(f"Found connectors ({len(found_conn)}): {found_conn}")

    print("\n=== 5. CONTRASTIVE NEGATIONS CHECK (Max 1 allowed in entire text) ===")
    cn_patterns = [
        r'\binstead of\b',
        r'\brather than\b',
        r',\s*not\s+',
        r'\bnot\b\s+[\w\s]+,\s*but\b',
        r'\bisn\'t\b',
        r'\bain\'t\b',
        r'\bdon\'t\s+[\w\s]+,\s*do\b'
    ]
    cn_matches = []
    for pat in cn_patterns:
        for m in re.finditer(pat, full_text, re.IGNORECASE):
            start = max(0, m.start() - 25)
            end = min(len(full_text), m.end() + 25)
            snippet = full_text[start:end].replace('\n', ' ')
            cn_matches.append((m.group(0), snippet))
    print(f"Found contrastive negations ({len(cn_matches)}):")
    for match_str, snippet in cn_matches:
        print(f"  [{match_str}] ...{snippet}...")

    print("\n=== 6. TREND KEYWORDS CHECK ===")
    keywords = [
        "short-form video Reels",
        "behind-the-scenes logistics",
        "#logisticslife",
        "freight forwarding engagement",
        "humanized B2B branding",
        "shipment visibility tools",
        "organic algorithmic reach"
    ]
    for kw in keywords:
        m = re.findall(re.escape(kw), full_text, re.IGNORECASE)
        print(f"  Keyword '{kw}': {'FOUND' if m else 'MISSING'} ({len(m)} times)")

    print("\n=== 7. 6-GRAM OVERLAP WITH ORIGINAL ===")
    if source_text_path:
        with open(source_text_path, "r", encoding="utf-8") as sf:
            source_text = sf.read()

        def get_6grams(txt):
            words = txt.lower().translate(str.maketrans("", "", string.punctuation)).split()
            return set(" ".join(words[i:i+6]) for i in range(len(words)-5))

        src_6g = get_6grams(source_text)
        bdy_6g = get_6grams(full_text)
        overlap = src_6g.intersection(bdy_6g)
        print(f"6-gram overlap count: {len(overlap)}")
        for g in list(overlap)[:10]:
            print(f"  Overlap: {g}")

    print("\n=== 8. SENTENCE BURSTINESS / LENGTHS ===")
    sentences = re.split(r'(?<=[.!?])\s+', body)
    sent_lengths = [len(s.split()) for s in sentences if s.strip()]
    if sent_lengths:
        print(f"Min sentence words: {min(sent_lengths)}")
        print(f"Max sentence words: {max(sent_lengths)}")
        print(f"Avg sentence words: {sum(sent_lengths)/len(sent_lengths):.1f}")
        print(f"Sample short sentences: {[s for s in sentences if len(s.split()) <= 6][:5]}")

if __name__ == "__main__":
    import sys
    json_p = sys.argv[1] if len(sys.argv) > 1 else "candidate.json"
    src_p = sys.argv[2] if len(sys.argv) > 2 else "source.txt"
    validate_candidate(json_p, src_p)
