import re

source_text = """
December 2024 Development Release: Empowering Business Users | SeaRates Blog Post

Your ongoing support and feedback are much appreciated. Our monthly updates to the website continue with the addition of new features and enhancements. Here are some of the products we've improved and tools we've launched that we think you'll find interesting. Stay updated with SeaRates by subscribing to our newsletter. You are welcome to investigate the updated options.

Tracking System
We are delighted to announce added support for Cosco Specialized and Dole Ocean Cargo Express, bringing the total amount of supported shipping lines to 180.
Furthermore, to the web access, we have added the Calendar tab to check logistics events out on your saved shipments.
Finally, we have improved the logic of location detection in the API.

Air Cargo Tracking
We are glad to inform you about added support for 4 airlines, including Aercaribe Peru, Air Cote D'Ivoire, Akasa Air, and Vensecar Internacional.
Also, you can check the newly added list and description for response statuses for the API documentation in our Developer Portal.

Route Planner
We are delighted to present a release of the Route Planner API. Explore a prompt and extended API for creating, editing, reviewing, and managing your own shipping routes. Simply add any details for routes: locations with types (seaport, airport, road/rail terminal), logistics events for each of them, and transport types in detail. Each custom route option has a unique ID number for easy sharing with customers and accessing tracking via the Tracking System tool.
Moreover, we have improved the API with the ability to complete routing and add details for each location if needed automatically. Kindly check the API documentation in our Developer Portal.

Ship Schedules
We are glad to introduce the added support to Ignazio Messina and Pacific Forum Line by Port.
Additionally, we have added the option to request schedules by alternative SCAC values.

SeaRates Mobile App
We are glad to present the Air Cargo Tracking tool in our mobile app. Simply track your air freight by AWB number with real-time data, access to history research, and route visualization on the world map directly via the app. Download for iOS or Android to access the Air Cargo Tracking tool through the app.
Up to 5 successful searches per day are available to unregistered users of the SeaRates Mobile App. Your search history in Air Cargo Tracking, Ship Schedules, and Container Tracking will be accessible once you log in.

Demurrage & Storage Calculator
We are happy to announce the Demurrage & Storage Calculator API.
For the API, we have added upgraded documentation, which you can find in our Developer Portal.
Moreover, find the updated web version with newly released options, namely the ability to check date availability, choose currency and calculation cost for import and export modes, and download calculation results in PDF format for further analytics.

Virtual Office
For the 'Bookings' tab, you can add more data to transport details in any shipping mode with our updated logic.
For the 'Counterparties' panel, we have improved generation for the invite link. The link is generated using the SeaRates.com domain or the user's platform domain as an owner of the platform with Counterparties integrated.

Other updates
We are glad to announce the web-integrated version of the Request a Quote. Kindly check the Developer Portal to get the integration code.
Finally, we have improved the Geocoding API database with 18,000 seaports across the world, synchronized with information from the World Sea Ports app.
"""

draft_text = """
Title: SeaRates December 2024 Release Notes: API Expansion and Platform Updates
Meta Title: SeaRates December 2024 Product Updates
Meta Description: SeaRates expanded carrier connections to 180, launched the Route Planner API, brought AWB tracking to mobile, and upgraded Virtual Office in December 2024.

Body Text:
SeaRates updated its core logistics tools and developer APIs in December 2024, expanding carrier tracking connections while introducing new route planning features.

### Container and Vessel Tracking
Ocean freight tracking now covers Cosco Specialized and Dole Ocean Cargo Express, bringing total supported carriers to 180. Users managing shipments on the container tracking web portal can view logistics milestones directly on a new Calendar tab. On the backend, the multi-carrier visibility API received updated location detection logic for precise event positioning.

Vessel schedule queries now accept Ignazio Messina and Pacific Forum Line by port. Users can also run schedule searches using alternative SCAC codes.

### Air Cargo Tracking
Air freight coverage grew to include four additional carriers: Aercaribe Peru, Air Cote D'Ivoire, Akasa Air, and Vensecar Internacional. Developers working with air cargo endpoints can review newly added status codes and response definitions in the Developer Portal.

Air freight visibility is also live on the SeaRates mobile app for iOS and Android. The mobile tool delivers real-time air freight AWB tracking with world map route visualization and search history. Unregistered users receive five free searches per day. Logging into an account restores saved search history for container tracking and ship schedules, alongside air cargo queries.

### Intermodal Route Planner API
The release of the Route Planner API gives logistics teams programmatic control over custom route builds within their intermodal route planning software. Users can define custom legs across seaports, airports, plus road and rail terminals. Each node supports specific transport modes and event milestones.

Every custom route generates a unique ID number. This ID simplifies sharing with customers and enables quick lookup in the Tracking System. The API can also complete routing structures automatically and populate missing location details upon request.

### Demurrage & Storage Calculator
Fee estimation tools received a dedicated backend. The Demurrage & Storage Calculator API is now live, accompanied by expanded documentation in the Developer Portal.

The web calculator updated its interface to support demurrage and storage risk calculation. Users can check valid date ranges, select import or export modes, calculate costs in preferred currencies, and download summary reports as PDF files.

### Virtual Office and Infrastructure
Workflow updates affected two Virtual Office modules:
* **Bookings Tab:** Updated logic supports additional data fields within transport details across every shipping mode.
* **Counterparties Panel:** Link generation logic was updated. Invite links now issue under SeaRates.com or under a client's custom platform domain.

Developer infrastructure received two final enhancements. SeaRates released a web-integrated Request a Quote component, adding ready-to-use snippets to the logistics API integration workflow. In addition, the Geocoding API database expanded to 18,000 global seaports, fully synchronized with data from the World Sea Ports app.
"""

print("Check terms in source vs draft:")

terms_to_check = [
    "intermodal",
    "risk",
    "dedicated backend",
    "multi-carrier visibility",
    "precise event positioning",
    "programmatic control",
    "node",
    "legs"
]

for t in terms_to_check:
    in_source = t in source_text.lower()
    in_draft = t in draft_text.lower()
    print(f"Term '{t}': in_source={in_source}, in_draft={in_draft}")

