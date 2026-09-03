import re
from test_overlap import tokenize, orig_tokens, rewrite_tokens, orig_words_raw, rewrite_words_raw

for N in [5, 4]:
    matches = []
    for i in range(len(rewrite_tokens) - N + 1):
        gram = rewrite_tokens[i:i+N]
        for j in range(len(orig_tokens) - N + 1):
            if orig_tokens[j:j+N] == gram:
                match_str = " ".join(rewrite_words_raw[i:i+N])
                matches.append(match_str)
    print(f"\n{N}-gram matches (total {len(matches)}):")
    for m in set(matches):
        print(f"  - '{m}'")

