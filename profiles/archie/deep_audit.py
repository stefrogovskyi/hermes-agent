import re
from collections import Counter

orig = """The SeaRates team thanks you for being loyal and supportive. We are always improving our platform to give you the best service possible. We’re happy to share our new updates with you and we believe they will enhance your experience.

To keep up with our news, please look at our previous improvements.

What’s new for week 34:

We are glad to introduce Load Calculator Version 2 of the web tool. Try out the improved logic for loading your pipe and boxed cargo into containers and trucks.

We have also added the ability to view the step-by-step loading of your cargo by downloading a PDF file and opening it in a browser.

Air Cargo Tracking updates: We are pleased to present that we have added support for 5 airlines, including Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, and Wizz Air.

We have enhanced our work with providers, including Batik Air, Qatar Airways, Delta Airlines, and SouthWest Airlines.

Tracking System improvements: For the Tracking History API, we have improved the container number query process, which allows you to get results for all shipments with BL and BK numbers.

We have enhanced how we work with providers, including Reel Shipping FZCO, Sinokor, Hapag-Lloyd, Kuehne + Nagel (KN), Swire Shipping, Westwood Shipping Lines, Hai Hua Shipping (HASCO), Jin Jiang Shipping (SHJJ), CMA CGM, Evergreen, DHL Global Forwarding, Dachser, Emirates Shipping Line, and Meratus Line.

Freight Index updates: We've enhanced the index calculation for your transportation routes and improved the display of historical data when requesting.

SeaRates Mobile App enhancements: We have updated the authorization system for iOS users by adding the ability to log in to the application without going to the SeaRates website, as well as the ability to log in via your Google account.

Other updates:

For the Request an IT Quote form, we added Mobile Application Web integration, Enterprise Web integration, Parcel Tracking Web access, Parcel Tracking Web integration, and Parcel Tracking API to provide you with the ability to quickly request a customized price quote for your chosen SeaRates IT tool.

Finally, we have created Parcel Tracking API and Distance & Time pages, as well as updated content and design on the IMO Classes page.

Announcements:
Geocoding API / Autocomplete service Version 0.8
New Version of Route Planner API
‘Transport’ tab in the Logistics Map tool
Freight Index 1.0
Mobile App Version 1.2 with Request System feature
Load Calculator Version 2.2
Booking System Version 1.1
Parcel Tracking API
Rail Tracking API
Map platform"""

rewrite = """Title: SeaRates Week 34 2024 Updates: Container Loading, Tracking APIs, and Carrier Upgrades
Meta Title: SeaRates Week 34 Updates: Tools & API Upgrades
Meta Description: Explore SeaRates Week 34 updates, featuring Load Calculator V2, air cargo integrations, tracking history API enhancements, and mobile login fixes.

Body:
The Load Calculator Version 2 web tool features refined container loading optimization logic for packing pipe and boxed cargo into containers and trucks. Users can download a step-by-step loading sequence as a PDF file and open it in a browser.

Air cargo tracking integration expands with direct support for five airlines: Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, and Wizz Air. Carrier data processing was refined for Batik Air, Qatar Airways, Delta Airlines, and SouthWest Airlines.

For ocean freight, the Tracking History API query mechanism for container numbers was overhauled to pull complete records across shipments booked under BL and BK numbers. Operational integrations saw enhancements across Reel Shipping FZCO, Sinokor, Hapag-Lloyd, Kuehne + Nagel (KN), Swire Shipping, Westwood Shipping Lines, Hai Hua Shipping (HASCO), Jin Jiang Shipping (SHJJ), CMA CGM, Evergreen, DHL Global Forwarding, Dachser, Emirates Shipping Line, and Meratus Line.

Engineers improved the freight index route calculation and historical data display. For teams using iOS mobile logistics access, the SeaRates Mobile App authorization system now allows direct in-app login without redirecting to the SeaRates website, along with Google account authentication.

The Request an IT Quote form now includes options for Mobile Application Web integration, Enterprise Web integration, Parcel Tracking Web access, Parcel Tracking Web integration, and the parcel tracking API. Dedicated pages were introduced for the Parcel Tracking API and Distance & Time, alongside updated content and design for the IMO Classes page.

Upcoming developments include Geocoding API / Autocomplete service Version 0.8, a new Version of Route Planner API, the 'Transport' tab in the Logistics Map tool, Freight Index 1.0, Mobile App Version 1.2 with Request System feature, Load Calculator Version 2.2, Booking System Version 1.1, Parcel Tracking API, Rail Tracking API, and the Map platform."""

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

orig_tokens = tokenize(orig)
rewrite_tokens = tokenize(rewrite)

print("=== DETAILED LAYER A: N-GRAM OVERLAP & PLAGIARISM METRICS ===")
for n in range(1, 11):
    orig_ngrams = [tuple(orig_tokens[i:i+n]) for i in range(len(orig_tokens)-n+1)]
    rewrite_ngrams = [tuple(rewrite_tokens[i:i+n]) for i in range(len(rewrite_tokens)-n+1)]
    
    orig_set = set(orig_ngrams)
    rewrite_set = set(rewrite_ngrams)
    common = orig_set.intersection(rewrite_set)
    
    # calculate percentage of rewrite n-grams that are verbatim from orig
    matches_in_rewrite = sum(1 for ng in rewrite_ngrams if ng in orig_set)
    pct = (matches_in_rewrite / len(rewrite_ngrams)) * 100 if rewrite_ngrams else 0
    
    print(f"{n}-grams | Total in Rewrite: {len(rewrite_ngrams)} | Verbatim from Orig: {matches_in_rewrite} ({pct:.2f}%) | Unique Common: {len(common)}")

print("\n=== VERBATIM LONG CLAUSES / STRINGS (4+ WORDS) ===")
# Find longest matching sequences
from difflib import SequenceMatcher
matcher = SequenceMatcher(None, orig_tokens, rewrite_tokens)
blocks = matcher.get_matching_blocks()
print("Longest contiguous token matches between Original and Rewrite:")
for b in sorted(blocks, key=lambda x: x.size, reverse=True):
    if b.size >= 4:
        matched_str = " ".join(orig_tokens[b.a:b.a+b.size])
        print(f"  - Length {b.size} words: \"{matched_str}\"")

print("\n=== LAYER B: VOCABULARY & STYLE MARKERS ===")
# Check specific AI / passive / formal stylistic patterns
passive_voice = re.findall(r'\b(?:was|were|has been|have been|is|are|saw)\s+\w+ed\b', rewrite, re.IGNORECASE)
print(f"Passive/Passive-leaning constructions: {passive_voice}")

cliches_to_check = [
    "delve", "testament", "realm", "landscape", "pivotal", "boasts", "beacon",
    "tapestry", "game-changer", "seamless", "seamlessly", "paramount", "fostering",
    "foster", "elevate", "elevating", "underscore", "underscores", "spearhead",
    "overhauled", "refined", "expands", "saw enhancements", "introduced", "options",
    "dedicated", "upcoming developments include"
]
print("Vocabulary markers check:")
for c in cliches_to_check:
    cnt = len(re.findall(r'\b' + re.escape(c) + r'\b', rewrite, re.IGNORECASE))
    if cnt > 0:
        print(f"  - '{c}': {cnt}")

print("\n=== LAYER C: STRUCTURAL & RHETORICAL TICS ===")
body_text = rewrite.split("Body:\n")[1] if "Body:\n" in rewrite else rewrite
paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]
print(f"Body paragraph count: {len(paragraphs)}")
for idx, p in enumerate(paragraphs):
    s_list = re.split(r'(?<=[.!?])\s+', p)
    print(f"Paragraph {idx+1}: {len(s_list)} sentences, {len(p.split())} words")

print("\nSentence openers in Body:")
for idx, p in enumerate(paragraphs):
    s_list = re.split(r'(?<=[.!?])\s+', p)
    for s_idx, s in enumerate(s_list):
        first_few = " ".join(s.split()[:3])
        print(f"  P{idx+1}S{s_idx+1}: {first_few}...")

print("\n=== LAYER D: ENTITY AND FACTUAL MAPPING ===")
# List of entities in original
airlines_orig = ["Cayman Airways", "FITS Aviation", "Iran Air", "SAC South American Airways", "Wizz Air"]
airlines_enhanced_orig = ["Batik Air", "Qatar Airways", "Delta Airlines", "SouthWest Airlines"]
providers_orig = [
    "Reel Shipping FZCO", "Sinokor", "Hapag-Lloyd", "Kuehne + Nagel (KN)", "Swire Shipping",
    "Westwood Shipping Lines", "Hai Hua Shipping (HASCO)", "Jin Jiang Shipping (SHJJ)",
    "CMA CGM", "Evergreen", "DHL Global Forwarding", "Dachser", "Emirates Shipping Line", "Meratus Line"
]
it_quote_options_orig = [
    "Mobile Application Web integration", "Enterprise Web integration",
    "Parcel Tracking Web access", "Parcel Tracking Web integration", "Parcel Tracking API"
]
announcements_orig = [
    "Geocoding API / Autocomplete service Version 0.8",
    "New Version of Route Planner API",
    "‘Transport’ tab in the Logistics Map tool",
    "Freight Index 1.0",
    "Mobile App Version 1.2 with Request System feature",
    "Load Calculator Version 2.2",
    "Booking System Version 1.1",
    "Parcel Tracking API",
    "Rail Tracking API",
    "Map platform"
]

print("Checking presence of all entities in rewrite:")
for group_name, group in [
    ("Added Airlines", airlines_orig),
    ("Enhanced Airlines", airlines_enhanced_orig),
    ("Tracking Providers", providers_orig),
    ("IT Quote Options", it_quote_options_orig),
    ("Announcements", announcements_orig)
]:
    print(f"\n--- {group_name} ---")
    for item in group:
        # Simple string search normalized
        clean_item = item.replace("‘", "'").replace("’", "'")
        present = clean_item.lower() in rewrite.lower()
        print(f"  [{'X' if present else ' '}] {item}")

