import re

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

# Split into words keeping position
def get_words_with_pos(text):
    words = []
    for m in re.finditer(r'\b[\w\.]+\b', text):
        words.append((m.group(0), m.start(), m.end()))
    return words

orig_w = get_words_with_pos(orig_text)
rewrite_w = get_words_with_pos(rewrite_text)

print("--- SEARCHING FOR ALL EXACT 6+ WORD SEQUENCE MATCHES ---")

# Let's find longest common substrings in terms of word sequences
matches = []
for i in range(len(orig_w)):
    for j in range(len(rewrite_w)):
        k = 0
        while (i + k < len(orig_w)) and (j + k < len(rewrite_w)) and (orig_w[i+k][0].lower() == rewrite_w[j+k][0].lower()):
            k += 1
        if k >= 6:
            orig_phrase = orig_text[orig_w[i][1]:orig_w[i+k-1][2]]
            rewrite_phrase = rewrite_text[rewrite_w[j][1]:rewrite_w[j+k-1][2]]
            matches.append((k, orig_phrase, rewrite_phrase))

# Deduplicate overlapping sub-matches
dedup = []
# sort by length desc
matches.sort(key=lambda x: x[0], reverse=True)
for m in matches:
    # check if m is sub-phrase of any already in dedup
    is_sub = False
    for d in dedup:
        if m[1] in d[1]:
            is_sub = True
            break
    if not is_sub:
        dedup.append(m)

print(f"Unique maximal word matches (length >= 6): {len(dedup)}")
for length, op, rp in dedup:
    print(f"\nMatch Length: {length} words")
    print(f"  Orig:    '{op}'")
    print(f"  Rewrite: '{rp}'")

