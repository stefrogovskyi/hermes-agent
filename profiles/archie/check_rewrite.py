import re

orig_text = """Freight Forwarding: What to Expect in the Next 10 Years
Future of Freight Forwarding in the next 10 years
The volume of the container shipping market will increase by approximately 4% by the end of 2024. Demand for maritime transportation is expected to grow by 7-8%. Meanwhile, air transportation showed a 9% increase in 2023, and this upward trend continues to this day. Conclusion: the multimodal transportation market is rapidly evolving. In this article, we will explore five trends we are likely to observe in the next 10 years.
But first, we would like to remind you that SeaRates provides logistics services, particularly container shipping services. To request an individual quote for shipping, you can use the appropriate form on our website. And our potential partners have the opportunity to join the community of logistics providers.
Popularization of Artificial Intelligence
Artificial intelligence is used to write articles, create memes, and develop software code. But who said the scope of this technology is limited to that? Logistics companies are already actively utilizing the latest advancements in artificial intelligence.
Smart software for freight forward transportation is engaged in planning, route development, data processing, and forecasting. Most likely, in the next 10 years, the market will see at least a few software products for air freight forwarding and other sectors, which will be able to take over some responsibilities and perform tasks better than humans.
For example, SeaRates already uses an AI chat that helps customers find freight rates for all types of transport to any destination, track their cargo, find schedules by vessel, port, or points, and answers all questions related to SeaRates products, logistics, and more.
Increased Complexity of Transportation
This is driven by two factors. First, there is geopolitical instability. Due to border closures and the implementation of sanctions, freight forwarding companies are forced to develop new routes and think about how to ensure that these significant changes do not severely impact profits.
Second, global forwarding is facing the challenge of natural disasters, which complicates logistics, in particular container drayage. Humanity has not been very careful with nature, and it is unlikely that we can expect major changes in this regard in the future. Purely natural factors should not be excluded either: storms, hurricanes, tsunamis, and volcanic eruptions. These incidents are happening more and more frequently harming international container transport market.
The bad news is that there are no signs of improvement in the situation. Consequently, every international freight forwarder should plan their business considering these factors.
But some companies prove that even under such conditions, it is possible to provide truly high-quality logistics services. For online quotes and bookings, click on this link.
It is worth noting that SeaRates provides customers with tools that help calculate transit time and route distance, taking into account real-time situations and data provided by carriers. This allows for the avoidance of delays in cargo transportation and provides customers with accurate information regarding logistics.
Increased Competition
Every year, dozens of new companies enter the air freight forwarding market, sea freight forwarding market, etc. This is facilitated by the successes and high profits of existing firms, as well as an increase in the number of professional personnel and greater availability of transportation means.
As a result, to not only become the best freight forwarder but also to avoid losing clients at all, companies need to work on competitive advantages. For example, providing additional services for a separate fee, using less popular routes, lowering prices, and so on. Many international freight forwarding companies are already doing this, offering not only transportation options but also developing a range of additional services related to cargo tracking.
If you want to provide your clients with top-notch logistics services, you can join the Digital Freight Alliance (DFA) network, which includes more than 8,000 freight forwarding companies worldwide. Your clients will be able to benefit from modern digital services offered by DFA, and your business will reach a new level, expanding the range of services. You will have the opportunity to exchange experience, promote your freight rates, or resell partner rates.
Collaboration Among Forwarders
The complexity of logistics due to the two factors above, as well as increased competition, will push companies to work together. Simply put, firms will delegate the transportation and handling of certain cargo to each other if a partner plans a route along a similar path.
Some companies are already working on the Less Container Load principle. Container freight forwarding is a particularly convenient option in terms of joint work of several logistic companies.
By the way, if your company needs logistics assistance, you have the opportunity to request support from our digital team in selecting a customized solution for your business or to request an individual IT quote for a specific solution. Our modern solutions will certainly help your business.
Decarbonization
Global organizations are paying attention to environmental pollution levels. For example, if you want to do international container shipping legally, you can no longer simply saturate the planet with greenhouse gases and byproducts of fuel consumption. Special attention from regulators is focused on sea freight logistics, which is setting negative records in this grim ranking. European organizations are already requiring companies (for example, companies engaged in ocean freight) to provide detailed reports on the technical condition of vehicles and the volume of harmful emissions. Most likely, the requirements will become stricter and will apply globally.
SeaRates offers partners to use a CO2 tool. With its help, you can calculate the volume of CO2 emissions for any type of transportation (by sea, air, or land). This tool can be used as a white label solution or API. If you integrate it into your business, you can also offer offset costs to your clients.
Our Solutions are at Your Service
Remember that one of the key modern trends, which is bound to evolve over the next 10 years, is digitalization. It doesn't matter who you are – a logistics company, a trader, or a participant of the logistics process – you need to pay attention to modern technologies. Our team is ready to help your company. Contact us, and we will select the latest and most effective solutions suitable for your specific business needs.
"""

def tokenize(text):
    text = text.lower()
    words = re.findall(r'\b[a-z0-9]+\b', text)
    return words

orig_tokens = tokenize(orig_text)

def get_ngrams(tokens, n):
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))

orig_6grams = get_ngrams(orig_tokens, 6)

def check_text(title, meta_title, meta_desc, body):
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    body_tokens = tokenize(full_text)
    
    # Check 6-gram overlaps
    overlaps = []
    for i in range(len(body_tokens)-5):
        gram = tuple(body_tokens[i:i+6])
        if gram in orig_6grams:
            overlaps.append(" ".join(gram))
            
    # Check rule violations
    errors = []
    
    # Em-dashes
    for dash in ['—', '--', '–']:
        if dash in full_text:
            errors.append(f"Dash found: '{dash}'")
            
    # Cliches
    cliches = [
        "delve into", "delve", "testament to", "crucial role", "in today's world",
        "it is worth noting", "game-changer", "game changer", "pivotal", "unraveling",
        "beacon", "landscape", "spearheading", "unlocking", "tapestry", "seamless",
        "realm", "foster", "dive into", "in conclusion", "elevate", "harness", "empower"
    ]
    for c in cliches:
        if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Cliche found: '{c}'")
            
    # Connectors
    connectors = ["Furthermore", "Moreover", "In conclusion", "Additionally", "Consequently", "On the other hand"]
    for conn in connectors:
        if re.search(r'\b' + re.escape(conn) + r'\b', full_text, re.IGNORECASE):
            errors.append(f"Forbidden connector found: '{conn}'")
            
    # Contrastive negation count: "not ... but ...", "not only ... but ...", "rather than", "instead of", "not X, Y"
    negation_patterns = [
        r'\bnot\b[^\.\?\!]{1,50}\bbut\b',
        r'\brather than\b',
        r'\binstead of\b',
    ]
    neg_matches = []
    for pat in negation_patterns:
        for m in re.finditer(pat, full_text, re.IGNORECASE):
            neg_matches.append(m.group(0))
            
    # Length checks
    if len(title) > 60: errors.append(f"Title too long ({len(title)} > 60)")
    if len(meta_title) > 60: errors.append(f"Meta title too long ({len(meta_title)} > 60)")
    if len(meta_desc) > 155: errors.append(f"Meta desc too long ({len(meta_desc)} > 155)")
    
    # Keyword checks
    required_keywords = [
        "digital freight forwarding trends",
        "multimodal route optimization",
        "AI in ocean freight planning",
        "maritime decarbonization reporting",
        "container tracking visibility"
    ]
    missing_kw = []
    for kw in required_keywords:
        if kw.lower() not in full_text.lower():
            missing_kw.append(kw)
            
    return overlaps, errors, neg_matches, missing_kw

print("Auditor loaded.")
