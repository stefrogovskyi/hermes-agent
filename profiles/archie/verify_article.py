import json
import re

title = "SeaRates Weekly Updates: Week 38, 2024"
meta_title = "SeaRates Week 38 Updates: Tracking & API Notes"
meta_description = "SeaRates Week 38 updates: air cargo tracking, container tracking, historical freight index API, vessel ship schedules, and Apple account login."

article_text = """# SeaRates Weekly Updates: Week 38, 2024

SeaRates released a series of updates in Week 38 of 2024 covering tracking integrations, API endpoints, and platform design.

Air cargo tracking now integrates directly with five additional carriers: Cathay Pacific Airways, British Airways, Astral Aviation, Bringer Air Cargo Taxi Aereo, and EVA Air. On the container side, tracking integrations were expanded for Orient Overseas Container Line (OOCL), Kuehne + Nagel (KN), and Volta Container Line.

API functionality received two targeted changes. The Freight Index now exposes historical indicative rates through both web and API channels. For proximity calculations, the distance & time API runs on updated logic to determine the closest location for every request.

Vessel ship schedules added tracking support for HR Lines and Great White Fleet, searchable by points, vessel, or port. Users navigating Logistics Explorer can now switch the tool interface to Spanish through new Spanish localization options.

Signing in is simpler with Apple account login and registration options. To finish the week's release, SeaRates updated the design and content on the About Us and Plans & Pricing pages."""

# 1. Em-dash check
full_content = f"{title}\n{meta_title}\n{meta_description}\n{article_text}"
em_dash_count = full_content.count("—") + full_content.count("--")

# 2. Length check
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# 3. N-gram check against original
with open('/opt/hermes/profiles/archie/original_article.txt', 'r', encoding='utf-8') as f:
    orig_raw = f.read()

def normalize_text(text):
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text.split() if w]

orig_words = normalize_text(orig_raw)
art_words = normalize_text(article_text)

orig_6grams = set()
for i in range(len(orig_words) - 5):
    orig_6grams.add(" ".join(orig_words[i:i+6]))

matches = []
for i in range(len(art_words) - 5):
    gram = " ".join(art_words[i:i+6])
    if gram in orig_6grams:
        matches.append(gram)

results = {
    "em_dash_count": em_dash_count,
    "title_length": f"{title_len} (max 60)",
    "meta_title_length": f"{meta_title_len} (max 60)",
    "meta_description_length": f"{meta_desc_len} (max 155)",
    "6gram_matches_count": len(matches),
    "matches": matches
}

print(json.dumps(results, indent=2))

# Save validated text
with open('/opt/hermes/profiles/archie/validated_article.json', 'w', encoding='utf-8') as f:
    json.dump({
        "title": title,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "body": article_text
    }, f, ensure_ascii=False, indent=2)
