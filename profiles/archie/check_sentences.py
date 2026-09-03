import re

# Let's inspect all sentences in Draft and compare with Original

draft_sentences = [
    "Software improves when small details accumulate into reliable tools.",
    "In Week 38 of 2024, SeaRates deployed updates across tracking integrations, developer endpoints, and platform design.",
    "Air cargo tracking now connects directly with five additional carriers: Cathay Pacific Airways, British Airways, Astral Aviation, Bringer Air Cargo Taxi Aereo, and EVA Air.",
    "Meanwhile, ocean container tracking expanded integrations for Orient Overseas Container Line (OOCL), Kuehne + Nagel (KN), and Volta Container Line.",
    "API functionality received two targeted changes.",
    "The Freight Index now exposes historical indicative rates through both web and API channels.",
    "For proximity calculations, the distance & time API runs on updated logic to determine the closest location for every request.",
    "Vessel ship schedules added tracking support for HR Lines and Great White Fleet, searchable by points, vessel, or port.",
    "Users navigating Logistics Explorer can now switch the tool interface to Spanish through new Spanish localization options.",
    "Signing in is simpler with Apple account login and registration options.",
    "To finish the week's release, SeaRates updated the design and content on the About Us and Plans & Pricing pages."
]

orig_text = """SeaRates Updates - Week 38, 2024
We are grateful for your constant support for SeaRates. We are passionate about refining our service and are thrilled to unveil new features designed to enhance your experience. Look over our previous updates to find the latest details.

What's new for week 38:
Air Cargo Tracking updates:
We have enhanced our work with providers, including Cathay Pacific Airways, British Airways, Astral Aviation, Bringer Air Cargo Taxi Aereo, and EVA Air.

Tracking System enhancements:
We have enhanced our work with providers, including the Orient Overseas Container Line (OOCL), Kuehne + Nagel (KN), and Volta Container Line.

Freight Index improvements:
We have implemented access to indicative rates based on historical data for web and API versions.

Distance & Time updates:
We have improved the logic of determination for the closet location for API requests.

Ship Schedules improvements:
We are pleased to present that we have added support for the HR Lines and Great White Fleet by Points, as well as for Great White Fleet by Vessel and by Port.

Other updates:
For the Logistics Explorer tool, we have added interface translation in the Spanish language.
We have implemented an option to log in and register by Apple account for an easier experience for SeaRates customers.
Finally, we have updated the content and design for the About Us and Plans & Pricing pages."""

print("--- Sentence by Sentence Check ---")
for s in draft_sentences:
    print(f"Draft: {s}")
