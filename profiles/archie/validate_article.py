import json, re

def validate_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_markdown", "")
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    issues = []

    # Rule 1: Zero em-dashes
    if '—' in full_text or '--' in full_text or '–' in full_text:
        issues.append("RULE 1 FAIL: Found em-dash or en-dash (—, --, –)")

    # Rule 2: AI clichés
    cliches = [
        "delve into", "testament to", "crucial role", "in today's world", "it is worth noting",
        "game-changer", "pivotal", "unraveling", "beacon", "landscape", "spearheading",
        "unlocking", "tapestry", "seamless", "ever-evolving", "fostering", "groundbreaking",
        "harnessing", "paradigm shift", "vital role", "leverage"
    ]
    for c in cliches:
        matches = re.findall(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE)
        if matches:
            issues.append(f"RULE 2 FAIL: Found AI cliché '{c}' ({len(matches)} times)")

    # Rule 5: Explicit connectors
    connectors = [
        "Furthermore", "Moreover", "In addition", "Consequently", "On the other hand",
        "Therefore", "Additionally", "It is important to remember"
    ]
    for conn in connectors:
        matches = re.findall(r'\b' + re.escape(conn) + r'\b', full_text, re.IGNORECASE)
        if matches:
            issues.append(f"RULE 5 FAIL: Found banned connector '{conn}'")

    # Rule 6: Contrastive negation check
    negation_patterns = [
        r'\binstead of\b',
        r'\brather than\b',
        r'\bnot\s+[^.,;!?]+\s+but\b'
    ]
    neg_count = 0
    found_negs = []
    for pat in negation_patterns:
        m = re.findall(pat, full_text, re.IGNORECASE)
        if m:
            neg_count += len(m)
            found_negs.extend(m)
    if neg_count > 1:
        issues.append(f"RULE 6 FAIL: Found {neg_count} contrastive negations (max 1 allowed): {found_negs}")
    else:
        print(f"Rule 6 Check: {neg_count} contrastive negations found ({found_negs})")

    # Rule 10: Metadata character limits
    print(f"Title length: {len(title)} / 60")
    print(f"Meta title length: {len(meta_title)} / 60")
    print(f"Meta description length: {len(meta_desc)} / 155")

    if len(title) > 60:
        issues.append(f"RULE 10 FAIL: Title length is {len(title)} (max 60)")
    if len(meta_title) > 60:
        issues.append(f"RULE 10 FAIL: Meta title length is {len(meta_title)} (max 60)")
    if len(meta_desc) > 155:
        issues.append(f"RULE 10 FAIL: Meta description length is {len(meta_desc)} (max 155)")

    # Rule 11: Exact figures and required terms
    required_terms = [
        "10%", "25%", "34%", "20%", "46%", "32%", "24%", "36%", "31%", "49%", "30%", "26-49%", "54%", "30%",
        "$14 billion", "$47.2 billion", "$18.5 billion", "$15 billion",
        "18,000+", "ICS2", "ENS", "EDI", "ACE", "IEEPA",
        "April 2", "April 1", "25+",
        "automobile", "Mexican", "Canadian", "Chinese", "EU", "Vietnamese", "Taiwanese", "Japanese", "South Korean",
        "Thai", "Swiss", "Indonesian", "Malaysian", "Cambodian", "United Kingdom", "South African",
        "Venezuelan oil", "Digital Service Taxes", "Copper", "Timber", "lumber", "semiconductor",
        "clothing", "laptops", "tablets", "footwear", "toys", "Canadian ports"
    ]
    for term in required_terms:
        if term.lower() not in full_text.lower():
            issues.append(f"RULE 11 FAIL: Missing required fact/term '{term}'")

    # Trend keywords check
    trend_kws = [
        "tariff volatility", "reciprocal duties", "HTS reclassification",
        "supply chain resilience", "blank sailings", "ICS2 compliance"
    ]
    for kw in trend_kws:
        if kw.lower() not in full_text.lower():
            issues.append(f"TREND KW FAIL: Missing trend keyword '{kw}'")

    if issues:
        print("\nISSUES FOUND:")
        for issue in issues:
            print(" -", issue)
    else:
        print("\nALL AUTOMATED CHECKS PASSED!")

if __name__ == "__main__":
    validate_json("output.json")
