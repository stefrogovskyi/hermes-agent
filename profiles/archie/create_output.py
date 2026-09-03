import json

data = {
  "title": "SeaRates Week 34 2024 Updates: Container Loading, Tracking APIs, and Carrier Upgrades",
  "meta_title": "SeaRates Week 34 Updates: Tools & API Upgrades",
  "meta_description": "Explore SeaRates Week 34 updates, featuring Load Calculator V2, air cargo integrations, tracking history API enhancements, and mobile login fixes.",
  "body": "The Load Calculator Version 2 web tool features refined container loading optimization logic for packing pipe and boxed cargo into containers and trucks. Users can download a step-by-step loading sequence as a PDF file and open it in a browser.\n\nAir cargo tracking integration expands with direct support for five airlines: Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, and Wizz Air. Carrier data processing was refined for Batik Air, Qatar Airways, Delta Airlines, and SouthWest Airlines.\n\nFor ocean freight, the Tracking History API query mechanism for container numbers was overhauled to pull complete records across shipments booked under BL and BK numbers. Operational integrations saw enhancements across Reel Shipping FZCO, Sinokor, Hapag-Lloyd, Kuehne + Nagel (KN), Swire Shipping, Westwood Shipping Lines, Hai Hua Shipping (HASCO), Jin Jiang Shipping (SHJJ), CMA CGM, Evergreen, DHL Global Forwarding, Dachser, Emirates Shipping Line, and Meratus Line.\n\nEngineers improved the freight index route calculation and historical data display. For teams using iOS mobile logistics access, the SeaRates Mobile App authorization system now allows direct in-app login without redirecting to the SeaRates website, along with Google account authentication.\n\nThe Request an IT Quote form now includes options for Mobile Application Web integration, Enterprise Web integration, Parcel Tracking Web access, Parcel Tracking Web integration, and the parcel tracking API. Dedicated pages were introduced for the Parcel Tracking API and Distance & Time, alongside updated content and design for the IMO Classes page.\n\nUpcoming developments include Geocoding API / Autocomplete service Version 0.8, a new Version of Route Planner API, the 'Transport' tab in the Logistics Map tool, Freight Index 1.0, Mobile App Version 1.2 with Request System feature, Load Calculator Version 2.2, Booking System Version 1.1, Parcel Tracking API, Rail Tracking API, and the Map platform."
}

with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved output.json")
