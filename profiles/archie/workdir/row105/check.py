import re, json, sys

base = "/opt/hermes/profiles/archie/workdir/row105/"
rw = open(base+"final_rewrite.txt").read()
orig = open(base+"original.txt").read()

title = "B2B Clients Expect Amazon-Level Tracking. Here's the Fix"
meta_title = "Why White Label Shipment Tracking Wins B2B Clients"
meta_desc = "B2B buyer expectations now mirror Amazon. See how an embeddable tracking widget with white label shipment tracking keeps clients on your site."

# em-dash check
def emdash(s): return s.count("\u2014") + s.count("--")
print("em-dash title:", emdash(title))
print("em-dash meta_title:", emdash(meta_title))
print("em-dash meta_desc:", emdash(meta_desc))
print("em-dash body:", emdash(rw))

# lengths
print("len title:", len(title), "meta_title:", len(meta_title), "meta_desc:", len(meta_desc))

# contrastive negation count in body
contr = re.findall(r"\bnot the carrier's\b|\binstead of\b|\bisn't\b|\baren't\b.*?,|\b, not \b", rw)
print("contrastive hits:", re.findall(r"[^.]*(?:\bnot\b|instead of)[^.]*\.", rw))

# n-gram overlap (6-grams)
def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return t.split()
EXEMPT = {"white label","white-label","tracking widget","sea rates","searates"}
rw_n = norm(re.sub(r"#+ ", "", rw))
or_n = norm(orig)
rw_grams = set(tuple(rw_n[i:i+6]) for i in range(len(rw_n)-5))
or_grams = set(tuple(or_n[i:i+6]) for i in range(len(or_n)-5))
inter = rw_grams & or_grams
print("\n6-gram overlaps (%d):" % len(inter))
for g in sorted(inter): print("  ", " ".join(g))
