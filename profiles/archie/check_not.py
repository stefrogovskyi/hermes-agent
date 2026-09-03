import re

rewrite_text = """Title:
SeaRates May 2025 Release: New Features & Tools

Meta Title:
SeaRates May 2025 Product & API Updates

Meta Description:
Explore SeaRates May 2025 release: Facilities management, 446 supported airlines, new API docs, and AI tools for logistics.

# SeaRates May 2025 Release: New Features & Tools

Logistics software works best when it stays out of your way.

Our May 2025 release delivers practical updates across Virtual Office, tracking APIs, rates, and search tools. If you missed April's release, you can check out those recent updates alongside our latest features. Subscribe to the SeaRates newsletter to receive future updates straight to your inbox.

## Warehouse Facilities in Virtual Office

You can now manage warehouse assets directly inside your Virtual Office profile. The Facilities panel lets you add, edit, import, and track facilities alongside offered services.

You can also share access with customers and partners so they can book warehouse services directly.

## Expanded Tracking and API Documentation

We updated several tracking modules this month.

* **Terminal API:** Terminal Tracking API documentation is live on our Developer Portal. It connects you to our database of worldwide terminals.
* **Air Tracking:** We added support for My Indo Airlines and Thai Vietair. That brings our total supported airline count to 446.
* **Road Tracking:** We added support for Kuehne + Nagel (KN). Check our API documentation to view the full list of supported road carriers.
* **Container Tracking:** The Exceptions tab now uses optimized logic for processing all 25 exception types. A dedicated field displays color markers for new dates: green marks positive changes for earlier arrival, while orange marks negative changes for delays. For API users, container type and size detection from shipping line descriptions is more accurate. We updated Predictive ETA logic too.

## AI Engine, Rates, and Location Data

SeaRates AI now runs on our own language model. Freight rate requests deliver improved results processing with a direct link to Logistics Explorer.

The Rate Management System includes five specific updates:
* Add tariffs for FCL and FTL by three options: 'Flat' (full cost), 'per km', or 'flat + per km'.
* Choose between ft³ and m³ for LCL type.
* Add air tariffs for D2D, D2P, and P2D types.
* Make groups of container types simultaneously (for example, grouping size 20 into 20ST, 20HC, 20REF, and others).
* Check added tooltips for columns in the tariff table.

For Geocoding & Autocomplete, we translated 217 capitals and 35,000 seaports into 8 major worldwide languages, including the top 100 world seaports. Data search also improved for the top 200+ world seaports.

## Pricing and Subscriptions

We added dedicated Pricing pages for five key products:
* Air Tracking
* Freight Index
* CO2 Calculator
* Ship Schedules
* DFA Membership

In the Ship Schedules tool, we updated the credit display and added a Pricing link to quickly continue your subscription. The Carbon Emissions Calculator features a subscription button to check credit limits and upgrade your plan. For API integrations, the CO2 Calculator supports calculation by Coordinates as an alternative option if there are no results by Carrier.

Need customized digital solutions for logistics? Reach out to us via the Request an IT Quote form or contact sales@searates.com anytime."""

print("ALL INSTANCES OF 'NOT':")
for m in re.finditer(r'\bnot\b', rewrite_text, re.IGNORECASE):
    start = max(0, m.start() - 30)
    end = min(len(rewrite_text), m.end() + 30)
    print("MATCH:", rewrite_text[start:end].replace('\n', ' '))

print("\nALL INSTANCES OF 'NO':")
for m in re.finditer(r'\bno\b', rewrite_text, re.IGNORECASE):
    start = max(0, m.start() - 30)
    end = min(len(rewrite_text), m.end() + 30)
    print("MATCH:", rewrite_text[start:end].replace('\n', ' '))

