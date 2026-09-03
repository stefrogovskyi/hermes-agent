import re

cand_sentences = [
    "SeaRates rolled out its Week 41 updates for 2024, focusing on clearer visual identification, streamlined quotation workflows, and expanded Virtual Office controls.",
    "Logistics Map updates bring carrier visual identities directly into vehicle tracking.",
    "Cards across both the vehicle list and open vehicle unit views now display the carrier name alongside their official logo.",
    "Confirmation emails sent after submitting requests now link directly to transport unit details within Logistics Map, allowing team members to jump straight from an inbox notification to live tracking data.",
    "Data management inside Virtual Office received several functional adjustments.",
    "Transport records now support editing, swapping, or appending extra images during record updates.",
    "Shipping line logos automatically appear based on SCAC codes.",
    "In the Counterparties section, users can group multiple active filters together to narrow down records faster.",
    "Operations involving leasing companies and providers ('by Points') have been refined, including specific updates for OOCL and X-Press.",
    "Quoting workflows now handle city-level origin and destination selections more intelligently.",
    "When requesting a sea freight quote with a City-type location and leaving the port field empty, the system automatically identifies and assigns the nearest port.",
    "Elsewhere in the platform, new content for the Smart Documents tool and the Smart Documents API landing page is now accessible under the Integration menu.",
    "Looking ahead, several updates and tools are in active development or queued for upcoming releases:"
]

print("Sentence count:", len(cand_sentences))
for idx, s in enumerate(cand_sentences):
    print(f"{idx+1}. {s}")

