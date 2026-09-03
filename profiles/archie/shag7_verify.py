import re

title = "SeaRates Platform Updates: Week 38, 2025 Release"
meta_title = "SeaRates Platform Updates: Week 38, 2025 Release"
meta_description = "Explore SeaRates Week 38 updates, including container tracking API tweaks, air cargo updates, new landing pages, and AI chat body streaming."

content = """We updated our services and tools during Week 38 of 2025.

Here is what shipped this week.

## Tracking & Data Updates

Our container tracking API now uses optimized logic to fetch vessel data and identify container size and type from shipping line descriptions.

We improved collaboration with ten ocean shipping lines:
* Hapag-Lloyd
* Kintetsu World Express
* Kanway Line
* Neptune Pacific Direct Line (NPDL)
* CMA CGM
* Nippon Express
* Samudera Shipping Line
* Wan Hai
* Arkas
* Maersk

For the air tracking API, we updated support across seven carriers:
* Japan Airlines
* Turkish Airlines
* Air Canada
* Shipco Transport
* Qantas
* Etihad Cargo
* China Cargo Airlines

For ship schedules, we updated collaboration with four shipping lines by Points:
* FESCO
* Wallenius Wilhelmsen
* Linea Peninsular
* Pacifica Shipping

## Tools, AI & Infrastructure

SeaRates AI chat now uses body streaming for streamed responses directly in the chat view.

We included Rate Management System options alongside the Vessel Tracking API in our Request IT Quote form.

Three new landing pages are live:
* Route Planner Pricing
* SeaRates AI API
* Tracking Campaign

## Announcements

Upcoming updates on our radar:
* Unified Tracking System
* Warehouse tab on the Logistics Map
* Load Calculator Web 3.0 (new design and features)
* Terminal Tracking API improvements
* Map Platform
* Road Tracking Web
* Geocoding API connection for Logistics Explorer
* Carrier Directory
* Inbox tools tied to Logistics Explorer, Bookings, and system notifications"""

original = """Our team deeply appreciates your tremendous support. At SeaRates, our main focus is on upgrading and improving our services and tools, providing you with high-quality, innovative, and personalized logistics.

Explore our earlier improvements, and let's dive into new updates from Week 38.

## What’s new for week 38:

- Container Tracking updates: For the API, we've optimized the logic for obtaining vessel data and determining the type and size of the container based on the shipping line's description.

- Also, we have improved our collaboration with shipping lines, namely Hapag-Lloyd, Kintetsu World Express, Kanway Line, Neptune Pacific Direct Line (NPDL), CMA CGM, Nippon Express, Samudera Shipping Line, Wan Hai, Arkas, and Maersk.

- Air Tracking enhancements: For the API, we have updated our support of airlines, including Japan Airlines, Turkish Airlines, Air Canada, Shipco Transport, Qantas, Etihad Cargo, and China Cargo Airlines.

- Ship Schedules improvements: We have improved collaboration with shipping lines, including FESCO, Wallenius Wilhelmsen, Linea Peninsular, and Pacifica Shipping by Points.

Other updates:

- For the SeaRates AI, we have implemented body stream for the literal display of responses in the chat.

- Moreover, we have added Rate Management System and Vessel Tracking API into the Request IT Quote form.

- Finally, we have created Route Planner Pricing, SeaRates AI API, and Tracking Campaign landing pages.

Announcements:

- Unified Tracking System

- Logistics Map ‘Warehouse’ tab

- Load Calculator Web 3.0 (new design and features)

- Terminal Tracking API improvements

- Map Platform

- Road Tracking Web

- Geocoding API integrated with Logistics Explorer

- Carrier Directory

- Inbox integration with Logistics Explorer, Bookings, and Notifications"""

# 1. Em-dash count
all_text = f"{title}\n{meta_title}\n{meta_description}\n{content}"
em_dashes = all_text.count("—") + all_text.count("--")

# 2. Lengths
t_len = len(title)
mt_len = len(meta_title)
md_len = len(meta_description)

# 3. N-gram overlaps
def get_words(text):
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    return text_clean.split()

orig_words = get_words(original)
draft_words = get_words(content)

orig_ngrams = set()
N = 6
for i in range(len(orig_words) - N + 1):
    orig_ngrams.add(" ".join(orig_words[i:i+N]))

matches = []
for i in range(len(draft_words) - N + 1):
    gram = " ".join(draft_words[i:i+N])
    if gram in orig_ngrams:
        matches.append(gram)

# 4. Contrastive negation check
neg_matches = re.findall(r'\b(not|instead of)\b', content, re.IGNORECASE)

print(f"=== PROGRAMMATIC VERIFICATION ===")
print(f"Em-dash count: {em_dashes} (Must be 0)")
print(f"Title length: {t_len} chars (Limit <= 60)")
print(f"Meta Title length: {mt_len} chars (Limit <= 60)")
print(f"Meta Description length: {md_len} chars (Limit <= 155)")
print(f"Contrastive negation count: {len(neg_matches)} (Limit <= 1)")
print(f"6-gram matches count: {len(matches)}")
for m in matches:
    print(f"  Match: {m}")

