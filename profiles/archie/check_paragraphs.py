import json

with open("output.json") as f:
    data = json.load(f)

body = data["body_markdown"]

paragraphs = body.split("\n\n")

for i, p in enumerate(paragraphs):
    p_strip = p.strip()
    if not p_strip:
        continue
    if p_strip.startswith("#") or p_strip.startswith("-"):
        continue
    lines = p_strip.split("\n")
    if any(line.strip().startswith("-") for line in lines):
        print(f"P{i} contains list items.")
        continue
    # Count sentences
    import re
    sentences = re.split(r'(?<=[.!?])\s+', p_strip)
    print(f"P{i} ({len(sentences)} sentences): {p_strip[:60]}...")
