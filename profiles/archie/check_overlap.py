import json
import re

orig_text = """We greatly appreciate your continued support of SeaRates. We are now thrilled to present new updates that will better serve your business needs. Improving our services remains one of our top priorities.

What’s new for week 49:

Tracking System improvements: We have added the Calendar tab with logistics events for your saved shipments in the web tool. For the API, we have improved the logic of location detection. We have improved how we work with providers, including SITC Container Lines, COSCO, Maritime Marfret, Pacific International Lines (PIL), and Hyundai Merchant Marine (HMM).
Air Cargo Tracking updates: We have improved how we work with providers, including FreightAero, CHAMP, Air India, TAP Portugal, FedEx Express, Aeromexico, Cargojet, DHL Aviation, IBS Software App, Etihad Cargo, Cathay Pacific Airways, SmartKargo, Air Canada, Air Arabia, ANA Cargo, China Airlines, Starlux Airlines, Air China Cargo.
Ship Schedules enhancements: We have added support for Kambara Kisen by Vessel. We have also improved how we work with providers, including Hapag-Lloyd, Yang Ming, Crowley, and DSV Ocean by Points, as well as Sinokor by Vessel.
SeaRates Mobile App enhancements: The Air Cargo Tracking tool is now available in the SeaRates Mobile App for iOS and Android. Users can track air shipments by Air Waybill, view detailed status data, access search history, and see route visualization on a world map in real time. Unregistered users in the mobile app have access to up to 5 successful searches per day. Logging in unlocks full search history and additional queries across Air Cargo Tracking, Ship Schedules, and Container Tracking.
Other updates: We created new landing pages for SeaRates AI and Air Cargo Tracking API, and updated the Find a Tool and Vessel Types pages.

Announcements:
New Version of Route Planner API
Freight Index 1.0
Mobile App Version 1.2 with Request System feature
Load Calculator Version 2.2
Map platform"""

with open("/opt/hermes/profiles/archie/test_draft.json") as f:
    draft = json.load(f)

def get_ngrams(text, n=6):
    words = re.sub(r'[^\w\s]', '', text.lower()).split()
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

orig_6grams = set(get_ngrams(orig_text, 6))
draft_6grams = set(get_ngrams(draft["body"], 6))

overlaps = orig_6grams.intersection(draft_6grams)
print(f"6-gram overlaps count: {len(overlaps)}")
for o in overlaps:
    print(f" Overlap: '{o}'")
