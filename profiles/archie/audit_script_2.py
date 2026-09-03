import re

original_text = """
Sophia Shkuro
We are incredibly grateful for your continued support of SeaRates. We are pleased to provide you innovative and enhanced solutions for all of your logistics and trading problems. Improving our services is something we're dedicated to doing.
If you would like the most accurate information, please look at our previous updates.

What’s new for week 11:
We are glad to announce we present the Affiliate program is available in your Virtual Office. Obtain up to a 5% discount just in 24 hours and provide a 5% off for the first bookings of your customers' and partners. Generate unique link to share access and track your bonuses in the Profile. Check all key details with our team to increase the profitability of your Affiliate program.

Tracking System updates:
For the API, we have added a field to the Container events with data about where the event date was received from and improved the logic of obtaining additional data on the vessel.
Moreover, check out the updated Tracking System API documentation on our Developer Portal.
Finally, we have made enhancements to our collaboration with shipping lines, including Atlantic Container Line, Fesco, DB Schenker, Hapag-Lloyd, Shipping Corporation of India (SCI), Jin Jiang Shipping, Interasia Lines, and Kambara Kisen.

Air Cargo Tracking improvements:
We have improved our support for airlines, namely Air China Cargo, Malaysia Airlines, and DHL Aviation.

Ship Schedules enhancements:
We have improved our support for providers, namely PIL for 'by Vessel' and Sinotrans for 'by Ports'.

Other updates:
For the Rate Management System, we have added a link to the Logistics Explorer via ID tariff.
Finally, we have created two landing pages, namely Vehicle & Automotive Shipping Solutions and Pharmaceutical & Healthcare Logistics Solutions.

Announcements:
Unified Tracking System
Vessel Tracking API v1
Logistics Map integration
Logistics Map ‘Warehouse’ tab
SeaRates AI 1.0
Parcel Tracking Web
Load Calculator Web 3.0 (new design and features)
Map Platform
Road Tracking API
"""

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

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

orig_tokens = tokenize(original_text)
rew_tokens = tokenize(rewrite_text)

def get_ngrams(tokens, n=6):
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))

orig_6grams = get_ngrams(orig_tokens, 6)

matches = []
for i in range(len(rew_tokens)-5):
    gram = tuple(rew_tokens[i:i+6])
    if gram in orig_6grams:
        matches.append(" ".join(gram))

# Unique 6-gram matched sequences
unique_matches = sorted(list(set(matches)))
print(f"Total matching 6-gram windows: {len(matches)}")
print(f"Unique matching 6-grams: {len(unique_matches)}")
for m in unique_matches:
    print(" -", m)

