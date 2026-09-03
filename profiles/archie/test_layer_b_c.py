import re

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

print("Checking full text sentence structures for Layer (c):")
sentences = re.split(r'(?<=[.!?])\s+', rewrite)
for idx, s in enumerate(sentences):
    s_clean = s.strip().replace('\n', ' ')
    if s_clean:
        print(f"S{idx+1}: {s_clean}")

