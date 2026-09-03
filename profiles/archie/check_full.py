import re

title = "SeaRates Week 20 Updates: API, Tracking & Schedules"
meta_title = "SeaRates Updates Week 20 2025: New APIs & Tools"
meta_desc = "Explore SeaRates Week 20 2025 updates: Terminal Tracking API docs, pricing plans, Thai Vietair support, and container tracking exceptions."

body = """Week 20 of 2025 brings new subscription options, documentation releases, and data updates across our multi-modal logistics software.

### Subscriptions and Developer Portal
Pricing plans are now active for both the Ship Schedules and Air Tracking tools. Subscriptions can be chosen to suit specific operational needs, including teams connecting via our ship schedules API.

On our Developer Portal, documentation for the terminal tracking API is now live. Developers can query our database of worldwide terminals for broad tracking coverage.

### Container Tracking and Shipping Lines
We updated the container tracking exceptions tab and refined our predictive ETA logic.

Data support was improved for thirteen shipping lines: Turkon, Pacific International Lines (PIL), Gold Star Line, Yang Ming, COSCO, Evergreen, Heung-A Shipping, W.E.C. (West European Container) Lines, Kawasaki Kisen Kaisha (K Line), Sinokor, Wan Hai, Emirates Shipping Line, and DHL Global Forwarding.

For schedules specifically, collaboration with Gold Star Line and Turkon now supports search by Points, while Evergreen supports search by Port.

### Air Freight Tracking
Thai Vietair joins our air freight tracking coverage. That brings our total supported air carriers to 446.

Tracking support was also upgraded for six carriers:
* Air India
* FedEx Express
* China Southern Airlines
* My Indo Airlines
* Air Canada
* ASL Airlines Belgium

### Geocoding and Page Updates
For geocoding autocomplete, alternative names are now integrated for 217 world capitals and the top 100 ports. Support includes translations across 8 major languages.

We also updated the content and visual design on our product pages for Bulk/Break Bulk, LCL (Less Container Load), and FCL (Full Container Load).

### In Development
* Unified Tracking System
* Vessel Tracking API v1
* Logistics Map 'Warehouse' tab
* SeaRates AI 1.0
* Parcel Tracking Web
* Load Calculator Web 3.0 (new design and features)
* Map Platform
"""

print("=== VALIDATION RESULTS ===")
print(f"Title length ({len(title)} / 60): {len(title) <= 60}")
print(f"Meta title length ({len(meta_title)} / 60): {len(meta_title) <= 60}")
print(f"Meta desc length ({len(meta_desc)} / 155): {len(meta_desc) <= 155}")

em_dash_matches = re.findall(r'—|--|–', title + meta_title + meta_desc + body)
print(f"Em-dashes / hyphens count: {len(em_dash_matches)}")

banned_words = [
    "game-changer", "dive into", "seamless", "delve", "crucial role", 
    "fast-paced world", "testament to", "tapestry", "beacon", "landscape", 
    "boasts", "realm", "unlock", "elevate", "fostering", "empower", 
    "revolutionize", "cutting-edge", "vital", "excited to present", "proudly announce"
]

found_banned = [w for w in banned_words if w.lower() in (title + meta_title + meta_desc + body).lower()]
print(f"Banned words found: {found_banned}")

keywords = [
    "terminal tracking API",
    "predictive ETA logic",
    "air freight tracking",
    "ship schedules API",
    "geocoding autocomplete",
    "container tracking exceptions",
    "multi-modal logistics software"
]

print("\nKeywords Check:")
all_kw_present = True
for kw in keywords:
    present = kw.lower() in (title + meta_title + meta_desc + body).lower()
    print(f"  [{'OK' if present else 'MISSING'}] '{kw}'")
    if not present:
        all_kw_present = False

# Sentences analysis for burstiness
sentences = [s.strip() for s in re.split(r'[.!?]', body) if s.strip()]
lengths = [len(s.split()) for s in sentences]
print(f"\nSentence counts: {len(sentences)}")
print(f"Sentence length distribution (words per sentence): {lengths[:10]}...")
