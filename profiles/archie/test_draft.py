import json
import re
from test_aug2024_rewrite import check_all_rules

draft = {
  "title": "SeaRates Development Release: August 2024 Updates",
  "meta_title": "SeaRates August 2024 Freight Platform Updates",
  "meta_description": "Discover SeaRates August 2024 updates, including Load Calculator 2.0, API routing tweaks, expanded tracking for 33 airlines, and new landing pages.",
  "body_markdown": """User feedback drives monthly site improvements across the SeaRates ecosystem. The August 2024 release brings updates to cargo planning, routing algorithms, tracking integrations, and office management tools. Subscribers to SeaRates news receive direct notifications whenever fresh platform updates go live.

## Cargo Calculation Tools

Load Calculator V. 2.0 now uses revised math for packing pipes and boxed goods into containers or trucks. Users can view step-by-step stuffing sequences by opening a downloaded PDF in their browser, complete with Play and Pause animation controls. Calculation results in 3D mode now display specific cargo names alongside structural dimensions. Meanwhile, Load Calculator V. 1.0 web access has updated usage thresholds, offering registered accounts three daily requests and up to twenty unique calculations each month, with customized plans available via email.

## Distance, Time, and Routing APIs

Distance & Time API versions v2 and v3 now feature a ferry_paths parameter to highlight waterborne segments on multi-modal paths. Routing calculations run more accurately when requests name a single destination country. Coordinate searches also pinpoint nearest locations with higher geographic precision.

## Airline and Ocean Carrier Visibility

Air Cargo Tracking logic handles shared IATA Prefix Codes when two different airlines use matching prefixes. Integration coverage expanded to thirty-three additional air carriers: Aercaribe, CMA CGM Air Cargo, Evelop Airlines, Icelandair, Kam Air, Stabo Air Limited, SunClass Airlines, Hong Kong Airlines, Airlink, Binter Canarias, Hainan Airlines, RwandAir, Tianjin Airlines, West Air, Yemen Airways, Air Tahiti Nui, Laparkan Airways, Norse Atlantic Airways, Transportes Aereos Bolivianos, YTO Cargo Airlines, Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, Wizz Air, Air Madagascar, LAM Mozambique Airlines, Nauru Airlines, Air Austral, MIAT Mongolian Airlines, US-Bangla Airlines, Canadian North, and Global Air. Direct system connectivity also improved across twenty existing providers, including Kuwait Airways, Suparna Airlines, DHL Aviation, Air New Zealand, Cathay Pacific Airways, Saudi, Allied Air, El Al Israel Airlines, Batik Air, Qatar Airways, Delta Airlines, SouthWest Airlines, Atlas Air, Singapore Airlines, United Airlines, Finnair, Emirates, TAP Portugal, Air China Cargo, and Air India.

## Container Tracking Engine

Four shipping lines joined the Container Tracking network: Safetrans Line, M-Line, Reel Shipping FZCO, and Hub Shipping. API responses now issue a SEALINE_NOT_SUPPORT_SHIPMENT_TYPE status when selected carriers do not support specific shipment categories. Response generation was refined for vessel names containing FEEDER, BARGE, or TBN, and high-volume queries exceeding one hundred containers under BL or BK numbers process with greater stability. The autodetect engine refined its shipment classification and line identification rules alongside Developer Portal documentation updates.

Web tracking now displays rail legs in distinct colors and supports interface translations across twenty additional languages. The Tracking History API speeds up container lookup queries for bills of lading and booking numbers. Carrier processing performance was upgraded for thirty-three providers: ECU Worldwide, CMA CGM, ZIM, Yang Ming, Avana Global FZCO (BALAJI), Evergreen, W.E.C. (West European Container) Lines, Hyundai Merchant Marine (HMM), Hapag-Lloyd, Shipco Transport, Orient Overseas Container Line (OOCL), Jin Jiang Shipping (SHJJ), Swire Shipping, Atlantic Container Line (ACL), TransContainer, Aladin Express, NewStar, Hellmann Worldwide Logistics, Turkon, Geodis Ocean, Reel Shipping FZCO, Sinokor, Kuehne + Nagel (KN), Westwood Shipping Lines, Hai Hua Shipping (HASCO), DHL Forwarding, Dachser, Emirates Shipping Line, Meratus Line, Pan Continental Shipping, Ocean Network Express (ONE), and COSCO.

## Schedules, Virtual Office, and Platform Updates

Ship Schedules added a port-based search function that gathers arriving and departing vessel movements within chosen timeframes. Dedicated detail pages for port and vessel schedule results allow planners to share specific itineraries with partners, backed by updated Developer Portal documentation. Provider integrations were updated for ZIM, OOCL, PIL, Namsung, and Evergreen by Points.

The iOS mobile app allows direct account login without routing through the main website, including Google single sign-on support. Within Virtual Office, the Access tab now displays paid limits statistics for the Distance & Time tool. Logistics teams can create tariffs for Door-to-Airport and Airport-to-Door routes, with mass export functionality sending tariff data to Logistics Explorer within one hour.

The Freight Index verifies whether selected ocean lines provide local port services to streamline historical data retrieval. Booking API logic was adjusted to process requests for Logistics Explorer API Version 3. CO2 emissions calculations in the Carbon Emissions Calculator were refined across all transport modes, while the Geocoding API and Autocomplete service optimized regional boundary displays and added world regions to query responses.

The IT Quote Request form expanded choices to include Mobile Application Web integration, Enterprise Web integration, Parcel Tracking Web access, Parcel Tracking Web integration, and Parcel Tracking API. Website visitors can request instant call-backs using updated buttons on the Contact Us page, and the Help Center simplified its topic tree for quicker navigation. New landing pages went live for Distance & Time, Vendors - Shipping Line, Affiliate Program, Rate Management System, Freight Index, Transport Management System, and LandRates.com Trucking Companies. Design and copy updates refreshed several landing pages, including Contact Us, About Us, Global Delivery API, Rate Management System API, Smart Documents, SeaRates Vendors, Carbon Emissions Calculator API, For Shippers, For Vendors, IMO Classes, and Ship Schedules API."""
}

if __name__ == "__main__":
    check_all_rules(draft)
