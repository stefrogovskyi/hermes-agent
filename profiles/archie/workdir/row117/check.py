import json, re, unicodedata

body = open('/opt/hermes/profiles/archie/workdir/row117/final_body.md').read()
orig = """How to Track a Road Shipment Online with SeaRates Road Tracking?

Today, you'll discover how to switch from chaotic attempts to get the current location of your single shipment or multiple trucks with cargo carried by road. It's time for 101% visibility across your supplies to reduce delays and prevent late deliveries.
Here's how to monitor truck movements, manage cross-border road transportation, and handle multi-stop deliveries to stay informed about road shipments' progress.
Explore our new guide about the Road Tracking tool by SeaRates & LandRates - the specifically targeted solution for full control over land freight in real time.

## How does the tool work?
After confirming your booking, let's proceed with real-time road shipment tracking of your cargo. The Road Tracking tool is available on both the SeaRates.com (on the top menu or the Tools page) and LandRates.com (the top menu) websites.
Here, you can see the Road shipment type in the All carrier section.
Enter your shipment number or tracking number provided by your carriers to start. Also, you can request multi-tracking to upload a file containing the list of tracking numbers for monitoring at once.
You don't have to run across various platforms of the carriers and transportation companies to gather updates about your shipment. All road logistics are visible here, as the tool supports multi-carrier road tracking worldwide.
Here is your shipment card with the most up-to-date details of your cargo carried by road:
Real-time status updates: Booked / Received / Departed / In transit / Arrived / Out for delivery / Delivered / Exception / Canceled
Cargo details (the number of packages and their total weight)
Tracking number and carrier logo
Origin and destination points
Key logistics event: Predictive and actual ETA tracking for road freight, as well as other data in real-time
Such accurate live shipment data and status updates ensure instant road freight visibility. This way, you or your logistics team can reduce delivery delays before they impact customers.

Road Tracking dashboard
The live road tracking map visualizes truck movements for accurate location updates.
Moreover, explore the 'History' and 'Route' tabs on the shipment card.
In the 'History' tab, check the complete shipment timeline & events log. Find all major logistics events: pickup and delivery confirmations; delay and exception events; proof of delivery (POD), when available.
The 'Route' tab provides detailed insights into the transport journey, with route history insights: route milestones (pickup, in transit, out for delivery, delivered, exception); extra information provided by the carrier (optionally); historical ETA accuracy.
This helps you to forecast delivery times and make a performance & on-time delivery analysis to optimize future road shipments based on verified carrier data. Copy the link to share real time tracking card for the road cargo of your customer or partner.
There's no chance to miss route changes, so you can manage cross-border or multi-stop delivery road tracking, as well as ensure early delay detection for road transport within a single solution.

Customize with extra benefits
If urban distribution is necessary for your trade business, or you're executing time-critical deliveries, you can customize Road Tracking with: GPS and telematics integration; ELD and hardware data sources; driver-based mobile tracking.
This way, you access last-mile tracking updates and support continuous truck monitoring, accurate stop detection, proof-of-delivery workflows, and last-mile customer notifications integrated with your Road Tracking tool.

White-label road tracking
SeaRates also offers a branded tracking page (white-label), web widget for road tracking, which can be embedded into your website or customer portals.
Raise engagement with a wider audience with an instant road tracking solution under your brand. Let shippers gain transit time, route details, live updates, and any available insights from road carriers on their shipments right from your source.

API integration
The API connection between the Road Tracking and your TMS/ERP/CRM system ensures: automate real-time road shipment tracking; predictive ETA for trucks; build custom dashboards or customer portals.
Check out the API documentation at the Developer Portal to create your own monitoring app or enterprise road tracking solution with the SeaRates Road Tracking SaaS.
To submit your needs for a demo or customized integration, drop a message at it.sales@searates.com."""

title = "Road Shipment Tracking Online: A Practical Guide to SeaRates"
meta_title = "Track Road Shipments Online with SeaRates Road Tracking"
meta_description = "See how SeaRates Road Tracking gives real-time road freight visibility, predictive ETA, multi-carrier tracking, white-label pages and TMS/ERP integration."

full = title + "\n" + meta_title + "\n" + meta_description + "\n" + body

# 1. em-dash check
print("EM-DASH counts:", {k: full.count("—") for k in ["all"]}, "| '--' count:", full.count("--"))

# 2. n-gram overlap (6-grams), normalized
def norm(t):
    t = t.lower()
    t = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in t)
    return t.split()

def ngrams(t, n=6):
    w = norm(t)
    return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}

EXEMPT = {"searates", "landrates", "road tracking", "tracking", "road", "sea", "air"}
o6 = ngrams(orig); r6 = ngrams(body)
inter = o6 & r6
print("\n6-gram overlaps:", len(inter))
for g in sorted(inter):
    print("  -", g)

# also 7-gram stricter on remaining
def ngramsN(t, n):
    w = norm(t)
    return {" ".join(w[i:i+n]) for i in range(len(w)-n+1)}
o7 = ngramsN(orig,7); r7 = ngramsN(body,7)
print("7-gram overlaps:", len(o7 & r7))

# 3. contrastive negation count
cn = re.findall(r"\bnot\b|\brather than\b|\binstead of\b", body.lower())
print("\ncontrastive-ish tokens ('not','rather than','instead of'):", len(cn))

# 4. lengths
print("title len:", len(title), "| meta_title len:", len(meta_title), "| meta_desc len:", len(meta_description))
print("body words:", len(norm(body)))
