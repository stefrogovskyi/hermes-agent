import json
import re

title = "SeaRates at VDS25: Building Green and Digital Logistics"
meta_title = "SeaRates VDS25 Recap: Smart Supply Chains in Valencia"
meta_description = "SeaRates joined 15,000 attendees at VDS25 in Valencia to highlight digital supply chain transformation and green logistics solutions for global trade."

content = """## SeaRates at Valencia Digital Summit 2025

Inside Valencia's City of Arts and Sciences, fifteen thousand people gathered under high white arches to figure out where global trade goes next.

The event was Valencia Digital Summit 2025 (VDS25), held on October 22-23, 2025. Over 15,000 participants, 1,500 startups, and 500 industry leaders attended the summit in Spain. Over two days, technical discussions covered artificial intelligence and supply chain management. Green technology and Industry 5.0 also took center stage.

For SeaRates, the summit offered space to show how software simplifies supply chain operations. The team spent the event running technical discussions, exploring startup exhibitions, and meeting with industry partners.

Valeriya Guliy represented SeaRates at VDS25 and published her personal reflections on LinkedIn following the event.

## Core Tools and Practical Trade Solutions

Modern shipping requires clear data. SeaRates demonstrated four core tools designed to handle everyday freight work within a single smart logistics ecosystem:

* Logistics Explorer handles freight calculation and real-time booking.
* Route Planner optimizes linear and multimodal routes.
* Ship Schedules manages sailing timelines.
* Tracking System operates as a dedicated application for monitoring all cargo types.

Together, these tools deliver supply chain visibility and real-time freight tracking across international routes. They give logisticians practical tools to solve complex transportation problems.

## Key Takeaways from Valencia

Three main insights stood out from the conference sessions and exhibition floors:

First, digital transformation is no longer optional. Companies adopting automation, clear data tracking, and software integrations gain the flexibility needed to navigate volatile markets.

Second, innovation is the child of sustainability. Building sustainable operations takes time, yet speakers repeatedly stressed the urgent requirement for green logistics solutions.

Third, progress relies on industry partnerships. Major breakthroughs happen through alliances joining freight forwarders, technology innovators, logistics providers, and commercial enterprises.

## Moving Forward in Global Trade

The two days in Valencia gave the SeaRates team renewed energy to improve global freight software. To explore these digital supply chain transformation tools or discuss partner opportunities, contact sales@searates.com."""

json_data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "content": content
}

# Run rule checks
full_text = f"{title}\n{meta_title}\n{meta_description}\n{content}"

print("=== CHECKING RULES ===")
print("Title len:", len(title), "<= 60:", len(title) <= 60)
print("Meta Title len:", len(meta_title), "<= 60:", len(meta_title) <= 60)
print("Meta Desc len:", len(meta_description), "<= 155:", len(meta_description) <= 155)

# Em-dashes
dashes = [c for c in full_text if c in ["—", "--", "–"]]
print("Em/en dashes found:", dashes)

# Target keywords
keywords = [
    "digital supply chain transformation",
    "green logistics solutions",
    "smart logistics ecosystem",
    "supply chain visibility",
    "real-time freight tracking"
]
for kw in keywords:
    print(f"Keyword '{kw}':", kw.lower() in full_text.lower())

# Check contrastive negations
x_not_y = re.findall(r',\s*not\b', full_text, re.IGNORECASE)
instead_of = re.findall(r'\binstead of\b', full_text, re.IGNORECASE)
no_longer = re.findall(r'\bno longer\b', full_text, re.IGNORECASE)
print("Contrastive negations - ', not':", x_not_y, "'instead of':", instead_of, "'no longer':", no_longer)

# Facts check
facts = [
    "15,000", "1,500", "500", "October 22-23, 2025",
    "City of Arts and Sciences", "Valencia", "Spain",
    "Valeriya Guliy", "Logistics Explorer", "Route Planner",
    "Ship Schedules", "Tracking System", "sales@searates.com",
    "LinkedIn", "VDS25"
]
for f in facts:
    if f.lower() not in full_text.lower():
        print(f"MISSING FACT: {f}")

with open("/opt/hermes/profiles/archie/output.json", "w") as f:
    json.dump(json_data, f, indent=2)

print("Saved output.json successfully.")
