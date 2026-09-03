import re
from audit_script import original, candidate

# Let's split into words keeping punctuation attached or simple word splitting
def get_words(text):
    return text.split()

cand_words = candidate.split()
orig_text = original

# Let's check contiguous sequences of length >= 6 words from candidate
found_overlaps = []

for i in range(len(cand_words)):
    for length in range(6, 25):
        if i + length > len(cand_words):
            break
        phrase = " ".join(cand_words[i:i+length])
        # clean quote/punctuation slightly if needed, or exact match
        # Let's clean punctuation at boundaries or check verbatim in text
        # normalized string search:
        norm_phrase = re.sub(r'\s+', ' ', phrase).strip()
        # strip trailing/leading punctuation for search?
        # Actually let's do word-level matching ignoring case and punctuation differences, but printing exact original and candidate quotes.
        pass

# Let's write a cleaner finder:
cand_tokens = [w.strip(".,;:()[]'\"") for w in candidate.split()]
orig_tokens = [w.strip(".,;:()[]'\"") for w in original.split()]

# filter empty
cand_tokens_clean = [w for w in cand_tokens if w]
orig_tokens_clean = [w for w in orig_tokens if w]

cand_lower = [w.lower() for w in cand_tokens_clean]
orig_lower = [w.lower() for w in orig_tokens_clean]

N_c = len(cand_lower)
N_o = len(orig_lower)

seen = set()
for i in range(N_c):
    for j in range(N_o):
        k = 0
        while (i + k < N_c) and (j + k < N_o) and (cand_lower[i+k] == orig_lower[j+k]):
            k += 1
        if k >= 6:
            c_phrase = " ".join(cand_tokens_clean[i:i+k])
            o_phrase = " ".join(orig_tokens_clean[j:j+k])
            found_overlaps.append((k, i, j, c_phrase, o_phrase))

# Keep maximal spans
maximal = []
for item in sorted(found_overlaps, key=lambda x: x[0], reverse=True):
    k, i, j, c_p, o_p = item
    # check if subsumed
    subsumed = False
    for m in maximal:
        mk, mi, mj, mc, mo = m
        if mi <= i and (mi + mk) >= (i + k):
            subsumed = True
            break
    if not subsumed:
        maximal.append(item)

for m in sorted(maximal, key=lambda x: x[1]):
    print(f"Len {m[0]}: Candidate: '{m[3]}'\n        Original:  '{m[4]}'\n")

