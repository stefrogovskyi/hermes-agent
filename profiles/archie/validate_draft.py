import re
import sys

def check_draft(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.strip().split('\n')
    
    title = ""
    meta_title = ""
    meta_desc = ""
    body = ""

    for line in lines:
        if line.startswith("Title:"):
            title = line.replace("Title:", "").strip()
        elif line.startswith("Meta-Title:"):
            meta_title = line.replace("Meta-Title:", "").strip()
        elif line.startswith("Meta-Description:"):
            meta_desc = line.replace("Meta-Description:", "").strip()

    body = text

    print("=== CHARACTER COUNT CHECKS ===")
    print(f"Title ({len(title)} chars, max 60): {title}")
    assert len(title) <= 60, "Title exceeds 60 chars!"
    print(f"Meta-Title ({len(meta_title)} chars, max 60): {meta_title}")
    assert len(meta_title) <= 60, "Meta-Title exceeds 60 chars!"
    print(f"Meta-Description ({len(meta_desc)} chars, max 155): {meta_desc}")
    assert len(meta_desc) <= 155, "Meta-Description exceeds 155 chars!"

    print("\n=== RULE 1: EM-DASH CHECK ===")
    if '—' in text or '--' in text:
        print("FAIL: Found em-dash or '--'")
        for i, line in enumerate(lines, 1):
            if '—' in line or '--' in line:
                print(f"  Line {i}: {line}")
    else:
        print("PASS: Zero em-dashes or '--'")

    print("\n=== RULE 2: BANNED WORDS/CLICHES CHECK ===")
    banned = [
        "delve into", "testament to", "crucial role", "in today's world", 
        "it is worth noting", "vital aspect", "seamlessly", "furthermore", 
        "moreover", "in conclusion", "unwavering commitment", "game-changer", 
        "game changer", "dive deep", "dive", "tapestry", "landscape", "beacon", 
        "unlock", "elevate", "harness", "foster", "paramount", "realm", 
        "digital age", "at your fingertips", "gamechanger", "vibrant", "revolutionize"
    ]
    found_banned = []
    text_lower = text.lower()
    for b in banned:
        if b in text_lower:
            found_banned.append(b)
    if found_banned:
        print(f"FAIL: Found banned words: {found_banned}")
    else:
        print("PASS: No AI clichés found.")

    print("\n=== RULE 7: CONTRASTIVE NEGATION CHECK ===")
    # Look for contrastive patterns like "not A, but B", "X, not Y", "instead of", "rather than"
    contrast_patterns = [
        r'\binstead of\b', r'\brather than\b', r'\bnot\b'
    ]
    matches = []
    for line_num, line in enumerate(lines, 1):
        for pat in contrast_patterns:
            for m in re.finditer(pat, line, re.IGNORECASE):
                # context
                start = max(0, m.start() - 20)
                end = min(len(line), m.end() + 20)
                matches.append((line_num, line[start:end]))
    print(f"Total potential contrastive negation candidates found: {len(matches)}")
    for l_num, ctx in matches:
        print(f"  Line {l_num}: ...{ctx}...")

    print("\n=== KEYWORD CHECK ===")
    keywords = [
        "air freight tracking app",
        "real-time air cargo monitoring",
        "air waybill (AWB) tracking",
        "iOS and Android logistics app"
    ]
    for kw in keywords:
        if kw.lower() in text_lower:
            print(f"PASS: Found keyword '{kw}'")
        else:
            print(f"FAIL: Missing keyword '{kw}'")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_draft(sys.argv[1])
