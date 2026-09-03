import re

orig_text = """TITLE: SeaRates Updates - Week 36, 2024

We at SeaRates are grateful for your steadfast help and encouragement. Our commitment to improving our service remains strong, and we are thrilled to introduce several new features designed to simplify your experience.

For the latest information, be sure to review our earlier updates.

What’s new for week 36:

Air Cargo Tracking improvements: We have enhanced our work with providers, including Shenzhen Airlines, Air India, FedEx Express, Lufthansa Cargo, Air France, ITA Airways, Czech Airlines, Challenge Airlines, Gulf Air, Egyptair, FITS Aviation, and UPS Air Cargos.

Tracking System updates: For API, we have improved the determination logic of container size and type and added a description of the ‘size_type’ parameter for the container into the documentation. Get the updated API V. 3 documentation on our Developer Portal.

For the web version, we have implemented limits for tracking bulk shipments uploaded in Excel. You can simultaneously track your shipments through the tool on SeaRates.com and by uploading a list of Excel files simultaneously within your subscription plan.

Finally, we have enhanced our work with providers, including Independent Container Line, Tarros, FESCO, Sea Hawk Lines (SHAL), Pacific International Lines (PIL), Eimskip, Hapag-Lloyd, Maersk, SITC Container Lines, Evergreen, and CK Line.

Ship Schedules enhancements: We are pleased to present that we have added support for the Evergreen for schedules searching by Port.

Also, we have enhanced how we work with providers, including Cordelia, Econship, Golden Fortune Shipping, Gold Star Line, Kambara Kisen, Laurel Navigation, Pacifica Shipping, Tanto, Vanguard Logistics, and W.E.C.

Load Calculator improvements: We have updated the web version of the tool, adding the "Disable stacking" checkbox on the "Stuffing settings" section for all cargo types (boxes, big bags, sacks, barrels, rolls, etc.). This way you can adjust online stuffing by mentioning the requirement to place cargo in only one layer if nothing can be placed on top.

You can also change the number of allowed layers or set a weight or height limit, entering the appropriate values in the “Mass” or “Height” fields.

Distance & Time updates: For the API, we have improved the determination logic for the nearest seaport.

Other updates:

For the Request a Quote and Quick Request forms, we have added additional transportation types for creating Land FTL requests.

Finally, we have created a new landing page Vendors - Freight Forwarders, and have made an update on content and design for the SeaRates Vendors page.

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
Rail Tracking Web on LandRates.com
Map platform
Unified Tracking System WEB"""

with open("/opt/hermes/profiles/archie/final_checked_rewrite.txt", "r", encoding="utf-8") as f:
    final_text = f.read()

# Parse Title, Meta-Title, Meta-Description, Body
title_match = re.search(r"^Title:\s*(.*)$", final_text, re.MULTILINE)
meta_title_match = re.search(r"^Meta-Title:\s*(.*)$", final_text, re.MULTILINE)
meta_desc_match = re.search(r"^Meta-Description:\s*(.*)$", final_text, re.MULTILINE)

title = title_match.group(1).strip() if title_match else ""
meta_title = meta_title_match.group(1).strip() if meta_title_match else ""
meta_desc = meta_desc_match.group(1).strip() if meta_desc_match else ""

# Extract body
lines = final_text.splitlines()
body_lines = [l for l in lines if not re.match(r"^(Title|Meta-Title|Meta-Description):", l)]
body = "\n".join(body_lines).strip()

print("--- PROGRAMMATIC VERIFICATION ---")

# 1. Em-dash check
em_dashes = ['—', '--', '–']
found_em_dashes = 0
for d in em_dashes:
    cnt = final_text.count(d)
    found_em_dashes += cnt
    if cnt > 0:
        print(f"ERROR: Found {cnt} occurrences of '{d}'")

print(f"1. Em-dash count: {found_em_dashes} (PASS)" if found_em_dashes == 0 else "1. Em-dash check: FAILED")

# 2. Length check
print(f"2. Lengths:")
print(f"   - Title: {len(title)} chars (limit 60) -> {'PASS' if len(title) <= 60 else 'FAIL'}")
print(f"   - Meta-Title: {len(meta_title)} chars (limit 60) -> {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
print(f"   - Meta-Description: {len(meta_desc)} chars (limit 155) -> {'PASS' if len(meta_desc) <= 155 else 'FAIL'}")

# 3. N-gram Overlap Check (6-grams)
def normalize(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    return text.split()

words_orig = normalize(orig_text)
words_final = normalize(body)

ngrams_orig = set()
for i in range(len(words_orig) - 5):
    ngrams_orig.add(" ".join(words_orig[i:i+6]))

found_ngrams = []
for i in range(len(words_final) - 5):
    ngram = " ".join(words_final[i:i+6])
    if ngram in ngrams_orig:
        found_ngrams.append(ngram)

exempt_terms = [
    "airlines", "india", "fedex", "express", "lufthansa", "cargo", "france", "airways", "czech", "gulf", "egyptair",
    "fits", "aviation", "ups", "carrier", "container", "line", "tarros", "fesco", "hawk", "lines", "shal", "pacific",
    "pil", "eimskip", "hapaglloyd", "maersk", "sitc", "evergreen", "ck", "cordelia", "econship", "golden", "fortune",
    "shipping", "gold", "star", "kambara", "kisen", "laurel", "navigation", "pacifica", "tanto", "vanguard", "logistics",
    "geocoding", "autocomplete", "route", "planner", "transport", "logistics", "freight", "index", "mobile", "app",
    "request", "booking", "parcel", "rail", "landratescom", "platform", "unified"
]

non_exempt_ngrams = []
for ng in found_ngrams:
    # Check if all words in the 6-gram are proper nouns / carrier names / version titles
    words_in_ng = ng.split()
    if not all(w in exempt_terms or w in ["08", "10", "11", "12", "22", "36", "2024", "v3", "api", "web", "in", "the", "on", "of", "with", "feature", "system", "tool", "and"] for w in words_in_ng):
        non_exempt_ngrams.append(ng)

print(f"3. Total 6-gram overlaps: {len(found_ngrams)}")
print(f"   - Non-exempt prose 6-gram overlaps: {len(non_exempt_ngrams)}")
for ng in non_exempt_ngrams:
    print(f"     * '{ng}'")
