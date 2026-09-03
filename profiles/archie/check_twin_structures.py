import json, re

with open("output.json") as f:
    data = json.load(f)

text = data["body_markdown"]

# Clean headings and bullets for sentence parsing
lines = text.split("\n")
clean_lines = []
for line in lines:
    line_s = line.strip()
    if line_s.startswith("#"):
        continue
    if line_s.startswith("- "):
        line_s = line_s[2:].strip()
    clean_lines.append(line_s)

clean_text = " ".join([l for l in clean_lines if l])
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean_text) if s.strip()]

print(f"Total sentences to analyze: {len(sentences)}\n")

for i in range(len(sentences) - 1):
    s1 = sentences[i]
    s2 = sentences[i+1]
    
    words1 = s1.split()
    words2 = s2.split()
    
    # Check POS / First word similarity / Length similarity
    first_word1 = words1[0].lower() if words1 else ""
    first_word2 = words2[0].lower() if words2 else ""
    
    # Structural check: do they start with the same word or phrase?
    w1_prefix = " ".join(words1[:2]).lower() if len(words1) >= 2 else ""
    w2_prefix = " ".join(words2[:2]).lower() if len(words2) >= 2 else ""
    
    print(f"Pair {i+1}-{i+2}:")
    print(f"  S1 ({len(words1)} w): {s1}")
    print(f"  S2 ({len(words2)} w): {s2}")
    if first_word1 == first_word2 or w1_prefix == w2_prefix:
        print(f"  *** WARNING: Similar start '{first_word1}' vs '{first_word2}' ***")
    print()
