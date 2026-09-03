import re

# Claims comparison script

claims = [
    {
        "draft_location": "Meta Description",
        "draft_text": "upgrades air tracking for three major carriers",
        "original_text": "Air Tracking updates: We have enhanced support for airlines, including Air Canada, FITS Aviation, and TAP Portugal.",
        "issue": "Original states 'including Air Canada, FITS Aviation, and TAP Portugal', indicating an non-exhaustive list of airlines. Draft asserts 'three major carriers', framing the list as exhaustive and mischaracterizing regional airlines like FITS Aviation as 'major carriers'."
    },
    {
        "draft_location": "Article Body (P2)",
        "draft_text": "upgraded the underlying fetch logic for vessel milestones to ensure more reliable vessel status reporting",
        "original_text": "improved the logic of obtaining additional data on the vessel.",
        "issue": "Draft invents technical terminology ('fetch logic for vessel milestones') and ungrounded benefit ('ensure more reliable vessel status reporting') not in source."
    },
    {
        "draft_location": "Article Body (P3)",
        "draft_text": "Air Waybill (AWB) tracking now runs with higher precision",
        "original_text": "Air Tracking updates: We have enhanced support for airlines",
        "issue": "Draft invents specific mechanism ('Air Waybill (AWB) tracking') and ungrounded claim ('runs with higher precision'). Source only mentions 'enhanced support for airlines'."
    },
    {
        "draft_location": "Article Body (P3)",
        "draft_text": "strengthening end-to-end supply chain tracking during primary feed downtime",
        "original_text": "updated the parcel tracking logic of obtaining data from alternative sources.",
        "issue": "Draft invents reason/mechanism ('during primary feed downtime') and benefit ('strengthening end-to-end supply chain tracking'). Source makes no mention of primary feed downtime."
    },
    {
        "draft_location": "Article Body (P4)",
        "draft_text": "Load Calculator Web 3.0 is receiving a complete overhaul with new features and a modernized interface",
        "original_text": "Load Calculator Web 3.0 (new design and features)",
        "issue": "Draft exaggerates 'new design' to 'receiving a complete overhaul' with a 'modernized interface'."
    },
    {
        "draft_location": "Article Body (P4)",
        "draft_text": "Looking ahead, several updates are currently in development. Our team is building...",
        "original_text": "Announcements: ...",
        "issue": "Draft assumes/claims all items under 'Announcements' are 'currently in development' and 'building', whereas the source simply lists them under 'Announcements'."
    }
]

print("=== LAYER 4 FINDINGS ===")
for i, c in enumerate(claims, 1):
    print(f"{i}. Location: {c['draft_location']}")
    print(f"   Draft Quote: \"{c['draft_text']}\"")
    print(f"   Original Quote: \"{c['original_text']}\"")
    print(f"   Analysis: {c['issue']}\n")

