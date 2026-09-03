rewrite = """NEW TITLE: SeaRates Expands Multi-Carrier Tracking to 207 Lines in Week 29 Update
META TITLE: SeaRates Week 29 Updates: Expanded Carrier Tracking
META DESCRIPTION: SeaRates Week 29 release notes: 4 new container lines added (207 total), updated air and rail tracking, new booking dates, and upcoming platform tools.

BODY:
SeaRates integrated four new shipping lines into its container tracking system during Week 29, 2025. The additions of Goodrich Maritime, Transliner, United Africa Feeder Line, and KLN Logistics Group Limited push the platform's total supported container lines to 207.

## Container, Air, and Rail Tracking Enhancements

Along with expanding carrier coverage, technical refinements went live for fourteen existing container lines: Unifeeder, Avana Logistek, Sealead Shipping, Viasea Shipping, DHL Global Forwarding, Blue Water Lines (BWL), Gold Star Line, Hellmann Worldwide Logistics, CMA CGM, Maersk, ZIM, AMASS, Sinotrans Container Lines, and Hapag-Lloyd. The container tracking tool also received updated autodetect logic to improve auto-identification of shipping line tracking numbers.

Intermodal visibility updates extended beyond ocean freight. Air cargo tracking saw data integration improvements for four carriers: FITS Aviation, British Airways, DHL Aviation, and IBC Airways. On rail networks, operational connections were updated for Tiedada Group and KiwiRail.

## Booking System and Financial Management Adjustments

The internal booking workspace introduced targeted interface changes. Users can now inspect paid invoices directly inside the Payment tab. Over on the Tracking tab, two dedicated fields ('Delivery' and 'Empty return') now display specific timestamps for cargo drop-off and empty container return. The Finance tab underwent background updates to streamline ledger displays.

## Upcoming Platform Capabilities

Engineering teams are finalizing several tools scheduled for near-term deployment:

* Logistics Map 'Warehouse' tab
* Load Calculator Web 3.0 featuring a revised interface and calculation engine
* Dedicated Map Platform
* AI Assistant integrated directly into Ship Schedules
* Unified Inbox connected with Logistics Explorer, Bookings, and Notifications"""

print("Em-dash (—):", rewrite.count("—"))
print("En-dash (–):", rewrite.count("–"))
print("Double-dash (--):", rewrite.count("--"))
print("Connectors count:")
for conn in ["Furthermore", "Moreover", "In addition", "Additionally", "Consequently", "On the other hand", "It is important to note"]:
    print(f"  {conn}: {rewrite.count(conn)}")

