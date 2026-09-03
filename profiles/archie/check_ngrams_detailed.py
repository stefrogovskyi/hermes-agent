import re
import json

title = "SeaRates System Release Notes: Week 48, 2024 Updates"
meta_title = "SeaRates Release Notes: Week 48, 2024 Platform Updates"
meta_description = "SeaRates Week 48 updates bring container tracking improvements, air cargo enhancements, Virtual Office document controls, and new LandRates pages."

body = """### Tracking System Integrations

Updates to ocean container tracking data feeds cover fourteen global shipping lines and freight forwarders:

* CMA CGM
* DB Schenker
* SITC Container Lines
* Trans Asian Shipping Services
* Cordelia Container Shipping Line
* Heung-A Shipping
* Shipco Transport
* Wan Hai
* Mariana Express Lines (MELL)
* ECU Worldwide
* Yusen Logistics
* Grimaldi Deep Sea S.P.A.
* Sinotrans Container Lines
* Marguisa Shipping Lines

### Air Cargo Data Updates

Air cargo tracking enhancements expand provider integration across twelve airlines:

* French Bee
* Air Caraibes
* Singapore Airlines
* Air Europa
* Hong Kong Air Cargo
* Air China Cargo
* UPS Air Cargo
* Vistara
* Vietnam Airlines
* Air Canada
* Etihad Cargo
* American Airlines

### Shipping Schedules Data Adjustments

Data processing updates for shipping schedules apply to specific provider parameters:

* By Points: ACL, MSC, Hapag-Lloyd, CMA CGM
* By Vessel: Culines

### Virtual Office Document Control

Interface layout and file permissions changed inside the Bookings tab under the Documents section. Downloaded documents default to restricted visibility, appearing exclusively to the booking owner and manager. Remaining booking participants view files only after explicit review and approval by selecting the Show option.

### Transport Management System Navigation

Selecting any Transport Name within the Transport Management System list now displays detailed transport unit data. The action opens the corresponding transport card directly inside the Logistics Map tool.

### Platform Documentation and Tools

Several additions expand documentation across the logistics management platform and freight rate management tools:

* Request an IT Quote form: Added tooltips explaining features including Freight Index, Air Cargo Tracking, Cargo Wizard, CO2 Calculator, Demurrage & Storage Calculator, World Sea Ports, SeaRates Mobile App, SeaRates Enterprise, and Parcel Tracking.
* Quotation System API: Published a dedicated landing page.
* FAQs: Added FAQ resources for the Logistics Explorer and Ship Schedules applications.
* Find a Tool page: Added documentation links for Rail Tracking Web and Road Tracking Web, alongside Freight Index API technical docs.
* LandRates.com: Published new landing pages covering Rail and Road Freight Tracking.

### Recent Feature Rollouts

* Calendar tab inside the Tracking System tool
* Updated Route Planner API version
* Freight Index 1.0 release
* SeaRates Mobile App Version 1.2 featuring the Request System
* Load Calculator Version 2.2 release
* Map platform update"""

with open("/opt/hermes/profiles/archie/article_315_text.txt") as f:
    orig = f.read()

def get_ngrams(text, n=6):
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    words = [w for w in cleaned.split() if w]
    ngrams = set()
    for i in range(len(words) - n + 1):
        ngrams.add(" ".join(words[i:i+n]))
    return ngrams

orig_ngrams = get_ngrams(orig, 6)
rewrite_ngrams = get_ngrams(body, 6)
overlap = orig_ngrams.intersection(rewrite_ngrams)

proper_words = {
    # Carriers & Airlines
    'cma', 'cgm', 'db', 'schenker', 'sitc', 'container', 'lines', 'trans', 'asian', 'shipping',
    'services', 'cordelia', 'heung', 'a', 'shipco', 'transport', 'wan', 'hai', 'mariana', 'express',
    'mell', 'ecu', 'worldwide', 'yusen', 'logistics', 'grimaldi', 'deep', 'sea', 's', 'p', 'sinotrans',
    'marguisa', 'french', 'bee', 'air', 'caraibes', 'singapore', 'airlines', 'europa', 'hong', 'kong',
    'china', 'cargo', 'ups', 'vistara', 'vietnam', 'canada', 'etihad', 'american', 'acl', 'msc', 'hapag',
    'lloyd', 'culines',
    # Tool names & Proper Nouns
    'freight', 'index', 'wizard', 'co2', 'calculator', 'demurrage', 'storage', 'world', 'ports',
    'searates', 'mobile', 'app', 'enterprise', 'parcel', 'tracking', 'system', 'tool', 'and'
}

non_proper_overlaps = []
for ng in overlap:
    words = ng.split()
    if not all(w in proper_words for w in words):
        non_proper_overlaps.append(ng)

print("Total 6-grams in body:", len(rewrite_ngrams))
print("Total 6-gram overlaps:", len(overlap))
print("Non-proper noun 6-gram overlaps:", len(non_proper_overlaps))
if non_proper_overlaps:
    print("Non-proper overlaps:", non_proper_overlaps)

print("\nLENGTH CHECKS:")
print("Title len:", len(title))
print("Meta title len:", len(meta_title))
print("Meta desc len:", len(meta_description))

final_data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}
with open("/opt/hermes/profiles/archie/final_verified_article.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)
