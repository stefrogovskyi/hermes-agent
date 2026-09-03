import re

def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9%/ ]+", " ", t)
    return [w for w in t.split() if w]

orig = open("orig.txt").read()
rew = open("rew.txt").read()
O, R = norm(orig), norm(rew)

o_ngrams = {}
for n in range(6, 15):
    for i in range(len(O)-n+1):
        o_ngrams.setdefault(tuple(O[i:i+n]), True)

# find maximal overlaps
found = set()
i = 0
while i < len(R):
    best = None
    for n in range(14, 5, -1):
        if i+n <= len(R) and tuple(R[i:i+n]) in o_ngrams:
            best = n
            break
    if best:
        found.add(" ".join(R[i:i+best]))
        i += best
    else:
        i += 1

for f in sorted(found, key=len, reverse=True):
    print(len(f.split()), "|", f)
print("TOTAL:", len(found))
