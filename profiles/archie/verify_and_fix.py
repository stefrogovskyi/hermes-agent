import json
import re

ORIGINAL_TEXT = """
There is one category of goods that invariably draws higher revenue in the service of ports, carriers, and insurance companies in international trade. These are dangerous goods or IMO cargo consisting of goods that may pose a risk to human life, a ship, or the environment.

And with the adage "dangerous," most of these cargoes are, in fact, perfectly safe, doing things by the book laid down by the IMDG Code (International Maritime Dangerous Goods Code). Trouble arises when the exporter is either unaware or negligent of the finer details.

This article is a neat guide for shippers, carriers, and freight forwarders working with or planning to ship IMO cargo. It examines what falls within the terminology of "dangerous" cargo, including which classes are most commonly "stuck" in ports, the documents a container must have to gain acceptance on a ship, and how to avoid the most common mistakes.

## 9 classes of dangerous goods

Class 1: Explosive substances - React explosively (e.g., fireworks, ammunition)
Class 2: Gases - Compressed, liquefied, dissolved (e.g., propane, oxygen, CO2)
Class 3: Flammable liquids - Evaporate and burn easily (e.g., paints, solvents, alcohols)
Class 4: Flammable solids - Can ignite from friction or heat (e.g., matches, powdered metals)
Class 5: Oxidizers and organic peroxides - Cause other substances to ignite (e.g., hydrogen peroxide, nitrates)
Class 6: Toxic and infectious substances - Harmful to humans (e.g., pesticides, medical samples)
Class 7: Radioactive materials - Emits radiation (e.g., isotopes, medical preparations)
Class 8: Corrosive substances - Destroys materials and fabrics (e.g., acids, alkalis)
Class 9: Other hazardous substances - Not included in previous categories but pose a risk (e.g., lithium batteries, dry ice)

Note: Each class has its own packaging, marking, and placard instructions (markings on the container). If these markings are absent or wrong, as well as packing or loading, the container cannot be admitted into the port or onto the ship. So, pay attention to labeling and proper container loading to ensure efficient and secure delivery and unloading further.

## Which cargo classes most often get "stuck" in ports?

Cargo delays in ports are generally not attributable to the "dangerous" nature of the cargo itself, but rather to human factors along with documentation issues, mostly. Here are some common scenarios:

### Class 3 — Flammable liquids
Paints, varnishes, solvents, perfumes, disinfectants.
Most often detained and delayed for wrong or no declaration or absence of MSDS (material safety data sheet).
Typical situation: the exporter simply states "paint" instead of "Paint, flammable, UN1263, Class 3, PG II".
You planned your route and made your reservations according to the shipping schedule to minimize the risk of losing your space while correcting your documents. However, the shipping line may block the container and require a DGD (dangerous goods declaration) correction, resulting in the loss of your shipment.

### Class 5 — Oxidizers and organic peroxides
Chemical reagents, fertilizers, disinfectants.
Problems — incompatibility with other cargoes.
Example: a loader placed a Class 5 container next to a Class 3 container (flammable liquids). The port authority blocks the shipment right away for fear of a mutual reaction. The container has to be segregated, which may last for days.

### Class 8 — Corrosive substances
Acids, alkalis, electrolytes.
Concerns are damage to the packaging. Even a small leak = automatic ban on loading.
Example: There was a slight acid stain on a pallet; the port service requires disposal of the packaging or repacking of the goods. Delay: 5 days maximum, plus additional cleaning charges.

### Class 9 — Other dangerous substances (especially lithium batteries)
The most common "stuck" class in 2020–2025.
The problem is the inconsistency of documents and labeling.
Example: The company ships electric scooters with built-in lithium-ion batteries, but fails to state that the batteries are Class 9. While scanning, the port finds the batteries, and the container is blocked and blacklisted by the carrier.

After dispatch, keep track of the shipment status via SeaRates Container Tracking, as it helps you react quickly if the container is "stuck".

### Why are ports particularly vigilant?
After a number of major accidents, namely in Beirut, Tianjin, and Hamburg, seaports have been enforcing extreme controls.
The container may be:
- unpacked for inspection;
- sent to a special site for verification;
- disposed of without compensation (if the risk is high).
Thus, a small mistake in the UN number or an incorrect label can cause loss of thousands of dollars and a contract.

## Documentation: essentials for the container to be accepted

Dangerous cargo is always subject to the rules of shipping documentation. For containers to be allowed for shipment, a complete set of IMO documentation must be submitted, with each document adhering to the IMDG standards.

### 1. Dangerous Goods Declaration (DGD)
This is the main document from the sender, which specifies:
- Proper Shipping Name (official name of the substance),
- UN Number,
- Class, Subclass, Packing Group,
- quantity, type of container, temperature, density,
- confirmation that the packaging complies with IMDG requirements.
The exporter or authorized representative signs the DGD. The container cannot gain entry into the port without this transportation document.

### 2. Material Safety Data Sheet (MSDS)
A safety data sheet from the manufacturer of the goods. It tells of the physical and chemical properties; hazards; safe handling measures; spill response, clean-up, etc. The carrier uses the MSDS to check whether the cargo does indeed fit its stated class.

### 3. Container Packing Certificate (CPC)
Proof that cargo has been loaded and packed correctly, free from damage or leakage; separation of incompatible substances has been taken care of. The CPC is usually signed by the forwarder or packing company.

### 4. Transport Document / Bill of Lading (B/L)
The field for the description should note that the cargo is an IMO cargo:
UN 3480, Lithium-ion batteries, Class 9, PG II, Marine pollutant
or a similar format for your product.

### 5. Packaging certificates (UN packaging certificate)
Every packaging for IMO cargo shall be capable of being certified under UN standards. The marking on the packaging shall be:
4G/Y30/S/23/UA/123456
where "UA" is the country that certified the packaging.

### 6. Container marking
Each side of the container will bear placards (stickers with the class symbol) and inscriptions with the correct Shipping Name. The stickers should be waterproof, with a minimum size of 250 mm, and in a contrasting color.

You can conveniently set rates and make bookings in the Logistics Explorer tool. For non-standard routes or digital support needs for your logistics, please submit your query via Request an IT Quote.

### How does it work in practice?
If there is any document missing or if the details conflict (for example, a discrepancy between DGD and B/L), the container will not be allowed to be loaded.
Furthermore, the big carriers (Maersk, MSC, and CMA CGM) take the extra step to automatically boycott such a container inside their computer systems, where even a line manager cannot "push" it through without the updated documentation.

## Common mistakes and how to avoid them

1. "Hidden" dangerous cargo: Goods are declared as ordinary when they fall under IMO (e.g., "cleaning agent" without class). Fine up to $10,000 + 6-month ban.
2. Incorrect packaging: Plastic canisters/pallets not UN certified. Results in repacking request and missed vessel.
3. Discrepancies in documents: UN Number on DGD does not match MSDS or B/L. Names must match absolutely.
4. No prior agreement with the line: Carrier hasn't pre-approved cargo. Container refused entry despite good docs.
5. Insufficient container labeling: Placards on only two sides or damaged = automatic hold.

## Checklist "How to avoid delays and fines"

1. Check UN Number and classification against IMDG Code / UN database.
2. Agree on IMO cargo with shipping line in advance (provide MSDS, draft DGD, route details, and cargo description).
3. Use UN certified packaging with UN markings.
4. Check container placards on all 4 sides.
5. Prepare full document set: DGD, MSDS, CPC, Bill of Lading with IMO mark, UN packaging certs, Cargo insurance policy.
6. Coordinate with forwarder and terminal/port in advance (notify IMO status).
7. Train staff (at least foundation course in IMDG Code, 50%+ staff certified).

## Discover cases

Case 1. Paint and varnish products, Class 3: Exporter declared "paint materials" without specifying Class 3. MSC held container before loading. 10-day delay, repacking required, $2,500 fine.
Case 2. Fertilizers, Class 5.1: Container with nitrates placed next to food products. Port detected segregation violation. Relocation cost $1,200, lost slot.
Case 3. Electric scooters with lithium-ion batteries, Class 9: Exporter omitted battery details on transport papers. Maersk blocked booking, issued official warning.

## Conclusion & Business Value
IMO requirements protect against downtime, fines, and customer loss. Well-packed cargo passes port inspection on first try. Improper docs or labels cause week-long delays and tens of thousands in losses.
IMO cargoes span cosmetics to electronics batteries. Proper prep, docs, and carrier coordination ensure containers never get stuck.
"""

def clean_words(text):
    text_lower = text.lower()
    text_clean = re.sub(r'[^\w\s]', '', text_lower)
    return text_clean.split()

def get_ngrams(words, n=6):
    return [tuple(words[i:i+n]) for i in range(len(words)-n+1)]

def main():
    with open('/opt/hermes/profiles/archie/final_output.json') as f:
        data = json.load(f)
        
    title = data['title']
    meta_title = data['meta_title']
    meta_desc = data['meta_description']
    article = data['article_text']
    
    print("--- STEP 7 AUDIT CHECKS ---")
    
    # 1. Em-dash check
    em_dashes = 0
    all_fields = [title, meta_title, meta_desc, article]
    for field in all_fields:
        em_dashes += field.count('—') + field.count('--')
    print(f"1. Em-dashes count: {em_dashes} (Target: 0)")
    
    # 2. Field length checks
    print(f"2. Title length: {len(title)} / 60 max")
    print(f"   Meta title length: {len(meta_title)} / 60 max")
    print(f"   Meta description length: {len(meta_desc)} / 155 max")
    
    # 3. 6-gram overlap check
    orig_words = clean_words(ORIGINAL_TEXT)
    draft_words = clean_words(article)
    
    orig_ngrams = set(get_ngrams(orig_words, 6))
    draft_ngrams = get_ngrams(draft_words, 6)
    
    overlapping = []
    for ng in draft_ngrams:
        if ng in orig_ngrams:
            overlapping.append(' '.join(ng))
            
    unique_overlaps = list(set(overlapping))
    print(f"3. 6-gram overlap count: {len(unique_overlaps)}")
    for ov in unique_overlaps:
        print(f"   - Overlap: \"{ov}\"")

    # 4. Check contrastive negations
    contrastive = len(re.findall(r'\bnot\b.*?\binstead\b|\binstead of\b|\bnot a\b|\bnot directly\b', article, re.IGNORECASE))
    print(f"4. Contrastive negation markers: {contrastive} (Limit: max 1)")

if __name__ == '__main__':
    main()
