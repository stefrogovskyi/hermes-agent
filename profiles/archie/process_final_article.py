import re
import json
import subprocess
import os

# 1. FINAL TEXT DEFINITIONS
TITLE = "SeaRates February 2025 Platform Updates"
META_TITLE = "SeaRates February 2025 Product Updates"
META_DESC = "SeaRates February 2025 updates: Terminal API 1.0, Rate Management app, 9 new ocean carriers, 4 new airlines, and expanded tracking tools."

BODY_MARKDOWN = """The February 2025 release brings Terminal API Version 1.0, a tariff management app, mobile quote requests, and expanded tracking coverage across 13 additional shipping lines and airlines.

### Terminal API 1.0

The Terminal API Version 1.0 retrieves data from a database of over 17,000 terminals. Users can query data for 33 initial terminals by SMDG and BIC codes:

* CONTAINER TERMINAL ODESSA (CTO)
* BROOKLYN-KIEV PORT (BKP)
* KHALIFA PORT CONTAINER TERMINAL
* APM Terminals Puerto Quetzal
* APM Terminals Moín
* APM Terminals Port Elizabeth
* Port of Pointe-Noire
* APM Terminals Mumbai
* APM Terminals Aarhus
* APM Terminals Callao
* Aqaba Container Terminal
* APM Terminals Buenos Aires
* APM Terminals MedPort Tangier
* APM Terminals Onne
* APM Terminals Gothenburg
* APM Terminals Yucatán
* APM Terminals Pier 400 Los Angeles
* APM Terminals Apapa
* APM Terminals Lázaro Cárdenas
* APM Terminals Poti
* APM Terminals Pecém
* APM Terminals Vado Ligure
* APM Terminals Mobile
* Suez Canal Container Terminal
* APM Terminals Liberia
* APM Terminals Pipavav
* APM Terminals Bahrain
* APM Terminals Tangier
* APM Terminals Maasvlakte II
* APM Terminals Miami
* APM Terminals Valencia
* APM Terminals Algeciras
* APM Terminals Barcelona

Supported terminal status responses include UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, and UNEXPECTED_ERROR. The API also provides endpoints to fetch complete terminal directories alongside SMDG and BIC metadata.

### Rates & Tariffs App

The Rates and Tariffs app is now available inside Virtual Office integrated directly into the platform's Rate Management suite. Users can review, filter, export in bulk, and update ocean freight rates directly within their Dashboard for FCL, LCL, Bulk, D2D, D2P, and P2D quotes.

Newly added tariffs remain valid for two weeks by default. Users can promote selected tariffs inside Logistics Explorer, marking specific rates to guarantee spot allocation and space. Rate status options can be adjusted with tags like 'Expires' or 'Prospective'. The tariff table view can be personalized, with data processing structured to return query results in two seconds.

### Mobile Quote Request System

The SeaRates mobile application for iOS and Android now features a Request System. Users can complete the Request a Quote form for shipping and warehouse inquiries to receive quotes from logistics providers.

### Carbon Calculator & Autocomplete Integration

SeaRates Autocomplete now integrates directly with the Carbon Emissions Calculator tool. This enables location selection alongside carbon offset estimation for shipments.

### Vessel and Air Tracking Coverage

Tracking support has been added for 9 shipping lines:
* Unifeeder
* Viasea Shipping
* Oceanic Star Line
* CEVA Logistics
* Awot Global Logistics
* Folk Maritime
* GS Lines
* Bahri (Saudi Arabia)
* Vuxx Shipping

This brings the total supported shipping lines to 191. System updates also include improved routing logic, AIS data ingestion, and API auto-detection.

Air Cargo Tracking now supports 4 additional airlines:
* Alis Cargo Airlines
* Norse Atlantic Airways
* SolitAir Express
* Uganda Airlines

Overall air carrier coverage now reaches 444 integrated airlines.

### Bookings Workspace Updates

Updates to the Bookings tool include:
* Map display showing bookings data and route endpoints.
* Contact information for assigned booking managers.
* Tracking API integration providing vessel movement updates by container number in Shipping instructions under the 'Tracking' tab.
* Visual route breakdowns organized by fulfillment and transport mode inside the 'Details' section.

### Additional Tool Enhancements

* **Ship Schedules:** Broadened schedule lookup windows to encompass a 10-week horizon for vessel timetables, backed by faster backend processing.
* **Distance & Time:** Enhanced location determination logic for airport and railway terminals.
* **Freight Index:** Added interface translation support.
* **Logistics Explorer:** Added flat rate display for D2D, D2P, and P2D across LCL and Bulk categories.
* **World Sea Ports API:** Added options to query country lists by country code and retrieve port details by port name."""

# SHAG 7: Programmatic Verification
def run_verifications():
    full_text = f"{TITLE} {META_TITLE} {META_DESC} {BODY_MARKDOWN}"
    
    # 1. Em-dash count
    em_dashes = full_text.count("—") + full_text.count("--") + full_text.count("–")
    print(f"[CHECK] Em-dashes count: {em_dashes}")
    assert em_dashes == 0, f"Error: Found {em_dashes} prohibited dashes!"

    # 2. Length limits
    print(f"[CHECK] Title length: {len(TITLE)} chars (Limit: <=60)")
    assert len(TITLE) <= 60, "Title too long!"
    
    print(f"[CHECK] Meta-Title length: {len(META_TITLE)} chars (Limit: <=60)")
    assert len(META_TITLE) <= 60, "Meta-Title too long!"
    
    print(f"[CHECK] Meta-Desc length: {len(META_DESC)} chars (Limit: <=155)")
    assert len(META_DESC) <= 155, "Meta-Desc too long!"

    # 3. N-gram overlap against original article
    with open("/opt/hermes/profiles/archie/original_article.txt", "r", encoding="utf-8") as f:
        orig_text = f.read()

    def normalize(t):
        t = t.lower()
        t = re.sub(r"[^\w\s]", " ", t)
        return t.split()

    orig_words = normalize(orig_text)
    rewrite_words = normalize(BODY_MARKDOWN)

    def get_ngrams(words, n=6):
        return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

    orig_6grams = get_ngrams(orig_words, 6)
    rewrite_6grams = get_ngrams(rewrite_words, 6)

    inter = rewrite_6grams.intersection(orig_6grams)
    
    exempt_terms = {
        "apm", "terminals", "container", "terminal", "port", "line", "shipping", "logistics",
        "unknown", "on_terminal", "not_on_terminal", "terminal_not_supported", "terminal_no_response", "unexpected_error",
        "odessa", "brooklyn", "kiev", "khalifa", "puerto", "quetzal", "moín", "elizabeth", "pointe", "noire",
        "mumbai", "aarhus", "callao", "aqaba", "buenos", "aires", "medport", "tangier", "onne", "gothenburg",
        "yucatán", "pier", "400", "los", "angeles", "apapa", "lázaro", "cárdenas", "poti", "pecém", "vado",
        "ligure", "mobile", "suez", "canal", "liberia", "pipavav", "bahrain", "maasvlakte", "ii", "miami",
        "valencia", "algeciras", "barcelona", "unifeeder", "viasea", "oceanic", "star", "ceva", "awot",
        "global", "folk", "maritime", "gs", "lines", "bahri", "vuxx", "alis", "cargo", "norse", "atlantic",
        "solitair", "express", "uganda", "airlines"
    }

    non_exempt_matches = []
    for g in inter:
        if not any(w in exempt_terms for w in g):
            non_exempt_matches.append(" ".join(g))

    print(f"[CHECK] 6-gram overlap count (total: {len(inter)}, non-exempt: {len(non_exempt_matches)})")
    if non_exempt_matches:
        print("Non-exempt matching 6-grams:")
        for m in non_exempt_matches:
            print(" -", m)
    assert len(non_exempt_matches) == 0, f"Found non-exempt 6-gram overlaps: {non_exempt_matches}"

    print("[VERIFICATION PASSED] All checks clean!")

if __name__ == "__main__":
    run_verifications()
