import json
import re

# Final text JSON
data = {
  "title": "SeaRates Product Update: Week 44, 2024",
  "meta_title": "SeaRates Updates Week 44, 2024: API and App Enhancements",
  "meta_description": "SeaRates Week 44 release notes covering container tracking API updates, air freight integration, parcel autodetect tracking, and Android app updates.",
  "body_markdown": """Here is what shipped across SeaRates APIs, ocean carrier integrations, air tracking, and mobile apps during Week 44 of 2024.

## Tracking & Fee APIs

Parameters for Storage, Demurrage, and Detention fees were added to API responses, along with the `cache_expires` parameter.

For predictive ETA logistics within the Tracking History API, we updated the underlying response processing logic to refine estimated arrival calculations.

For parcel tracking, we improved the Autodetect logic for the parcel tracking API.

## Carrier Integrations

Ocean freight integrations were updated for 11 shipping lines and logistics partners:
* Vanguard Logistics
* Hyundai Merchant Marine (HMM)
* COSCO
* Pacific International Lines (PIL)
* Sealead Shipping
* Gold Star Line
* Yusen Logistics
* Ocean Network Express (ONE)
* Hellmann Worldwide Logistics
* DHL Global Forwarding
* Nirint Shipping

Air freight tracking API support grew to 435 total airlines with the addition of Air Arabia Maroc and Challenge Airlines Malta.

We also enhanced integrations with 11 air cargo providers: Amerijet International, Binter Canarias, United Airlines, Hong Kong Air Cargo, Turkish Airlines, Asiana Airlines, American Airlines, LOT Polish Airlines, Mahan Air, Air France, and DHL Aviation.

## Mobile Application

Android users can now sign in directly inside the SeaRates Mobile Application. The update removes the redirect to the SeaRates website and adds single sign-on via Google and Apple accounts. Separately, the Profile and Settings views received layout adjustments.

## New Landing Pages and Tools

- A new Freight Carrier API page is live. You can also reach it through the Sea Lines Explorer API on the Find a Tool page.
- We published a dedicated landing page for the Demurrage & Storage Calculator API.
- Interface updates were applied to the Find a Tool page, the Cargo Wizard web experience, and the LandRates.com homepage."""
}

# 1. Em-dash check
full_text = f"{data['title']}\n{data['meta_title']}\n{data['meta_description']}\n{data['body_markdown']}"
em_dash_count = full_text.count("—") + full_text.count("--")
print(f"1. Em-dash count: {em_dash_count}")

# 2. Length check
title_len = len(data['title'])
meta_title_len = len(data['meta_title'])
meta_desc_len = len(data['meta_description'])
print(f"2. Title length: {title_len} (max 60)")
print(f"   Meta Title length: {meta_title_len} (max 60)")
print(f"   Meta Description length: {meta_desc_len} (max 155)")

# 3. N-gram overlap check against original
with open('original_source.txt') as f:
    orig_text = f.read()

def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(zip(*[words[i:] for i in range(n)]))

orig_ngrams = get_ngrams(orig_text, 6)
rewrite_ngrams = get_ngrams(full_text, 6)
common_ngrams = orig_ngrams.intersection(rewrite_ngrams)

print(f"3. 6-gram overlap count: {len(common_ngrams)}")
for gram in common_ngrams:
    gram_str = " ".join(gram)
    print("   Overlap 6-gram:", gram_str)

# 4. Contrastive negation check
negations = re.findall(r'\b(not|isn\'t|aren\'t|doesn\'t|don\'t|instead of)\b', full_text, re.IGNORECASE)
print(f"4. Negation words found: {negations}")

with open('final_clean_rewrite.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
