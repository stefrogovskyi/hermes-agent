import json
import re

with open("output.json") as f:
    data = json.load(f)

title = data["title"]
meta_title = data["meta_title"]
meta_desc = data["meta_description"]
body = data["body"]
full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== LENGTH CHECKS ===")
print(f"Title ({len(title)} chars): {title}")
print(f"Meta Title ({len(meta_title)} chars): {meta_title}")
print(f"Meta Description ({len(meta_desc)} chars): {meta_desc}")

assert len(title) <= 60, "Title > 60"
assert len(meta_title) <= 60, "Meta Title > 60"
assert len(meta_desc) <= 155, "Meta Desc > 155"

print("\n=== RULE 1: DASHES ===")
dashes = ['—', '–', '--']
for d in dashes:
    if d in full_text:
        print(f"VIOLATION: Found dash '{d}'")

print("\n=== RULE 3: BANNED HEADINGS & META ===")
banned_headings = ["introduction", "conclusion", "overview", "summary"]
for line in body.split('\n'):
    if line.startswith('#'):
        heading_text = line.lstrip('#').strip().lower()
        for bh in banned_headings:
            if bh == heading_text:
                print(f"VIOLATION: Banned heading '{heading_text}'")

banned_meta = ["in this article", "this post will explore", "we will look at"]
for bm in banned_meta:
    if bm in full_text.lower():
        print(f"VIOLATION: Banned meta-announcement '{bm}'")

print("\n=== RULE 4: BANNED SENTENCE STARTERS ===")
banned_starters = [
    "furthermore", "moreover", "in addition", "however", "therefore",
    "that's why", "which is why", "consequently", "additionally",
    "as a result", "hence", "thus", "because of this"
]

# Extract all sentences
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', full_text) if s.strip()]

for s in sentences:
    clean_s = re.sub(r'^[#*\-\s\d\.]+', '', s).strip()
    low_s = clean_s.lower()
    for starter in banned_starters:
        if low_s.startswith(starter + ",") or low_s.startswith(starter + " "):
            print(f"VIOLATION: Starter '{starter}' in sentence: '{clean_s}'")

print("\n=== RULE 5: CONTRASTIVE NEGATIONS ===")
# List of potential contrastive negation patterns
neg_patterns = [
    r'\binstead of\b',
    r'\brather than\b',
    r'\bnot only\b',
    r'\bnot just\b',
    r',\s*not\s+'
]
neg_count = 0
found_negs = []
for pat in neg_patterns:
    matches = re.findall(pat, full_text, re.IGNORECASE)
    if matches:
        neg_count += len(matches)
        found_negs.extend(matches)

print(f"Contrastive negations count: {neg_count}, found: {found_negs}")

print("\n=== RULE 7: TWIN SENTENCE STARTERS ===")
prev_two = None
for s in sentences:
    words = re.findall(r'\b[A-Za-z0-9]+\b', s)
    if len(words) >= 2:
        two = (words[0].lower(), words[1].lower())
        if two == prev_two:
            print(f"VIOLATION: Twin sentence starter '{two}': '{s}'")
        prev_two = two
    else:
        prev_two = None

print("\n=== RULE 9: BANNED AI WORDS ===")
banned_ai = [
    "delve", "seamless", "seamlessly", "unlock", "unlocking", "game-changer",
    "testament", "tapestry", "pivotal", "elevate", "cutting-edge", "fostering",
    "vibrant", "landscape", "realm", "harness", "empower", "in today's fast-paced world",
    "it is crucial to note"
]
for w in banned_ai:
    if re.search(rf"\b{re.escape(w)}\b", full_text, re.IGNORECASE):
        print(f"VIOLATION: Banned AI word/phrase '{w}' found!")

print("\n=== KEYWORDS CHECK ===")
kw1 = "agentic AI workflows & predictive analytics"
kw2 = "no-code AI workflow automation & Zapier integrations"
print(f"KW1 '{kw1}': {kw1 in body}")
print(f"KW2 '{kw2}': {kw2 in body}")

print("\nCheck complete!")
