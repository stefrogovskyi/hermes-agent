import re

def check_rules(title, meta_title, meta_desc, body):
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    print("--- CHECKING RULES ---")
    
    # Rule 1: Forbidden dashes (em-dash, en-dash, double hyphen)
    forbidden_dashes = ['—', '–', '--']
    dash_found = False
    for d in forbidden_dashes:
        if d in full_text:
            print(f"FAIL Rule 1: Found forbidden dash '{d}'")
            dash_found = True
    if not dash_found:
        print("PASS Rule 1: No forbidden dashes found.")

    # Rule 9: Banned AI vocabulary
    banned_words = [
        "delve", "tapestry", "beacon", "testament", "crucial", "pivotal",
        "game-changer", "seamless", "ever-evolving", "paramount", "foster",
        "unlock", "harness", "empower", "spearhead", "robust", "demystify",
        "revolutionize", "cutting-edge", "realm"
    ]
    words_found = []
    for w in banned_words:
        if re.search(r'\b' + re.escape(w) + r'\b', full_text, re.IGNORECASE):
            words_found.append(w)
    if words_found:
        print(f"FAIL Rule 9: Found banned words: {words_found}")
    else:
        print("PASS Rule 9: No banned AI words found.")

    # Rule 4: Forced connectors
    forced_connectors = ["that's why", "this is because", "as a result", "consequently"]
    connectors_found = []
    for c in forced_connectors:
        if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
            connectors_found.append(c)
    if connectors_found:
        print(f"FAIL Rule 4: Found forced connectors: {connectors_found}")
    else:
        print("PASS Rule 4: No forced connectors found.")

    # Rule 3: Cliché transitions
    cliches = ["in conclusion", "as we have seen", "furthermore", "moreover", "let's dive into", "to sum up"]
    cliches_found = []
    for cl in cliches:
        if re.search(r'\b' + re.escape(cl) + r'\b', full_text, re.IGNORECASE):
            cliches_found.append(cl)
    if cliches_found:
        print(f"FAIL Rule 3: Found cliché transitions: {cliches_found}")
    else:
        print("PASS Rule 3: No cliché transitions found.")

    # Rule 5: Contrastive negation check
    # Check for "not", "rather than", "instead of"
    negations = re.findall(r'\b(rather than|instead of)\b', full_text, re.IGNORECASE)
    print(f"INFO Rule 5: Found contrastive negations (rather than/instead of): {negations}")

    # Rule 10: Lengths
    print(f"Rule 10 Lengths:")
    print(f"  Title length: {len(title)} / 60 ({'PASS' if len(title) <= 60 else 'FAIL'})")
    print(f"  Meta Title length: {len(meta_title)} / 60 ({'PASS' if len(meta_title) <= 60 else 'FAIL'})")
    print(f"  Meta Description length: {len(meta_desc)} / 155 ({'PASS' if len(meta_desc) <= 155 else 'FAIL'})")

