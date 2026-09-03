import re

original_text = """TITLE: Explore New Feature: Search by Port in SeaRates’ Ship Schedules tool

To facilitate a better understanding of shipping schedules, we at SeaRates have introduced a new feature for searching schedules by Port for easily obtaining logistics insights on particular world ports. Let's explore how to get schedule data following various shipments requirements, routes, and other details. Continue with our valuable insights on using Ship Schedules by Port for your thoughtful shipping planning and management.

How does it work?
The Ship Schedules tool’s interface has been enriched by a newly released opportunity to search sailing schedules by Port to expand data gathering for shipments. The ‘Port’ tab is located next to the ‘Route’ for points-searching and the ‘Vessel’ tab.

When searching for ship schedules on the ‘Port’ tab, the user needs to enter the name of the seaport or choose from the history of recent searches. The SeaRates Autocomplete service provides rapid geographical detection of the user's request and offers results to pick from. Also, date and other parameters, such as time frame by weeks and shipping line, can be selected or stayed by default.

There are handy Filter on the left, an interactive real-time world map that displays the user’s port of choice, and sailing results provided by global shipping carriers.

For the port, clients’ search sailing schedules by, the tool provides major key information such as port name, state, LOCODE, latitude, longitude, and the timezone for convenient planning the supply chain operations according to SeaRates database.

Adjusting the Filter, there are options to set the results for particular arrival or departure dates, selecting one or more shipping lines from the list, as well as the vessel name and voyage number.

Continuing with schedule results by port, the schedule cards of main shipping lines carriers cargo transportation by this port are displayed. Even without opening the card, you can check the name of shipping line, voyage number, and ETA/ETD. The cards consist of vessel details on the top. Next, choosing a specific vessel, voyage, or dates under the shipping line, users get detailed information on the route, including broader ETA, ETD data, service name and code, as well as terminal name and code. Then, voyages are displayed with their local code, and the Cut off Dates are listed in detail.

An add-on value of the Ship Schedules tool is the newly created results details page that appears by clicking the 'View Details' button, which allows the user to share a unique link to the results with customers and partners by clicking the 'Copy link' button.

Finally, the Ship Schedules API has also undergone a range of updates to enable easy integration of the schedule search by Port capability into our customers' TMS/ERP/CRM systems.

Benefits of using Ship Schedules by Port
There are several advantages to using the searching by Port feature via SeaRates Ship Schedules:
- Convenience and quickness: The newest feature of the Ship Schedules tool allows for advanced schedule search services by any ports of users’ choice. Easy-to-use query filtering logic simplifies the approach to finding any data requested.
- Broad data research: Comprehensive information on logistics events, port, vessel, and carrier details, voyages, and more via a single ultimate tool. Advanced data on all shipment schedules from global shipping lines across world locations and seaports.
- Improved customer experience: With the new feature of Ship Schedules, customers can obtain particular information on chosen port or location among all sailing data faster and in more detail, ensuring relevant and accurate results. The possibility to apply settings when requesting provides a wide choice of schedules by world shipping lines, vessels, or voyages.

Summarizing
We developed a feature to look up ship schedules by Port, allowing you to easily access sailing information for any global destination or seaport in one place. Within moments, a wealth of shipping data from companies and destinations across the globe is processed efficiently and clearly. By utilizing this effective tool, predicting and managing the supply chain becomes simpler, resulting in an improved experience for customers in digital logistics.

The SeaRates team is focused on a comprehensive and customized approach for each of the users, providing this accessible and easy-to-navigate interface supports logistics businesses across the globe in improving their management of shipping activities. Our IT solutions enhance the shipping and delivery experience for companies around the globe.

Reach out to us via sales@searates.com to take your logistics planning to the next level with our intuitive, advanced products tailored to your needs.
"""

rewrite_text = """Title: Searching Sailing Schedules by Port in the SeaRates Ship Schedules Tool
Meta Title: Search Sailing Schedules by Port | SeaRates
Meta Description: Search sailing schedules by port on SeaRates. Filter ETA/ETD voyage updates, view cutoff dates and terminal codes, or integrate the vessel schedules API.

Body Markdown:
## Port Schedule Search Interface and Filtering Logic

The SeaRates Ship Schedules tool includes a dedicated Port tab situated alongside the existing Route and Vessel tabs. This setup allows logistics planners to run sailing schedules by port when evaluating carrier coverage for specific locations. Entering a seaport name triggers the SeaRates Autocomplete service, which detects geographical locations and returns matching ports. Users can select from the autocomplete dropdown or pick a location directly from their recent search history. Default settings display standard parameters, while manual controls allow users to adjust time frames by weeks or filter by preferred shipping lines.

## Port Data Records and Real-Time Interactive Mapping

Running a query generates a port summary powered by the SeaRates database. The interface displays the port name, state, LOCODE, latitude, longitude, and timezone to support precise operational planning. A left-hand Filter panel works alongside an interactive real-time world map that highlights the selected port alongside sailing results from global ocean carriers. Planners using this maritime logistics scheduler can refine search parameters by setting specific arrival or departure date ranges, filtering for one or multiple shipping lines, or searching directly by vessel name and voyage number.

## Schedule Cards, Vessel Details, and Voyage Tracking

Search results appear as schedule cards organized by shipping line. Without expanding a card, users can view the carrier name, voyage number, basic vessel details at the top, and initial ETA/ETD estimates. Selecting a specific vessel, voyage, or date range reveals expanded route information. This detailed view delivers ETA/ETD voyage updates, service names and codes, terminal names and codes, voyage local codes, and detailed cutoff dates. Clicking the View Details button opens a dedicated result details page, where users can click Copy link to share a unique URL with clients or freight partners.

## TMS, ERP, and CRM System Integration

The underlying vessel schedules API has received corresponding updates to support direct schedule searches by port across external software. Logistics teams can embed this functionality into existing TMS, ERP, or CRM platforms to automate port-to-port vessel schedules and enable real-time port schedule tracking across internal workflows. Teams seeking customized platform integrations or schedule data feeds can contact the SeaRates team at sales@searates.com.
"""

# Let's inspect raw text exact matches for contiguous word sequences
def find_exact_word_sequences(orig, rew, min_len=6):
    # tokenize preserving hyphenated words
    orig_words = re.findall(r'[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*', orig.lower())
    rew_words = re.findall(r'[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*', rew.lower())

    matches = []
    for i in range(len(rew_words) - min_len + 1):
        for j in range(len(orig_words) - min_len + 1):
            k = 0
            while (i + k < len(rew_words)) and (j + k < len(orig_words)) and (rew_words[i + k] == orig_words[j + k]):
                k += 1
            if k >= min_len:
                seq = " ".join(rew_words[i:i+k])
                matches.append((k, seq, i, j))
    
    # Filter out duplicates contained in longer matches
    unique_matches = []
    for m in sorted(matches, key=lambda x: x[0], reverse=True):
        if not any(m[1] in existing[1] for existing in unique_matches):
            unique_matches.append(m)
    return unique_matches

print("--- Exact Word Sequence Overlaps (6+ words) ---")
exact_overlaps = find_exact_word_sequences(original_text, rewrite_text, min_len=6)
for length, seq, i, j in exact_overlaps:
    print(f"Length {length}: '{seq}'")

