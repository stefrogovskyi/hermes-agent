import json
import re

# Final text from subagent 3
title = "SeaRates Weekly Updates: Week 47, 2024"
meta_title = "SeaRates Platform Updates for Week 47, 2024"
meta_description = "Discover the latest SeaRates updates for Week 47, 2024, including tracking updates, new airline support, ship schedules, and LandRates features."
body_markdown = """SeaRates released several tool improvements and platform updates for Week 47, 2024.

## Tracking System Improvements
For the web version, SeaRates updated the Filter and added tooltips displaying shipping line names on carrier logos. Collaboration was also enhanced for Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL.

## Air Cargo Tracking Enhancements
Support was added for Azerbaijan Airlines and Air Arabia Abu Dhabi.

## Ship Schedules Updates
Support was added for KambaraKisen, Culines, and Sinokor by Vessel, alongside KambaraKisen by Port.

## Parcel Tracking Improvements
For the API version, autodetect logic was enhanced for requesting.

## Other Updates
- Search Filter: Added a customization option for Button hover color to adjust the search button color.
- FAQ Sections: Added FAQ sections to the Container Tracking, Distance & Time, and Load Calculator pages.
- LandRates.com: Added a Special Offers section to the main page on LandRates.com to compare global land freight rates.

## Announcements
- Calendar tab in the Tracking System tool
- New Version of Route Planner API
- Freight Index 1.0
- Mobile App Version 1.2 with Request System feature
- Load Calculator Version 2.2
- Booking System Version 1.1
- Map platform"""

# 1. Em-dash / En-dash / Double hyphen check
all_text = f"{title}\n{meta_title}\n{meta_description}\n{body_markdown}"
em_dash_count = all_text.count("—") + all_text.count("–") + all_text.count("--")

# 2. Length check
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# 3. 6-gram overlap check against original
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

# List of allowed proper nouns / logistics terms in overlaps
allowed_tokens = [
    "heung a shipping", "ignazio messina", "hoegh autoliners", "oocl",
    "azerbaijan airlines", "air arabia abu dhabi",
    "kambarakisen", "culines", "sinokor",
    "container tracking", "distance time", "load calculator",
    "tracking system tool", "route planner api", "freight index",
    "mobile app version", "request system feature", "booking system",
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

print("=== VERIFICATION RESULTS ===")
print(json.dumps(results, indent=2))

# Save verified article json
verified_article = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body_markdown": body_markdown
}
with open("/opt/hermes/profiles/archie/final_article_verified.json", "w") as f:
    json.dump(verified_article, f, indent=2)

with open("/opt/hermes/profiles/archie/check_results.json", "w") as f:
    json.dump(results, f, indent=2)
