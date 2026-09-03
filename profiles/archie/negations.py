import re

rewrite = """Title: SeaRates September 2025 Release: Tracking & RMS Updates
Meta Title: SeaRates Updates: Tracking APIs, RMS & Schedules
Meta Description: SeaRates September 2025 updates bring 215 tracked lines, upgraded container tracking APIs, FCL LCL port rates in RMS, and expanded vessel schedules.

Body:
# September 2025 SeaRates Engineering and System Updates

September's release expands carrier coverage across tracking tools, refines API payload structures, and updates the rate management system (RMS) with structured port rate tools.

## Tracking Engine and API Adjustments

TVS Supply Chain Solutions and De Well Group are now integrated into the tracking engine, bringing total supported lines to 215.

Bulk tracking workflows received an interface tweak: uploading an Excel spreadsheet in the web dashboard now creates individual shipment cards automatically. Registered accounts on free subscriptions can now see their daily and monthly query limits directly inside the dashboard to track remaining usage.

On the developer side, our container tracking APIs received updates targeting carrier data normalization. The backend logic now parses vessel data faster and standardizes container type and size details directly from raw carrier descriptions. Response building in the History API was also rewritten to deliver cleaner JSON structures.

## Rate Management System (RMS) Upgrades

A major revision to the rate management system (RMS) introduces a dedicated module for managing FCL LCL port rates. Users can create, store, and edit rate structures across varied transport types, ports, and trade directions:

* Configurable rate profiles for import, export, or bidirectional routes
* Direct export and bulk upload options for rate tables
* Time-bound validity periods assigned per rate entry
* Central Directory section listing all active port rates

These controls streamline rate entry without requiring manual spreadsheet work for every freight quote.

## Expanded Vessel Schedules and Carrier Map Filters

Routing tools now include new ocean and air carrier coverage. We updated vessel schedules across three distinct query modes:

* **By Points:** Linea Peninsular, Marfret, and Unifeeder
* **By Vessel:** Neptune Pacific Direct Line and Universal Africa Lines
* **By Port:** Ethiopian

Flight schedule tracking added support for United Airlines.

For fleet operations, the Logistics Map Transport tool now features an extended carrier filter to isolate specific transport units. A "To be nominated" filter toggle isolates unassigned units on the live map to improve shipment visibility.

Finally, SeaRates AI was updated with body streaming. Chat responses now render live on screen as text streams in, eliminating latency delays during interactive prompts."""

# Check for all forms of negation or contrast
patterns = [
    (r'\bnot\b', "not"),
    (r'\binstead of\b', "instead of"),
    (r'\brather than\b', "rather than"),
    (r'\bwithout\b', "without"),
    (r'\bno longer\b', "no longer"),
    (r'\bnever\b', "never"),
    (r'\bnor\b', "nor"),
    (r'\bneither\b', "neither")
]

for p, name in patterns:
    matches = re.findall(p, rewrite, re.IGNORECASE)
    print(f"Pattern '{name}': {len(matches)} matches")

sentences = re.split(r'\n+|\. ', rewrite)
for s in sentences:
    for p, name in patterns:
        if re.search(p, s, re.IGNORECASE):
            print(f"[{name}] -> {s.strip()}")

