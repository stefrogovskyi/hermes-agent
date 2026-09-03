import re

original = """SeaRates Updates - Week 47, 2024

We appreciate your continued support of SeaRates and are excited to present new products that will better meet your needs. Improving our services remains a key priority for us.

What's new for week 47:

Tracking System improvements:
For the web version, we have improved the design of the tool by adding tooltips with the names of shipping lines on the logo and updating the Filter. We've also enhanced our collaboration with providers, including Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL.

Air Cargo Tracking enhancements:
We've added support for Azerbaijan Airlines and Air Arabia Abu Dhabi. Discover the list of supported airlines here.

Ship Schedules updates:
We have added support for KambaraKisen, Culines, and Sinokor by Vessel, and KambaraKisen by Port.

Parcel Tracking improvements:
For the API version, we have enhanced autodetect logic for streamlined requesting.

Other updates:
- Search Filter: For the Search Filter, we have added a new customization option: the Button hover color for color adjusting the search button.
- FAQ sections: For the Container Tracking, Distance & Time, and Load Calculator pages, we have added FAQ sections.
- LandRates.com: Added the Special Offers section to the main page on LandRates.com to find and compare land freight rates across the globe easily.

Announcements:
- Calendar tab in the Tracking System tool
- New Version of Route Planner API
- Freight Index 1.0
- Mobile App Version 1.2 with Request System feature
- Load Calculator Version 2.2
- Booking System Version 1.1
- Map platform"""

draft = """Title: SeaRates Week 47 Updates: Tracking, Schedules & APIs
Meta-Title: SeaRates Week 47 Updates | Logistics & Tracking Tools
Meta-Description: Discover SeaRates Week 47 updates: container tracking, air cargo coverage, ship schedules, API enhancements, and global land freight rate search.

Body:
## Ocean and Air Tracking Upgrades

Managing freight across global routes requires clear, immediate details. In the web version of the Tracking System, new logo tooltips display carrier names on hover, paired with an updated Filter to sort active shipments quickly. Direct data collaboration has also expanded across four ocean carriers: Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL. Teams using supply chain visibility tools gain immediate clarity on active legs.

Air transport coverage broadens as well. Air cargo tracking integrations now include Azerbaijan Airlines and Air Arabia Abu Dhabi, pulling direct flight status updates into the main dashboard.

## Expanded Vessel Schedules and API Logic

Planning sea routes depends on reliable departure and arrival timelines. Vessel sailing schedules automation now covers KambaraKisen, Culines, and Sinokor by Vessel, along with KambaraKisen by Port.

On the developer side, Parcel Tracking for the API version features upgraded autodetect logic. The system identifies tracking number formats automatically, streamlining data retrieval for teams running a real-time container tracking API interface.

## Interface Fine-Tuning and Land Freight Options

Small workflow adjustments improve daily site navigation and rates discovery:

* Search Filter customization now includes a button hover color option for tailored visual styling.
* Container Tracking, Distance & Time, and Load Calculator pages now feature dedicated FAQ sections.
* LandRates.com added a Special Offers section to its main page, giving shippers a direct tool for land freight rate search and comparison worldwide.

## Upcoming Platform Features and Releases

Development continues across several core modules, with upcoming releases including:

* Calendar tab in the Tracking System tool
* New Version of Route Planner API
* Freight Index 1.0
* Mobile App Version 1.2 with Request System feature
* Load Calculator Version 2.2
* Booking System Version 1.1
* Map platform"""

# Tokenize into words
orig_tokens = re.findall(r'\b\w+\b', original.lower())
draft_tokens = re.findall(r'\b\w+\b', draft.lower())

# Find all consecutive sequences of length >= 6
def get_sequences(tokens, min_len=6):
    seqs = {}
    for l in range(min_len, len(tokens)+1):
        for i in range(len(tokens)-l+1):
            s = tuple(tokens[i:i+l])
            seqs[s] = (i, l)
    return seqs

orig_seqs = get_sequences(orig_tokens, 6)

matches = []
for i in range(len(draft_tokens)):
    for l in range(15, 5, -1):
        if i + l <= len(draft_tokens):
            sub = tuple(draft_tokens[i:i+l])
            if sub in orig_seqs:
                matches.append(" ".join(sub))

# Deduplicate overlaps by keeping longest
def filter_subsequences(matches):
    long_matches = set()
    for m in sorted(matches, key=len, reverse=True):
        if not any(m in existing for existing in long_matches):
            long_matches.add(m)
    return list(long_matches)

unique_matches = filter_subsequences(matches)
print("Unique matching 6+ word phrases:")
for m in unique_matches:
    print(f"- '{m}'")

