import re

with open('/opt/hermes/profiles/archie/draft1.txt', 'r') as f:
    rewrite = f.read()

source_text = """
We are glad to announce the AirRates Mobile App V. 1.0 release. From now on, you have access to a user-friendly air freight monitoring tool with real-time updates on your supply chain.
Let's discover advanced features for complete transparency of operations, a straightforward accurate air cargo tracking, automatic updates, and a wide scope of comprehensive data on your air shipments from 400+ world-trusted airlines.
All of these unique insights are available in one place — the AirRates mobile application.
Keep reading for a tutorial below on how to take advantage of our new release for ultimate air tracking, all to assist you get the best use out of the AirRates Mobile App.

How does it work?
The first version of the AirRates Mobile Application provides access to the Air Cargo Tracking features on iOS and Android. Using the improved Air Cargo Tracking API allows you to take advantage of the following benefits of air freight monitoring:
To access the Air Tracking tool, find the ‘Tools’ tab in the menu and choose Air Tracking.
All it takes is simply to enter the air waybill number provided by the carrier or shipping lines and start tracking for air freight in real-time.
There is an air shipment card displaying one’s number, ETA, status (booked, received, departed, in_transit, arrived, notified, delivered, or canceled), cargo info, and airline, as well as a route visualizing on the interactive world map.
The ‘Details’ tab summarizes such significant info for quick tracking analysis as flight number, transport type, places of origin/destination, and ATD & ETA or ATA. Furthermore, there is a ‘History’ tab with the entire air shipment description and route details on each transshipment point, logistics events, flight information, and more.
Moreover, you can delete the shipment card from the saved or copy the automatically generated link to this particular air shipment to provide unique access to the tracking information for your customers and partners. The link will go to the shipment card on AirRates.com.
This way, any current details on air cargo are available with the accurate real-time monitoring solution on users’ mobile phones.

Going back to the ‘Tools’ menu, take a look at the list of the nearest digital tools for logistics releases available at the AirRates mobile app. To keep up with announcements of new end-to-end freight management solutions, follow our weekly updates here.
You can also have access to a comprehensive Settings menu. Optionally, choose a light or dark theme for the application interface, get a closer look at the AirRates team, familiarize yourself with the Terms of Services and Privacy Policy, and reach out to us with the Contact Us and Help form.
Currently, the app supports four languages:
Also, receive notifications about air freight tracking details on your phone to stay updated about any supply chain changes anytime and anywhere. On the Homepage there is quick access to air shipment tracking history to simply go back to saved results, as well as familiarize themselves with promotional solutions by AirRates for application users on iOS and Android.
Finally, on the homepage you can go to the articles on the Blog.

Advantages of using AirRates Mobile Application
There are several benefits to using the AirRates Mobile App Version 1.0:
Improved Air Cargo Tracking version of the tool: All data upon air shipment monitoring are available with a single user-friendly application to avoid any extra time needed to get decision-making data. The mobile app is designed for enhancement and management anytime and anywhere. Complete visibility and transparency for the sake of easy-to-use digital logistics.
Convenient real-time tracking for air freight: The solution to track and trace shipments by air and get all data rapidly anywhere, right on their phone. Our team ensures users can set and receive air tracking notifications with the latest updates or monitor in real-time mode on the interactive world map right at the fingertips.
Advanced and reliable information: Detailed air freight monitoring data for simplified search by default in the app. With the help of the application, all urgent information, such as logistics events, shipment updates, route data, and more from 400+ global airlines in one place, fully satisfies the customer's desire to check any updates on their supply chain at any time.

Conclusion
AirRates Mobile Application Version 1.0 with Air Cargo Tracking available was created to provide access to all relevant data on air freight tracking in the most convenient format for you. The application allows users to receive detailed information on shipments by air and monitor logistics operations from anywhere. This app enables AirRates to introduce user-friendly innovations to better serve the logistics needs of our customers.
Our state-of-the-art products for freight management offer businesses the ultimate level of supply chain transparency and flows visibility. With the entire ecosystem of SeaRates, AirRates, and LandRates, it is easy to streamline logistics operations and solve daily challenges as never before — right at your fingertips. Dive deeply into opportunities for your business to improve your logistics and trade — stay tuned for updates on further AirRates app features!
Interested in a successful journey into digital logistics and trade with our IT products? Kindly reach to us at sales@searates.com for customized and seamless integration solutions.
"""

def clean_words(text):
    return re.findall(r'\b\w+\b', text.lower())

src_words = clean_words(source_text)
rew_words = clean_words(rewrite)

def get_ngrams(words, n):
    return [tuple(words[i:i+n]) for i in range(len(words)-n+1)]

src_6grams = set(get_ngrams(src_words, 6))
rew_6grams = get_ngrams(rew_words, 6)

overlaps = []
for g in rew_6grams:
    if g in src_6grams:
        overlaps.append(" ".join(g))

print(f"6-gram overlaps found: {len(overlaps)}")
for o in set(overlaps):
    print(" - Overlap:", o)

