import json
import re

title = "SeaRates Weekly Updates: Week 47, 2024"
meta_title = "SeaRates Platform Updates for Week 47, 2024"
meta_description = "Discover the latest SeaRates updates for Week 47, 2024, including tracking updates, new airline support, ship schedules, and LandRates features."

body_markdown = """SeaRates released several tool improvements and platform updates for Week 47, 2024.

## Tracking Tool Enhancements
On the web platform, SeaRates updated the Filter interface and introduced hover tooltips showing shipping line names on carrier logos. Direct data integration was also expanded with four ocean lines: Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL.

## Air Freight Tracking Updates
Tracking support now includes Azerbaijan Airlines and Air Arabia Abu Dhabi.

## Vessel Sailing Schedules
Schedules coverage was added for KambaraKisen, Culines, and Sinokor by Vessel, plus KambaraKisen by Port.

## API Parcel Tracking Logic
The API edition features enhanced autodetection logic to streamline tracking requests.

## Platform and Interface Upgrades
- Search Filter: Introduced a Button hover color setting to customize search button appearance.
- FAQ Sections: Added dedicated FAQ blocks across the Container Tracking, Distance & Time, and Load Calculator pages.
- LandRates.com: Published a Special Offers block on the LandRates.com homepage to help users compare land freight rates globally.

## Roadmap and Upcoming Releases
- Calendar tab inside the Tracking System
- Updated Route Planner API edition
- Freight Index 1.0 analytics release
- Mobile App Version 1.2 featuring the Request System
- Load Calculator Version 2.2 engine
- Booking System Version 1.1 upgrade
- Interactive Map platform"""

# Check em-dashes
all_text = f"{title}\n{meta_title}\n{meta_description}\n{body_markdown}"
em_dash_count = all_text.count("—") + all_text.count("–") + all_text.count("--")

# Check lengths
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# 6-gram overlap check against original
with open("/opt/hermes/profiles/archie/original_article_clean.txt") as f:
    orig_text = f.read()

def get_words(text):
    clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return clean.split()

def get_ngrams(words, n=6):
    return set([" ".join(words[i:i+n]) for i in range(len(words)-n+1)])

orig_words = get_words(orig_text)
rewrite_words = get_words(body_markdown)

orig_6grams = get_ngrams(orig_words, 6)
rewrite_6grams = get_ngrams(rewrite_words, 6)

overlap_6grams = orig_6grams.intersection(rewrite_6grams)

allowed_tokens = [
    "heung a shipping", "ignazio messina", "hoegh autoliners", "oocl",
    "azerbaijan airlines", "air arabia abu dhabi",
    "kambarakisen", "culines", "sinokor",
    "container tracking", "distance time", "load calculator",
    "tracking system", "route planner api", "freight index",
    "mobile app version", "request system", "booking system",
    "calendar tab", "landrates com", "button hover color", "search filter"
]

non_exempt_overlaps = []
for gram in overlap_6grams:
    if not any(tok in gram for tok in allowed_tokens):
        non_exempt_overlaps.append(gram)

results = {
    "em_dash_count": em_dash_count,
    "title_length": title_len,
    "meta_title_length": meta_title_len,
    "meta_description_length": meta_desc_len,
    "length_check_pass": (title_len <= 60 and meta_title_len <= 60 and meta_desc_len <= 155),
    "total_6gram_overlaps": len(overlap_6grams),
    "non_exempt_6gram_overlaps": len(non_exempt_overlaps),
    "non_exempt_examples": non_exempt_overlaps,
    "exempt_examples": list(overlap_6grams - set(non_exempt_overlaps))
}

print("=== PARAPHRASE VERIFICATION RESULTS ===")
print(json.dumps(results, indent=2))

if len(non_exempt_overlaps) == 0 and em_dash_count == 0 and results["length_check_pass"]:
    print("ALL CHECKS PASSED PERFECTLY!")
    final_verified = {
        "title": title,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "body_markdown": body_markdown
    }
    with open("/opt/hermes/profiles/archie/final_verified_article.json", "w") as f:
        json.dump(final_verified, f, indent=2)
