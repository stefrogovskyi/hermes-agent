import re
from check_ngrams import orig_words, rewrite_words

matches = []
for n in range(4, 6):
    for i in range(len(rewrite_words) - n + 1):
        sub = rewrite_words[i:i+n]
        for j in range(len(orig_words) - n + 1):
            if orig_words[j:j+n] == sub:
                matches.append((n, " ".join(sub)))

print("Matches of length 4-5:")
for n, phrase in set(matches):
    print(f"Length {n}: '{phrase}'")
