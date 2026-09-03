import json
import re
import sys

def check_article(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body", "")
    
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    errors = []
    
    # 1. Dash checks
    for dash_char in ["—", "--", "–"]:
        if dash_char in full_text:
            errors.append(f"Forbidden dash character found: {repr(dash_char)}")
            
    # 2. Length checks
    if len(title) > 60:
        errors.append(f"Title length ({len(title)}) exceeds 60 chars: {title}")
    if len(meta_title) > 60:
        errors.append(f"Meta title length ({len(meta_title)}) exceeds 60 chars: {meta_title}")
    if len(meta_desc) > 155:
        errors.append(f"Meta description length ({len(meta_desc)}) exceeds 155 chars: {meta_desc}")
        
    # 3. AI clichés & forbidden phrases
    cliches = [
        "delve", "testament", "crucial", "in today's world", "it is worth noting",
        "game-changer", "seamless", "pivotal", "unlock", "navigate", "realm",
        "landscape", "beacon", "foster", "tailored", "paradigm", "cutting-edge",
        "ever-changing", "harness", "empower", "tapestry", "revolutionize",
        "vital", "strategic"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Forbidden AI cliché found: '{c}'")
            
    # 4. Connectors
    connectors = ["that's why", "which is why", "this explains why"]
    for conn in connectors:
        if conn in full_text.lower():
            errors.append(f"Forbidden connector found: '{conn}'")
            
    # 5. Required target keywords
    keywords = [
        "LCL consolidation and deconsolidation",
        "FCL yard storage",
        "Foreign Trade Zone benefits",
        "Bonded warehouse customs compliance",
        "Supply chain tariff optimization",
        "Import duty deferral strategy"
    ]
    for kw in keywords:
        if kw.lower() not in full_text.lower():
            errors.append(f"Missing target keyword: '{kw}'")
            
    # 6. Required factual entities & country rules
    required_entities = [
        "CFS", "CY", "FTZ", "Bonded Warehouse",
        "LCL", "FCL", "CBP", "HMRC", "VAT",
        "United States", "European Union", "United Kingdom", "China", "India", "Singapore", "Singapore Customs"
    ]
    for ent in required_entities:
        if ent.lower() not in full_text.lower():
            errors.append(f"Missing required entity/fact: '{ent}'")
            
    # 7. Contrastive negation check (max 1)
    # Searching for typical contrastive patterns: "X, not Y", "instead of", "rather than", "unlike"
    negation_patterns = [
        r'\binstead of\b',
        r'\brather than\b',
        r'\bunlike\b',
        r',\s*not\b'
    ]
    matches = []
    for pat in negation_patterns:
        found = re.findall(pat, full_text, re.IGNORECASE)
        matches.extend(found)
    if len(matches) > 1:
        errors.append(f"Too many contrastive negations ({len(matches)} > 1): {matches}")
        
    # 8. 6-gram overlap check against original_article.md
    with open("/opt/hermes/profiles/archie/original_article.md", "r", encoding="utf-8") as f:
        orig_text = f.read()
        
    def normalize_words(text):
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.split()
        
    orig_words = normalize_words(orig_text)
    body_words = normalize_words(body)
    
    orig_6grams = set()
    for i in range(len(orig_words) - 5):
        orig_6grams.add(" ".join(orig_words[i:i+6]))
        
    exempt_terms = [
        "container freight station", "less than container load",
        "full container load", "foreign trade zone",
        "bonded warehouse", "customs and border protection",
        "hm revenue and customs", "singapore customs"
    ]
    
    overlaps = []
    for i in range(len(body_words) - 5):
        ngram = " ".join(body_words[i:i+6])
        if ngram in orig_6grams:
            if not any(exempt in ngram for exempt in exempt_terms):
                overlaps.append(ngram)
                
    if overlaps:
        errors.append(f"Non-exempt 6-gram overlaps found ({len(overlaps)}): {overlaps}")
        
    print("=== CHECK RESULTS ===")
    print(f"Title: '{title}' ({len(title)} chars)")
    print(f"Meta Title: '{meta_title}' ({len(meta_title)} chars)")
    print(f"Meta Description: '{meta_desc}' ({len(meta_desc)} chars)")
    print(f"Em-dashes count: {full_text.count('—') + full_text.count('--') + full_text.count('–')}")
    print(f"Contrastive negations count: {len(matches)}")
    print(f"6-gram overlaps count: {len(overlaps)}")
    if errors:
        print("\nERRORS ENCOUNTERED:")
        for err in errors:
            print(f"- {err}")
        return False
    else:
        print("\nALL CHECKS PASSED PERFECTLY!")
        return True

if __name__ == "__main__":
    check_article("/opt/hermes/profiles/archie/draft_cfs.json")
