import json, re

orig = """Title: Truck Towing Service in Germany – Costs, Assistance & Emergency Guide

## Truck Towing Service in Germany – How to Act Correctly at Night and on Public Holidays
Imagine your truck breaks down in the middle of a German highway – it is late at night or during a public holiday. Immediate questions arise: Who should I call? What are the costs of towing a truck? Can a truck towing service even handle my vehicle and trailer? With the right roadside assistance, you can resolve the situation quickly and safely.

## Night or Holiday: Where to Get Help if the Truck Breaks Down
When the engine fails or a technical issue immobilizes the truck, it is crucial to remain calm. First, bring the truck safely to the roadside, switch on the hazard lights, and set up the warning triangle. Breakdowns at night or on public holidays are particularly stressful. Many workshops are closed, and only a limited number of truck towing services are available. Emergency services are heavily utilized, and waiting times can escalate quickly.

When selecting the right provider, you should consider the following points: availability around the clock, expertise with trucks, equipment with a crane, and the ability to lower components such as the cardan shaft or oil. The expected arrival time should also be clearly confirmed.

In Germany, the police are only responsible for breakdowns or towing in exceptional cases. Generally, it is not worthwhile to call a patrol car – this can become unnecessarily expensive. It is faster and more cost-efficient to directly engage a truck towing service yourself. The most effective option is contacting an established company with a nationwide partner network. This way, you have only one point of contact, and a suitable truck towing service near you will be organized immediately.

For foreign drivers, it is helpful if the roadside assistance staff speaks English, Polish, or Russian – this significantly reduces the risk of misunderstandings. To ensure the truck towing service can respond quickly and with the right equipment, drivers should be prepared to provide key information during the first call.

## Essential information for the emergency call:
- Vehicle type and load weight
- Whether truck, trailer, or both are affected
- Current location (GPS data) and desired destination (e.g., workshop or parking area)
- Relevant photos of the breakdown
- License plates of a truck and trailer
- Whether the vehicle is still partially operational

Experienced providers such as MT onroad report from practice that precisely this information is often crucial for efficiently organizing a repair or truck towing.

## Costs of Truck Towing in Germany
The cost of towing a truck in Germany can vary significantly. Influencing factors include time of day, load complexity, distance traveled, weight, and dimensions of the vehicle. To ensure reliable shipping cost planning, you should always request a clear cost estimate in advance and clarify which services are included.

Particularly important aspects to check:
- Whether load handling and waiting times are included in the price
- Which additional fees may apply, such as for night, holiday, or long-distance operations
- Whether a per-kilometer rate is charged
- Whether a separate fee is required for a trailer

Serious providers present prices transparently and confirm them in writing or via messenger. In practice, companies working at market-level prices are generally reliable and predictable – whereas extremely cheap offers carry the risk that the job may not be fulfilled at short notice.

## Technical Requirements for Truck Towing Services
Not every tow truck can handle a loaded truck with a semi-trailer or special body. Therefore, it is important to describe the situation precisely from the outset – ideally with photos. Often, a picture shows only one side of the truck, while the actual obstacle is on the other side, such as a large rock or uneven surface.

When making the call, prepare all relevant vehicle data:
- Total weight
- Length and height of the truck
- Presence of a trailer or semi-trailer
- Specific loading conditions, such as blocked wheels

Unsuitable equipment leads to time loss, repeated calls, and additional costs. Therefore, select services that have heavy-duty tow trucks with sufficient load capacity and appropriate equipment in their fleet.

## Extra Practical Tip for Truck Drivers
Prevention pays off: save emergency contacts, keep all vehicle data ready, and document a defect as accurately as possible – photos often say more than words. Such small preparations can be decisive in an emergency and ensure that help arrives faster and the process runs smoothly.

Explore more opportunities with SeaRates by contacting us according to your interest category."""

with open('article.json') as f:
    cand_data = json.load(f)

cand_full = cand_data.get('title','') + "\n" + cand_data.get('meta_title','') + "\n" + cand_data.get('meta_description','') + "\n" + cand_data.get('body_markdown','')

def tokenize(text):
    # keep punctuation or tokenize words
    return re.findall(r'\b[\w\'-]+\b', text)

orig_tokens = tokenize(orig)
cand_tokens = tokenize(cand_full)

# Find max matching subsequences
from difflib import SequenceMatcher

matcher = SequenceMatcher(None, [t.lower() for t in orig_tokens], [t.lower() for t in cand_tokens])
for match in matcher.get_matching_blocks():
    i, j, n = match
    if n >= 4:
        orig_seq = " ".join(orig_tokens[i:i+n])
        cand_seq = " ".join(cand_tokens[j:j+n])
        print(f"Match length {n}:")
        print(f"  Orig: '{orig_seq}'")
        print(f"  Cand: '{cand_seq}'")

