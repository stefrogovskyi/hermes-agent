import re, sys

def audit_article(text, title, meta_title, meta_description):
    errors = []

    # Rule 1: No em-dashes or double hyphens
    full_text = f"{title}\n{meta_title}\n{meta_description}\n{text}"
    if '—' in full_text or '--' in full_text:
        errors.append("RULE 1 FAIL: Contains em-dash (—) or double hyphen (--).")

    # Rule 4: No explicit connectors as sentence openers
    banned_openers = [
        "that's why", "which is why", "furthermore", "moreover", "in addition", 
        "consequently", "therefore", "thus", "as a result", "hence", "accordingly"
    ]
    # split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        s_clean = s.strip().lstrip('#').strip()
        s_lower = s_clean.lower()
        for opener in banned_openers:
            if s_lower.startswith(opener + " ") or s_lower.startswith(opener + ","):
                errors.append(f"RULE 4 FAIL: Sentence starts with banned connector '{opener}': {s[:50]}...")

    # Rule 5: Contrastive negation limit (MAX 1)
    # Search for "instead of", "rather than", "not only", "not X, but Y", etc.
    negations = []
    for match in re.finditer(r'\b(instead of|rather than|not only|not\b.*?\bbut)\b', full_text, re.IGNORECASE):
        negations.append(match.group(0))
    if len(negations) > 1:
        errors.append(f"RULE 5 FAIL: Found {len(negations)} contrastive negations (MAX 1 allowed): {negations}")

    # Rule 6: Aphoristic one-liner limit (MAX 1-2 single-sentence paragraphs)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and not p.strip().startswith('#') and not p.strip().startswith('***')]
    single_sentence_paras = []
    for p in paragraphs:
        # count sentences in paragraph
        p_sents = [s for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        if len(p_sents) == 1:
            single_sentence_paras.append(p)
    if len(single_sentence_paras) > 2:
        errors.append(f"RULE 6 FAIL: Found {len(single_sentence_paras)} single-sentence paragraphs (MAX 2 allowed): {single_sentence_paras}")

    # Rule 9: AI vocabulary clichés
    ai_cliches = [
        "seamless", "delve", "testament", "game-changer", "realm", "beacon", 
        "tapestry", "holistic", "foster", "robust", "spearhead", "pivotal", 
        "elevate", "unlock", "revolutionize", "vital", "crucial", "underscore", 
        "empower", "streamline", "harness", "leveraging"
    ]
    found_cliches = []
    for w in ai_cliches:
        if re.search(r'\b' + re.escape(w) + r'\b', full_text, re.IGNORECASE):
            found_cliches.append(w)
    if found_cliches:
        errors.append(f"RULE 9 FAIL: Found AI vocabulary clichés: {found_cliches}")

    # Rule 10: Character & Word Limits
    meta_title_len = len(meta_title)
    meta_desc_len = len(meta_description)
    words = len(re.findall(r'\b\w+\b', text))

    if meta_title_len > 60:
        errors.append(f"RULE 10 FAIL: Meta title is {meta_title_len} chars (MAX 60).")
    if meta_desc_len > 155:
        errors.append(f"RULE 10 FAIL: Meta description is {meta_desc_len} chars (MAX 155).")
    if words < 700 or words > 1050:
        errors.append(f"RULE 10 WARNING/FAIL: Body word count is {words} words (target 750-1000).")

    print(f"--- AUDIT REPORT ---")
    print(f"Meta Title Length: {meta_title_len} / 60")
    print(f"Meta Desc Length: {meta_desc_len} / 155")
    print(f"Body Word Count: {words} words")
    print(f"Single-sentence paragraphs: {len(single_sentence_paras)}")
    print(f"Contrastive negations found ({len(negations)}): {negations}")
    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print(" - " + e)
    else:
        print("ALL AUDIT CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    # Test script runner
    pass
