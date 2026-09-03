import json, re

with open("output.json") as f:
    data = json.load(f)

title = data["title"]
meta_title = data["meta_title"]
meta_desc = data["meta_description"]
md = data["content_markdown"]
full = f"{title}\n{meta_title}\n{meta_desc}\n{md}"

print(f"Title length: {len(title)} (max 60)")
print(f"Meta title length: {len(meta_title)} (max 60)")
print(f"Meta desc length: {len(meta_desc)} (max 155)")

# Check rule 1: em-dashes
dashes = [c for c in full if c in ['—', '–'] or '--' in full]
print("Dashes found:", dashes)

# Check rule 2: AI clichés / slop
cliches = [
    "in today's world", "today's", "it's important to note", "delve into", "delving", "plays a vital role",
    "vital role", "crucial role", "pivotal", "it is not merely", "in conclusion", "ever-changing",
    "landscape", "testament", "tapestry", "beacon", "game-changer", "unravel", "navigate",
    "boasts", "furthermore", "moreover", "in summary", "overall", "unlocking", "fostering",
    "driving force", "paramount", "unprecedented" # check if unprecedented is from source or cliché
]
for c in cliches:
    matches = re.findall(r'\b' + re.escape(c) + r'\b', full, re.IGNORECASE)
    if matches:
        print(f"Cliché check: found '{c}': {matches}")

# Check rule 6: over-explaining connectors
connectors = ["that's why", "which is why", "this explains why", "because of this", "as a result", "consequently", "due to this"]
for conn in connectors:
    matches = re.findall(r'\b' + re.escape(conn) + r'\b', full, re.IGNORECASE)
    if matches:
        print(f"Connector check: found '{conn}': {matches}")

# Check rule 7: Contrastive negations ("X, not Y", "It isn't X, it's Y", "instead of", "rather than")
neg_words = ["instead of", "rather than", "not merely", "not only", "not X", "is not", "isn't", "aren't", "not"]
print("Instances of 'not':", len(re.findall(r'\bnot\b', full, re.IGNORECASE)))
print("Instances of 'instead of':", len(re.findall(r'\binstead of\b', full, re.IGNORECASE)))
print("Instances of 'rather than':", len(re.findall(r'\brather than\b', full, re.IGNORECASE)))

# Print all sentences containing 'not' or 'instead' or 'rather'
sentences = re.split(r'(?<=[.!?])\s+', full)
for s in sentences:
    if any(w in s.lower() for w in ["not", "instead", "rather"]):
        print("Sentence with neg/contrast:", s.strip())

# Check bullet lists
bullet_blocks = re.findall(r'(?:^[ \t]*[\*\-\+\d\.]+\s+.*\n?)+', md, re.MULTILINE)
print(f"Total list blocks: {len(bullet_blocks)}")
for i, block in enumerate(bullet_blocks):
    items = [line for line in block.strip().split('\n') if line.strip()]
    print(f"List {i+1} item count: {len(items)}")

