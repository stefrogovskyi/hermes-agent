import re

def thorough_check(title, meta_title, meta_desc, body):
    errors = []

    # Rule 10: Limits
    print(f"Title length: {len(title)} / 60")
    print(f"Meta Title length: {len(meta_title)} / 60")
    print(f"Meta Description length: {len(meta_desc)} / 155")
    
    if len(title) > 60:
        errors.append(f"Title too long: {len(title)}")
    if len(meta_title) > 60:
        errors.append(f"Meta Title too long: {len(meta_title)}")
    if len(meta_desc) > 155:
        errors.append(f"Meta Description too long: {len(meta_desc)}")

    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    # Rule 1: Dash check
    if '—' in full_text:
        errors.append("Found em-dash —")
    if '–' in full_text:
        errors.append("Found en-dash –")
    if '--' in full_text:
        errors.append("Found double hyphen --")

    # Rule 3: Textbook architecture
    textbook_phrases = ["in this article", "we discuss", "let's look at", "in conclusion", "to summarize", "let us explore", "in summary", "we will examine"]
    for tp in textbook_phrases:
        if tp in full_text.lower():
            errors.append(f"Textbook phrase: '{tp}'")

    # Rule 4: Banned connectors
    banned_openers = [
        "Furthermore", "Moreover", "In addition", "However", "Therefore", 
        "That's why", "Which is why", "Consequently", "Additionally", 
        "As a result", "Hence", "Thus", "Because of this"
    ]
    
    # Split body into sentences across paragraphs
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
    all_sentences = []
    
    single_sentence_paras = []
    
    for p_idx, p in enumerate(paragraphs):
        if p.startswith('#'):
            continue
        # Split paragraph into sentences
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        if len(sents) == 1:
            single_sentence_paras.append(p)
            
        for s_idx, s in enumerate(sents):
            all_sentences.append(s)
            # Check banned openers
            s_clean = s.lstrip('#').strip()
            for bo in banned_openers:
                if re.match(r'^' + re.escape(bo) + r'[\s,]', s_clean, re.IGNORECASE):
                    errors.append(f"Banned opener '{bo}' in sentence: '{s_clean}'")

    if len(single_sentence_paras) > 1:
        errors.append(f"Too many single-sentence paragraphs ({len(single_sentence_paras)}): {single_sentence_paras}")

    # Rule 5: Contrastive negations
    contrastive_patterns = [
        r'\bnot\b.*?\bbut\b', r'\binstead of\b', r'\brather than\b', r'\bnot only\b.*?\bbut\b'
    ]
    c_matches = []
    for pat in contrastive_patterns:
        for m in re.finditer(pat, full_text, re.IGNORECASE):
            c_matches.append(m.group(0))
    if len(c_matches) > 1:
        errors.append(f"Too many contrastive negations ({len(c_matches)}): {c_matches}")

    # Rule 7: Parallel twin-sentences
    for i in range(len(all_sentences) - 1):
        s1 = all_sentences[i].strip()
        s2 = all_sentences[i+1].strip()
        w1 = s1.split()[0].lower() if s1.split() else ""
        w2 = s2.split()[0].lower() if s2.split() else ""
        if w1 and w1 == w2 and len(w1) > 2:
            # Check first two words
            w1_2 = " ".join(s1.split()[:2]).lower()
            w2_2 = " ".join(s2.split()[:2]).lower()
            if w1_2 == w2_2:
                errors.append(f"Twin sentence opener '{w1_2}':\n  1: {s1}\n  2: {s2}")

    # Rule 9: AI slop words
    slop_words = [
        "delve", "seamless", "unlock", "game-changer", "testament", "tapestry", 
        "pivotal", "elevate", "cutting-edge", "fostering", "vibrant", "landscape", 
        "realm", "harness", "empower", "vital", "paramount", "beacon", 
        "in today's world", "cornerstone"
    ]
    for sw in slop_words:
        matches = re.findall(r'\b' + re.escape(sw) + r'\b', full_text, re.IGNORECASE)
        if matches:
            errors.append(f"AI slop word found: '{sw}' ({len(matches)} times)")

    # Target trend keywords check
    target_keywords = [
        "cloud logistics SaaS",
        "real-time container tracking",
        "digitalization of trade flows",
        "supply chain cybersecurity & VPN",
        "freight rate visibility"
    ]
    missing_kw = []
    for kw in target_keywords:
        if kw.lower() not in full_text.lower():
            missing_kw.append(kw)
    if missing_kw:
        errors.append(f"Missing target trend keywords: {missing_kw}")

    words = body.split()
    print(f"Total Body Word Count: {len(words)}")

    return errors

