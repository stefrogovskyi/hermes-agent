import json
import re

with open('/opt/hermes/profiles/archie/final_output.json', 'r') as f:
    data = json.load(f)

body = data.get('body', '')
paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]

all_sentences = []
for p_idx, p in enumerate(paragraphs):
    s_list = re.split(r'(?<=[.!?])\s+', p)
    for s_idx, s in enumerate(s_list):
        all_sentences.append((p_idx+1, s_idx+1, len(s_list), s))

print("=== ALL PARAGRAPH CLOSING SENTENCES (Aphoristic / Summary Check) ===")
for p_idx, s_idx, total, s in all_sentences:
    if s_idx == total:
        print(f"P{p_idx} (end): {s}")

print("\n=== PARALLEL STRUCTURE / SYNTAX PATTERN CHECK ===")
# Check sentence structures across closing sentences or consecutive sentences
for p_idx, s_idx, total, s in all_sentences:
    if s_idx == total:
        # Check if closing sentence ends with -ing participle or generic aphorism
        if re.search(r'(ing|essential for|ensuring|aligns|lowers|provides|allows)\b.*$', s, re.IGNORECASE):
            print(f"P{p_idx} end pattern: {s}")

