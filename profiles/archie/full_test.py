import json, re

with open("output.json") as f:
    data = json.load(f)

def validate_deliverable(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    md = data.get("content_markdown", "")
    full = f"{title}\n{meta_title}\n{meta_desc}\n{md}"
    
    print("=== RUNNING RIGOROUS VALIDATION ===")
    
    # Check 1: Lengths
    assert len(title) <= 60, f"Title length {len(title)} > 60"
    assert len(meta_title) <= 60, f"Meta title length {len(meta_title)} > 60"
    assert len(meta_desc) <= 155, f"Meta description length {len(meta_desc)} > 155"
    print("✓ Title and Meta length constraints passed.")
    
    # Check 2: Em-dashes / en-dashes / double hyphens (Rule 1)
    dashes = [c for c in full if c in ['—', '–'] or '--' in full]
    assert len(dashes) == 0, f"Rule 1 violation: found dashes {dashes}"
    print("✓ Rule 1 (No em-dashes/en-dashes/double hyphens) passed.")
    
    # Check 3: AI clichés / slop (Rule 2)
    cliches = [
        "today's world", "fast-paced", "it's important to note", "delve into", "delving into",
        "plays a vital role", "vital role", "crucial role", "pivotal role", "it is not merely",
        "in conclusion", "ever-changing", "landscape", "testament", "tapestry", "beacon",
        "game-changer", "unravel", "navigate", "navigating", "boasts", "furthermore", "moreover",
        "in summary", "overall", "unlocking", "fostering", "driving force", "beacon of",
        "testament to", "delve", "plays a crucial role", "paramount"
    ]
    found_cliches = []
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full, re.IGNORECASE):
            found_cliches.append(c)
    assert len(found_cliches) == 0, f"Rule 2 violation: found clichés {found_cliches}"
    print("✓ Rule 2 (No AI clichés/slop) passed.")
    
    # Check 4: Rule 4 (No rigid rule-of-three bullet lists)
    bullet_blocks = re.findall(r'(?:^[ \t]*[\*\-\+\d\.]+\s+.*\n?)+', md, re.MULTILINE)
    three_item_lists = 0
    for block in bullet_blocks:
        items = [line for line in block.strip().split('\n') if line.strip()]
        if len(items) == 3:
            three_item_lists += 1
    assert three_item_lists == 0, f"Rule 4 violation: found {three_item_lists} 3-item list(s)."
    print("✓ Rule 4 (No rule-of-three bullet lists) passed.")
    
    # Check 5: Rule 6 (No over-explaining connectors)
    connectors = ["that's why", "which is why", "this explains why", "because of this", "as a result", "consequently", "due to this"]
    found_conn = []
    for conn in connectors:
        if re.search(r'\b' + re.escape(conn) + r'\b', full, re.IGNORECASE):
            found_conn.append(conn)
    assert len(found_conn) == 0, f"Rule 6 violation: found connectors {found_conn}"
    print("✓ Rule 6 (No over-explaining connectors) passed.")
    
    # Check 6: Rule 7 (Max 1 contrastive negation across piece)
    cn_count = 0
    for term in ["instead of", "rather than", "not merely", "not only"]:
        cnt = len(re.findall(r'\b' + re.escape(term) + r'\b', full, re.IGNORECASE))
        cn_count += cnt
    assert cn_count <= 1, f"Rule 7 violation: found {cn_count} contrastive negations (max 1 allowed)."
    print(f"✓ Rule 7 (Max 1 contrastive negation) passed. Found count: {cn_count}")
    
    # Check 7: Keywords
    keywords = [
        "port dwell time", "global supply chain bottleneck", "maritime freight rate volatility",
        "container shipping delays", "transshipment congestion", "berth utilization",
        "multimodal route diversification", "real-time cargo tracking"
    ]
    missing_kw = []
    for kw in keywords:
        if not re.search(r'\b' + re.escape(kw) + r'\b', full, re.IGNORECASE):
            missing_kw.append(kw)
    assert len(missing_kw) == 0, f"Missing keywords: {missing_kw}"
    print("✓ Required keywords present.")
    
    print("ALL VERIFICATIONS SUCCESSFUL!")

validate_deliverable(data)
