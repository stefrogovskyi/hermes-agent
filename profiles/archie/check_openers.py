import re
import test_full

sentences = re.split(r'(?<=[.!?])\s+', test_full.body)
print(f"Total sentences: {len(sentences)}")
for i, s in enumerate(sentences):
    s_clean = s.strip().lstrip('#').strip()
    if not s_clean:
        continue
    first_word = s_clean.split()[0] if s_clean.split() else ""
    first_two = " ".join(s_clean.split()[:2]) if len(s_clean.split()) >= 2 else first_word
    print(f"{i+1:02d}: {first_two:<25} | {s_clean[:60]}...")
