import re

rewrite_text = """
Sophia Shkuro here with our product release notes for Week 11 of 2025. Our engineering team spent the past seven days expanding developer tools, refining data sources, and opening up new earning options in your account dashboard.

### Affiliate Program Launch

You can now access our Affiliate program directly inside your Virtual Office. When you share access with customers or business partners using your unique link, they get 5% off their first freight bookings. In turn, you earn bonuses tracked straight in your Profile, alongside discounts reaching up to 5% within 24 hours. Talk with our team if you want to optimize your affiliate logistics rewards.

### Tracking System API Upgrades

We added a dedicated field to Container events inside the API. This field shows exactly where the event timestamp originated. We also reworked how our system pulls additional vessel details to support accurate real-time freight tracking across active routes.

If you build tools on top of our infrastructure, check out the updated documentation on the Developer Portal. We also upgraded our data connections for our container tracking API and expanded vessel tracking integration across several ocean carriers:

* Atlantic Container Line
* Fesco
* DB Schenker
* Hapag-Lloyd
* Shipping Corporation of India (SCI)
* Jin Jiang Shipping
* Interasia Lines
* Kambara Kisen

### Air Cargo and Schedule Revisions

Air cargo coverage expands this week with better data processing for three carriers: Air China Cargo, Malaysia Airlines, and DHL Aviation.

On the Ship Schedules side, we updated provider integrations to sharpen overall supply chain visibility. PIL now has stronger support under the 'by Vessel' search option, while Sinotrans received updates under the 'by Ports' query mode.

### Rate Management and Solutions Pages

Inside the Rate Management System, tariffs now link directly to Logistics Explorer using their unique tariff ID. 

We also published two specialized landing pages for sector-specific operations:

* Vehicle & Automotive Shipping Solutions
* Pharmaceutical & Healthcare Logistics Solutions

### What We Are Working On Next

Here is what our development team is building for upcoming releases:

* Unified Tracking System
* Vessel Tracking API v1
* Logistics Map integration
* Logistics Map 'Warehouse' tab
* SeaRates AI 1.0
* Parcel Tracking Web
* Load Calculator Web 3.0 featuring a redrawn interface and extra calculation tools
* Map Platform
* Road Tracking API

Refer to our earlier weekly posts if you need historical reference data or older platform changes.
"""

# Check for contrastive negations
# Patterns like "not X, Y", "X, not Y", "not X but Y", "instead of", "rather than"
negations = re.findall(r'\b(not|instead of|rather than|n\'t)\b', rewrite_text, re.IGNORECASE)
print(f"Negation words found: {negations}")

# Print lines containing negation words
lines = rewrite_text.split('\n')
for line in lines:
    if any(w in line.lower() for w in ['not', 'instead', 'rather']):
        print("Line with negation:", line)

# Connectors check
connectors = ['that\'s why', 'which is why', 'this is why', 'as a result', 'therefore', 'thus', 'consequently', 'in turn', 'which explains']
for conn in connectors:
    matches = re.findall(rf'\b{re.escape(conn)}\b', rewrite_text, re.IGNORECASE)
    if matches:
        print(f"Connector found: '{conn}' ({len(matches)} times)")

