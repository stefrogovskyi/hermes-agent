import json
import re
import string

def clean_text(text):
    # Remove markdown headers and formatting for n-gram checks
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text

def get_words(text):
    text = text.lower()
    for c in string.punctuation + '“”‘’—–-':
        text = text.replace(c, ' ')
    return [w for w in text.split() if w]

def main():
    with open('/opt/hermes/profiles/archie/draft_rewrite.json') as f:
        data = json.load(f)

    title = data['title']
    meta_title = data['meta_title']
    meta_description = data['meta_description']
    body = data['body']

    full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

    # Check 1: Em-dashes
    em_dashes = ['—', '–', '--']
    em_dash_counts = {}
    for em in em_dashes:
        cnt = full_text.count(em)
        if cnt > 0:
            em_dash_counts[em] = cnt

    print("=== CHECK 1: EM-DASHES ===")
    print("Em-dash counts:", em_dash_counts)

    # Check 2: Lengths
    print("\n=== CHECK 2: LENGTHS ===")
    print(f"Title ({len(title)} chars, max 60): {title}")
    print(f"Meta Title ({len(meta_title)} chars, max 60): {meta_title}")
    print(f"Meta Description ({len(meta_description)} chars, max 155): {meta_description}")

    # Check 3: N-gram Overlaps
    with open('/opt/hermes/profiles/archie/original_article.txt') as f:
        orig_text = f.read()

    orig_words = get_words(orig_text)
    rewrite_words = get_words(full_text)

    n = 6
    orig_ngrams = set()
    for i in range(len(orig_words) - n + 1):
        orig_ngrams.add(tuple(orig_words[i:i+n]))

    overlap_ngrams = []
    for i in range(len(rewrite_words) - n + 1):
        ng = tuple(rewrite_words[i:i+n])
        if ng in orig_ngrams:
            overlap_ngrams.append(' '.join(ng))

    # Allow list of trade terms / proper names
    trade_proper_words = {
        'searates', 'mediterranean', 'shipping', 'company', 'msc', 'wan', 'hai', 'zim',
        'mitsui', 'm', 'o', 's', 'k', 'lines', 'mol', 'marguisa', 'volta', 'container',
        'line', 'crowley', 'maritime', 't', 's', 'acl', 'grimaldi', 'turkon', 'cosco',
        'specialized', 'aercaribe', 'peru', 'air', 'cote', 'd', 'ivoire', 'akasa',
        'vensecar', 'internacional', 'aliedair', 'alliedair', 'fedex', 'express', 'pil',
        'points', 'port', 'vessel', 'geocoding', 'api', '18', '000', 'seaports', 'world',
        'sea', 'ports', 'app', 'demurrage', 'storage', 'calculator', 'virtual', 'office',
        'bookings', 'load', 'logistics', 'map', 'route', 'planner', 'freight', 'index',
        '1', '0', 'mobile', '1', '2', '2', '2', 'request', 'system', 'faqs'
    }

    filtered_overlaps = []
    for match in overlap_ngrams:
        match_words = match.split()
        non_trade = [w for w in match_words if w not in trade_proper_words]
        if len(non_trade) > 0:
            filtered_overlaps.append(match)

    print("\n=== CHECK 3: 6-GRAM OVERLAPS ===")
    print("Total 6-gram matches found:", len(overlap_ngrams))
    print("Filtered non-trade matches:", len(filtered_overlaps))
    for m in filtered_overlaps:
        print("  - Overlap:", m)

    # Check 4: Clichés & connectors
    cliches = ["delve", "game-changer", "testament", "seamless", "crucial aspect", "in today's world", "it is not just", "furthermore", "moreover", "that's why", "which is why"]
    found_cliches = []
    for cl in cliches:
        if cl in full_text.lower():
            found_cliches.append(cl)

    print("\n=== CHECK 4: CLICHES & CONNECTORS ===")
    print("Found clichés/connectors:", found_cliches)

if __name__ == "__main__":
    main()
