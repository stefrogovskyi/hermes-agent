import json
import re

def test_everything():
    with open("output.json") as f:
        data = json.load(f)
        
    title = data["title"]
    meta_title = data["meta_title"]
    meta_description = data["meta_description"]
    body = data["body"]
    
    full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"
    
    print("--- METADATA LENGTHS ---")
    print(f"Title ({len(title)} chars): '{title}'")
    print(f"Meta Title ({len(meta_title)} chars): '{meta_title}'")
    print(f"Meta Description ({len(meta_description)} chars): '{meta_description}'")
    
    assert len(title) <= 60, "Title > 60 chars"
    assert len(meta_title) <= 60, "Meta Title > 60 chars"
    assert len(meta_description) <= 155, "Meta Description > 155 chars"
    
    print("\n--- RULE 1: NO EM DASHES ---")
    assert "—" not in full_text and "--" not in full_text, "Em-dash found"
    print("PASS: No em-dashes found.")
    
    print("\n--- RULE 2: AI CLICHES AND FILLER ---")
    banned = [
        'important to note', 'crucial aspect', "in today's world", 'dive into', 
        'integral part', 'unique balance', 'not just', 'to sum up', 
        'it should be emphasized', 'in conclusion', 'delve', 'realm', 'navigating',
        'testament', 'ever-changing', 'dynamic landscape', 'fostering', 'seamless',
        'leverage', 'vital', 'pivotal', 'game-changer', 'tapestry', 'beacon',
        'nestled', 'interplay', 'cornerstone', 'paradigm', 'synergy'
    ]
    for b in banned:
        assert b not in full_text.lower(), f"Banned cliché found: {b}"
    print("PASS: No AI clichés found.")
    
    print("\n--- RULE 6: OVER-EXPLAINING CONNECTORS ---")
    connectors = ["that's why", "which is why", "that's a sign of", "this is why", "because of this,"]
    for conn in connectors:
        assert conn not in full_text.lower(), f"Connector found: {conn}"
    print("PASS: No over-explaining connectors.")
    
    print("\n--- RULE 7: CONTRASTIVE NEGATIONS ---")
    instead_count = full_text.lower().count("instead of")
    not_count = len(re.findall(r'\b\w+\s*,\s*not\s+\w+', full_text.lower()))
    isn_t_count = len(re.findall(r"isn't\s+[^,.!]+,\s*it's", full_text.lower()))
    total = instead_count + not_count + isn_t_count
    assert total <= 1, f"Too many contrastive negations: {total}"
    print(f"PASS: Contrastive negation count is {total} (<= 1).")
    
    print("\n--- REQUIRED KEYWORDS ---")
    keywords = ["spot rates", "spot rate volatility", "capacity management", "digital freight marketplaces", "route diversions"]
    for kw in keywords:
        assert kw in full_text.lower(), f"Missing keyword: {kw}"
        print(f"PASS: Found keyword '{kw}'")
        
    print("\n--- SOURCE FACTS CHECK ---")
    facts = ["traze", "turmeric", "india", "ukraine", "tracking software", "gold"]
    for fact in facts:
        assert fact in full_text.lower(), f"Missing source fact: {fact}"
        print(f"PASS: Found source fact '{fact}'")
        
    print("\nALL VERIFICATIONS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_everything()
