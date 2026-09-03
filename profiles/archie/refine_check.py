import re

body = """Recent updates across the SeaRates platform bring fresh tools to developers and logistics operators, following our previous work. Subscribing to the SeaRates Newsletter keeps you updated on future releases.

## Ocean, Air, and Road Tracking Improvements

Maritime tracking expands with version 1.0 of the Vessel Tracking API. Developers can implement real-time vessel tracking using enhanced vessel search parameters alongside AIS data capture, with full documentation available on the Developer Portal.

Air freight tracking and scheduling received significant additions. The beta version of the Flight Schedules API lets users query cargo flight timetables across chosen dates, classifying aircraft into freighters, narrow-body, or wide-body setups, and sorting flights by Cargo, Passenger, or Truck types. It includes intermediate loading airports and partner airline schedules, with Lufthansa newly added to the airline list. Air Tracking now supports 448 airlines following the addition of China Postal Airlines and Fly Jinnah. Developer documentation also incorporates event code TGC (Transferred to Customs/Government Control). Contact our team for further details on air freight schedules.

Surface movement updates expand our carrier tracking API features. Road Tracking adds DB Schenker and DSV, bringing the total number of supported road carriers to 5. Event codes and their list now appear in the Developer Portal documentation, alongside the new 'cargo_units' field for retrieving detailed cargo data such as ULD or container numbers via API. Container Tracking API facility detection logic has also been upgraded.

## Geocoding, Routing, and Mapping

Location intelligence tools now process broader geographic data to strengthen multimodal freight visibility. Seaport geocoding gets documentation on the Developer Portal for the World Sea Ports API, which operates within the SeaRates Geocoding API suite to query international seaports using ID, country code, or keyword queries. Complementing this, Geocoding API Autocomplete adds translated descriptions for over 140,000 global seaports across 8 major languages.

Route calculations handle complex legs involving water transit. In the Distance and Time API, location determination logic was upgraded, and the new 'sections' field splits routes into specific legs. Each segment specifies whether transport happens by truck or ferry, supplying transit time, distance, and average speed. Think of this breakdown as an exact blueprint for combined ferry and road journeys. Map display for land and sea transportation has also been added to the Carbon Emissions Calculator.

## Rate Management and AirRates Services

Freight rate inquiries in SeaRates AI now support air, road, and rail rate requests. For company owners using the Virtual Office account, newly published Rate Management System API documentation explains how to review all rates placed by employees from their profiles.

AirRates.com introduced a dedicated Pricing Page. Users can select subscription plans tailored to air logistics needs, with access to tools including Air Tracking, Container Tracking, Load Calculator, Distance & Time, Freight Index, CO2 Calculator, Ship Schedules, and DFA Membership."""

def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

with open('cleaned_original.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

orig_ngrams = get_ngrams(orig_text, 6)
rewrite_ngrams = get_ngrams(body, 6)

overlaps = orig_ngrams.intersection(rewrite_ngrams)
print("Remaining Overlaps Count:", len(overlaps))
for o in overlaps:
    print(" -", o)
