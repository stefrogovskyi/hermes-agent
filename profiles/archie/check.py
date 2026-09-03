import json
import re

def validate_all():
    with open("output.json", "r") as f:
        data = json.load(f)

    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_markdown", "")

    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    errors = []

    # 1. EM-DASHES
    dashes = ["—", "--", "–"]
    for d in dashes:
        if d in full_text:
            errors.append(f"Rule 1 FAIL: Em-dash or en-dash '{d}' found.")

    # Meta lengths
    if len(meta_title) > 60:
        errors.append(f"Meta title length ({len(meta_title)}) exceeds 60 chars.")
    if len(meta_desc) > 155:
        errors.append(f"Meta description length ({len(meta_desc)}) exceeds 155 chars.")

    # 3. Cliché headings and fluff
    cliché_terms = ["introduction", "conclusion", "benefits of", "in this article", "in conclusion"]
    for ct in cliché_terms:
        if ct in full_text.lower():
            errors.append(f"Rule 3 FAIL: Cliché term '{ct}' found.")

    # 4. Connectors
    forbidden_connectors = [
        "Furthermore", "Moreover", "In conclusion", "Additionally", 
        "Consequently", "Ultimately", "Indeed", "Importantly", 
        "In summary", "First and foremost", "To summarize", "On the other hand"
    ]
    for conn in forbidden_connectors:
        if re.search(r'\b' + re.escape(conn) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Rule 4 FAIL: Forbidden connector '{conn}' found.")

    # 5. Contrastive negation check ("not X, but Y", "it's not X, it's Y", "not only X, but Y")
    cn_matches = re.findall(r'\bnot\b.*?\bbut\b', full_text, re.IGNORECASE)
    print(f"Contrastive negation candidates found: {len(cn_matches)}")
    if len(cn_matches) > 1:
        errors.append(f"Rule 5 FAIL: More than 1 contrastive negation found: {cn_matches}")

    # Keywords
    keywords = [
        "Maritime logistics analytics",
        "Freight rate breakdown",
        "PDF to PPTX conversion",
        "Cargo tracking reporting",
        "Logistics presentation tools"
    ]
    for kw in keywords:
        if not re.search(r'\b' + re.escape(kw) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"MISSING KEYWORD: '{kw}'")

    if errors:
        print("VALIDATION ERRORS:")
        for err in errors:
            print("-", err)
    else:
        print("ALL PROGRAMMATIC CHECKS PASSED!")

if __name__ == "__main__":
    validate_all()
