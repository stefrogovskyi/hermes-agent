import re

rewrite_text = """
Title:
SeaRates Week 11 Updates: New Affiliate Portal and API Tools

Meta-Title:
SeaRates Week 11, 2025: Affiliate Program & Tracking APIs

Meta-Description:
Explore SeaRates Week 11, 2025 updates: launch of affiliate logistics rewards, container tracking API enhancements, and upgraded shipping line integrations.

Full Body Text:
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

# Check for em-dashes and double hyphens
em_dashes = re.findall(r'—|--', rewrite_text)

# Check for common AI clichés (English & Russian AI tells)
ai_cliches = [
    'delve', 'testament', 'game-changer', 'seamless', 'robust', 'elevate', 
    'cutting-edge', 'landscape', 'in conclusion', 'unwavering', 'pleased to announce',
    'in order to', 'it is important to note', 'not only', 'realm', 'beacon',
    'tapestry', 'crucial role', 'vital role', 'paramount', 'furthermore', 'moreover',
    'additionally', 'in summary', 'to summarize'
]

cliche_matches = []
for word in ai_cliches:
    matches = re.findall(rf'\b{re.escape(word)}\b', rewrite_text, re.IGNORECASE)
    if matches:
        cliche_matches.append((word, len(matches)))

print(f"Em-dashes count (— or --): {len(em_dashes)}")
print(f"Clichés found: {cliche_matches}")

