import json
import re

def validate_rewrite(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_description = data.get("meta_description", "")
    body = data.get("body_markdown", "")
    full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

    issues = []

    # Char limits
    if len(title) > 60:
        issues.append(f"Title length {len(title)} > 60")
    if len(meta_title) > 60:
        issues.append(f"Meta title length {len(meta_title)} > 60")
    if len(meta_description) > 155:
        issues.append(f"Meta description length {len(meta_description)} > 155")

    # Rule 1: Zero em-dashes
    if "—" in full_text or "--" in full_text or "–" in full_text:
        issues.append("Rule 1 VIOLATION: Em-dash or double dash found!")

    # Rule 2: AI clichés / slop
    cliches = [
        "game-changer", "game changer", "delve", "testament", "crucial", "in today's",
        "seamless", "landscape", "foster", "elevate", "unlock", "empower", "harnessing",
        "vital role", "key takeaway", "pivotal", "beacon", "tapestry", "realm", "synergy",
        "underscores", "vivid"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
            issues.append(f"Rule 2 VIOLATION: AI cliché/slop found: '{c}'")

    # Rule 6: Over-explaining connectors
    connectors = ["that's why", "which is why", "because of this", "this is because", "as a result of this"]
    for conn in connectors:
        if re.search(r'\b' + re.escape(conn) + r'\b', full_text, re.IGNORECASE):
            issues.append(f"Rule 6 VIOLATION: Banned connector found: '{conn}'")

    # Rule 7: Limit contrastive negation to max 1
    # Look for "instead of", "rather than", "not X, but Y", "X, not Y"
    negations = len(re.findall(r'\binstead of\b|\brather than\b|\bnot\s+\w+,\s*but\b', full_text, re.IGNORECASE))
    if negations > 1:
        issues.append(f"Rule 7 VIOLATION: Contrastive negation count ({negations}) > 1")

    # Rule 10: Symmetric antithesis / "from X to Y" / "not only... but also"
    if re.search(r'\bfrom\s+[\w\s]+\s+to\s+[\w\s]+', full_text, re.IGNORECASE):
        # check if it's "from X to Y" style
        # let's flag matches to inspect
        matches = re.findall(r'\bfrom\s+\w+(?:\s+\w+)?\s+to\s+\w+(?:\s+\w+)?', full_text, re.IGNORECASE)
        issues.append(f"Rule 10 WARNING/CHECK: 'from... to...' pattern found: {matches}")

    if re.search(r'not only.*but also', full_text, re.IGNORECASE):
        issues.append("Rule 10 VIOLATION: 'not only... but also' found")

    # Keywords check
    required_keywords = [
        "real-time freight analytics",
        "supply chain control tower",
        "logistics telemetry dashboards",
        "predictive route optimization",
        "cargo capacity heatmaps",
        "carrier performance metrics"
    ]
    for kw in required_keywords:
        if kw.lower() not in full_text.lower():
            issues.append(f"KEYWORD MISSING: '{kw}'")

    return issues

if __name__ == "__main__":
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else "/opt/hermes/profiles/archie/writer_output.json"
    with open(file_path, "r") as f:
        data = json.load(f)
    issues = validate_rewrite(data)
    if issues:
        print("ISSUES FOUND:")
        for i in issues:
            print("-", i)
    else:
        print("ALL AUTOMATED CHECKS PASSED!")
