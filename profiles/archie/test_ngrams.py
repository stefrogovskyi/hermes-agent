import re

orig = """February 2025 Development Release: Empowering Business Users
Innovations - Mar 6, 2025
Author: Sophia Shkuro

Terminal API:
The SeaRates team is proud to announce the Terminal API Version 1.0 launch. The API is designed to seamlessly collect and provide data from an updated database of 17,000+ terminals. Simply query data of 33 supported terminals by SMDG and BIC codes in minutes:
CONTAINER TERMINAL ODESSA (CTO), BROOKLYN-KIEV PORT (BKP), KHALIFA PORT CONTAINER TERMINAL, APM Terminals Puerto Quetzal, APM Terminals Moín, APM Terminals Port Elizabeth, Port of Pointe-Noire, APM Terminals Mumbai, APM Terminals Aarhus, APM Terminals Callao, Aqaba Container Terminal, APM Terminals Buenos Aires, APM Terminals MedPort Tangier, APM Terminals Onne, APM Terminals Gothenburg, APM Terminals Yucatán, APM Terminals Pier 400 Los Angeles, APM Terminals Apapa, APM Terminals Lázaro Cárdenas, APM Terminals Poti, APM Terminals Pecém, APM Terminals Vado Ligure, APM Terminals Mobile, Suez Canal Container Terminal, APM Terminals Liberia, APM Terminals Pipavav, APM Terminals Bahrain, APM Terminals Tangier, APM Terminals Maasvlakte II, APM Terminals Miami, APM Terminals Valencia, APM Terminals Algeciras, and APM Terminals Barcelona.
We have implemented support for terminal statuses, including UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, and UNEXPECTED_ERROR.
Moreover, we have created the API to request the full list of supported terminals, details, and SMDG & BIC codes.

Rates & Tariffs:
We are glad to announce the launch of the new app — Rates and Tariffs in your Virtual Office — as a part of the Rate Management System. Effectively handle your sea tariffs right in the personal Dashboard.
Simply add, account, filter, download in bulk, and manage tariffs for many container types, including FCL, LCL, and Bulk, as well as D2D, D2P, and P2D. By default, your newly added tariffs will be valid for two weeks.
Promote your tariffs in the Logistics Explorer tool, and designate one as a spot and space guarantee.
Adjust a collection of rate statuses, such as 'Expires' or 'Prospective'. Finally, personalize your tariff table to display rates in a perfect way for you.
Our team has implemented fast data processing to ensure that you receive the result request in 2 seconds.

SeaRates Mobile App:
We are happy to introduce the Request System in the SeaRates App, which is available for quick and convenient shipping request management at your fingertips!
You can download the app on iOS and Android to find the Request a Quote form ready for your shipping and warehouse inquiries. Simply fill in all necessary details and receive quotes from world-reliable logistics providers.

SeaRates Autocomplete:
Our team is glad to present a smooth integration of the SeaRates Autocomplete and Carbon Emissions Calculator tool. This way, you can cover global geography with the comprehensive SeaRates database and estimate carbon offset for your shipments in a few seconds.

Tracking System:
We are glad to announce added support for 9 shipping lines, namely Unifeeder, Viasea Shipping, Oceanic Star Line, CEVA Logistics, Awot Global Logistics, Folk Maritime, GS Lines, Bahri (Saudi Arabia), and Vuxx Shipping, bringing the total number to 191.
Also, we have improved the logic for routing, receiving AIS data, and auto-detection for the API.

Air Cargo Tracking:
We are pleased to announce added support for 4 airlines, including Alis Cargo Airlines, Norse Atlantic Airways, SolitAir Express, and Uganda Airlines, bringing the total number of supported airlines to 444.

Other updates:
For the Bookings, we've made several enhancements, including the following:
- added a map with bookings data and route endpoints;
- display of the manager assigned to your booking for quick contact;
- integration with the Tracking API for getting updates on vessels' movement by container number in Shipping instruction under the 'Tracking' tab;
- route displaying by shipment and delivery type under the 'Details' tab.

For the Ship Schedules tool, we have implemented a wider result range to cover 10 weeks of vessel schedules and optimized results processing.
Moreover, we have enhanced the logic of location determination for airport & railway terminals in the Distance & Time tool.
Furthermore, we have added the ability to translate the Freight Index tool’s interface.
Also, for the Logistics Explorer, added a display for flat rate D2D, D2P, and P2D for LCL and Bulk categories.
Finally, we have added options to get the list of countries by country code and receive data by port name for the World Sea Ports API.
"""

rewrite = """Title: SeaRates February 2025 Platform Updates
Meta Title: SeaRates February 2025 Product Updates
Meta Description: SeaRates February 2025 updates: Terminal API 1.0, Rate Management app, 9 new ocean carriers, 4 new airlines, and expanded tracking tools.

Body:
The February 2025 release brings Terminal API Version 1.0, a tariff management app, mobile quote requests, and expanded tracking coverage across 13 additional shipping lines and airlines.

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

Supported terminal status responses include UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, and UNEXPECTED_ERROR. Users can also request the full list of supported terminals, details, and associated SMDG and BIC codes through the API.

### Rates & Tariffs App

The Rates and Tariffs app is now available inside Virtual Office as part of the Rate Management System. Users can add, account, filter, download in bulk, and manage sea freight tariffs directly in their Dashboard across FCL, LCL, Bulk, D2D, D2P, and P2D options.

Newly added tariffs remain valid for two weeks by default. Users can promote specific tariffs in Logistics Explorer and designate one as a spot and space guarantee. Rate status options can be adjusted with tags like 'Expires' or 'Prospective'. The tariff table view can be personalized, with data processing structured to return query results in two seconds.

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

The total number of supported airlines is now 444.

### Bookings Workspace Updates

Updates to the Bookings tool include:
* Map display showing bookings data and route endpoints.
* Contact information for assigned booking managers.
* Tracking API integration providing vessel movement updates by container number in Shipping instructions under the 'Tracking' tab.
* Route visualization by shipment and delivery type under the 'Details' tab.

### Additional Tool Enhancements

* **Ship Schedules:** Expanded search results to cover 10 weeks of vessel schedules, along with optimized data processing.
* **Distance & Time:** Enhanced location determination logic for airport and railway terminals.
* **Freight Index:** Added interface translation support.
* **Logistics Explorer:** Added flat rate display for D2D, D2P, and P2D across LCL and Bulk categories.
* **World Sea Ports API:** Added options to query country lists by country code and retrieve port details by port name.
"""

# Let's clean punctuation to tokenize words
def tokenize(text):
    return re.findall(r'[A-Za-z0-9_]+', text)

orig_tokens = tokenize(orig)
rewrite_tokens = tokenize(rewrite)

# Find max non-overlapping or maximal matching runs of >= 6 tokens
orig_str = " ".join([t.lower() for t in orig_tokens])

# We can search for exact matching token sequences of length N >= 6 in rewrite
matches = []
i = 0
n = len(rewrite_tokens)
while i < n:
    # try longest match starting at i
    best_len = 0
    for l in range(6, n - i + 1):
        sub = " ".join([t.lower() for t in rewrite_tokens[i:i+l]])
        if sub in orig_str:
            best_len = l
        else:
            break
    if best_len >= 6:
        matched_tokens = rewrite_tokens[i:i+best_len]
        matches.append((i, best_len, " ".join(matched_tokens)))
        i += best_len
    else:
        i += 1

print(f"Total matching sequences of >=6 words: {len(matches)}")
for idx, l, m in matches:
    print(f"[{l} words]: {m}")

