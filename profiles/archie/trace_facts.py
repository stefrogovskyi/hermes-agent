source = """Title: SeaRates Updates - Week 46, 2024

We are grateful for your ongoing support of SeaRates and eager to introduce new products that will further satisfy you. Enhancing our services is a top focus for us. For the most recent information, see our previous releases.

What’s new for week 46:

Tracking System improvements.
For the web version, we’ve updated the design and functionality.
For the API connection, we have improved the logic for retrieving additional vessel data and implemented a new formula for predictive ETA.
We’ve also enhanced our collaboration with providers, including COSCO, NVO Consolidation Lines, Westwood Shipping Lines, and Evergreen.

Air Tracking enhancements.
We’ve added support for Aloha Air Cargo and Corendon Dutch Airlines, bringing the total number of supported airlines to 436.
Additionally, we’ve improved our work with providers like China Airlines, Kenia Airways, Japan Airlines, TAP Portugal, China Southern Airlines, Air India, Silk Way West Airlines, and Lufthansa Cargo.

Virtual Office Dashboard updates.
We've added more booking analytics. Now, when you switch between the Active Bookings and Requests tabs, the data updates both on the map and in the Overview by Shipping Type chart.
Additionally, under the More Info section from the Bookings Overview by Shipping Type chart, you can now see extended analytics, including: Bookings by Countries, Mode of Transport, Shipping Type, and Route.

Other updates:
We have implemented the ability to create a cover image (thumbnail) for a transport unit in the Logistics Map and TMS tools.
We added DFA ERP to the Integration tab, making it easier to request a quote for these services.

Announcements:
- Calendar tab in Tracking System tool
- New Version of Route Planner API
- Freight Index 1.0
- Mobile App Version 1.2 with Request System feature
- Load Calculator Version 2.2
- Booking System Version 1.1
- Map platform"""

# Check each entity / carrier in source vs draft
carriers_source = [
    "COSCO", "NVO Consolidation Lines", "Westwood Shipping Lines", "Evergreen",
    "Aloha Air Cargo", "Corendon Dutch Airlines", "China Airlines", "Kenia Airways",
    "Japan Airlines", "TAP Portugal", "China Southern Airlines", "Air India",
    "Silk Way West Airlines", "Lufthansa Cargo", "DFA ERP"
]

draft = """Title: SeaRates Updates: Week 46, 2024 Product Improvements
Meta Title: SeaRates Week 46, 2024 Updates and System Releases
Meta Description: Check out SeaRates Week 46 updates: Tracking System API upgrades, Virtual Office dashboard analytics, new air tracking carriers, and upcoming tools.

Body:
Here is the latest round of product updates for week 46 of 2024 across SeaRates systems and integrations.

### Tracking System Upgrades

The web version features refreshed interface design and updated functionality. On the API side, updated logic now handles additional vessel data retrieval, paired with a revised predictive ETA formula. Carrier data handling has been refined for COSCO, NVO Consolidation Lines, Westwood Shipping Lines, and Evergreen.

### Air Tracking Expansions

Aloha Air Cargo and Corendon Dutch Airlines are now supported, expanding the total network to 436 airlines. Performance and data processing have been updated for several existing carriers: China Airlines, Kenia Airways, Japan Airlines, TAP Portugal, China Southern Airlines, Air India, Silk Way West Airlines, and Lufthansa Cargo.

### Virtual Office Dashboard Analytics

The dashboard now provides expanded booking analytics. Switching between the Active Bookings and Requests tabs automatically refreshes the map display alongside the Overview by Shipping Type chart.

Opening the More Info section inside the Overview by Shipping Type chart reveals broken-down metrics:
* Bookings by Countries
* Mode of Transport
* Shipping Type
* Route

### Logistics Map, TMS, and ERP Integration

Logistics Map and TMS tools now support thumbnail cover images for individual transport units. The Integration tab includes DFA ERP, allowing users to submit quote requests directly for these services.

### Upcoming Releases

Work continues on several upcoming features and system versions:
* Calendar tab in the Tracking System tool
* Updated Route Planner API version
* Freight Index 1.0
* Mobile App Version 1.2 containing the Request System feature
* Load Calculator Version 2.2
* Booking System Version 1.1
* Map platform"""

print("--- CARRIER / ENTITY AUDIT ---")
for c in carriers_source:
    in_draft = c in draft
    print(f"{c}: {'PRESENT' if in_draft else 'MISSING'}")

# Metric check
print("\n--- METRICS CHECK ---")
print("436 airlines:", "436" in draft)

