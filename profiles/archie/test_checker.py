import json
import re
import sys

def check_rules(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_markdown", "")
    
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    errors = []
    
    # Rule 1: ZERO EM-DASHES
    em_dashes = ['—', '–', '--', '\u2014', '\u2013']
    for dash in em_dashes:
        if dash in full_text:
            errors.append(f"Rule 1 Violation: Found em-dash or en-dash '{dash}' in text")
            
    # Rule 3: NO EXPLICIT CONNECTORS
    banned_connectors = [
        r"\bthat's why\b", r"\bwhich is why\b", r"\bfurthermore\b", r"\bmoreover\b", 
        r"\bin addition\b", r"\bhowever\b", r"\bconsequently\b", r"\btherefore\b",
        r"\bas a result\b"
    ]
    for conn in banned_connectors:
        matches = re.findall(conn, full_text, re.IGNORECASE)
        if matches:
            errors.append(f"Rule 3 Violation: Found connector '{matches[0]}'")
            
    # Rule 4: CONTRASTIVE NEGATION (max 1)
    negation_patterns = [r"\binstead of\b", r"\brather than\b", r", not\b"]
    neg_count = 0
    for pat in negation_patterns:
        neg_count += len(re.findall(pat, full_text, re.IGNORECASE))
    if neg_count > 1:
        errors.append(f"Rule 4 Violation: Found {neg_count} instances of contrastive negation (max 1 allowed)")

    # Rule 9: NO AI VOCABULARY & CLICHES
    ai_words = [
        r"\bdelve\b", r"\bseamless\b", r"\bseamlessly\b", r"\btapestry\b", 
        r"\bgame-changer\b", r"\bgame changer\b", r"\btestament\b", 
        r"\bin today's fast-paced world\b", r"\bvital role\b", r"\bleverage\b", 
        r"\bparadigm shift\b", r"\bbeacon\b", r"not only .* but also",
        r"\brevolutionize\b", r"\brevolutionizes\b", r"\brevolutionizing\b", r"\brevolution\b",
        r"\bfoster\b", r"\bintertwined\b", r"\brealm\b", r"\blandscape\b", r"\bunwavering\b",
        r"\bin conclusion\b", r"\bto sum up\b"
    ]
    for word in ai_words:
        matches = re.findall(word, full_text, re.IGNORECASE)
        if matches:
            errors.append(f"Rule 9 Violation: Found AI cliché/banned word '{matches[0]}'")

    # Rule 10: METADATA LENGTH LIMITS
    if len(meta_title) > 60:
        errors.append(f"Rule 10 Violation: meta_title is {len(meta_title)} chars (max 60): '{meta_title}'")
    if len(meta_desc) > 155:
        errors.append(f"Rule 10 Violation: meta_description is {len(meta_desc)} chars (max 155): '{meta_desc}'")

    print(f"Meta Title Length: {len(meta_title)} chars")
    print(f"Meta Description Length: {len(meta_desc)} chars")
    
    if errors:
        print("\n--- VIOLATIONS FOUND ---")
        for e in errors:
            print("❌", e)
        return False
    else:
        print("\n✅ ALL AUTOMATED RULE CHECKS PASSED!")
        return True

if __name__ == "__main__":
    with open("output.json", "r") as f:
        data = json.load(f)
    check_rules(data)
