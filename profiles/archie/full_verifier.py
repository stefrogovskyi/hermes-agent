import re

def verify_all(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    title, meta_title, meta_desc = "", "", ""
    body_lines = []
    in_body = False

    for line in lines:
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("META_TITLE:"):
            meta_title = line.replace("META_TITLE:", "").strip()
        elif line.startswith("META_DESCRIPTION:"):
            meta_desc = line.replace("META_DESCRIPTION:", "").strip()
        elif line.startswith("## Body Content"):
            in_body = True
        elif in_body:
            body_lines.append(line)

    body_text = "\n".join(body_lines)

    errors = []
    warnings = []

    # Rule 10: Character Limits
    if len(title) > 60:
        errors.append(f"TITLE length ({len(title)}) exceeds 60 chars")
    if len(meta_title) > 60:
        errors.append(f"META_TITLE length ({len(meta_title)}) exceeds 60 chars")
    if len(meta_desc) > 155:
        errors.append(f"META_DESCRIPTION length ({len(meta_desc)}) exceeds 155 chars")

    # Rule 1: Em-dashes
    em_matches = re.findall(r'[—–]|--', content)
    if em_matches:
        errors.append(f"Found em-dashes/en-dashes/double-hyphens: {em_matches}")

    # Rule 9: Banned AI words
    banned_ai = [
        "delve", "seamless", "unlock", "game-changer", "testament", 
        "tapestry", "pivotal", "elevate", "cutting-edge", "fostering", 
        "vibrant", "it is crucial to note", "in today's fast-paced world"
    ]
    for w in banned_ai:
        if re.search(r'\b' + re.escape(w) + r'\b', content, re.IGNORECASE):
            errors.append(f"Banned AI word found: '{w}'")

    # Additional standard AI buzzwords check (warn)
    buzzwords = ["landscape", "realm", "harness", "empower", "vital", "paramount", "beacon", "mastering", "beacon", "tapestry"]
    for w in buzzwords:
        if re.search(r'\b' + re.escape(w) + r'\b', content, re.IGNORECASE):
            warnings.append(f"Potential AI buzzword: '{w}'")

    # Rule 4: Ban explicit connectors at sentence start
    banned_starters = [
        "Furthermore", "Moreover", "In addition", "However", "Therefore", 
        "That's why", "Which is why", "Consequently", "Additionally", "As a result",
        "Hence", "Thus", "Because of this"
    ]
    for i, l in enumerate(lines, 1):
        if l.startswith('#') or not l.strip():
            continue
        sentences = re.split(r'(?<=[.!?])\s+', l.strip())
        for s in sentences:
            s_clean = s.strip().lstrip('-').lstrip('*').lstrip('0123456789.').strip()
            for bs in banned_starters:
                if s_clean.lower().startswith(bs.lower() + " ") or s_clean.lower().startswith(bs.lower() + ","):
                    errors.append(f"Line {i}: Banned sentence starter '{bs}' in: '{s_clean[:40]}...'")

    # Rule 5: Limit contrastive negations
    # "X, not Y", "instead of", "rather than", "not X but Y", "not only X but Y"
    cn_patterns = [
        (r'\binstead of\b', 'instead of'),
        (r'\brather than\b', 'rather than'),
        (r'\bnot\b\s+[\w\s]+,\s*but\b', 'not X, but Y'),
        (r',\s*not\s+', ', not ')
    ]
    found_cn = []
    for pat, label in cn_patterns:
        matches = re.findall(pat, body_text, re.IGNORECASE)
        for m in matches:
            found_cn.append((label, m))
    
    print(f"Contrastive negations found ({len(found_cn)}): {found_cn}")
    if len(found_cn) > 1:
        errors.append(f"Rule 5 violation: Found {len(found_cn)} contrastive negations (max 1 allowed). Details: {found_cn}")

    # Rule 6: Aphoristic Sentence Limit (short punchy one-liner, e.g., < 6 words standalone sentence or paragraph)
    paragraphs = [p.strip() for p in body_text.split('\n\n') if p.strip()]
    short_lines = []
    for p in paragraphs:
        if p.startswith('#') or p.startswith('-') or p.startswith('*') or p.startswith('1.'):
            continue
        p_sents = re.split(r'(?<=[.!?])\s+', p)
        if len(p_sents) == 1 and len(p_sents[0].split()) <= 6:
            short_lines.append(p_sents[0])
    print(f"Short standalone punchy one-liners found ({len(short_lines)}): {short_lines}")
    if len(short_lines) > 1:
        warnings.append(f"Multiple short standalone one-liners found: {short_lines}")

    # Rule 7: Parallel Twin Sentences
    for p in paragraphs:
        if p.startswith('#'): continue
        lines_p = p.split('\n')
        for l in lines_p:
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', l) if s.strip()]
            for idx in range(len(sents)-1):
                w1 = [w.lower() for w in re.findall(r'\b\w+\b', sents[idx])[:3]]
                w2 = [w.lower() for w in re.findall(r'\b\w+\b', sents[idx+1])[:3]]
                if w1 and w2 and w1 == w2:
                    errors.append(f"Parallel twin sentence structure detected: '{sents[idx]}' AND '{sents[idx+1]}'")

    print("\n=== VERIFICATION RESULTS ===")
    print(f"Title: '{title}' ({len(title)} chars)")
    print(f"Meta Title: '{meta_title}' ({len(meta_title)} chars)")
    print(f"Meta Desc: '{meta_desc}' ({len(meta_desc)} chars)")
    
    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f" - {e}")
    else:
        print("\nNO ERRORS FOUND!")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f" - {w}")

verify_all('draft.md')
