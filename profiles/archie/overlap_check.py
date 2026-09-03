import re

original = """Track changes in freight indexes, analyze the logistics market, and historical freight rates for sea, land, and air freight in real time. Freight Index by SeaRates provides accurate data on freight index and market trends. Perform excellent logistics management for shippers, logistics providers, and analytical companies. Let's improve your analytics with confidence.

How to use Freight Index?
Make sure your supply chain planning is executed properly, effectively, and based on accurate analytics on market index shifts:
* over 10,000,000 tariffs from the past five years
* 1 billion+ route coverage
* 70+ million price points
* 99.99% accuracy of rate forecasting

Start with Trending indexes, including average spot rates data on popular destinations. Scroll to the sides to find more.
Moving forward, choose the Shipping and Transport Unit types in both dropdown lists. For shipping, sea (FCL, LCL, Bulk), land (FTL, FCL, LTL), rail (FWL, LWL, FCL, FTL), and air (standard cargo and ULD container) are available.

Freight Index is available in two plans - Default and Premium:

Default features:
4 levels of data coverage: Area, Continent, Subregion, Coast.
Check freight indexes by a particular world region. Under the Default subscription, you have access to indexes searching by global areas, continents, subregions, and coasts.
Just choose the 'From'/'To' points with interactive world map autodetection powered by SeaRates Autocomplete.
You get the results of freight index changes as increased, decreased, or flat prices for the transportation route (mentioned From and To points), or separately from or to a particular area/region/city/etc.
Moreover, here you can expand the market research and get index shift analytics for the last 3 months.
Also, share your results with customers, partners, or social media followers to complete your report updates or insights takeaways.

Premium features:
8 levels of data coverage: Area, Continent, Subregion, Coast, Country, State, Province, Point (City, Port, Airport, Station).
In the addition of Default functionality, you can get the following enhancements:
* comparing the freight indexes by time ranges;
* accessing the deeper and more detailed searching by geography levels;
* searching index by Carriers;
* checking the history of freight indexes for 6 months, 1 year, and a particular date, as well as picking the period in the calendar;
* downloading the result data in a convenient format.
As a Premium user, you can cover index research by countries, states, provinces, cities, ports, airports, and stations.
Choose a particular carrier to get detailed statistics, as well as pick 'All carriers' for 'Shipping line not selected' options.
Moreover, compare indexes by weeks, months, and years for extensive analytics.
Additionally, select the currency type in the dropdown list for displaying the appropriate one for you.
Simply set notifications on changes per freight index and download results on your research.

White-label integration:
Interested in the upselling capabilities of market in-depth index analytics? Integrate the Freight Index functionalities as a customized white-labeled solution on your website. Engage the audience with advanced benchmarking under your brand. Reduce the need to reach for market information on your competitors' sources as much as possible.

API connection:
All Premium features are available for Freight Index API integration into your CRM/ERP/TMS systems. Connect to the SeaRates global database to provide market insights under your brand.
Kindly check the API documentation for the Freight Index in our Developer Portal. There is all general information and detailed descriptions of requests you can submit, tailored to your particular needs.

Find Your Customized Freight Index Plan:
You're always welcome to let us know about your requirements by filling out the Request an IT Quote form or reaching out to us at sales for a tailored solution."""

rewrite = """Title: SeaRates Freight Index: How to Track and Benchmark Rates
Meta-Title: SeaRates Freight Index Guide: Rate Benchmarking and Data
Meta-Description: Track ocean freight rate trends, compare historical freight tariffs, and integrate a white-label freight index API for supply chain rate forecasting.

Body Text:
Shipping rates move fast, but raw market data usually moves faster than the teams trying to track it. SeaRates Freight Index pulls from a database built on over 10,000,000 tariffs logged across the past five years, covering more than 1 billion routes and 70+ million price points. That engine delivers 99.99% accuracy of supply chain rate forecasting across sea, land, rail, and air modes.

When you open the tool, the main view loads trending indexes with average spot rates for high-traffic trade lanes. Horizontal scrolling exposes additional lanes. Two primary dropdown menus control mode and equipment settings.
Sea options include FCL, LCL, and Bulk.
Land lists FTL, FCL, and LTL.
Rail supports FWL, LWL, FCL, and FTL.
Air cargo breaks down into standard cargo and ULD containers.

The platform runs on two tiers. Default access gives you four geographical search levels: Area, Continent, Subregion, and Coast. Autocomplete map detection identifies origin and destination points, showing price movement as increased, decreased, or flat rates along specific lanes or regional nodes. The Default plan limits historical freight tariffs research to a 3-month window, with direct export options to share findings with customers, partners, or social media followers.

Premium expands geographical search to eight levels by adding Country, State, Province, and Point parameters, which cover cities, ports, airports, and rail stations. You can run freight index market analytics across weekly, monthly, or yearly increments.

Filtering by carrier is exclusive to Premium. You can isolate a single carrier or set the filter to All carriers or Shipping line not selected. Date selection opens up options for 6 months, 1 year, a specific date, or custom calendar ranges. Premium users can run container spot rate benchmarking, switch display currencies on the fly, set notifications on rate changes, and download research data in a convenient format.

For software platforms, all Premium features connect through the Freight Index API into CRM, ERP, or TMS infrastructure using the SeaRates global database and Developer Portal documentation. Alternatively, companies can embed container spot rate benchmarking functionality as a white-label freight index API setup directly on their own websites, enabling advanced benchmarking under their own brand and keeping users from checking competitors' sources for ocean freight rate trends.

To set up a custom plan or white-label portal, fill out the Request an IT Quote form or reaching out to sales."""

def clean_words(s):
    # return list of words ignoring punctuation
    return re.findall(r'\b[a-zA-Z0-9]+\b', s.lower())

orig_w = clean_words(original)
rew_w = clean_words(rewrite)

# Find all matching sequences of length >= 6
def find_exact_overlaps(w1, w2, min_len=6):
    matches = []
    for i in range(len(w2) - min_len + 1):
        for length in range(min_len, len(w2) - i + 1):
            sub = w2[i:i+length]
            # check if sub exists in w1
            sub_tuple = tuple(sub)
            # search in w1
            found = False
            for j in range(len(w1) - length + 1):
                if tuple(w1[j:j+length]) == sub_tuple:
                    found = True
                    break
            if found:
                matches.append((i, length, " ".join(sub)))
            else:
                break # if length doesn't match, longer won't match starting at i
    return matches

matches = find_exact_overlaps(orig_w, rew_w, 6)

# Deduplicate overlapping matches to get max length matches
max_matches = []
for i, length, text in matches:
    # check if this is contained in another match with larger length or starting earlier
    is_sub = False
    for i2, len2, text2 in matches:
        if (i2 <= i and i2 + len2 >= i + length) and (len2 > length):
            is_sub = True
            break
    if not is_sub and (i, length, text) not in max_matches:
        max_matches.append((i, length, text))

print("Max Overlaps (>=6 words):")
for m in max_matches:
    print(m)

