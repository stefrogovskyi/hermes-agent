import re

original_lines = [
    "SeaRates Updates - Week 47, 2024",
    "We appreciate your continued support of SeaRates and are excited to present new products that will better meet your needs. Improving our services remains a key priority for us.",
    "What's new for week 47:",
    "Tracking System improvements:",
    "For the web version, we have improved the design of the tool by adding tooltips with the names of shipping lines on the logo and updating the Filter. We've also enhanced our collaboration with providers, including Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL.",
    "Air Cargo Tracking enhancements:",
    "We've added support for Azerbaijan Airlines and Air Arabia Abu Dhabi. Discover the list of supported airlines here.",
    "Ship Schedules updates:",
    "We have added support for KambaraKisen, Culines, and Sinokor by Vessel, and KambaraKisen by Port.",
    "Parcel Tracking improvements:",
    "For the API version, we have enhanced autodetect logic for streamlined requesting.",
    "Other updates:",
    "Search Filter: For the Search Filter, we have added a new customization option: the Button hover color for color adjusting the search button.",
    "FAQ sections: For the Container Tracking, Distance & Time, and Load Calculator pages, we have added FAQ sections.",
    "LandRates.com: Added the Special Offers section to the main page on LandRates.com to find and compare land freight rates across the globe easily.",
    "Announcements:",
    "Calendar tab in the Tracking System tool",
    "New Version of Route Planner API",
    "Freight Index 1.0",
    "Mobile App Version 1.2 with Request System feature",
    "Load Calculator Version 2.2",
    "Booking System Version 1.1",
    "Map platform"
]

draft_lines = [
    "Title: SeaRates Week 47 Updates: Tracking, Schedules & APIs",
    "Meta-Title: SeaRates Week 47 Updates | Logistics & Tracking Tools",
    "Meta-Description: Discover SeaRates Week 47 updates: container tracking, air cargo coverage, ship schedules, API enhancements, and global land freight rate search.",
    "## Ocean and Air Tracking Upgrades",
    "Managing freight across global routes requires clear, immediate details.",
    "In the web version of the Tracking System, new logo tooltips display carrier names on hover, paired with an updated Filter to sort active shipments quickly.",
    "Direct data collaboration has also expanded across four ocean carriers: Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL.",
    "Teams using supply chain visibility tools gain immediate clarity on active legs.",
    "Air transport coverage broadens as well.",
    "Air cargo tracking integrations now include Azerbaijan Airlines and Air Arabia Abu Dhabi, pulling direct flight status updates into the main dashboard.",
    "## Expanded Vessel Schedules and API Logic",
    "Planning sea routes depends on reliable departure and arrival timelines.",
    "Vessel sailing schedules automation now covers KambaraKisen, Culines, and Sinokor by Vessel, along with KambaraKisen by Port.",
    "On the developer side, Parcel Tracking for the API version features upgraded autodetect logic.",
    "The system identifies tracking number formats automatically, streamlining data retrieval for teams running a real-time container tracking API interface.",
    "## Interface Fine-Tuning and Land Freight Options",
    "Small workflow adjustments improve daily site navigation and rates discovery:",
    "Search Filter customization now includes a button hover color option for tailored visual styling.",
    "Container Tracking, Distance & Time, and Load Calculator pages now feature dedicated FAQ sections.",
    "LandRates.com added a Special Offers section to its main page, giving shippers a direct tool for land freight rate search and comparison worldwide.",
    "## Upcoming Platform Features and Releases",
    "Development continues across several core modules, with upcoming releases including:",
    "Calendar tab in the Tracking System tool",
    "New Version of Route Planner API",
    "Freight Index 1.0",
    "Mobile App Version 1.2 with Request System feature",
    "Load Calculator Version 2.2",
    "Booking System Version 1.1",
    "Map platform"
]

def clean_words(text):
    return re.findall(r'\b[\w\.\-\&]+\b', text.lower())

for d_idx, d_line in enumerate(draft_lines):
    d_words = clean_words(d_line)
    for o_idx, o_line in enumerate(original_lines):
        o_words = clean_words(o_line)
        # Check longest common substring of words
        for i in range(len(d_words)):
            for j in range(len(o_words)):
                k = 0
                while i + k < len(d_words) and j + k < len(o_words) and d_words[i+k] == o_words[j+k]:
                    k += 1
                if k >= 6:
                    match_str = " ".join(d_words[i:i+k])
                    print(f"Draft L{d_idx+1} matches Orig L{o_idx+1} (length {k}): '{match_str}'")

