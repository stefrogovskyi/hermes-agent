import re

original = """We highly appreciate your support and loyal feedback about SeaRates products and services. With your participation, our team continuously upgrades the digital and traditional logistics every week. Let’s find out development insights on our improvement this month:

## Road Tracking
Monitor your road cargo in real-time 24/7 just by entering the equipment ID received from your carrier into the Road Tracking tool available on LandRates.com. Get logistics events, live updates on any shifts, and shipment statuses in a few seconds.
Also, we have updated the Road Tracking API documentation. Find out the integration options on our Developer Portal.

## Demurrage & Storage Calculator
We’ve added tariffs for the Evergreen shipping line to accurately calculate your demurrage and storage rates for shipments carried by this shipping line in the tool.
Also, we have updated the API documentation by implementing the option to receive the ID port data by country, LOCODE, or coordinates.

## Container Tracking
We're glad to announce newly added support for 3 shipping lines: Danmar Lines, Ti2 Container Lines, and Famous Pacific Shipping, bringing the total number of supported shipping lines to 218.
For the web version, we've enhanced integration with Route Planner for accurate monitoring by track numbers generated in this tool.
For the API, we have upgraded documentation, as well as added the display of shipments with the CANCELLED status to the History API.

## Air Tracking
Our team is glad to announce the addition of support for Air Corsica, Hong Kong Express, and Jazeera Airways, bringing the total number of supported airlines to 445.
Moreover, we have updated the API for smoother data retrieval from airlines.

## Load Calculator
We’ve improved our Load Calculator by adding an Auto count checkbox for automatic calculation of the number of containers. This allows you to select one or more container types for loading estimation.

## Ship Schedules
We are glad to present added support for Hoegh Autoliners, AEL, and Tailwind by Points and by Vessel accordingly.

## Geocoding
We have made a range of key upgrades for the Geocoding API to ensure smooth autocomplete and stable integration with all SeaRates products.
Also, we have added several abilities, namely:
- filtering options, such as showing only seaports, airports, countries, or cities
- postcodes for various countries in the database
- 611 alternative UN/LOCODES synced with the Tracking database
Find the updated API documentation and integration options here.

## Other updates
For the Individual Quotes, our team has made a few improvements, including an improved tariff page, added a schedule request to choose the right timeline for booking creation, and added a detailed map section.
For the Rate Management System (RMS), the ability to copy links to individual tariffs for all types of transportation and the option to sort port tariffs by the Pet lot parameter were added.
For the Carrier Directory, we’ve added a new design for shipping lines' pages. To find the Carrier Directory, open the top drop-down menu and go to the References section.
Finally, guide your logistics operations and find any answers about our tools and services in our upgraded Help Center.
We’re loving your feedback and questions! Feel free to ask us at it.sales@searates.com. Let’s address your business needs with customized logistics solutions."""

draft = """Title: SeaRates October 2025 Release: New Features & Updates
Meta Title: SeaRates October 2025 Updates: Tracking, APIs & Tools
Meta Description: Discover SeaRates October 2025 updates with expanded carrier support, API upgrades, geocoding additions, and enhanced planning tools.

Body:
October brought a fresh set of updates across the SeaRates platform, covering tracking tools, API documentation, and daily rate management features. Here is a breakdown of what moved into production this month.

### Real-Time Road Cargo Tracking

LandRates.com now gives operators real-time shipment monitoring 24/7 for road cargo. By entering the equipment ID provided by your carrier into the Road Tracking tool, you can pull logistics events, schedule shifts, and shipment status changes in seconds.

Developers integrating road freight workflows will also find updated Road Tracking API documentation on our Developer Portal.

### Ocean Container and Air Tracking Expansion

Expanding multi-carrier shipping API integration across ocean and air routes remains a core focus. This month we added support for three ocean carriers: Danmar Lines, Ti2 Container Lines, and Famous Pacific Shipping. That brings our ocean coverage to 218 supported shipping lines.

On the web platform, container tracking now connects directly with Route Planner to monitor shipments using track numbers generated inside that tool. For API users, we upgraded documentation and updated the History API to display shipments marked with CANCELLED status.

For logistics teams managing ocean supply chains, standardized freight tracking data makes operational visibility far easier to maintain.

Air tracking expanded as well. With the addition of Air Corsica, Hong Kong Express, and Jazeera Airways, SeaRates now supports 445 airlines. Data retrieval calls through the Air Tracking API were also refined for quicker execution.

### Demurrage, Schedules, and Load Planning

The Demurrage & Storage Calculator now includes tariffs for Evergreen shipments. We also updated the tool's API so users can fetch port ID data filtered by country, LOCODE, or geographical coordinates.

For vessel schedules, support was added for Hoegh Autoliners, AEL, and Tailwind, with search capabilities available by Points and by Vessel depending on carrier data structures.

We updated the Load Calculator to streamline container load optimization when preparing cargo shipments. A new Auto count checkbox automatically calculates the required number of containers based on one or several selected container types.

### Geocoding Database and API Enhancements

Location matching sits behind almost every operational workflow. Our updated UN/LOCODE geocoding database now syncs 611 alternative codes directly with our Tracking database to keep location records consistent.

Key upgrades to the Geocoding API improve autocomplete stability across all SeaRates tools. New capabilities include:

* Category filters to narrow searches to seaports, airports, countries, or cities
* Postcode coverage for multiple countries across the database
* Synced UN/LOCODE entries for improved cross-tool accuracy

Revised API documentation and integration guides are available on the Developer Portal.

### Quoting, RMS, and Platform Usability

Several workspace tools received functional updates this month:

* **Individual Quotes:** Redesigned tariff pages, a schedule request option to select booking timelines, and a detailed map view.
* **Rate Management System (RMS):** Direct link copying for individual tariffs across all transport modes, plus sorting for port tariffs by Pet lot parameter.
* **Carrier Directory:** Updated page design for shipping lines, accessible under References in the top drop-down menu.
* **Help Center:** Upgraded documentation and search guides for faster troubleshooting.

Questions or feedback on custom integrations can be sent directly to our team at it.sales@searates.com."""

with open('/opt/hermes/profiles/archie/source.txt', 'w') as f:
    f.write(original)

with open('/opt/hermes/profiles/archie/draft.txt', 'w') as f:
    f.write(draft)

print("Files written successfully.")
