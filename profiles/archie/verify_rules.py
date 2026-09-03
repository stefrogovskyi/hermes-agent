import re
import sys

def check_draft(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')
    title = ""
    meta_title = ""
    meta_desc = ""

    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
        elif line.startswith('**Meta Title:**'):
            meta_title = line.replace('**Meta Title:**', '').strip()
        elif line.startswith('**Meta Description:**'):
            meta_desc = line.replace('**Meta Description:**', '').strip()

    errors = []
    warnings = []

    # Rule 1: NO EM-DASH BAN
    # Check for em-dash '—', en-dash '–', double hyphen '--', or spaced hyphens ' - '
    dash_matches = re.findall(r'[—–]|\-\-| \- ', text)
    if dash_matches:
        errors.append(f"Rule 1 Violation: Found forbidden dashes/hyphens: {set(dash_matches)}")

    # Rule 9: Forbidden AI words
    forbidden_words = [
        "delve", "testament", "tapestry", "beacon", "pivotal", "realm", 
        "crucial role", "game-changer", "seamless", "unlock", "landscape", 
        "spearhead", "navigate", "foster", "ever-evolving", "paramount",
        "robust", "multifaceted", "imperative", "underscore", "embark",
        "vibrant", "elevate", "harness", "demystify", "dive into", "in summary",
        "in conclusion", "to sum up"
    ]
    for word in forbidden_words:
        if re.search(rf'\b{re.escape(word)}\b', text, re.IGNORECASE):
            errors.append(f"Rule 9 Violation: Found forbidden AI word/phrase: '{word}'")

    # Rule 4: Forbidden explicit connectors
    explicit_connectors = [
        "Furthermore", "Moreover", "In addition", "Additionally", 
        "Consequently", "On the other hand", "It is important to note"
    ]
    for conn in explicit_connectors:
        if re.search(rf'\b{re.escape(conn)}\b', text, re.IGNORECASE):
            errors.append(f"Rule 4 Violation: Found explicit connector: '{conn}'")

    # Rule 10: Meta limits
    if len(meta_title) > 60:
        errors.append(f"Rule 10 Violation: Meta Title length is {len(meta_title)} chars (max 60): '{meta_title}'")
    else:
        print(f"Meta Title length OK: {len(meta_title)} chars")

    if len(meta_desc) > 155:
        errors.append(f"Rule 10 Violation: Meta Description length is {len(meta_desc)} chars (max 155): '{meta_desc}'")
    else:
        print(f"Meta Description length OK: {len(meta_desc)} chars")

    if '—' in title or '–' in title or '--' in title:
        errors.append("Rule 10 Violation: Title contains forbidden dashes")
    if '—' in meta_title or '–' in meta_title or '--' in meta_title:
        errors.append("Rule 10 Violation: Meta Title contains forbidden dashes")
    if '—' in meta_desc or '–' in meta_desc or '--' in meta_desc:
        errors.append("Rule 10 Violation: Meta Description contains forbidden dashes")

    # Rule 5: Contrastive Negation limit (max 1)
    # Check "not X, but Y", "instead of"
    negation_matches = re.findall(r'\bnot\b.*?\bbut\b|\binstead of\b', text, re.IGNORECASE)
    print(f"Contrastive negation count: {len(negation_matches)} -> {negation_matches}")
    if len(negation_matches) > 1:
        errors.append(f"Rule 5 Violation: Found {len(negation_matches)} contrastive negations (max 1): {negation_matches}")

    print("\n--- RESULTS ---")
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
    else:
        print("NO AUTOMATED ERRORS FOUND!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_draft(sys.argv[1])
    else:
        print("Provide filename as argument")
