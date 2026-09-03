import re

title = "Growth Strategies and Social Media Tools for Ocean Freight Marketers"
meta_title = "Growth Strategies for Ocean Freight Social Media"
meta_desc = "Discover social media tools and content strategies to build credibility, generate B2B logistics leads, and grow your maritime shipping business."

body = """Maritime shipping handles 80 percent of international trade, making it a massive commercial market. Expanding an ocean freight or logistics operation requires reaching new client bases, and modern digital promotion offers a clear path toward qualified accounts. Applying targeted software tools alongside disciplined content publishing builds audience trust and attracts prospective cargo owners.

### Quick Exposure and Channel Growth

Building an initial online footprint or expanding existing account reach requires dedicated channel management. Platforms such as LikesID.com, LikesAround.com, SocialBoss.org, and VideosGrow.com help raise social media metrics, increasing brand awareness and driving inbound traffic to maritime shipping profiles.

### Schedule Planning and B2B Lead Monitoring

Managing daily freight operations leaves little time for manual social media updates. Scheduling tools like Hootsuite and Planoly.com allow teams to organize, plan, and queue content weeks in advance. Automating publication schedules keeps company accounts active without distracting management from core logistics duties, while helping track B2B logistics social media marketing leads generated from online campaigns.

### Audience Analytics and Research

Sustained growth requires detailed market research and regular performance reviews. Analytics platforms such as Emplifi and Sproutsocial provide quantitative data on target client demographics, helping shipping companies evaluate prior promotional efforts and refine future messaging.

### Visual Graphics and Video Production

Visual presentation forms the initial impression prospective clients have of a transport enterprise. Graphic editors like VSCO, Picsart, and Canva allow marketers to draft polished images and promotional graphics without hiring outside agencies.

Video posts perform exceptionally well across maritime social platforms. Sharing logistics insights, equipment demonstrations, and ocean shipping trends builds industry authority. Platforms like Wave.video and Veed, as well as AI Video Maker tools, turn operational clips into engaging videos that build audience trust.

### Copywriting and Presentation Tools

Drafting captions, tags, and written updates can slow down marketing efforts. Content generation tools like ChatGPT and Tagsfinder.com write post copy and select relevant industry tags, saving time for core supply chain tasks. Presentation platforms like Visme and Beautiful AI help turn raw logistics data into visually appealing graphics.

### Practical Tactics for Freight Forwarders

Software alone cannot replace a sound freight forwarding content strategy. Simple operational habits significantly improve audience engagement and conversion rates.

- Maintain a Regular Schedule: Publishing updates every few days establishes predictable touchpoints with prospects, reinforcing company credibility.
- Showcase Client Reviews: Featuring authentic customer reviews inside posts, such as container transport promotions, proves that service levels meet expectations.
- Partner with Logistics Influencers: Collaborating with local industry figures or logistics partners with established audiences opens access to new enterprise accounts. Offering discounted freight services in exchange for endorsements creates a practical marketing trade.
- Act on Client Feedback: Paying attention to criticism and implementing user feedback demonstrates commercial accountability. Resolving client concerns mirrors converting MS Excel files to PDF documents for universal accessibility, ensuring clear communication and showing dedication to service quality.

### Expanding Beyond Social Media

Social channels work best when integrated into a broader commercial strategy. Email campaigns keep existing clients informed about current shipping deals and specialized service options, strengthening customer retention. Integrating specialized IT systems that streamline logistics workflows and app store optimization improves mobile application visibility, supporting social media credibility and lead generation in shipping across every digital touchpoint."""

full_combined = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

# 1. Em-dash check
em_dashes = re.findall(r'[—–]|--', full_combined)
print("EM-DASH COUNT:", len(em_dashes))

# 2. Lengths
print(f"Title length: {len(title)}")
print(f"Meta Title length: {len(meta_title)} (Limit <= 60)")
print(f"Meta Description length: {len(meta_desc)} (Limit <= 155)")

# 3. N-gram comparison with original
with open('/opt/hermes/profiles/archie/original_article.txt', 'r', encoding='utf-8') as f:
    orig_text = f.read()

def get_ngrams(text, n=6):
    words = re.findall(r'\b[a-zA-Z0-9\.]+\b', text.lower())
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

orig_6grams = get_ngrams(orig_text, 6)
rewrite_6grams = get_ngrams(body, 6)

overlap = orig_6grams.intersection(rewrite_6grams)
print(f"6-GRAM OVERLAPS COUNT: {len(overlap)}")
for ov in overlap:
    print("OVERLAP:", ov)
