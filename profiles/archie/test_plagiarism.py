import re

orig = """SeaRates Updates - Week 44, 2024

We are grateful for your ongoing support of SeaRates and eager to introduce new products that will further satisfy you. Enhancing our services is a top focus for us.

For the most recent information, see our previous releases.

What’s new for week 44:

For the API, we have added parameters on Storage, Demurrage, and Detention fees.

For the Tracking History API, we have enhanced response processing logic for Predictive ETA estimation.

We have enhanced our work with providers, including Vanguard Logistics, Hyundai Merchant Marine (HMM), COSCO, Pacific International Lines (PIL), Sealead Shipping, Gold Star Line, Yusen Logistics, Ocean Network Express (ONE), Hellmann Worldwide Logistics, DHL Global Forwarding, and Nirint Shipping.

Air Tracking enhancements: We are glad to announce we have added support for 2 airlines, including Air Arabia Maroc and Challenge Airlines Malta. The total number of supported airlines reaches 435.

Also, we have added the ‘cache_expires’ parameter to the API responses.

Finally, we have enhanced our work with providers, including Amerijet International, Binter Canarias, United Airlines, Hong Kong Air Cargo, Turkish Airlines, Asiana Airlines, American Airlines, LOT (LOT Polish Airlines), Mahan Air, Air France, and DHL Aviation.

Parcel Tracking updates: For the API, we have improved Autodetect logic.

SeaRates Mobile Application improvements: We have comprehensively updated the authorization system for Android users by implementing authorization without going to the SeaRates website, as well as the ability to log in via Google and Apple accounts.

Also, we have updated the ‘Profile’ and ‘Settings’ sections in the App.

Other updates:

We have created the Freight Carrier API page, which you can also assess via the Sea Lines Explorer API on the Find a Tool page.

Also, we have created the Demurrage & Storage Calculator API landing page.

Finally, we have updated the design and content for the Find a Tool and Cargo Wizard Web pages, as well as for the Homepage on LandRates.com."""

rewr = """Title: SeaRates Product Update: Week 44, 2024
Meta Title: SeaRates Updates Week 44, 2024: API and App Enhancements
Meta Description: SeaRates Week 44 release notes covering container tracking API updates, air freight integration, parcel autodetect tracking, and Android app updates.

Body:
Here is what shipped across SeaRates APIs, ocean carrier integrations, air tracking, and mobile apps during Week 44 of 2024.

## Tracking & Fee APIs

Our container tracking API responses now return parameters for Storage, Demurrage, and Detention fees. This brings direct demurrage and detention fee tracking into the primary API data payload alongside a new `cache_expires` parameter.

For predictive ETA logistics within the Tracking History API, we updated the underlying response processing logic to refine estimated arrival calculations.

On parcel tracking, we adjusted the parcel autodetect tracking system to increase detection accuracy across API requests.

## Carrier Integrations

Ocean freight integrations were updated for 11 shipping lines and logistics partners:
* Vanguard Logistics
* Hyundai Merchant Marine (HMM)
* COSCO
* Pacific International Lines (PIL)
* Sealead Shipping
* Gold Star Line
* Yusen Logistics
* Ocean Network Express (ONE)
* Hellmann Worldwide Logistics
* DHL Global Forwarding
* Nirint Shipping

Air freight tracking API support grew to 435 total airlines with the addition of Air Arabia Maroc and Challenge Airlines Malta.

We also revised backend connections for 11 air cargo providers: Amerijet International, Binter Canarias, United Airlines, Hong Kong Air Cargo, Turkish Airlines, Asiana Airlines, American Airlines, LOT Polish Airlines, Mahan Air, Air France, and DHL Aviation.

## Mobile Application

Android users can now sign in directly inside the SeaRates Mobile Application. The update removes the redirect to the SeaRates website and adds single sign-on via Google and Apple accounts. The Profile and Settings views received layout adjustments to match the new authentication flow.

## New Landing Pages and Tools

- A new Freight Carrier API documentation page is live. You can also reach it through the Sea Lines Explorer API on the Find a Tool page.
- We published a dedicated landing page for the Demurrage & Storage Calculator API.
- Interface updates were applied to the Find a Tool page, the Cargo Wizard web experience, and the LandRates.com homepage.
"""

# Let's clean text of punctuation and find all 6-gram overlaps
def clean_words(t):
    return re.findall(r'[a-zA-Z0-9]+', t)

w_orig = clean_words(orig.lower())
w_rewr = clean_words(rewr.lower())

orig_6grams = set()
for i in range(len(w_orig)-5):
    orig_6grams.add(" ".join(w_orig[i:i+6]))

found_overlaps = []
for i in range(len(w_rewr)-5):
    gram = " ".join(w_rewr[i:i+6])
    if gram in orig_6grams:
        found_overlaps.append(gram)

print(f"Total 6-grams overlapping: {len(found_overlaps)}")
unique_overlaps = set(found_overlaps)
for u in sorted(unique_overlaps):
    print("Overlap:", u)

