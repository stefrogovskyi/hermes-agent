import re

original = """The SeaRates team truly values your continued feedback and support. We add new features and make the site better every month, and this month is no different. We would like to highlight what we've successfully completed. If you sign up for our SeaRates news, we will let you know when there is a new update.
You're welcome to take a look at the new functionalities.
Load Calculator
We are glad to announce a range of updates to
Load Calculator V. 2.0
:
improved logic for loading your pipe and boxed cargo into containers and trucks.
added the ability to view the step-by-step loading of cargo by downloading a PDF file and opening it in a browser
implemented loading animation to adjust loading steps visualizing by the ‘Play’ and ‘Pause’ buttons
added cargo names displayed when viewing 3D calculation results
Moreover, we have added limits for the web version of the Load Calculator V. 1.0 tool. Authorized users have free access with 3 requests daily and up to 20 unique stuffing calculations per month. Get your individual quotation plan by reaching out to us at sales@searates.com.
Distance & Time
For API v2 and API v3, we have added a new ‘ferry_paths’ parameter to display route segments ferry transport type used in.
Also, we have improved routing logic in case you specify only one country in the request.
Finally, we have enhanced the logic of the nearest location determination for searched coordinates.
Air Cargo Tracking
We released API request processing logic when 2 different airlines have the same IATA Prefix Code.
We are glad to announce added support for 33 airlines: Aercaribe, CMA CGM Air Cargo, Evelop Airlines, Icelandair, Kam Air, Stabo Air Limited, SunClass Airlines, Hong Kong Airlines, Airlink, Binter Canarias, Hainan Airlines, RwandAir, Tianjin Airlines, West Air, Yemen Airways, Air Tahiti Nui, Laparkan Airways, Norse Atlantic Airways, Transportes Aereos Bolivianos, YTO Cargo Airlines, Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, Wizz Air, Air Madagascar, LAM Mozambique Airlines, Nauru Airlines, Air Austral, MIAT Mongolian Airlines, US-Bangla Airlines, Canadian North, and Global Air.
Finally, we have improved how we work with providers, including Kuwait Airways, Suparna Airlines, DHL Aviation, Air New Zealand, Cathay Pacific Airways, Saudi, Allied Air, El Al Israel Airlines, Batik Air, Qatar Airways, Delta Airlines, SouthWest Airlines, Atlas Air, Singapore Airlines, United Airlines, Finnair, Emirates, TAP Portugal, Air China Cargo, and Air India.
Tracking System
Added support for 4 shipping lines: Safetrans Line, M-Line, Reel Shipping FZCO, and Hub Shipping.
For the API, we have implemented a range of improvements, including:
Added a new status ‘SEALINE_NOT_SUPPORT_SHIPMENT_TYPE’ to respond to chosen shipment types that are currently not supported by the particular shipping lines
Enhanced the response generation logic if the vessel’s name is received from the line containing one of the words — FEEDER, BARGE, or TBN
Enhanced the result processing for requests by BL/BK when the number of containers exceeds 100
Updated the autodetect service for the logic of shipment type and shipping line determining, as well as routing logic
Updated documentation on our Developer Portal
For the web version, we have released rail route sections displayed in different colors, as well as implemented interface translation into an additional 20 languages.
For the Tracking History API, we have improved the container number query process for all shipments under BL and BK numbers.
Finally, we have improved how we work with providers, including ECU Worldwide, CMA CGM, ZIM, Yang Ming, Avana Global FZCO (BALAJI), Evergreen, W.E.C. (West European Container) Lines, Hyundai Merchant Marine (HMM), Hapag-Lloyd, Shipco Transport, Orient Overseas Container Line (OOCL), Jin Jiang Shipping (SHJJ), Swire Shipping, Atlantic Container Line (ACL), TransContainer, Aladin Express, NewStar, Hellmann Worldwide Logistics, Turkon, Geodis Ocean, Reel Shipping FZCO, Sinokor, Kuehne + Nagel (KN), Westwood Shipping Lines, Hai Hua Shipping (HASCO), DHL Global Forwarding, Dachser, Emirates Shipping Line, Meratus Line, Pan Continental Shipping, Ocean Network Express (ONE), and COSCO.
Ship Schedules
We are glad to announce an implemented search for schedules by Port to receive sailing data for a specific port, including all vessels arriving and departing from that port within a specified time frame.
Also, we have added details pages for schedules by Port and by Vessel to share particular schedule results. Get updated API documentation by the link.
Finally, we have improved how we work with providers, including ZIM, OOCL, PIL, Namsung, and Evergreen by Points.
SeaRates Mobile App
We have updated the authorization system for iOS users by adding the ability to log in to the application without going to the SeaRates website, as well as the ability to log in via your Google account.
Virtual Office
For the ‘Tools’ section, we have implemented the ability to view paid limits statistics for the Distance & Time tool under the ‘Access’ tab.
For the ‘Rates and tariffs’ section, we have added the option to create tariffs for Door-to-Airport and Airport-to-Door delivery. Also, we have implemented the functionality of mass downloading for such tariffs to be displayed in the Logistics Explorer tool in one hour.
Other updates
For the Freight Index, we have verified whether the selected carrier is capable of offering port services upon request. This facilitates a smoother search for historical data.
For the Booking API, we have made several updates, including creation of a new request for the Logistics Explorer API Version 3.
For the Carbon Emissions Calculator, we have improved CO2 emissions calculations for all shipping types.
For the Geocoding API / Autocomplete service, we have optimized the display of regional borders as well as added world regions to API query results.
For the Request an IT Quote form, we added Mobile Application Web integration, Enterprise Web integration, Parcel Tracking Web access, Parcel Tracking Web integration, and Parcel Tracking API to provide you with the ability to quickly request a customized price quote for your chosen SeaRates IT tool.
Moreover, we have improved the Contact Us form with the option to be called by clicking on the buttons on the website’s pages, as well as updated the Help Center with a simplified display of categories and questions for easy access to questions you are interested in.
We are excited to introduce a range of newly created landing pages, including Distance & Time, Vendors – Shipping Line, Affiliate Program, Rate Management System, Freight Index, and Transport Management System, as well as Trucking Companies pages for LandRates.com.
Finally, we have upgraded the content and design to Contact Us, About Us, Global Delivery API, Rate Management System API, Smart Documents, SeaRates Vendors, Carbon Emissions Calculator API, ‘For Shippers’, ‘For Vendors’, IMO Classes, and Ship Schedules API landing pages."""

candidate = """Title: SeaRates Development Release: August 2024 Updates
Meta Title: SeaRates August 2024 Freight Platform Updates
Meta Description: Discover SeaRates August 2024 updates, including Load Calculator 2.0, API routing tweaks, expanded tracking for 33 airlines, and new landing pages.

Body:
User feedback drives monthly site updates across the SeaRates platform. The August 2024 release brings improvements to cargo planning, routing calculations, tracking integrations, and office management tools. Subscribers to SeaRates news receive direct notifications whenever fresh platform updates go live.

## Cargo Calculation Tools

Load Calculator V. 2.0 features updated logic for packing pipe and boxed cargo into containers and trucks. Step-by-step loading sequences can be saved by downloading a PDF file and opening it in a browser. Interactive loading animations allow users to adjust step-by-step visuals with Play and Pause buttons. Viewing 3D calculation results now displays cargo names alongside visual dimensions. Usage limits apply to the web version of Load Calculator V. 1.0, where authorized users receive free access for 3 daily requests and up to 20 unique stuffing calculations per month. Individual quotation plans are available by contacting sales@searates.com.

## Distance, Time, and Routing APIs

Distance & Time API v2 and API v3 introduced a new ferry_paths parameter to highlight route segments utilizing ferry transport. Routing logic handles requests more smoothly when specifying only one country. System logic for identifying nearest locations from searched coordinates was also upgraded.

## Airline and Ocean Carrier Visibility

Air Cargo Tracking API logic handles shared IATA Prefix Codes when two different airlines use matching prefixes. Integration coverage expanded to 33 additional air carriers: Aercaribe, CMA CGM Air Cargo, Evelop Airlines, Icelandair, Kam Air, Stabo Air Limited, SunClass Airlines, Hong Kong Airlines, Airlink, Binter Canarias, Hainan Airlines, RwandAir, Tianjin Airlines, West Air, Yemen Airways, Air Tahiti Nui, Laparkan Airways, Norse Atlantic Airways, Transportes Aereos Bolivianos, YTO Cargo Airlines, Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, Wizz Air, Air Madagascar, LAM Mozambique Airlines, Nauru Airlines, Air Austral, MIAT Mongolian Airlines, US-Bangla Airlines, Canadian North, and Global Air. System processing improved across 20 existing air providers: Kuwait Airways, Suparna Airlines, DHL Aviation, Air New Zealand, Cathay Pacific Airways, Saudi, Allied Air, El Al Israel Airlines, Batik Air, Qatar Airways, Delta Airlines, SouthWest Airlines, Atlas Air, Singapore Airlines, United Airlines, Finnair, Emirates, TAP Portugal, Air China Cargo, and Air India.

## Container Tracking Engine

Four shipping lines joined the Container Tracking network: Safetrans Line, M-Line, Reel Shipping FZCO, and Hub Shipping. API responses now issue a SEALINE_NOT_SUPPORT_SHIPMENT_TYPE status when selected carriers do not support specific shipment categories. Response generation was refined for vessel names containing FEEDER, BARGE, or TBN, while requests by BL/BK exceeding 100 containers process with higher reliability. The autodetect service refined its shipment classification, shipping line determination, and routing logic alongside Developer Portal documentation updates.

Web tracking displays rail route sections in distinct colors and supports interface translation into an additional 20 languages. The Tracking History API refined container number queries for shipments under BL and BK numbers. Carrier processing performance was upgraded for 33 providers: ECU Worldwide, CMA CGM, ZIM, Yang Ming, Avana Global FZCO (BALAJI), Evergreen, W.E.C. (West European Container) Lines, Hyundai Merchant Marine (HMM), Hapag-Lloyd, Shipco Transport, Orient Overseas Container Line (OOCL), Jin Jiang Shipping (SHJJ), Swire Shipping, Atlantic Container Line (ACL), TransContainer, Aladin Express, NewStar, Hellmann Worldwide Logistics, Turkon, Geodis Ocean, Reel Shipping FZCO, Sinokor, Kuehne + Nagel (KN), Westwood Shipping Lines, Hai Hua Shipping (HASCO), DHL Global Forwarding, Dachser, Emirates Shipping Line, Meratus Line, Pan Continental Shipping, Ocean Network Express (ONE), and COSCO.

## Schedules, Virtual Office, and Platform Updates

Ship Schedules added a port-based search function that gathers arriving and departing vessel movements within specified timeframes. Dedicated detail pages for port and vessel schedule results allow planners to share specific itineraries, backed by updated Developer Portal documentation. Provider integrations were updated for ZIM, OOCL, PIL, Namsung, and Evergreen by Points.

The iOS mobile app authorization system lets users log in without visiting the SeaRates website, adding support for Google account login. Within Virtual Office, the Access tab under the Tools section displays paid limits statistics for the Distance & Time tool. In Rates and tariffs, logistics teams can create tariffs for Door-to-Airport and Airport-to-Door delivery, with mass downloading functionality sending tariff data to Logistics Explorer within one hour.

The Freight Index verifies whether selected carriers offer port services upon request to assist historical data searches. Booking API logic was adjusted to process requests for Logistics Explorer API Version 3. Carbon Emissions Calculator CO2 calculations were refined across all shipping types. The Geocoding API and Autocomplete service optimized regional border displays and added world regions to API query results.

The Request an IT Quote form added Mobile Application Web integration, Enterprise Web integration, Parcel Tracking Web access, Parcel Tracking Web integration, and Parcel Tracking API for customized pricing. Website visitors can request calls by clicking buttons on website pages, while the Help Center simplified category and question displays. New landing pages launched for Distance & Time, Vendors - Shipping Line, Affiliate Program, Rate Management System, Freight Index, Transport Management System, and LandRates.com Trucking Companies. Design and content updates refreshed landing pages for Contact Us, About Us, Global Delivery API, Rate Management System API, Smart Documents, SeaRates Vendors, Carbon Emissions Calculator API, For Shippers, For Vendors, IMO Classes, and Ship Schedules API."""

print("Loaded texts.")
