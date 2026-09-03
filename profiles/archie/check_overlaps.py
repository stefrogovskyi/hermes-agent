import audit_pass

with open('/opt/hermes/profiles/archie/draft2.txt') as f:
    rew = f.read()

src_words = audit_pass.clean_words(audit_pass.source_text)
rew_words = audit_pass.clean_words(rew)
src_6grams = set(audit_pass.get_ngrams(src_words, 6))
rew_6grams = audit_pass.get_ngrams(rew_words, 6)
overlaps = [ ' '.join(g) for g in rew_6grams if g in src_6grams ]

print('Overlaps count:', len(overlaps))
for o in set(overlaps):
    print(' - Overlap:', o)
