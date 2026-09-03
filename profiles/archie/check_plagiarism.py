import re

orig = """We at SeaRates are grateful for your steadfast help and encouragement. Our commitment to improving our service remains strong, and we are thrilled to introduce several new features designed to simplify your experience.
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

draft = """Title: SeaRates Logistics Platform Updates: Week 36, 2024
Meta-Title: SeaRates Updates Week 36: Tracking, Schedules & Tools
Meta-Description: Explore SeaRates Week 36, 2024 updates, including air tracking improvements, Load Calculator stacking rules, and API enhancements.

We are continuously refining SeaRates to give you clearer visibility and better operational control across your cargo workflows. Here is a roundup of technical upgrades, platform integrations, and feature rollouts deployed in Week 36 of 2024.

### Air Cargo Tracking Integrations

Our engineering team expanded data accuracy and direct integration support for several global air carriers. Tracking performance and reliability have been improved for:
* Shenzhen Airlines
* Air India
* FedEx Express
* Lufthansa Cargo
* Air France
* ITA Airways
* Czech Airlines
* Challenge Airlines
* Gulf Air
* Egyptair
* FITS Aviation
* UPS Air Cargos

### Tracking System Upgrades

#### Container Tracking API V3
For developers integrating our API V. 3, we updated the determination logic that identifies container size and type. The official documentation on our Developer Portal now includes a dedicated description of the `size_type` parameter to help you map container specifications cleanly.

#### Web Platform Bulk Tracking
On SeaRates.com, we added clear usage limits for bulk tracking uploads in Excel. Depending on your active subscription plan, you can now run simultaneous web tracking while uploading Excel lists to monitor multiple shipments at once.

#### Ocean Carrier Integrations
We updated integration logic and data processing for eleven container shipping lines:
* Independent Container Line
* Tarros
* FESCO
* Sea Hawk Lines (SHAL)
* Pacific International Lines (PIL)
* Eimskip
* Hapag-Lloyd
* Maersk
* SITC Container Lines
* Evergreen
* CK Line

### Ship Schedules Enhancements

Searching sailing schedules by Port now fully supports Evergreen schedules.

In addition, we refined data processing and connection stability across ten regional and global ocean carriers:
* Cordelia
* Econship
* Golden Fortune Shipping
* Gold Star Line
* Kambara Kisen
* Laurel Navigation
* Pacifica Shipping
* Tanto
* Vanguard Logistics
* W.E.C.

### Load Calculator: Stacking Controls and Limits

We rolled out a practical update to the web version of Load Calculator. Under the "Stuffing settings" section, you will find a new "Disable stacking" checkbox available for every cargo format (including boxes, big bags, sacks, barrels, and rolls). Checking this box forces the calculation engine to keep items in a single layer whenever cargo cannot bear weight on top.

If your cargo allows limited stacking, you can define precise mass or height boundaries. Simply input exact thresholds into the "Mass" or "Height" fields or adjust the permitted layer count to generate accurate stuffing diagrams.

### Distance & Time API Update

For API users, we upgraded the seaport detection logic in our Distance & Time engine. The system now determines the nearest seaport with higher precision when calculating transit itineraries.

### Quote Forms & Vendor Portal Updates

We added new transportation modes to the Request a Quote and Quick Request forms, specifically catering to Land FTL inquiries.

We also published a new dedicated landing page for Vendors - Freight Forwarders, alongside an updated design and refreshed content on the main SeaRates Vendors page.

### Recent Announcements & Ecosystem Releases

Here is a look at recent tool rollouts and service upgrades available across our ecosystem:
* Geocoding API / Autocomplete service Version 0.8
* New Version of Route Planner API
* ‘Transport’ tab in the Logistics Map tool
* Freight Index 1.0
* Mobile App Version 1.2 with Request System feature
* Load Calculator Version 2.2
* Booking System Version 1.1
* Parcel Tracking API
* Rail Tracking API
* Rail Tracking Web on LandRates.com
* Map platform
* Unified Tracking System WEB"""

def normalize_words(t):
    return [w.lower() for w in re.findall(r'\b[\w\.\-]+?\b', t)]

o_words = normalize_words(orig)
d_words = normalize_words(draft)

def get_ngrams(words, n):
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

matches = set()
for n in range(6, 15):
    o_ngrams = set(get_ngrams(o_words, n))
    d_ngrams = get_ngrams(d_words, n)
    for g in d_ngrams:
        if g in o_ngrams:
            matches.add(g)

# Filter out sub-ngrams
final_matches = []
sorted_matches = sorted(list(matches), key=len, reverse=True)
for m in sorted_matches:
    if not any(m in bigger and m != bigger for bigger in final_matches):
        final_matches.append(m)

print("Final 6+ word overlaps:")
for fm in sorted(final_matches):
    print("MATCH:", fm)
