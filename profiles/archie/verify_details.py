import re

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

lines = draft.split('\n')
for idx, line in enumerate(lines, 1):
    if line.strip():
        print(f"L{idx}: {line[:80]}...")

