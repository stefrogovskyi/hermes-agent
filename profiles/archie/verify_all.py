import re
import sys

def check_all_rules(filename):
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
    dash_matches = re.findall(r'[—–]|\-\-| \- ', text)
    if dash_matches:
        errors.append(f"Rule 1 Violation: Found forbidden dashes/hyphens: {set(dash_matches)}")

    # Rule 4: Forbidden explicit connectors
    explicit_connectors = [
        "Furthermore", "Moreover", "In addition", "Additionally", 
        "Consequently", "On the other hand", "It is important to note",
        "That being said", "In fact", "As a result", "Therefore"
    ]
    for conn in explicit_connectors:
        matches = re.findall(rf'\b{re.escape(conn)}\b', text, re.IGNORECASE)
        if matches:
            errors.append(f"Rule 4 Violation: Found explicit connector: '{conn}'")

    # Rule 5: Contrastive Negation limit (max 1)
    # Check "not X, but Y", "instead of X, Y"
    negations = re.findall(r'\bnot\b.*?\bbut\b|\binstead of\b', text, re.IGNORECASE)
    if len(negations) > 1:
        errors.append(f"Rule 5 Violation: Found {len(negations)} contrastive negations (max 1): {negations}")
    else:
        print(f"Rule 5 OK: Contrastive negations count = {len(negations)}")

    # Rule 7: Parallel twin-sentence ban
    # Split text into sentences and check consecutive sentence start words
    paragraphs = text.split('\n\n')
    for p in paragraphs:
        # crude sentence split
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        for i in range(len(sentences) - 1):
            s1_words = sentences[i].split()
            s2_words = sentences[i+1].split()
            if len(s1_words) > 0 and len(s2_words) > 0:
                if s1_words[0].lower() == s2_words[0].lower() and len(s1_words[0]) > 3:
                    warnings.append(f"Rule 7 Warning: Twin sentence start '{s1_words[0]}' in sentences:\n  1: {sentences[i]}\n  2: {sentences[i+1]}")

    # Rule 9: Forbidden AI words
    forbidden_words = [
        "delve", "testament", "tapestry", "beacon", "pivotal", "realm", 
        "crucial role", "game-changer", "seamless", "unlock", "landscape", 
        "spearhead", "navigate", "foster", "ever-evolving", "paramount",
        "robust", "multifaceted", "imperative", "underscore", "embark",
        "vibrant", "elevate", "harness", "demystify", "dive into", "in summary",
        "in conclusion", "to sum up", "vital role", "testament to"
    ]
    for word in forbidden_words:
        matches = re.findall(rf'\b{re.escape(word)}\b', text, re.IGNORECASE)
        if matches:
            errors.append(f"Rule 9 Violation: Found forbidden AI word/phrase: '{word}'")

    # Rule 10: Meta limits
    if len(meta_title) > 60:
        errors.append(f"Rule 10 Violation: Meta Title length is {len(meta_title)} chars (max 60): '{meta_title}'")
    else:
        print(f"Meta Title length OK: {len(meta_title)} chars")

    if len(meta_desc) > 155:
        errors.append(f"Rule 10 Violation: Meta Description length is {len(meta_desc)} chars (max 155): '{meta_desc}'")
    else:
        print(f"Meta Description length OK: {len(meta_desc)} chars")

    if any(d in title for d in ['—', '–', '--']):
        errors.append("Rule 10 Violation: Title contains forbidden dashes")
    if any(d in meta_title for d in ['—', '–', '--']):
        errors.append("Rule 10 Violation: Meta Title contains forbidden dashes")
    if any(d in meta_desc for d in ['—', '–', '--']):
        errors.append("Rule 10 Violation: Meta Description contains forbidden dashes")

    # Rule 11: Grounding / tool names check
    required_tools = [
        "LikesID.com", "LikesAround.com", "SocialBoss.org", "VideosGrow.com",
        "Hootsuite", "Planoly.com", "Emplifi", "VSCO", "Picsart", "Canva",
        "Wave.video", "Veed", "ChatGPT", "Tagsfinder.com", "Visme", "Beautiful AI"
    ]
    for tool in required_tools:
        if tool.lower() not in text.lower():
            errors.append(f"Rule 11 Violation: Missing required tool from source: '{tool}'")

    # Check Sprout Social / Sproutsocial
    if "sprout" not in text.lower():
        errors.append("Rule 11 Violation: Missing Sprout Social / Sproutsocial")

    print("\n--- RESULTS ---")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print("  -", w)
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
    else:
        print("NO AUTOMATED ERRORS FOUND!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_all_rules(sys.argv[1])
    else:
        print("Provide filename as argument")
