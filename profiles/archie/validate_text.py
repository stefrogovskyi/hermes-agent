import re

def check_rules(text, title, desc):
    print("=== VALIDATION REPORT ===")
    
    # 1. Dash check
    dashes = ["—", "–", "--"]
    found_dashes = [d for d in dashes if d in text or d in title or d in desc]
    if found_dashes:
        print(f"FAIL Rule 1: Found dashes {found_dashes}")
    else:
        print("PASS Rule 1: No forbidden dashes found.")
        
    # 2. AI Clichés
    banned_phrases = [
        "crucial role", "in today's world", "delve", "important to note",
        "dive into", "seamlessly", "game-changer", "it's not just",
        "in conclusion", "vital role", "uninterrupted supply chains",
        "end-to-end visibility", "testament to", "foster", "landscape", "pivotal"
    ]
    found_cliches = [p for p in banned_phrases if p.lower() in text.lower() or p.lower() in title.lower() or p.lower() in desc.lower()]
    if found_cliches:
        print(f"FAIL Rule 2: Found AI clichés {found_cliches}")
    else:
        print("PASS Rule 2: No AI clichés found.")

    # 5. Connectors at start of sentences
    connectors = ["Furthermore", "Moreover", "In addition", "Additionally", "On the other hand", "Therefore", "As a result", "Consequently"]
    found_conn = []
    for line in text.split('\n'):
        for c in connectors:
            if re.match(r'^\s*' + re.escape(c) + r'[\s,]', line, re.IGNORECASE):
                found_conn.append((c, line))
    if found_conn:
        print(f"FAIL Rule 5: Sentence starting connectors found: {found_conn}")
    else:
        print("PASS Rule 5: No explicit connectors at start of sentences.")

    # Meta lengths
    print(f"Meta Title length: {len(title)} (MAX 60)")
    if len(title) > 60:
        print("FAIL: Title exceeds 60 chars")
    else:
        print("PASS: Title length valid")

    print(f"Meta Desc length: {len(desc)} (MAX 155)")
    if len(desc) > 155:
        print("FAIL: Desc exceeds 155 chars")
    else:
        print("PASS: Desc length valid")

if __name__ == "__main__":
    print("Validator ready.")
