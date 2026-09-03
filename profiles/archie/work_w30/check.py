import re, string

title = "SeaRates Week 30: New Carriers, Faster Tracking"
meta_title = "SeaRates Week 30, 2026 Update: New Carriers & Tools"
meta_desc = "New carriers and airlines join SeaRates tracking, plus updates to ship and flight schedules, the logistics map, load calculator, and booking tools."

body = """Week 30 landed with more names on the carrier list and fewer clicks between a shipment and its status. This week's SeaRates release, put together by Sophia Shkuro, touches container and air tracking, ship and flight schedules, the logistics map, the load calculator, autocomplete, routing, and booking. A couple of these changes are bigger than they look at first glance.

More Carriers on the Board

Container tracking picked up ten new shipping line connections this week: TransContainer, Namsung Shipping, Sea Legend Shipping, Dong Young Shipping, Leschaco, Oceanic Star Line, Meratus Line, COSCO Specialized, Atlantic Container Line (ACL), and Jin Jiang Shipping (SHJJ). Each new carrier feeds into the same unified tracking dashboard, adding to a much larger share of global container movement now visible in one place and cutting the need to check a dozen separate carrier portals. More coverage also means the predictive ETA models have more data points to draw on, and exception detection has a better shot at catching a problem before a container sits too long at a terminal racking up demurrage and detention charges.

Air tracking got its own list of additions: My Freighter (Centrum Air), Air Canada, United Airlines, Air New Zealand, SF Airlines, Nippon Cargo Airlines, Air Europa, Qantas, and Uzbekistan Airways. That's nine airlines added to carrier coverage in a single week, a fast pace even by SeaRates' usual release rhythm. For anyone tracking air freight next to ocean freight, this closes gaps that used to force a separate lookup on the airline's own site.

Schedules Move Too

Ship Schedules now support Seaboard Marine by Vessel. Wan Hai, KMTC, and Eucon got better support by Points, and Emirates, MTT, and RAL improved by Vessel. On the air side, Flight Schedules added SpiceJet. These are small updates on their own, spread across specific vessels, points, and one added airline schedule.

The Logistics Map Gets a Table View

Warehouses finally get a table view. Every tab in the Logistics Map now switches between map and table modes, useful for scanning through dozens of warehouse locations at once. SeaRates also brought back all transport types, Truck, Vessel, Wagon, and Aircraft, in both the Logistics Map and Virtual Office.

Load Calculator, Autocomplete, and a Few Small Fixes

The Load Calculator can now import and export Packages and Pallets directly, and users can toggle between metric and imperial units without re-entering every figure by hand. Autocomplete quietly added terminal ports as a filter option too, letting location searches target a specific terminal address directly.

Smarter Routes and Faster Bookings

Logistics Explorer changed how multimodal routes get calculated. For LWL shipments, LTL transportation is now automatically added as the first mile of the route, and port search now prioritizes locations in the country where the shipment originates. Both changes produce more relevant routing results without extra manual filtering, useful for anyone tracking a shipment across multiple transport modes.

The Booking System picked up improvements to booking creation for LWL shipments, moving another step toward real booking automation. The real-time world map used to display shipment routes also got an update this week, so watching a route unfold should feel a little less laggy than before."""

original = """SeaRates Updates - Week 30, 2026

We continue working on SeaRates to ensure our services remain efficient and relevant. Regular updates help us maintain consistent quality.

Last week's updates provide helpful background for this release.

What's new for week 30:

Container Tracking improvements: We have improved our collaboration with shipping lines, including TransContainer, Namsung Shipping, Sea Legend Shipping, Dong Young Shipping, Leschaco, Oceanic Star Line, Meratus Line, COSCO Specialized, Atlantic Container Line (ACL), and Jin Jiang Shipping (SHJJ).
Air Tracking updates: We have improved our support of airlines, including My Freighter (Centrum Air), Air Canada, United Airlines, Air New Zealand, SF Airlines, Nippon Cargo Airlines, Air Europa, Qantas, and Uzbekistan Airways.
Ship Schedules improvements: We have added support for Seaboard Marine by Vessel.
In addition, we have improved support for Wan Hai, KMTC and Eucon by Points, as well as Emirates, MTT and RAL by Vessel.
Flight Schedules updates: We have expanded airline coverage by adding support for SpiceJet.
Logistics Map enhancements: We are glad to present the new table view for Warehouses. All Logistics Map tabs now support switching between map and table modes.
Also, we have restored all transport types in Logistics Map and Virtual Office, including Truck, Vessel, Wagon, and Aircraft.
Load Calculator updates: We have added import and export for Packages and Pallets. Moreover, users can now switch between International and Imperial measurement systems.
Autocomplete enhancements: Terminal ports are now supported in Autocomplete filters, allowing more precise location selection.
Logistics Explorer improvements: We have updated multimodal route calculations by automatically including LTL transportation as the first-mile option for LWL shipments. Also, we have improved port search by prioritizing locations within the shipment's country of origin, providing more relevant routing results.
Booking System enhancements: We have improved booking creation for LWL shipments. Finally, we have updated the real-time world map for your shipment route display."""

# 1. em-dash count
all_text = title + " " + meta_title + " " + meta_desc + " " + body
em_count = all_text.count("—")
print("EM-DASH COUNT:", em_count)
print("double-hyphen count:", all_text.count("--"))

# 2. lengths
print("TITLE len:", len(title))
print("META-TITLE len:", len(meta_title))
print("META-DESC len:", len(meta_desc))

# 3. n-gram overlap (6-grams)
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.split()

def ngrams(words, n):
    return [tuple(words[i:i+n]) for i in range(len(words)-n+1)]

orig_words = normalize(original)
body_words = normalize(body)

n = 6
orig_6grams = set(ngrams(orig_words, n))
body_6grams = ngrams(body_words, n)

overlaps = [g for g in body_6grams if g in orig_6grams]
print("\n6-GRAM OVERLAPS COUNT:", len(overlaps))
for g in overlaps:
    print(" ", " ".join(g))
