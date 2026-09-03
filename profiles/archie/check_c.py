import re

rewrite_text = """
Title: SeaRates November 2024 Product Update
Meta Title: SeaRates Nov 2024 Update: Tracking, Schedules & TMS
Meta Description: SeaRates November 2024 release updates ocean, air, rail, parcel tracking, ship schedules, Virtual Office controls, and TMS transport cards.

Body Markdown:
Monthly platform updates for November 2024 deliver functional improvements across the SeaRates ecosystem based on user feedback.

## Tracking and Vessel Schedule Enhancements

Tracking features on web platforms and web-integrated setups receive a refreshed interface alongside a Book Now button connecting directly to the updated Logistics Explorer. Shipping line logos now display tooltips with carrier names. On the backend, data retrieval logic for extended vessel details was upgraded, and a new predictive ETA calculation formula was implemented.

Coverage across transport modes expanded:
* Air Cargo Tracking added five carriers (AirMax (Peru), Aloha Air Cargo, Corendon Dutch Airlines, Azerbaijan Airlines, and Air Arabia Abu Dhabi), reaching 437 supported airlines.
* Parcel Tracking added provider Leman, bringing total supported services to 2,417, while improving autodetect logic for API requests.
* Rail Tracking API added a dedicated endpoint to fetch supported rail carriers, introduced the `container_size_type` field to output container specifications such as "20' Dry Standard", refined arrival time calculation logic, and published complete API documentation on the Developer Portal.

Ship Schedules broadened carrier query options. Searches by Vessel now support Namsung, SITC, Kambara Kisen, CULines, and Sinokor. Search by Points supports Romocean, while search by Port supports Namsung and Kambara Kisen. For port searches, results surface vessels currently present or recorded within the past 48 hours, alongside ships arriving or departing during that same timeframe.

## Virtual Office, TMS, and Interface Adjustments

Virtual Office dashboard analytics now offer deeper breakdowns. Under the Bookings Overview by Shipping Type chart, selecting More Info reveals detailed metrics covering country, transport mode, shipping type, and route. Toggling between Active Bookings and Requests refreshes linked chart graphics and map displays simultaneously.

The Documents section inside the Bookings tab features a completely redesigned layout. Downloaded files are restricted by default to the booking owner and manager. Other involved parties can access downloaded files through the Show button once review and approval are completed.

Logistics Map and TMS tools now allow users to generate custom thumbnail cover images for transport units. In TMS, selecting Transport Name from the list opens the complete transport card within Logistics Map.

Site customization options now include a Button hover color setting inside Search Filter. The Request an IT Quote form adds informative tooltips across 12 tools, including Freight Index, Air Cargo Tracking, Cargo Wizard, CO2 Calculator, Demurrage and Storage Calculator, and World Sea Ports. Additional tooltips cover SeaRates Mobile App, SeaRates Enterprise, Parcel Tracking, Logistics Map Web access, Web integration, and API.
"""

# Connectors
connectors = ["Furthermore", "Moreover", "In addition", "That's why", "Additionally", "Consequently", "Therefore", "Thus", "Hence", "In conclusion", "Overall"]

for c in connectors:
    found = re.findall(r'\b' + c + r'\b', rewrite_text, re.I)
    if found:
        print("Found connector:", c, len(found))

# Contrastive negations
negations = re.findall(r'\b(not [^.,;]+, but|not only|instead of|rather than|X, not Y)\b', rewrite_text, re.I)
print("Contrastive negations:", negations)

# Sentences count and structure
paragraphs = [p.strip() for p in rewrite_text.split('\n\n') if p.strip()]

print("\nParagraph structures:")
for idx, p in enumerate(paragraphs):
    print(f"P{idx}: {p[:60]}...")

