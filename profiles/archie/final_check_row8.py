import re

title = "SeaRates Week 29: Tracking and Rate Updates"
meta_title = "SeaRates Release Notes: Week 29 Updates"
meta_desc = "SeaRates week 29: broader carrier integrations, vessel tracking pricing plans, Load Calculator 3.0 pallets, and multimodal Rail shipments."

body = """Small changes pile up fast, and by the time you notice it, the whole platform has shifted under your feet. That's roughly how SeaRates development works: incremental, always shipping something. Check last week's updates first if you haven't already, this one builds on it.

Here's what changed in week 29.

Carrier Integrations: Container and Air Tracking

Container tracking picked up deeper integration work with seven carriers this round: Evergreen, Swire Shipping, Shipping Corporation of India (SCI), CMA CGM, Yang Ming, COSCO, and Shipco Transport. Tracking accuracy and reliability improved for all of them. Air tracking's logistics API connection got stronger too, with better support now in place for Delta Air Lines and T'way Air.

Vessel Tracking Platform: Pricing Plans and New Languages

The vessel tracking platform now has pricing plans, the main addition to this section this round. Alongside it, the vessel monitoring application picked up interface localization, so it's now available in multiple languages.

Flight Schedules and Ship Schedules Grow

Airline coverage widened in Flight Schedules with Asiana Airlines and Qantas Airways added to the list. Ship Schedules grew as well, the vessel database gained 9,245 additional fleet records.

Load Calculator 3.0

Pallets are in. Version 3.0 of the Load Calculator now supports them, including the option to build custom pallet configurations. Load planning gets more flexible, more accurate too.

Distance & Time: Route Visualization in Color

Route visualization changed this week. Each transportation mode now carries its own dedicated color, making it quicker to scan and follow a route.

Virtual Office: Facilities Section for Vendors

Virtual Office added a Facilities section. Vendors can now handle their warehouse locations on their own, from setup to day-to-day management.

Improved Booking Status Visibility

The Booking System got an interface refresh. Booking status synchronization also improved, so what's displayed always matches the actual state of the booking, regardless of what's happening in the browser.

Rate Management: Alternative LOCODE Lookup

Rate imports, whether through files or API requests, now have an alternative LOCODE lookup option available, making data matching more accurate and imports more reliable.

Multimodal Rail Shipments in Logistics Explorer

Logistics Explorer added support for multimodal Rail shipments, feeding into freight rate calculations."""

original = """SeaRates evolves through continuous improvements that enhance both functionality and performance. Each update builds on previous progress.

We recommend checking last week's updates before exploring the latest ones.

What's new for week 29:

Container Tracking improvements: We have enhanced our integration with shipping lines, including Evergreen, Swire Shipping, Shipping Corporation of India (SCI), CMA CGM, Yang Ming, COSCO, and Shipco Transport, improving tracking accuracy and reliability.

Air Tracking enhancements: For the API connection, we have improved support for Delta Air Lines and T'way Air.

Vessel Tracking updates: We are glad to present the Pricing plans for Vessel Tracking.

Also, we have added interface localization, making the vessel monitoring application available in multiple languages.

Load Calculator updates: For version 3.0, we have introduced support for pallets, including the ability to create custom pallet configurations, making load planning more flexible and accurate.

Distance & Time improvements: We have updated the route visualization by introducing dedicated colors for each transportation mode, making route information easier to read and navigate.

Flight Schedules enhancements: We have expanded airline coverage with the addition of Asiana Airlines and Qantas Airways.

Ship Schedules improvements: We have updated the vessel database with 9,245 additional fleet records.

Virtual Office enhancements: We are glad to present the Facilities section for Vendors to create and manage warehouse locations independently.

Booking System improvements: We have enhanced the interface and improved booking status synchronization so that the displayed status always reflects the actual booking state, regardless of browser activity.

Rate Management System updates: We have added an alternative LOCODE lookup during rate imports via files and API requests, improving data matching and import reliability.

Logistics Explorer enhancements: We have added support for creating multimodal Rail shipments for further freight rate calculations."""

# 1. em-dash count
all_text = title + " " + meta_title + " " + meta_desc + " " + body
em_count = all_text.count("—") + all_text.count("--")
print("EM-DASH / -- count:", em_count)

# 2. n-gram overlap (6-grams)
def normalize(t):
    t = t.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return t.split()

def ngrams(words, n=6):
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

orig_words = normalize(original)
body_words = normalize(body)

orig_6grams = set(ngrams(orig_words, 6))
body_6grams = ngrams(body_words, 6)

overlaps = [g for g in body_6grams if g in orig_6grams]
print("\n6-gram overlaps count:", len(overlaps))
for o in overlaps:
    print(" -", o)

# 3. lengths
print("\nTitle length:", len(title), "(limit 60)")
print("Meta-title length:", len(meta_title), "(limit 60)")
print("Meta-description length:", len(meta_desc), "(limit 155)")

# 4. contrastive negation check (rough)
contrastive_patterns = [" not ", "instead of", "rather than"]
for p in contrastive_patterns:
    c = body.lower().count(p)
    if c:
        print(f"\nContrastive pattern '{p}' found {c}x")

# 5. "that's why" chains
for p in ["that's why", "which is why"]:
    c = body.lower().count(p)
    print(f"'{p}' count:", c)
