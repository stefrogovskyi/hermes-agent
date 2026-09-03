import re

orig = """Title: Big Guide: How to Use Ship Schedules? Manage Shipments by Points, Vessels, and Ports

We are pleased to introduce the SeaRates Big Guide on how to streamline shipping planning with the Ship Schedules tool to save precious resources and enjoy surprise-free planning with no extra effort.

Make a major breakthrough as a logistics provider or shipper — know up-to-the-minute insights on schedules for worldwide destinations by points, specific vessels, or ports you will ever need.

Let’s start smart logistics planning with a single tool — oversee more than 15 million schedules from world-trusted carriers, cover 95K+ voyages, 6K+ seaports, 180K+ port pairs, and 5K+ vessels data in one place. Find the best routes and shipping lines, increase delivery speed, and plan to scale your trade with accurate forecasting. Today, you’ll discover the way to empower your trading with data-backed decisions.

Keep tuned for a functionality overview in our article!

How does the tool work?
Sign up here to get up to 5 free daily searches for schedules and up to 20 unique ones monthly. Get your subscription plan to adjust the number of searches.
Let us know about your intention for your own Ship Schedules tool and get a customized solution to meet your needs.

Let's take a closer look at the tool’s functionality.

1. Here’s the first tab of Ship Schedules — search schedules by Points :
Simply enter the points of the route for which you planned shipments;
Find the right timelines on the Calendar;
Set Other parameters — choose how you want to filter schedules: by Shipping Line, Arrival date, Departure date, Transit time, or direct routes (without Transshipments);
And click Search to review options.

You'll see all available shipping lines for your route with Departure date, Transit time, Arrival date, Transshipment ports, and Vessel name for each line option. Also, under each option, you will find a link to the Logistics Explorer for instant freight rate calculation. To select a vessel, click on its name to navigate to Vessel Tracking or click on the Shipping Line logo to review all available schedules for this carrier. To sort schedule search results, click on transit time, vessel name, or dates.
You can clear all or selected filters anytime to restart the search.
Need to download, copy, or print schedule search results? Click on the three dots icon in the top right corner of the results tab to easily export options.

2. Need to track a specific vessel schedule? Turn to the Vessel tab:
Type the Vessel name or IMO;
Set the vessel schedule search parameters: specify Departure date and Shipping line;
And click Search .

Now you can review vessel details: Vessel name, Flag, IMO, MMSI, Built year, Vessel type, Capacity (TEU), and Length (m).
For full information about the vessel and its location, click on the Vessel details button to open the Vessel Tracking tool in a new tab.
Below the vessel details, check out the vessel schedule table — Departure and Arrival ports with corresponding ETS/ATD and ETA/ATA dates, along with direct links to Port Schedules.
Need to adjust or clear filters? Modify the parameters anytime in the top search panel. You can also print, copy, or download the results using the three dots icon.

3. Want to view all arrivals and departures at a specific port? Use the Ports tab:
Type the Port name or UN/LOCODE;
Select a country, specify the dates in the Calendar, and choose a Shipping line if needed;
And click Search .

Review all schedule options for the selected port, including Port name, UN/LOCODE, Flag, and Location coordinates. Click on the Port details button to open the Port tool in a new tab for deeper insights into port facilities, infrastructure, and services.
Below, check out all upcoming vessel arrivals and departures at this port: Shipping line, Vessel name, Voyage, ETS/ATD, and ETA/ATA. Filter results by line or date, or sort by any column. Need to save or share? Use the three dots icon to copy, print, or download data.

Integrations and customized solutions
Want to integrate Ship Schedules directly into your ERP, TMS, or website? We offer flexible API integration options to embed real-time schedule search capabilities seamlessly into your workflow.

Contact the SeaRates team to discuss custom solutions tailored to your business needs, whether you need higher search limits, custom web widgets, or dedicated support."""

rewrite = """Title: How to Use SeaRates Ship Schedules for Ocean Freight
Meta Title: SeaRates Ship Schedules Guide for Ocean Freight Tracking
Meta Description: Track port-to-port vessel schedules and get real-time shipping schedule data across 15M+ schedules, 6K+ seaports, and 5K+ vessels on SeaRates.

Planning ocean freight requires reliable timing across international supply chains. The SeaRates Ship Schedules tool simplifies ocean freight schedule tracking by pulling together over 15 million carrier schedules in one place. Shippers and logistics providers can review data covering 95K+ voyages, 6K+ seaports, 180K+ port pairs, and 5K+ vessels to find efficient routes and shorten transit times.

Free accounts include up to 5 daily searches and 20 unique monthly searches upon signup. Teams that require higher search volume can choose a paid subscription or request a customized solution.

## Route Searches with the Points Tab

Finding a port-to-port vessel schedule begins on the Points tab. Enter the origin and destination points, then pick target dates on the Calendar. 

The search filter panel offers additional settings to refine results:
* Filter options: Shipping Line, Arrival date, Departure date, Transit time, or direct routes (without Transshipments).
* Results summary: Every matching line lists the Departure date, Transit time, Arrival date, Transshipment ports, and Vessel name.
* Rate calculation: A direct link to Logistics Explorer sits below each option for instant freight rate estimates.
* Carrier and vessel details: Selecting a vessel name opens Vessel Tracking, while clicking a carrier logo displays all listed schedules for that line.
* Sorting and export: Click transit times, vessel names, or dates to sort the list. The three dots icon in the top right corner copies, prints, or downloads the search results.

Filters can be cleared or adjusted at any point during a search session.

## Individual Tracking on the Vessel Tab

When monitoring a specific container ship, switch to the Vessel tab. Enter the vessel name or IMO number, set the departure date or shipping line if needed, and run the search.

The top panel displays technical specifications for the vessel: Vessel name, Flag, IMO, MMSI, Built year, Vessel type, Capacity (TEU), and Length (m). Selecting the Vessel details button opens the Vessel Tracking tool in a separate browser tab for live positions.

Below the specifications, the schedule table displays departure and arrival ports alongside ETS/ATD and ETA/ATA dates. Direct links connect each entry to Port Schedules. Search parameters remain editable in the top panel, and the three dots icon exports data for external use.

## Monitoring Traffic on the Ports Tab

To view all activity at a single port, open the Ports tab. Enter the port name or UN/LOCODE, select a country, and set the calendar range. Optional filters allow sorting by specific shipping line.

Results list the port name, UN/LOCODE, country flag, and location coordinates. Opening the Port details button loads comprehensive information on infrastructure, terminals, and facilities. The main schedule section lists upcoming arrivals and departures with carrier names, vessel names, voyage numbers, ETS/ATD, and ETA/ATA figures. These entries can be sorted or exported at any time.

## Container Ship Schedule Integration and Custom APIs

Businesses looking to automate ocean freight schedule tracking can connect directly via API. This container ship schedule integration embeds real-time shipping schedule data into existing TMS, ERP, or web platforms.

Custom setups support higher query limits, tailored interface widgets, and direct technical support to match specific operational requirements."""

def find_longest_overlaps(text1, text2):
    # normalize words
    w1 = [(m.group(0), m.start(), m.end()) for m in re.finditer(r'\b[\w/+-]+\b', text1)]
    w2 = [(m.group(0), m.start(), m.end()) for m in re.finditer(r'\b[\w/+-]+\b', text2)]
    
    words1 = [w[0].lower() for w in w1]
    words2 = [w[0].lower() for w in w2]
    
    overlaps = []
    for i in range(len(words2)):
        for j in range(len(words1)):
            k = 0
            while i+k < len(words2) and j+k < len(words1) and words2[i+k] == words1[j+k]:
                k += 1
            if k >= 6:
                phrase_r = " ".join([w2[i+x][0] for x in range(k)])
                overlaps.append((k, phrase_r, i, j))
    
    # filter sub-matches
    overlaps.sort(key=lambda x: x[0], reverse=True)
    dedup = []
    seen = set()
    for k, phrase, i, j in overlaps:
        range_r = set(range(i, i+k))
        if not range_r.issubset(seen):
            dedup.append((k, phrase))
            seen.update(range_r)
            
    return dedup

print("Longest Overlaps:")
for k, phrase in find_longest_overlaps(orig, rewrite):
    print(f"[{k} words] {phrase}")

