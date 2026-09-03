import re

orig = """We appreciate your continuous help with SeaRates and are excited to roll out new features that will enhance your experience. We place a high importance on service improvement.
Browse our earlier releases for the latest data.

What’s new for week 41:

Logistics Map improvements:
- For the ‘Transport’ tab, we have added the display of the carrier's logo and name to the card in the vehicle list and the open vehicle unit card.
- In addition, you can go to the detailed information about the transport unit in the Logistics Map directly from the emails confirming your request.

Virtual Office updates:
- For the ‘Transport’, we have implemented the ability to change, edit, or add extra images when editing data on the transport unit, as well as added the display of shipping line logos by SCAC code.
- For the ‘Counterparties’, we have improved the filter to allow you to group several applied filters simultaneously.
- Also, we have enhanced our work with leasing companies and providers, including OOCL and X-Press for ‘by Points’.

Other updates:
- For the Request a Quote form, we have implemented the selection of the nearest port in case you have not selected one for sea transportation when choosing a location of the City type.
- Finally, we have created content for the Smart Documents tool and Smart Documents API landing page to the ‘Integration’ menu."""

cand_body_prose = """SeaRates rolled out its Week 41 updates for 2024, focusing on clearer visual identification, streamlined quotation workflows, and expanded Virtual Office controls.

Logistics Map updates bring carrier visual identities directly into vehicle tracking. Cards across both the vehicle list and open vehicle unit views now display the carrier name alongside their official logo. Confirmation emails sent after submitting requests now link directly to transport unit details within Logistics Map, allowing team members to jump straight from an inbox notification to live tracking data.

Data management inside Virtual Office received several functional adjustments. Transport records now support editing, swapping, or appending extra images during record updates. Shipping line logos automatically appear based on SCAC codes. In the Counterparties section, users can group multiple active filters together to narrow down records faster. Operations involving leasing companies and providers ('by Points') have been refined, including specific updates for OOCL and X-Press.

Quoting workflows now handle city-level origin and destination selections more intelligently. When requesting a sea freight quote with a City-type location and leaving the port field empty, the system automatically identifies and assigns the nearest port. Elsewhere in the platform, new content for the Smart Documents tool and the Smart Documents API landing page is now accessible under the Integration menu."""

def normalize_words(text):
    return [w.lower() for w in re.findall(r'\b\w+\b', text)]

o_words = normalize_words(orig)
c_words = normalize_words(cand_body_prose)

for length in range(6, 15):
    o_ngrams = set(tuple(o_words[i:i+length]) for i in range(len(o_words)-length+1))
    c_ngrams = set(tuple(c_words[i:i+length]) for i in range(len(c_words)-length+1))
    common = o_ngrams.intersection(c_ngrams)
    if common:
        print(f"Length {length} matches in prose:")
        for g in common:
            print("  ", " ".join(g))

