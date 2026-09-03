import json
import re

def check_rules(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_markdown", "")
    
    full_text = f"{title}\n{body}"
    
    print(f"Meta Title Length: {len(meta_title)} (Max 60)")
    print(f"Meta Description Length: {len(meta_desc)} (Max 155)")
    
    if len(meta_title) > 60:
        print("FAIL: Meta title exceeds 60 characters!")
    if len(meta_desc) > 155:
        print("FAIL: Meta description exceeds 155 characters!")
        
    # Check 1: EM-DASHES
    if "—" in full_text or "--" in full_text:
        print("FAIL: Contains em-dash (— or --)!")
    else:
        print("PASS: No em-dashes.")
        
    # Check 4: Explicit Connectors
    forbidden_connectors = [
        r"\bfurthermore\b", r"\bin addition\b", r"\bmoreover\b", 
        r"\bthat's why\b", r"\bconsequently\b", r"\bthus\b", 
        r"\badditionally\b", r"\boverall\b", r"\bin conclusion\b"
    ]
    for conn in forbidden_connectors:
        matches = re.findall(conn, full_text, re.IGNORECASE)
        if matches:
            print(f"FAIL: Found forbidden connector: {matches}")
            
    # Check 5: Contrastive negation
    contrastive_patterns = [
        r"not only\b.*?\bbut also",
        r"\bnot\b.*?\bbut\b",
        r"\binstead of\b",
        r"\brather than\b"
    ]
    c_count = 0
    for pat in contrastive_patterns:
        matches = re.findall(pat, full_text, re.IGNORECASE)
        c_count += len(matches)
        if matches:
            print(f"Contrastive matches ({pat}): {matches}")
    print(f"Total contrastive negation count: {c_count} (Max 1)")
    if c_count > 1:
        print("FAIL: Exceeds contrastive negation limit!")

if __name__ == "__main__":
    with open("output.json", "r") as f:
        data = json.load(f)
    check_rules(data)
