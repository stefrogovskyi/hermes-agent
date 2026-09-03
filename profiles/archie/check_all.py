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

keywords = [
    "freight index market analytics",
    "container spot rate benchmarking",
    "historical freight tariffs",
    "ocean freight rate trends",
    "white-label freight index API",
    "supply chain rate forecasting"
]

print("=== VERIFICATION REPORT ===")
print("Title length:", len(title), "(max 60)")
print("Meta-Title length:", len(meta_title), "(max 60)")
print("Meta-Desc length:", len(meta_desc), "(max 155)")

print("\n--- EM-DASH CHECK ---")
has_em_dash = "—" in full_text or "--" in full_text
print("Em-dashes or double-hyphens found:", has_em_dash)

print("\n--- KEYWORD CHECK ---")
for kw in keywords:
    count = full_text.lower().count(kw.lower())
    print(f"'{kw}': {count}")

print("\n--- SLOP WORDS CHECK ---")
slop_list = [
    'delve', 'testament', 'crucial', 'seamless', 'landscape', 'tapestry',
    "today's world", 'vital', 'unlock', 'game-changer', 'revolutionize',
    'elevate', 'transform', 'empower', 'robust', 'paradigm', 'comprehensive',
    'fostering', 'cutting-edge', 'in conclusion', 'to summarize'
]
found_slop = [s for s in slop_list if s in full_text.lower()]
print("Slop words found:", found_slop)

print("\n--- OVER-EXPLAINING CONNECTORS ---")
connectors = ["that's why", "which is why", "that explains why", "this is why"]
found_conn = [c for c in connectors if c in full_text.lower()]
print("Connectors found:", found_conn)

print("\n--- CONTRASTIVE NEGATIONS ---")
neg_patterns = [
    r'\binstead of\b',
    r'\bnot [a-zA-Z0-9\s]+, but\b',
    r'\bnot [a-zA-Z0-9\s]+, [a-zA-Z0-9\s]+\b',
    r'\bisn\'t\b',
    r'\bis not\b'
]
neg_found = []
for pat in neg_patterns:
    matches = re.findall(pat, full_text, re.IGNORECASE)
    if matches:
        neg_found.extend(matches)
print("Negations found:", neg_found)

print("\n--- FACT CHECK ---")
facts = {
    "10,000,000 tariffs": "10,000,000" in full_text,
    "five years": "five years" in full_text,
    "1 billion+ routes": "1 billion" in full_text,
    "70+ million price points": "70+ million" in full_text,
    "99.99% accuracy": "99.99%" in full_text,
    "3 months / 3-month": "3-month" in full_text or "3 months" in full_text,
    "6 months": "6 months" in full_text,
    "1 year": "1 year" in full_text,
    "4 levels": "four" in full_text.lower() or "4" in full_text,
    "8 levels": "eight" in full_text.lower() or "8" in full_text,
    "FCL, LCL, Bulk": "FCL, LCL, and Bulk" in full_text,
    "FTL, FCL, LTL": "FTL, FCL, and LTL" in full_text,
    "FWL, LWL, FCL, FTL": "FWL, LWL, FCL, and FTL" in full_text,
    "standard cargo and ULD container": "standard cargo and ULD containers" in full_text,
    "Area, Continent, Subregion, Coast": "Area, Continent, Subregion, and Coast" in full_text,
    "Country, State, Province, Point": "Country, State, Province, and Point" in full_text,
    "City, Port, Airport, Station": "cities, ports, airports, and rail stations" in full_text,
    "All carriers / Shipping line not selected": "All carriers or Shipping line not selected" in full_text,
    "Developer Portal": "Developer Portal" in full_text,
    "Request an IT Quote": "Request an IT Quote" in full_text
}
for fact, present in facts.items():
    print(f"Fact '{fact}': {present}")
