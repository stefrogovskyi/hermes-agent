import json
import re
import string

def check_text():
    with open("/opt/hermes/profiles/archie/fixed_rewrite.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    with open("/opt/hermes/profiles/archie/source_clean.txt", "r", encoding="utf-8") as f:
        source_text = f.read()

    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_markdown", "")
    
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    # 1. Em-dash count
    em_dashes = full_text.count("—") + full_text.count("--") + full_text.count("–")
    print(f"1. Em-dashes count: {em_dashes}")
    
    # 2. Length limits
    print(f"2. Title length: {len(title)} (limit 60)")
    print(f"   Meta Title length: {len(meta_title)} (limit 60)")
    print(f"   Meta Description length: {len(meta_desc)} (limit 155)")
    
    # 3. 6-gram overlap check
    def clean_words(text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.split()

    source_words = clean_words(source_text)
    rewrite_words = clean_words(full_text)

    source_6grams = set()
    for i in range(len(source_words) - 5):
        gram = " ".join(source_words[i:i+6])
        source_6grams.add(gram)

    overlapping_6grams = []
    for i in range(len(rewrite_words) - 5):
        gram = " ".join(rewrite_words[i:i+6])
        if gram in source_6grams:
            overlapping_6grams.append(gram)

    print(f"3. 6-gram overlaps count: {len(overlapping_6grams)}")
    if overlapping_6grams:
        print("   Overlaps found:", overlapping_6grams)

    # 4. Check for "X, not Y" / contrastive negation
    not_pattern = re.findall(r'\bnot\b|\binstead of\b', full_text, re.IGNORECASE)
    print(f"4. 'not' / 'instead of' occurrences: {len(not_pattern)}")
    
    return {
        "em_dashes": em_dashes,
        "title_len": len(title),
        "meta_title_len": len(meta_title),
        "meta_desc_len": len(meta_desc),
        "ngram_overlap": len(overlapping_6grams),
        "overlapping_grams": overlapping_6grams
    }

if __name__ == "__main__":
    check_text()
