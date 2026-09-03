import json
import re

from generate_json import data

def audit():
    title = data["title"]
    meta_title = data["meta_title"]
    meta_desc = data["meta_description"]
    body = data["body_markdown"]
    full = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    errors = []

    # 1. Dash check
    if '—' in full:
        errors.append("EM-DASH found")
    if '–' in full:
        errors.append("EN-DASH found")
    if '--' in full:
        errors.append("DOUBLE HYPHEN found")

    # 2. Cliche check
    cliches = [
        "delve into", "testament to", "crucial role", "game-changer", "in today's world",
        "unwavering commitment", "it is worth noting", "beacon of", "seamlessly", "seamless",
        "tapestry", "fostering", "foster", "elevate", "cutting-edge", "paramount", "pivotal",
        "moreover", "furthermore", "unlock", "realm", "holistic", "empower", "spearhead",
        "vital", "crucial", "underscore", "streamline", "harness", "leveraging", "transformative"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full, re.IGNORECASE):
            errors.append(f"Forbidden cliché: '{c}'")

    # 3. Connector check
    banned_connectors = [
        "furthermore", "moreover", "additionally", "that's why", "this is because",
        "as a result", "consequently", "therefore", "thus", "hence", "accordingly",
        "which is why"
    ]
    sents = re.split(r'(?<=[.!?])\s+', body)
    for s in sents:
        s_clean = s.strip().lstrip('#').strip()
        s_lower = s_clean.lower()
        for conn in banned_connectors:
            if s_lower.startswith(conn + " ") or s_lower.startswith(conn + ","):
                errors.append(f"Forbidden connector opener '{conn}': {s[:50]}")

    # 4. Contrastive negation check
    negations = []
    patterns = [r'\binstead of\b', r'\brather than\b', r'\bnot only\b', r'\bnot\s+[^,.!?]+\s*,?\s*but\b']
    for pat in patterns:
        m = re.findall(pat, full, re.IGNORECASE)
        negations.extend(m)
    if len(negations) > 1:
        errors.append(f"Too many contrastive negations ({len(negations)}): {negations}")

    # 5. Metadata length
    if len(title) > 60:
        errors.append(f"Title length {len(title)} > 60")
    if len(meta_title) > 60:
        errors.append(f"Meta title length {len(meta_title)} > 60")
    if len(meta_desc) > 155:
        errors.append(f"Meta desc length {len(meta_desc)} > 155")

    # 6. Single sentence paragraphs
    paras = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    single_paras = [p for p in paras if len([s for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]) == 1]
    if len(single_paras) > 1:
        errors.append(f"Too many single-sentence paragraphs ({len(single_paras)}): {single_paras}")

    print("Title length:", len(title))
    print("Meta title length:", len(meta_title))
    print("Meta desc length:", len(meta_desc))
    print("Single sentence paragraphs count:", len(single_paras))
    print("Contrastive negations count:", len(negations), negations)
    print("Word count:", len(re.findall(r'\b\w+\b', body)))

    if errors:
        print("\nERRORS:")
        for e in errors:
            print("-", e)
        return False
    else:
        print("\nALL AUTOMATED CHECKS PASSED PERFECTLY!")
        return True

if __name__ == "__main__":
    audit()
