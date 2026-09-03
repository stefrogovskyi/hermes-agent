import json
import re

def validate_article(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body", "")
    
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    errors = []

    # 1. Em-dashes check
    em_dash_chars = ["—", "--", "–"]
    for ed in em_dash_chars:
        if ed in full_text:
            errors.append(f"Rule 1 Violations: Found em-dash/dash variant '{ed}'")

    # 2. Banned words/phrases check
    banned_words = [
        "delve into", "testament to", "crucial role", "in today's world",
        "it is worth noting", "game-changer", "seamless", "unlock",
        "pivotal", "elevate", "cutting-edge", "landscape", "realm",
        "harness", "empower", "tapestry", "in conclusion",
        "furthermore", "moreover", "that's why", "in addition",
        "therefore", "thus", "as a result", "this is because",
        "to sum up", "let's dive into", "as we have seen"
    ]
    for bw in banned_words:
        if re.search(r'\b' + re.escape(bw) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Rule 2/4 Violation: Banned phrase found: '{bw}'")

    # 3. Headers check for textbook architecture
    textbook_headers = ["introduction", "overview", "conclusion", "summary", "background"]
    for line in body.split("\n"):
        if line.startswith("#"):
            header_text = line.lstrip("#").strip().lower()
            if header_text in textbook_headers:
                errors.append(f"Rule 3 Violation: Generic textbook header '{header_text}'")

    # 4. Meta constraints check
    if len(title) > 60:
        errors.append(f"Rule 10 Violation: title length {len(title)} > 60")
    if len(meta_title) > 60:
        errors.append(f"Rule 10 Violation: meta_title length {len(meta_title)} > 60")
    if len(meta_desc) > 155:
        errors.append(f"Rule 10 Violation: meta_description length {len(meta_desc)} > 155")

    # 5. Contrastive negation check
    negation_patterns = [r'\brather than\b', r'\binstead of\b', r'\bnot [a-z0-9\s]+, but\b', r'\bnot [a-z0-9\s]+ but\b']
    negation_count = sum(len(re.findall(p, full_text, re.IGNORECASE)) for p in negation_patterns)
    if negation_count > 1:
        errors.append(f"Rule 5 Violation: Contrastive negation count {negation_count} > 1")

    # 6. Required keywords check
    required_keywords = [
        "Air Cargo Tracking API",
        "Air Waybill (AWB) real-time tracking",
        "Container tracking API location detection",
        "Ocean carrier schedule integration"
    ]
    for kw in required_keywords:
        if kw.lower() not in full_text.lower():
            errors.append(f"Missing Keyword: '{kw}'")

    if not errors:
        print("Validation Successful! All automated checks passed.")
        return True
    else:
        print(f"Validation Failed with {len(errors)} errors:")
        for e in errors:
            print(f" - {e}")
        return False

if __name__ == "__main__":
    with open("/opt/hermes/profiles/archie/test_draft.json") as f:
        d = json.load(f)
    validate_article(d)
