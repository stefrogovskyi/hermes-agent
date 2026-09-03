import re

original_text = """Title: VDS 2024: Valencia Conference Summary
The VDS 2024 took place in Valencia, Spain, over two days on October 23 and 24 at the City of Arts and Sciences. There were shipping and logistics professionals from around the globe. The venue accommodated up to 12,000 guests, 600+ speakers, 700+ investors, and 2,500+ start-ups over two days.
The SeaRates team attended important conferences and several private meetings, getting a unique opportunity to present the functionality of the global marketplace for digital logistics to companies worldwide.
Representatives from the IT industry, material handling, packaging, warehousing, and other sectors shared insights on digital logistics management and supply chain technology.
SeaRates serves over 1 million users worldwide with digital logistics tools and shipment tracking. Contact: sales@searates.com."""

title = "SeaRates Spotlights Digital Freight Tools at VDS 2024"
meta_title = "SeaRates at VDS 2024: Digital Logistics Innovations"
meta_desc = "SeaRates presented its web freight platform at VDS 2024 in Valencia, connecting with global logistics leaders and expanding shipment tracking tools."

body = """## International Freight Gathering in Valencia

The Valencia Digital Summit 2024 brought international shipping and freight specialists to Spain's City of Arts and Sciences on October 23 and 24. The venue offered space for up to 12,000 attendees alongside more than 600 speakers, 700 venture investors, and 2,500 emerging tech firms across the two-day schedule, creating an expansive environment for trade discussions.

## Cross-Industry Engagement and Strategic Discussions

Delegates specializing in enterprise IT, industrial material handling, protective packaging, warehouse management, and related freight disciplines shared strategic perspectives on supply chain technology. Active throughout conference panels and non-public business sessions, the SeaRates team demonstrated how its web-based freight platform helps international businesses streamline cargo operations.

## Global Digital Solutions for Freight Operations

SeaRates supports more than one million clients globally through tailored digital logistics software and real-time cargo tracking capabilities. Organizations looking to enhance their shipping workflows can reach the team directly at sales@searates.com."""

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

def get_ngrams(words, n):
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

orig_words = re.findall(r'\b\w+\b', original_text.lower())
draft_words = re.findall(r'\b\w+\b', full_text.lower())

for n in [5, 6, 7, 8]:
    orig_ng = get_ngrams(orig_words, n)
    draft_ng = get_ngrams(draft_words, n)
    common = orig_ng.intersection(draft_ng)
    print(f"Matching {n}-grams count: {len(common)}")
    for c in common:
        print(f"  {n}-gram: {' '.join(c)}")
