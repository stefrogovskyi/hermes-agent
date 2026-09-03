import re

title = "SeaRates January 2025 Updates: New Tracking & App Release"
meta_title = "SeaRates January 2025 Release: App, APIs, Carrier Updates"
meta_description = "SeaRates released the AirRates mobile app, added Kanway and Sidra lines, updated geocoding APIs, and expanded air cargo tracking in January 2025."

body = """Shipping updates rarely arrive with fanfare, yet small adjustments to tracking logic often carry the heaviest freight in daily operations.

We launched the AirRates Mobile App on iOS and Android. Users can pull up air cargo tracking by AWB numbers directly on their phones, getting clear supply chain visibility tools in a mobile view.

On the ocean side, the tracking system now covers Kanway Line and Sidra Line. That brings the total count of supported shipping lines to 182. Behind the scenes, updates to our tracking API refine how the system determines event types and auto-detects shipping lines.

Air freight tracking gained support for Tianjin Air Cargo. Alongside the new carrier, the backend received logic adjustments that sort route steps in chronological order and handle incoming requests with higher accuracy.

A few other updates round out the release:

* The logistics geocoding API now returns cleaner output data.
* A freight index subscription selector is available on the Plans & Pricing page.
* SeaRates content is now published in French, with open channels for collaboration inquiries."""

orig_text = """January 2025 Development Release: Empowering Business Users
Your continuous encouragement and suggestions are much valued. Take a look at our updated digital solutions and products that we believe may pique your interest. By signing up for our newsletter, you can stay informed about SeaRates.
Feel free to peruse the revised choices at your leisure.
AirRates Mobile App
Our team is glad to announce the AirRates Mobile App release! Download the application on the Apple Store or Google Play to seamlessly track all of your air shipments by simply entering an AWB number. Get comprehensive transparency and visibility of the entire supply chain at your fingertips!
Tracking System
We are pleased to announce added support for 2 more shipping lines, namely Kanway Line and Sidra Line, bringing the total number to 182.
Also, kindly check our API improvements: There are enhancements of logic for type event determination and improved auto-detection logic for shipping lines to ensure your tracking experience is empowered with smooth real-time monitoring and data reliability.
Air Cargo Tracking
We are glad to announce support for Tianjin Air Cargo airline.
Moreover, we have improved the logic for determining the chronological order of routes and processing requests to provide you with higher visibility and accuracy in your air freight tracking experience.
Other updates
We are pleased to announce the SeaRates Blog in French. If you are interested in starting a collaboration, you are always welcome to contact us at [email].
Also, we have improved output data results for the Geocoding API.
Finally, we are glad to present a new option to choose your subscription for the Freight Index tool on the Plans & Pricing page."""

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# 1. Em-dash check
em_dashes = full_text.count("—") + full_text.count("--") + full_text.count("–")

# 2. Length checks
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# 3. 6-gram overlap check
def get_ngrams(text, n=6):
    words = re.sub(r'[^\w\s]', '', text.lower()).split()
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

orig_ngrams = get_ngrams(orig_text, 6)
body_ngrams = get_ngrams(body, 6)
overlap = orig_ngrams.intersection(body_ngrams)

# 4. Contrastive negation check
contrastive_count = len(re.findall(r'\bnot\b', body, re.IGNORECASE)) + len(re.findall(r'\binstead of\b', body, re.IGNORECASE))

# 5. Connectors check
connectors = len(re.findall(r"that's why|which is why|this ensures that", body, re.IGNORECASE))

print(f"Em-dashes count: {em_dashes}")
print(f"Title length ({title_len}): {'PASS' if title_len <= 60 else 'FAIL'}")
print(f"Meta Title length ({meta_title_len}): {'PASS' if meta_title_len <= 60 else 'FAIL'}")
print(f"Meta Description length ({meta_desc_len}): {'PASS' if meta_desc_len <= 155 else 'FAIL'}")
print(f"6-gram overlaps count: {len(overlap)}")
if overlap:
    print("Overlaps found:", overlap)
print(f"Contrastive negation count: {contrastive_count}")
print(f"Connectors count: {connectors}")
