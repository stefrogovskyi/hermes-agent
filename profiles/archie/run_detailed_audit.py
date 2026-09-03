import re, json

orig_text = """We are grateful for your ongoing assistance with SeaRates. We place a high value on service enhancement and are thrilled to introduce new features that will improve your experience.
Explore our previous updates to get the most up-to-date insights.
What’s new for week 40:
Air Cargo Tracking updates:
We have enhanced our work with providers, including Cathay Pacific Airways, Air Canada, Delta Air Lines, Air India, and FedEx Express.
Tracking System enhancements:
We have enhanced our work with leasing companies and providers, including Shipco Transport, SETH Shipping, and Vanguard Logistics.
Ship Schedules improvements:
We are glad to announce that we have added support for Dong Young, Culines, and Sinokor for ‘by Port’.
Geocoding API enhancements:
We have implemented a scoring system for Autocomplete that allows you to find the locations you choose most often at the top of the list
Other updates:
We have improved the logic of determining the nearest ports when entering the City type of location in the Request a Quote form, as well as updated the Contact Us form.
Finally, we have updated the design and content for the SeaRates Affiliate Program and Find Freight Routes pages, as well as for the Homepage on AirRates.com
Announcements:
New features to the Air Cargo Tracking Web Version
Geocoding API / Autocomplete service Version 0.8
New Version of Route Planner API
Freight Index 1.0
Mobile App Version 1.2 with Request System feature
Load Calculator Version 2.2
Booking System Version 1.1
Rail Tracking API
Rail Tracking Web on LandRates.com
Map platform
Unified Tracking System WEB"""

rewrite_text = """Title: SeaRates Platform Updates: Week 40 Developments in Freight Tracking and Geocoding
Meta Title: SeaRates Week 40 Updates: Carrier Tracking & Geocoding
Meta Description: SeaRates Week 40 updates cover expanded carrier tracking, Geocoding API v0.8 scoring, Ship Schedules additions, and mobile app version 1.2 features.

Body:
## Expanded Carrier Tracking Across Air and Sea Networks

Air cargo tracking software capabilities and air cargo tracking API workflows now feature enhanced integration with major international airlines, including Cathay Pacific Airways, Air Canada, Delta Air Lines, Air India, and FedEx Express. On the container and consolidation side, the tracking system has expanded operational support across leasing companies and logistics providers, specifically Shipco Transport, SETH Shipping, and Vanguard Logistics. For ocean carrier integration within Ship Schedules, search by port functionality now supports Dong Young, Culines, and Sinokor. These additions extend tracking coverage across regional and global trade lanes.

## Geocoding API Scoring and Location Routing Enhancements

Logistics geocoding autocomplete receives a functional update in Geocoding API version 0.8. A location scoring algorithm now prioritizes frequently selected hubs, placing most-used origin and destination points at the top of autocomplete queries. Within the Request a Quote workflow, city inputs now benefit from refined spatial logic that identifies nearest commercial ports with higher accuracy. The platform Contact Us form has also been updated to streamline user inquiries.

## Interface Redesigns Across SeaRates and AirRates Web Pages

Visual design and content revisions have rolled out across key web properties within the digital supply chain platform. The SeaRates Affiliate Program page and the Find Freight Routes tool feature revised layouts to clarify partnership structures and route lookup pathways. AirRates.com has updated its primary homepage interface to reflect current service capabilities.

## Release Versions and Platform Deployments

Several platform services received updates and new version deployments during this release cycle. Web users can access the updated Air Cargo Tracking Web Version alongside the Unified Tracking System WEB and the updated Map platform. Development updates include Geocoding API / Autocomplete service Version 0.8, the New Version of Route Planner API, Freight Index 1.0, Booking System Version 1.1, and Load Calculator Version 2.2. Mobile logistics workflows now run on Mobile App Version 1.2, which integrates the Request System feature. Surface freight tracking capabilities extend through the Rail Tracking API and Rail Tracking Web on LandRates.com."""

def tokenize(text):
    # tokenize into words, ignoring punctuation for n-grams
    return re.findall(r'\b\w+\b', text)

orig_tokens = tokenize(orig_text)
rewrite_tokens = tokenize(rewrite_text)

print(f"Orig word count: {len(orig_tokens)}, Rewrite word count: {len(rewrite_tokens)}")

# --- LAYER (A): 6-gram overlap ---
print("\n--- LAYER (A): 6-GRAM OVERLAP CHECK ---")

proper_nouns_terms = {
    'cathay', 'pacific', 'airways', 'air', 'canada', 'delta', 'lines', 'india', 'fedex', 'express',
    'shipco', 'transport', 'seth', 'shipping', 'vanguard', 'logistics', 'dong', 'young', 'culines', 'sinokor',
    'searates', 'airrates', 'com', 'landrates', 'geocoding', 'api', 'autocomplete', 'version', '0', '8', '1', '2',
    '2', '2', '1', '1', '1', '0'
}

def get_ngrams(tokens, n=6):
    ngrams = {}
    for i in range(len(tokens) - n + 1):
        gram = tuple(t.lower() for t in tokens[i:i+n])
        gram_str = " ".join(tokens[i:i+n])
        ngrams[gram] = gram_str
    return ngrams

orig_6grams = get_ngrams(orig_tokens, 6)
rewrite_6grams = get_ngrams(rewrite_tokens, 6)

overlap_6grams = []
for gram, orig_str in orig_6grams.items():
    if gram in rewrite_6grams:
        # Check if it consists purely of proper nouns/carrier names
        non_prop = [w for w in gram if w not in proper_nouns_terms]
        overlap_6grams.append((orig_str, rewrite_6grams[gram], non_prop))

print(f"Total 6-gram overlaps found: {len(overlap_6grams)}")
for o in overlap_6grams:
    print(f"  Orig: '{o[0]}' | Rewrite: '{o[1]}' | Non-proper words: {o[2]}")

# Check 5-grams and 7-grams as well for completeness
orig_7grams = get_ngrams(orig_tokens, 7)
rewrite_7grams = get_ngrams(rewrite_tokens, 7)
overlap_7grams = [rewrite_7grams[g] for g in orig_7grams if g in rewrite_7grams]
print(f"Total 7-gram overlaps found: {len(overlap_7grams)}")

# --- LAYER (B): Vocabulary AI Markers ---
print("\n--- LAYER (B): VOCABULARY AI MARKERS ---")
dashes = re.findall(r'—|--|–', rewrite_text)
print(f"Em-dashes/en-dashes/double-hyphens count: {len(dashes)} ({dashes})")

cliches_list = [
    "delve", "seamless", "seamlessly", "crucial", "testament", "landscape", "beacon", "pivot",
    "game-changer", "pivotal", "elevate", "cutting-edge", "fostering", "tapestry", "realm",
    "harness", "empower", "unlock", "in today's world", "in today's fast-paced world",
    "it is worth noting", "vital role", "crucial role", "unraveling", "spearheading",
    "unlocking", "game changer", "vibrant", "revolutionize", "streamline"
]

found_cliches = []
for c in cliches_list:
    matches = re.findall(r'\b' + re.escape(c) + r'\b', rewrite_text, re.IGNORECASE)
    if matches:
        found_cliches.append((c, len(matches)))

print(f"AI Clichés found: {found_cliches}")

# --- LAYER (C): Structural & Rhetorical Tics ---
print("\n--- LAYER (C): STRUCTURAL & RHETORICAL TICS ---")

headers = re.findall(r'^#+\s*(.*)$', rewrite_text, re.MULTILINE)
print(f"Subheadings found ({len(headers)}): {headers}")

# Explicit connectors as sentence starters
explicit_connectors = [
    "Furthermore", "Moreover", "In addition", "Consequently", "Additionally",
    "However", "Therefore", "That's why", "Which is why", "As a result",
    "Hence", "Thus", "Because of this", "Finally", "First", "Second", "Third"
]

found_connectors = []
for line in rewrite_text.split('\n'):
    sents = re.split(r'(?<=[.!?])\s+', line)
    for s in sents:
        for conn in explicit_connectors:
            if re.match(r'^' + re.escape(conn) + r'[\s,.]', s.strip(), re.IGNORECASE):
                found_connectors.append((conn, s.strip()))

print(f"Explicit connectors as sentence starters count: {len(found_connectors)}: {found_connectors}")

# Contrastive negations
cn_patterns = [
    r'\binstead of\b',
    r'\brather than\b',
    r'\bnot [^,.!?\n]+,\s*but\b',
    r'\bnot only\b.*?\bbut\b',
    r'\bit isn\'t\b',
    r'\bit\'s not\b'
]
cn_matches = []
for pat in cn_patterns:
    for m in re.finditer(pat, rewrite_text, re.IGNORECASE):
        cn_matches.append(m.group(0))

print(f"Contrastive negations count: {len(cn_matches)}: {cn_matches}")

# Aphoristic short sentences
short_sents = []
for line in rewrite_text.split('\n'):
    if line.startswith('#') or line.startswith('Title:') or line.startswith('Meta'):
        continue
    sents = re.split(r'(?<=[.!?])\s+', line)
    for s in sents:
        s_clean = s.strip()
        words = re.findall(r'\b\w+\b', s_clean)
        if 1 <= len(words) <= 5 and s_clean:
            short_sents.append(s_clean)

print(f"Short sentences (1-5 words) count: {len(short_sents)}: {short_sents}")

# Parallel twin-sentences
all_sentences = []
for line in rewrite_text.split('\n'):
    if line.startswith('#') or line.startswith('Title:') or line.startswith('Meta') or not line.strip():
        continue
    sents = re.split(r'(?<=[.!?])\s+', line)
    for s in sents:
        if s.strip():
            all_sentences.append(s.strip())

parallel_twins = []
for i in range(len(all_sentences)-1):
    w1 = [w.lower() for w in re.findall(r'\b\w+\b', all_sentences[i])]
    w2 = [w.lower() for w in re.findall(r'\b\w+\b', all_sentences[i+1])]
    if len(w1) >= 2 and len(w2) >= 2 and w1[:2] == w2[:2]:
        parallel_twins.append((all_sentences[i], all_sentences[i+1]))

print(f"Parallel twin-sentences count: {len(parallel_twins)}: {parallel_twins}")

# --- LAYER (D): Factual Accuracy (Rule 11) ---
print("\n--- LAYER (D): FACTUAL ACCURACY & ENTITY TRACE ---")

# List entities from Original
# Air Cargo: Cathay Pacific Airways, Air Canada, Delta Air Lines, Air India, FedEx Express
# Tracking System: Shipco Transport, SETH Shipping, Vanguard Logistics
# Ship Schedules: Dong Young, Culines, Sinokor ('by Port')
# Geocoding API: scoring system for Autocomplete (find locations chosen most often at top of list)
# Other updates: nearest ports logic for City location in Request a Quote form; Contact Us form updated.
# Affiliate/Find Freight Routes/AirRates Homepage: design and content updated
# Announcements / Versions:
# - Air Cargo Tracking Web Version (New features)
# - Geocoding API / Autocomplete service Version 0.8
# - New Version of Route Planner API
# - Freight Index 1.0
# - Mobile App Version 1.2 with Request System feature
# - Load Calculator Version 2.2
# - Booking System Version 1.1
# - Rail Tracking API
# - Rail Tracking Web on LandRates.com
# - Map platform
# - Unified Tracking System WEB

print("Script completed.")
