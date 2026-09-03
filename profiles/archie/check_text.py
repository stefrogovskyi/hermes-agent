import re
import sys

def check_rules(article_str):
    lines = article_str.strip().split('\n')
    
    title = ""
    meta_title = ""
    meta_desc = ""
    full_text = ""
    
    mode = None
    full_text_lines = []
    
    for line in lines:
        if line.startswith("ARTICLE TITLE:"):
            title = line.replace("ARTICLE TITLE:", "").strip()
        elif line.startswith("META TITLE:"):
            meta_title = line.replace("META TITLE:", "").strip()
        elif line.startswith("META DESCRIPTION:"):
            meta_desc = line.replace("META DESCRIPTION:", "").strip()
        elif line.startswith("FULL TEXT:"):
            mode = "full_text"
        elif mode == "full_text":
            full_text_lines.append(line)
            
    full_text = "\n".join(full_text_lines)
    all_text = article_str
    
    print(f"Article Title ({len(title)} chars, max 60): {title}")
    print(f"Meta Title ({len(meta_title)} chars, max 60): {meta_title}")
    print(f"Meta Description ({len(meta_desc)} chars, max 155): {meta_desc}")
    
    errors = []
    
    # Check 1: No em-dashes
    if "—" in all_text or "--" in all_text:
        errors.append("Rule 1 violated: Em-dash or -- found")
        
    # Check 2: AI clichés
    cliches = [
        "today's fast-paced world", "delve into", "not just", "plays a crucial role",
        "paramount importance", "game-changer", "testament to", "in conclusion",
        "landscape", "tapestry", "realm", "ever-evolving", "game changer",
        "crucial role", "vital role", "key role", "in summary", "to sum up"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', all_text, re.IGNORECASE):
            errors.append(f"Rule 2 violated: Cliche found: '{c}'")
            
    # Check 6: Over-explaining connectors
    connectors = ["that's why", "which is why", "this is because", "because of this", "therefore"]
    for conn in connectors:
        if re.search(r'\b' + re.escape(conn) + r'\b', all_text, re.IGNORECASE):
            errors.append(f"Rule 6 violated: Connector found: '{conn}'")
            
    # Check required trend keywords:
    keywords = ["acoustic AI", "predictive maintenance", "spatial audio", "audio branding", "telematics integration"]
    for kw in keywords:
        if kw.lower() not in all_text.lower():
            errors.append(f"Missing required trend keyword: '{kw}'")
            
    if len(title) > 60:
        errors.append("Article title exceeds 60 chars")
    if len(meta_title) > 60:
        errors.append("Meta title exceeds 60 chars")
    if len(meta_desc) > 155:
        errors.append("Meta description exceeds 155 chars")
        
    if errors:
        print("\nERRORS / VIOLATIONS:")
        for e in errors:
            print(f"- {e}")
    else:
        print("\nALL AUTOMATED CHECKS PASSED!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            check_rules(f.read())
