import re

orig_text = """At SeaRates, we appreciate your continued support and encouragement. We are also committed to improving our services and are pleased to introduce many new features that will make your work easier.

Catch your last chance on our Black Friday Sale and get 15% off all SeaRates tools and API integrations: https://www.searates.com/tools

Check out our previous updates (Week 47, 2025) for the latest details.

What’s new for week 48:
- Unified Tracking System for monitoring all shipping modes (sea, air, rail, road). Current location and real-time updates in one place.
- Container Tracking updates: Improved logic for determining ISO code for container type and size in Container Tracking API.
- Improved collaboration with shipping lines: Akkon Lines, Hecny Shipping, Yang Ming, Dole Ocean Cargo Express, Carpenters Shipping, Stolt Tank Containers (STC), Cosiarma S.p.A., CK Line, Namsung Shipping, Dong Young Shipping, and Lucky Logistics.
- Air Tracking enhancements: Updated support for airlines in API: Malaysia Airlines, Saudi, Sichuan Airlines, FedEx Express.
- Virtual Office updates: New tools added to Tools -> General section: Parcel Tracking (API statistics), World Sea Ports (API statistics), Freight Index (API and Access statistics).
- Upgraded performance of Transport and Facilities management panels.
- Booking System improvements: Added API documentation for booking management on Developer Portal.
- Other updates:
  * Updated Search Filter on Homepage.
  * Upgraded Rail FCL rate calculations to Logistics Explorer and implemented autocomplete, as well as for Ship Schedules (by Points and by Vessel).
  * Rate Management System: Added Rail FCL rate types and customization for adjusting rate types.

Announcements:
- Load Calculator Web 3.0 (new design and features)
- Map Platform
- Geocoding API integrated with Logistics Explorer
- Inbox integration with Logistics Explorer, Bookings, and Notifications"""

rewrite_text = """TITLE: SeaRates Updates: Week 48, 2025
META_TITLE: SeaRates Release Notes Week 48, 2025 Updates
META_DESCRIPTION: Track cargo across sea, air, rail, and road in one place with SeaRates Week 48 updates, including expanded carrier integrations and API tools.

BODY:
Week 48 introduces a Unified Tracking System alongside speed enhancements across core management panels and broader carrier coverage. Shippers and developers can still claim a 15% Black Friday discount on all SeaRates tools and API integrations at https://www.searates.com/tools before the offer ends. Previous updates from Week 47, 2025 remain accessible on the platform.

## Multimodal and Container Tracking Improvements

The Unified Tracking System centralizes sea, air, rail, and road shipment tracking into a single view for real-time location monitoring.

Inside the Container Tracking API, updated logic now determines ISO code values for container types and sizes. Integration logic has also been upgraded across ocean lines, including Akkon Lines, Hecny Shipping, Yang Ming, Dole Ocean Cargo Express, Carpenters Shipping, Stolt Tank Containers (STC), Cosiarma S.p.A., CK Line, Namsung Shipping, Dong Young Shipping, and Lucky Logistics.

Air tracking API capabilities now cover updated data structures for Malaysia Airlines, Saudi, Sichuan Airlines, and FedEx Express.

## Rates, Search, and Operational Tools

Rail FCL rate calculations are available in Logistics Explorer with autocomplete support. Autocomplete is also active for Ship Schedules when searching by Points or by Vessel. For logistics rate management, the Rate Management System now incorporates Rail FCL rate types and settings to adjust rate parameters.

Virtual Office users will find new tools under Tools -> General. This area now displays usage statistics for Parcel Tracking (API statistics), World Sea Ports (API statistics), and Freight Index (API and Access statistics).

Additional technical updates in this release:
* Improved operational performance in Transport and Facilities management panels
* Booking management API documentation on the Developer Portal
* Revised Search Filter on the Homepage

## Upcoming Features

Development continues on several tools scheduled for release:
* Load Calculator Web 3.0 with a new design and features
* Map Platform
* Geocoding API integrated with Logistics Explorer
* Inbox integration linking Logistics Explorer, Bookings, and Notifications"""

def norm(t):
    return re.sub(r'[^\w\s]', ' ', t.lower()).split()

o_words = norm(orig_text)
r_words = norm(rewrite_text)

# Find contiguous matching sub-sequences of length >= 6
def find_long_matches(a, b, min_len=6):
    matches = []
    # Dynamic programming or simple search
    len_a, len_b = len(a), len(b)
    visited_b = [False] * len_b
    
    i = 0
    results = []
    for i in range(len_b):
        for j in range(len_a):
            k = 0
            while i + k < len_b and j + k < len_a and b[i+k] == a[j+k]:
                k += 1
            if k >= min_len:
                match_str = " ".join(b[i:i+k])
                results.append((i, k, match_str))
    # Deduplicate overlapping matches
    results.sort(key=lambda x: (x[0], -x[1]))
    filtered = []
    last_end = -1
    for pos, length, text in results:
        if pos >= last_end:
            filtered.append((pos, length, text))
            last_end = pos + length
    return filtered

long_matches = find_long_matches(o_words, r_words, min_len=6)
print(f"Contiguous matches of length >= 6 words: {len(long_matches)}")
for pos, length, text in long_matches:
    print(f"Length {length}: '{text}'")

