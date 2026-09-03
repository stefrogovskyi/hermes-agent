import json
import re

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    return tokens

def get_ngrams(tokens, n=6):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def run_checks():
    with open("candidate_draft.json", "r") as f:
        draft = json.load(f)
        
    with open("article_orig.txt", "r") as f:
        orig_text = f.read()

    title = draft["title"]
    meta_title = draft["meta_title"]
    meta_desc = draft["meta_description"]
    body = draft["body_markdown"]
    
    full_draft_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    # 1. Em-dash check
    em_dashes = re.findall(r'[—–]|--', full_draft_text)
    print(f"1. Em-dash count: {len(em_dashes)}")
    
    # 2. Length check
    print(f"2. Length checks:")
    print(f"   - Title: {len(title)} chars")
    print(f"   - Meta Title: {len(meta_title)} chars (limit <= 60)")
    print(f"   - Meta Description: {len(meta_desc)} chars (limit <= 155)")
    
    # 3. 6-gram overlap check
    orig_tokens = normalize_text(orig_text)
    draft_tokens = normalize_text(body)
    
    orig_6grams = set(get_ngrams(orig_tokens, 6))
    draft_6grams = get_ngrams(draft_tokens, 6)
    
    overlaps = []
    for gram in draft_6grams:
        if gram in orig_6grams:
            overlaps.append(" ".join(gram))
            
    # Deduplicate overlapping 6-grams that are contiguous
    unique_overlaps = set(overlaps)
    print(f"3. 6-gram overlap count: {len(unique_overlaps)}")
    if unique_overlaps:
        print("   Overlaps detected:")
        for ov in sorted(unique_overlaps):
            print(f"   - '{ov}'")
            
    # 4. Cliché & connector check
    cliches = ['delve', 'tapestry', 'testament', 'game-changer', 'beacon', 'seamless', 'in conclusion', 'furthermore', 'moreover', "that's why", 'as a result', 'in order to']
    found_cliches = []
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full_draft_text, re.I):
            found_cliches.append(c)
    print(f"4. Forbidden AI Clichés / Connectors found: {found_cliches}")

if __name__ == '__main__':
    run_checks()
