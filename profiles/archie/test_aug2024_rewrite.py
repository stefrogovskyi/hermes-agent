import re
import json

def check_all_rules(data):
    title = data.get("title", "")
    meta_title = data.get("meta_title", "")
    meta_desc = data.get("meta_description", "")
    body = data.get("body_markdown", "")
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    errors = []

    # Rule 1: Zero em-dashes, en-dashes, double hyphens
    if '—' in full_text:
        errors.append("Rule 1 Fail: Contains em-dash (—)")
    if '–' in full_text:
        errors.append("Rule 1 Fail: Contains en-dash (–)")
    if '--' in full_text:
        errors.append("Rule 1 Fail: Contains double hyphen (--)")

    # Rule 2: Forbidden AI clichés
    cliches = [
        "delve into", "testament to", "crucial role", "game-changer", "in today's world",
        "unwavering commitment", "it is worth noting", "beacon of", "seamlessly", "seamless",
        "tapestry", "fostering", "foster", "elevate", "cutting-edge", "paramount", "pivotal",
        "moreover", "furthermore", "unlock", "realm", "holistic", "empower", "spearhead",
        "vital", "crucial", "underscore", "streamline", "harness", "leveraging", "transformative",
        "game changer", "testament", "delve"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Rule 2 Fail: Found forbidden cliché '{c}'")

    # Rule 5: Forbidden explicit connectors
    forbidden_connectors = [
        "furthermore", "moreover", "additionally", "that's why", "this is because",
        "as a result", "consequently", "therefore", "thus", "hence", "accordingly",
        "which is why"
    ]
    # Check if sentence starts with these
    sentences = re.split(r'(?<=[.!?])\s+', body)
    for s in sentences:
        s_clean = s.strip().lstrip('#').strip()
        s_lower = s_clean.lower()
        for conn in forbidden_connectors:
            if s_lower.startswith(conn + " ") or s_lower.startswith(conn + ","):
                errors.append(f"Rule 5 Fail: Sentence starts with explicit connector '{conn}': '{s[:60]}...'")

    # Rule 6: Contrastive negation limit (Max 1 instance)
    # Expressions like "X, not Y", "instead of", "rather than", "not only"
    negations = []
    neg_patterns = [r'\binstead of\b', r'\brather than\b', r'\bnot only\b', r'\bnot\s+[^,.!?]+\s*,?\s*but\b']
    for pat in neg_patterns:
        matches = re.findall(pat, full_text, re.IGNORECASE)
        negations.extend(matches)
    if len(negations) > 1:
        errors.append(f"Rule 6 Fail: Found {len(negations)} contrastive negations (Max 1 allowed): {negations}")

    # Rule 7: Single-sentence paragraph limit (0 or 1, preferably 0)
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#') and not p.strip().startswith('***')]
    single_sent_paras = []
    for p in paragraphs:
        p_sents = [s for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        if len(p_sents) == 1:
            single_sent_paras.append(p)
    if len(single_sent_paras) > 1:
        errors.append(f"Rule 7 Fail: Found {len(single_sent_paras)} single-sentence paragraphs (Max 1 allowed): {single_sent_paras}")

    # Rule 9: Metadata length
    if len(title) > 60:
        errors.append(f"Rule 9 Fail: Title is {len(title)} chars (Max 60): '{title}'")
    if len(meta_title) > 60:
        errors.append(f"Rule 9 Fail: Meta Title is {len(meta_title)} chars (Max 60): '{meta_title}'")
    if len(meta_desc) > 155:
        errors.append(f"Rule 9 Fail: Meta Description is {len(meta_desc)} chars (Max 155): '{meta_desc}'")

    print(f"=== CHECK RESULTS ===")
    print(f"Title ({len(title)}): {title}")
    print(f"Meta Title ({len(meta_title)}): {meta_title}")
    print(f"Meta Description ({len(meta_desc)}): {meta_desc}")
    print(f"Body length: {len(body)} chars, {len(re.findall(r'\\b\\w+\\b', body))} words")
    print(f"Single sentence paragraphs: {len(single_sent_paras)}")
    print(f"Contrastive negations: {len(negations)} {negations}")
    
    if errors:
        print("\nERRORS DETECTED:")
        for e in errors:
            print(f"- {e}")
        return False
    else:
        print("\nALL RULES PASSED PERFECTLY!")
        return True

if __name__ == "__main__":
    pass
