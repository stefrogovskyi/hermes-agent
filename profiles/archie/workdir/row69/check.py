import re

base = "/opt/hermes/profiles/archie/workdir/row69"
with open(f"{base}/final_rewrite.txt") as f:
    final = f.read()
with open(f"{base}/original_article.txt") as f:
    orig = f.read()

emdash_count = final.count('\u2014') + final.count('--')
print("EM-DASH COUNT (final, body+meta+title):", emdash_count)

lines = final.split('\n')
title_line = [l for l in lines if l.startswith('TITLE:')][0]
meta_title_line = [l for l in lines if l.startswith('META_TITLE:')][0]
meta_desc_line = [l for l in lines if l.startswith('META_DESCRIPTION:')][0]
title = title_line.split('TITLE:',1)[1].strip()
meta_title = meta_title_line.split('META_TITLE:',1)[1].strip()
meta_desc = meta_desc_line.split('META_DESCRIPTION:',1)[1].strip()

print("TITLE:", repr(title), "len:", len(title))
print("META_TITLE:", repr(meta_title), "len:", len(meta_title))
print("META_DESC:", repr(meta_desc), "len:", len(meta_desc))

print("em-dash in title:", title.count('\u2014')+title.count('--'))
print("em-dash in meta_title:", meta_title.count('\u2014')+meta_title.count('--'))
print("em-dash in meta_desc:", meta_desc.count('\u2014')+meta_desc.count('--'))

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def ngrams(text, n=6):
    words = text.split()
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

norm_final = normalize(final)
norm_orig = normalize(orig)

final_6grams = ngrams(norm_final, 6)
orig_6grams = ngrams(norm_orig, 6)

overlap = final_6grams & orig_6grams
print()
print("6-GRAM OVERLAP COUNT:", len(overlap))
for g in sorted(overlap):
    print(" ", ' '.join(g))

body_lower = final.lower()
neg_patterns = re.findall(r'\b\w+, not \w+', body_lower)
instead_of = body_lower.count('instead of')
print()
print("instead of count:", instead_of)
print("', not ' patterns:", neg_patterns)

# check "it isn't X, it's Y" pattern
isnt_pattern = re.findall(r"isn'?t \w+.{0,40}it'?s \w+", body_lower)
print("isn't X it's Y patterns:", isnt_pattern)
