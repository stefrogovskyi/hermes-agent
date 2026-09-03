import re, itertools

def norm_tokens(text):
    text = text.replace('\n', ' ')
    tokens = re.findall(r"[A-Za-z0-9']+", text)
    return [t.lower() for t in tokens]

orig = open('original.txt').read()
rew = open('rewrite.txt').read()

ot = norm_tokens(orig)
rt = norm_tokens(rew)

N = 6
orig_ngrams = {}
for i in range(len(ot)-N+1):
    gram = tuple(ot[i:i+N])
    orig_ngrams.setdefault(gram, []).append(i)

matches = []
for i in range(len(rt)-N+1):
    gram = tuple(rt[i:i+N])
    if gram in orig_ngrams:
        matches.append((i, gram))

# merge consecutive overlapping matches into runs
matches.sort()
runs = []
cur_start = None
cur_end = None
prev_i = None
for i, gram in matches:
    if prev_i is not None and i == prev_i + 1:
        cur_end = i
    else:
        if cur_start is not None:
            runs.append((cur_start, cur_end))
        cur_start = i
        cur_end = i
    prev_i = i
if cur_start is not None:
    runs.append((cur_start, cur_end))

print(f"Total 6-gram matches: {len(matches)}")
print(f"Number of distinct runs: {len(runs)}")
for s, e in runs:
    length = e - s + N
    phrase = ' '.join(rt[s:e+N])
    print(f"Run length {length} tokens: '{phrase}'")
