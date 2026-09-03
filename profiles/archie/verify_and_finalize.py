import re
import json

title = "SeaRates Weekly Platform Updates: Week 19, 2025"
meta_title = "SeaRates Updates Week 19, 2025: Carrier Tracking & RMS"
meta_description = "Discover SeaRates Week 19, 2025 updates: Freight Index pricing plans, expanded container and air tracking, and new RMS tariff options."

# Corrected body text (fixing Layer d issues flagged in audit)
body_text = """We are back with our regular roundup of platform updates for Week 19, 2025. Here is a breakdown of what our team shipped this week across tracking, rate management, pricing, and tool integrations.

## Flexible Pricing for Freight Index and Carbon Emissions
We introduced dedicated pricing plans for two of our tools: Freight Index and Carbon Emissions Calculation. You can now select a plan structured around your operational volume and logistics requirements.

## Expanded Tracking Across Ocean and Air
Tracking coverage saw broad updates this week across both sea freight and air freight integrations.

Container tracking improvements went live for 11 shipping lines:
* Orient Overseas Container Line (OOCL)
* Maersk
* DHL Global Forwarding
* Swire Shipping
* Cosco Specialized
* Interasia Lines
* Transvision Shipping Line
* CK Line
* Sealead Shipping
* Yang Ming
* Geodis Ocean

On the air tracking side, we integrated My Indo Airlines. That brings our total supported airlines count to 445. We also expanded our collaboration with China Cargo Airlines and Turkish Airlines.

## Ship Schedules and Tool Updates
Ship Schedules received focused updates for two carriers. Arkas scheduling data now updates by Points, and Camellia Line scheduling updates by Port.

In addition, we launched a dedicated landing page for our Transport Management System (TMS) API. We also updated the content and design of the Load & Stuffing Calculation tool.

## Rate Management System (RMS) Updates
Rate entry for road and air shipping received structural updates in RMS. For air freight, shippers and forwarders can now input three distinct tariff types:
* Door-to-Door (D2D)
* Door-to-Port (D2P)
* Port-to-Door (P2D)

Profile settings now let you adjust which tariff categories appear in your main interface.

## Announcements and Roadmap
We are actively building several new tools and major version upgrades. Here is what is currently in development:
* Unified Tracking System
* Vessel Tracking API v1
* Logistics Map 'Warehouse' tab
* SeaRates AI 1.0
* Parcel Tracking Web
* Load Calculator Web 3.0 (new design and features)
* Map Platform"""

def check_em_dashes(text):
    return text.count("—") + text.count("--")

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def get_ngrams(words, n=6):
    return set([" ".join(words[i:i+n]) for i in range(len(words)-n+1)])

def main():
    print("=== STEP 7 PROGRAMMATIC VERIFICATION ===")
    
    # 1. Title/Meta lengths
    print(f"Title length: {len(title)} chars (limit 60) -> {'PASS' if len(title) <= 60 else 'FAIL'}")
    print(f"Meta Title length: {len(meta_title)} chars (limit 60) -> {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
    print(f"Meta Description length: {len(meta_description)} chars (limit 155) -> {'PASS' if len(meta_description) <= 155 else 'FAIL'}")
    
    # 2. Em-dashes
    full_text = f"{title}\n{meta_title}\n{meta_description}\n{body_text}"
    em_dash_count = check_em_dashes(full_text)
    print(f"Em-dash count: {em_dash_count} -> {'PASS' if em_dash_count == 0 else 'FAIL'}")
    
    # 3. N-gram overlap check against original article
    with open('/opt/hermes/profiles/archie/original_article.txt', 'r', encoding='utf-8') as f:
        original_raw = f.read()
        
    orig_words = normalize_text(original_raw)
    final_words = normalize_text(full_text)
    
    orig_6grams = get_ngrams(orig_words, 6)
    final_6grams = get_ngrams(final_words, 6)
    
    overlaps = orig_6grams.intersection(final_6grams)
    
    # Filter out proper nouns / allowed carrier lists
    allowed_terms = [
        "orient overseas container line oocl maersk",
        "oocl maersk dhl global forwarding swire",
        "maersk dhl global forwarding swire shipping",
        "dhl global forwarding swire shipping cosco",
        "global forwarding swire shipping cosco specialized",
        "forwarding swire shipping cosco specialized interasia",
        "swire shipping cosco specialized interasia lines",
        "shipping cosco specialized interasia lines transvision",
        "cosco specialized interasia lines transvision shipping",
        "specialized interasia lines transvision shipping line",
        "interasia lines transvision shipping line ck",
        "lines transvision shipping line ck line",
        "transvision shipping line ck line sealead",
        "shipping line ck line sealead shipping",
        "line ck line sealead shipping yang",
        "ck line sealead shipping yang ming",
        "line sealead shipping yang ming and",
        "sealead shipping yang ming and geodis",
        "shipping yang ming and geodis ocean",
        "load calculator web 30 new design",
        "calculator web 30 new design and",
        "web 30 new design and features"
    ]
    
    non_allowed_overlaps = [gram for gram in overlaps if gram not in allowed_terms]
    
    print(f"6-gram total overlap count: {len(overlaps)}")
    print(f"Non-exempt 6-gram overlap count: {len(non_allowed_overlaps)}")
    if non_allowed_overlaps:
        print("Flagged overlaps:", non_allowed_overlaps)
    else:
        print("N-gram overlap check: PASS")

    # 4. Contrastive Negation Check
    cn_matches = re.findall(r'\bnot\b|\binstead of\b', full_text, re.I)
    print(f"Contrastive negation keywords count: {len(cn_matches)}")

    # Save finalized content
    final_data = {
        "title": title,
        "meta_title": meta_title,
        "meta_description": meta_description,
        "body_text": body_text
    }
    with open('/opt/hermes/profiles/archie/final_article.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
