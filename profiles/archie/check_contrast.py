import re
import test_full

text = f"{test_full.title}\n{test_full.meta_title}\n{test_full.meta_desc}\n{test_full.body}"

contrast_phrases = [
    "instead of", "rather than", "not only", "not but", "not"
]

for cp in contrast_phrases:
    matches = list(re.finditer(r'\b' + re.escape(cp) + r'\b', text, re.IGNORECASE))
    print(f"Phrase '{cp}': found {len(matches)} times")
    for m in matches:
        start = max(0, m.start() - 30)
        end = min(len(text), m.end() + 30)
        print("  Context:", text[start:end].replace('\n', ' '))
