import re

source_text = """May 2025 Development Release: Empowering Business Users

The SeaRates team appreciates your ongoing assistance and input. We update our digital ecosystem with new features and improvements every month, and this month is no exception. We want to highlight the accomplished products we have enhanced. Subscribe to our SeaRates newsletter, and we'll notify you of any updates.

Explore our new features for May and check out the most recent updates for the previous month.

## Facilities Management System
The SeaRates team is proud to announce that our 'Facilities' management panel is available in your Virtual Office profile. Handle any type of warehouse assets in one place: Add, edit, import, and fully account for facilities and offered services you’d like to promote.
Share access with customers and partners to book your warehouse services. Start to streamline your warehouse management, and stay tuned for the upcoming improvements!

## SeaRates Pricing
We are glad to present the newly added Pricing pages for a set of our products. Find your tool and choose the right package tailored to your logistics needs:
- Air Tracking
- Freight Index
- CO2 Calculator
- Ship Schedules
- DFA Membership

## Terminal API
Our team is proud to announce Terminal Tracking API documentation on our Developer Portal. Connect to our database of worldwide terminals for effortless and wide coverage tracking.

## Road Tracking
We’re glad to inform you about the added support for 1 more carrier: Kuehne + Nagel (KN). Find the list of supported carriers via API by following the link.

## Container Tracking
We are glad to present a range of improvements for the 'Exceptions' tab in the Container Tracking tool, namely:
- Optimized logic for processing all 25 exception types
- Added the field with color markers for 'positive' (green mark for earlier arrival) and 'negative' (orange mark for delays) changes with new dates
For API, we have improved the logic for the detection of a container's type and size by description from the shipping line.
Finally, the Predictive ETA logic has also been updated.

## Air Tracking
Our team is happy to announce added support for 2 airlines: My Indo Airlines and Thai Vietair, bringing the total number of supported airlines to 446.

## Ship Schedules
We have updated the credit display in the tool and added a Pricing link to quickly continue your subscription.

## Carbon Emissions Calculator
We have added a subscription button to easily check your credit limits and upgrade your plan for smooth usage of the CO2 Calculator.
Moreover, for API, we have added calculation by Coordinates as an alternative option if there are no results by Carrier.

## Other updates
We are proud to announce the implementation of our own language model for SeaRates AI, as well as improved results processing for freight rate requests with a direct link to the Logistics Explorer.

For the Rate Management System, we have made a range of improvements for the following capabilities:
- Add your tariffs for FCL and FTL by 3 options: ‘Flat’ (full cost), ‘per km’, and ‘flat + per km’; Choose between ft³ and m³ for LCL type;
- Add air tariffs for D2D, D2P, and P2D types;
- Make groups of container types simultaneously (e.g., group 20: 20ST, 20HC, 20REF, etc.);
- Check added tooltips for the columns in the tariff table.

Finally, for Geocoding & Autocomplete, we have made translations into 8 major worldwide languages for 217 capitals, 35,000 seaports, and the top 100 world seaports, as well as improved data search for the top 200+ world seaports.

You’re always welcome to reach out to us for customized digital solutions for logistics via the Request an IT Quote form or by contacting us at sales@searates.com anytime."""

rewrite_text = """Title:
SeaRates May 2025 Release: New Features & Tools

Meta Title:
SeaRates May 2025 Product & API Updates

Meta Description:
Explore SeaRates May 2025 release: Facilities management, 446 supported airlines, new API docs, and AI tools for logistics.

# SeaRates May 2025 Release: New Features & Tools

Logistics software works best when it stays out of your way.

Our May 2025 release delivers practical updates across Virtual Office, tracking APIs, rates, and search tools. If you missed April's release, you can check out those recent updates alongside our latest features. Subscribe to the SeaRates newsletter to receive future updates straight to your inbox.

## Warehouse Facilities in Virtual Office

You can now manage warehouse assets directly inside your Virtual Office profile. The Facilities panel lets you add, edit, import, and track facilities alongside offered services.

You can also share access with customers and partners so they can book warehouse services directly.

## Expanded Tracking and API Documentation

We updated several tracking modules this month.

* **Terminal API:** Terminal Tracking API documentation is live on our Developer Portal. It connects you to our database of worldwide terminals.
* **Air Tracking:** We added support for My Indo Airlines and Thai Vietair. That brings our total supported airline count to 446.
* **Road Tracking:** We added support for Kuehne + Nagel (KN). Check our API documentation to view the full list of supported road carriers.
* **Container Tracking:** The Exceptions tab now uses optimized logic for processing all 25 exception types. A dedicated field displays color markers for new dates: green marks positive changes for earlier arrival, while orange marks negative changes for delays. For API users, container type and size detection from shipping line descriptions is more accurate. We updated Predictive ETA logic too.

## AI Engine, Rates, and Location Data

SeaRates AI now runs on our own language model. Freight rate requests deliver improved results processing with a direct link to Logistics Explorer.

The Rate Management System includes five specific updates:
* Add tariffs for FCL and FTL by three options: 'Flat' (full cost), 'per km', or 'flat + per km'.
* Choose between ft³ and m³ for LCL type.
* Add air tariffs for D2D, D2P, and P2D types.
* Make groups of container types simultaneously (for example, grouping size 20 into 20ST, 20HC, 20REF, and others).
* Check added tooltips for columns in the tariff table.

For Geocoding & Autocomplete, we translated 217 capitals and 35,000 seaports into 8 major worldwide languages, including the top 100 world seaports. Data search also improved for the top 200+ world seaports.

## Pricing and Subscriptions

We added dedicated Pricing pages for five key products:
* Air Tracking
* Freight Index
* CO2 Calculator
* Ship Schedules
* DFA Membership

In the Ship Schedules tool, we updated the credit display and added a Pricing link to quickly continue your subscription. The Carbon Emissions Calculator features a subscription button to check credit limits and upgrade your plan. For API integrations, the CO2 Calculator supports calculation by Coordinates as an alternative option if there are no results by Carrier.

Need customized digital solutions for logistics? Reach out to us via the Request an IT Quote form or contact sales@searates.com anytime."""

# Let's write a clean word-by-word comparison maintaining string positions
words_src = [m.group(0) for m in re.finditer(r'\S+', source_text)]
words_rew = [m.group(0) for m in re.finditer(r'\S+', rewrite_text)]

def clean_word(w):
    return re.sub(r'^[^\w]+|[^\w]+$', '', w).lower()

cleaned_src = [clean_word(w) for w in words_src]
cleaned_rew = [clean_word(w) for w in words_rew]

# Let's find all consecutive matches of length >= 6
matches = []
i = 0
while i < len(cleaned_rew):
    best_len = 0
    best_j = -1
    for j in range(len(cleaned_src)):
        k = 0
        while (i + k < len(cleaned_rew) and j + k < len(cleaned_src) and 
               cleaned_rew[i+k] == cleaned_src[j+k] and cleaned_rew[i+k] != ''):
            k += 1
        if k > best_len:
            best_len = k
            best_j = j
    if best_len >= 6:
        raw_rew = " ".join(words_rew[i:i+best_len])
        raw_src = " ".join(words_src[best_j:best_j+best_len])
        matches.append((best_len, raw_rew, raw_src))
        i += best_len
    else:
        i += 1

print(f"Total 6+ word matches found: {len(matches)}\n")
for idx, (l, r, s) in enumerate(matches, 1):
    print(f"Match {idx} ({l} words):")
    print(f"  Rewrite: {r}")
    print(f"  Source:  {s}\n")

