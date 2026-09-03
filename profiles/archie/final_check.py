import re

title = "SeaRates Freight Index: How to Track and Benchmark Rates"
meta_title = "SeaRates Freight Index Guide: Rate Benchmarking and Data"
meta_desc = "Track ocean freight rate trends, compare historical freight tariffs, and integrate a white-label freight index API for supply chain rate forecasting."

body = """Shipping rates move fast, but raw market data usually moves faster than the teams trying to track it. SeaRates Freight Index pulls from a database built on over 10,000,000 tariffs logged across the past five years, covering more than 1 billion routes and 70+ million price points. That engine delivers 99.99% accuracy of supply chain rate forecasting across sea, land, rail, and air modes.

When you open the tool, the main view loads trending indexes with average spot rates for high-traffic trade lanes. Horizontal scrolling exposes additional lanes. Two primary dropdown menus control mode and equipment settings.
Sea options include FCL, LCL, and Bulk.
Land lists FTL, FCL, and LTL.
Rail supports FWL, LWL, FCL, and FTL.
Air cargo breaks down into standard cargo and ULD containers.

The platform runs on two tiers. Default access gives you four geographical search levels: Area, Continent, Subregion, and Coast. Autocomplete map detection identifies origin and destination points, showing price movement as increased, decreased, or flat rates along specific lanes or regional nodes. The Default plan limits historical freight tariffs research to a 3-month window, with direct export options to share findings with customers, partners, or social media followers.

Premium expands geographical search to eight levels by adding Country, State, Province, and Point parameters, which cover cities, ports, airports, and rail stations. You can run freight index market analytics across weekly, monthly, or yearly increments.

Filtering by carrier is exclusive to Premium. You can isolate a single carrier or set the filter to All carriers or Shipping line not selected. Date selection opens up options for 6 months, 1 year, a specific date, or custom calendar ranges. Premium users can run container spot rate benchmarking, switch display currencies on the fly, set notifications on rate changes, and download research data in a convenient format.

For software platforms, all Premium features connect through the Freight Index API into CRM, ERP, or TMS infrastructure using the SeaRates global database and Developer Portal documentation. Alternatively, companies can embed container spot rate benchmarking functionality as a white-label freight index API setup directly on their own websites, enabling advanced benchmarking under their own brand and keeping users from checking competitors' sources for ocean freight rate trends.

To set up a custom plan or white-label portal, fill out the Request an IT Quote form or reach out to sales."""

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

# Final verification checks
errors = []

if len(title) > 60:
    errors.append(f"Title too long: {len(title)} chars")
if len(meta_title) > 60:
    errors.append(f"Meta-title too long: {len(meta_title)} chars")
if len(meta_desc) > 155:
    errors.append(f"Meta-description too long: {len(meta_desc)} chars")

if "—" in full_text or "--" in full_text:
    errors.append("Em-dash or double-hyphen detected!")

slop_words = [
    'delve', 'testament', 'crucial', 'seamless', 'landscape', 'tapestry',
    "today's world", 'vital', 'unlock', 'game-changer', 'revolutionize',
    'elevate', 'transform', 'empower', 'robust', 'paradigm', 'comprehensive',
    'fostering', 'cutting-edge', 'in conclusion', 'to summarize'
]
for s in slop_words:
    if s in full_text.lower():
        errors.append(f"Slop word detected: {s}")

connectors = ["that's why", "which is why", "that explains why", "this is why"]
for c in connectors:
    if c in full_text.lower():
        errors.append(f"Over-explaining connector detected: {c}")

keywords = [
    "freight index market analytics",
    "container spot rate benchmarking",
    "historical freight tariffs",
    "ocean freight rate trends",
    "white-label freight index API",
    "supply chain rate forecasting"
]
for kw in keywords:
    if kw.lower() not in full_text.lower():
        errors.append(f"Missing target keyword: {kw}")

if errors:
    print("ERRORS FOUND:")
    for err in errors:
        print("-", err)
else:
    print("ALL VERIFICATION CHECKS PASSED PERFECTLY!")
