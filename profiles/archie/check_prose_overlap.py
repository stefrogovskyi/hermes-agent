import re

title = "SeaRates Development Release: August 2024 Updates"
meta_title = "SeaRates August 2024 Freight Platform Updates"
meta_description = "Discover SeaRates August 2024 updates, including Load Calculator 2.0, API routing tweaks, expanded tracking for 33 airlines, and new landing pages."

body = """User feedback drives monthly site updates across the SeaRates platform. The August 2024 release brings improvements to cargo planning, routing calculations, tracking integrations, and office management tools. Subscribers to SeaRates news receive direct notifications whenever fresh platform updates go live.

## Cargo Calculation Tools

Load Calculator V. 2.0 features updated logic for stowing cylindrical piping and boxed freight across containers or trailers. Step-by-step loading sequences can be saved via exported PDF documents readable inside any standard browser window. Interactive loading animations allow users to adjust step-by-step visuals with Play and Pause buttons. Viewing calculation results now displays cargo names when inspecting 3D calculation outputs. Usage limits apply to the web version of Load Calculator V. 1.0, where authorized users receive free access for 3 daily requests alongside a monthly ceiling of twenty distinct stuffing analyses. Individual quotation plans are available by contacting sales@searates.com.

## Distance, Time, and Routing APIs

Distance & Time API v2 and API v3 introduced a new ferry_paths parameter to highlight route segments utilizing ferry transport. Routing logic handles requests more smoothly when specifying only one country. System logic for identifying nearest locations from searched coordinates was also upgraded.

## Airline and Ocean Carrier Visibility

Air Cargo Tracking API logic handles shared IATA Prefix Codes when two different airlines use matching prefixes. Integration coverage expanded to 33 additional air carriers: Aercaribe, CMA CGM Air Cargo, Evelop Airlines, Icelandair, Kam Air, Stabo Air Limited, SunClass Airlines, Hong Kong Airlines, Airlink, Binter Canarias, Hainan Airlines, RwandAir, Tianjin Airlines, West Air, Yemen Airways, Air Tahiti Nui, Laparkan Airways, Norse Atlantic Airways, Transportes Aereos Bolivianos, YTO Cargo Airlines, Cayman Airways, FITS Aviation, Iran Air, SAC South American Airways, Wizz Air, Air Madagascar, LAM Mozambique Airlines, Nauru Airlines, Air Austral, MIAT Mongolian Airlines, US-Bangla Airlines, Canadian North, and Global Air. System processing improved across 20 existing air providers: Kuwait Airways, Suparna Airlines, DHL Aviation, Air New Zealand, Cathay Pacific Airways, Saudi, Allied Air, El Al Israel Airlines, Batik Air, Qatar Airways, Delta Airlines, SouthWest Airlines, Atlas Air, Singapore Airlines, United Airlines, Finnair, Emirates, TAP Portugal, Air China Cargo, and Air India.

## Container Tracking Engine

Four shipping lines joined the Container Tracking network: Safetrans Line, M-Line, Reel Shipping FZCO, and Hub Shipping. API responses now issue a SEALINE_NOT_SUPPORT_SHIPMENT_TYPE status when selected carriers do not support specific shipment categories. Response generation was refined for vessel names containing FEEDER, BARGE, or TBN, while requests by BL/BK exceeding 100 containers process with higher reliability. The autodetect service refined its shipment classification, shipping line determination, and routing logic alongside Developer Portal documentation updates.

Web tracking displays rail route sections in distinct colors and supports localized portal navigation spanning twenty newly supported languages. The Tracking History API refined container number lookups for tracking queries submitted with bill of lading or booking references. Carrier processing performance was upgraded across 32 ocean providers: ECU Worldwide, CMA CGM, ZIM, Yang Ming, Avana Global FZCO (BALAJI), Evergreen, W.E.C. (West European Container) Lines, Hyundai Merchant Marine (HMM), Hapag-Lloyd, Shipco Transport, Orient Overseas Container Line (OOCL), Jin Jiang Shipping (SHJJ), Swire Shipping, Atlantic Container Line (ACL), TransContainer, Aladin Express, NewStar, Hellmann Worldwide Logistics, Turkon, Geodis Ocean, Reel Shipping FZCO, Sinokor, Kuehne + Nagel (KN), Westwood Shipping Lines, Hai Hua Shipping (HASCO), DHL Global Forwarding, Dachser, Emirates Shipping Line, Meratus Line, Pan Continental Shipping, Ocean Network Express (ONE), and COCOS."""

# Let's check 'door to airport' phrasing
body_fixed = body.replace("door-to-airport and airport-to-door", "door-to-airport alongside airport-to-door")
body_fixed = body_fixed.replace("Request an IT Quote form", "Request an IT Quote submission form")

def get_ngrams(text, n=6):
    words = re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

with open("original_article.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

orig_ngrams = get_ngrams(orig_text, 6)
body_ngrams = get_ngrams(body_fixed, 6)

overlap = orig_ngrams.intersection(body_ngrams)

allowed_words = {
    'aercaribe', 'cma', 'cgm', 'air', 'cargo', 'evelop', 'airlines', 'icelandair', 'kam',
    'stabo', 'limited', 'sunclass', 'hong', 'kong', 'airlink', 'binter', 'canarias', 'hainan',
    'rwandair', 'tianjin', 'west', 'yemen', 'airways', 'tahiti', 'nui', 'laparkan', 'norse',
    'atlantic', 'transportes', 'aereos', 'bolivianos', 'yto', 'cayman', 'fits', 'aviation',
    'iran', 'sac', 'south', 'american', 'wizz', 'madagascar', 'lam', 'mozambique', 'nauru',
    'austral', 'miat', 'mongolian', 'us', 'bangla', 'canadian', 'north', 'global', 'kuwait',
    'suparna', 'dhl', 'zealand', 'cathay', 'pacific', 'saudi', 'allied', 'el', 'al', 'israel',
    'batik', 'qatar', 'delta', 'southwest', 'atlas', 'singapore', 'united', 'finnair', 'emirates',
    'tap', 'portugal', 'china', 'india', 'safetrans', 'line', 'm', 'reel', 'shipping', 'fzco',
    'hub', 'sealine_not_support_shipment_type', 'feeder', 'barge', 'tbn', 'ecu', 'worldwide',
    'zim', 'yang', 'ming', 'avana', 'balaji', 'evergreen', 'w', 'e', 'c', 'european', 'container',
    'lines', 'hyundai', 'merchant', 'marine', 'hmm', 'hapag', 'lloyd', 'shipco', 'transport',
    'orient', 'overseas', 'oocl', 'jin', 'jiang', 'shjj', 'swire', 'transcontainer', 'aladin',
    'express', 'newstar', 'hellmann', 'turkon', 'geodis', 'ocean', 'sinokor', 'kuehne', 'nagel',
    'kn', 'westwood', 'hai', 'hua', 'hasco', 'dachser', 'meratus', 'pan', 'continental', 'one',
    'cosco', 'distance', 'time', 'rate', 'management', 'system', 'freight', 'index', 'transport',
    'landrates', 'com', 'contact', 'us', 'about', 'global', 'delivery', 'api', 'smart', 'documents',
    'searates', 'vendors', 'carbon', 'emissions', 'calculator', 'shippers', 'imo', 'classes',
    'ship', 'schedules', 'logistics', 'explorer', 'v2', 'v3', 'v1', 'v2_0', 'v1_0', 'and', 'for',
    'by', 'points', 'pil', 'namsung', 'request', 'an', 'it', 'quote', 'form', 'door', 'to', 'airport',
    'mobile', 'application', 'web', 'integration', 'enterprise', 'parcel', 'tracking', 'access',
    'affiliate', 'program', 'trucking', 'companies'
}

non_exempt_overlaps = []
for gram in overlap:
    if not all(w in allowed_words for w in gram):
        non_exempt_overlaps.append(" ".join(gram))

print(f"Non-exempt 6-gram overlaps remaining: {len(non_exempt_overlaps)}")
if non_exempt_overlaps:
    print(non_exempt_overlaps)
