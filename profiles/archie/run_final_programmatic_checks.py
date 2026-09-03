import json
import re

original_text = """
SeaRates was ecstatic to take part in TPM25, one of the most important international logistics conferences organized by S&P Global. Over four intensive days, our team showcased digital solutions for cargo transportation while addressing pressing challenges and exchanging experiences with leading industry experts.

The event was a solid avenue for strengthening relationships and holding conversations on trends in international trade. Besides this, we participated in significant panel discussions with our partners on automation in logistics, the introduction of artificial intelligence (AI) in transportation, and digital technologies in the supply chain.

Conference insights

The chief topics of discussion were as follows:
- The automation of logistics processes
- AI implementation and Big data in logistics for in-depth analytics and automation of cargo transportation
- Environmental responsibility and how companies are transitioning to accommodate the new regressive measures for CO₂ emissions
- The role of marketplaces in cargo transportation

We were pleased to see how bright the uniqueness of the SeaRates digital platform is, how we add value to global markets, and the relevance of our proposals to transform the global shipping market.

Key impressions from our team were:
- High interest in digital solutions, especially in the fields of automation of freight rates and online supply chain monitoring
- New partnerships were the conference, which offered a wonderful opportunity to expand business network and future project discussions
- Demand for transparency in logistics participants actively discussed the need for access to actual transportation data and the use of digital tools to improve effectiveness

Find our team at TMP25: Katherine Kernesh, IT Sales Manager, and Maria Slabenko, Head of the DFA, on their LinkedIn accounts for further networking.

What's next?
SeaRates won't stop; we keep growing, improving the range of products offered, and developing new perceptions of international shipping. For any inquiries about its services or if you'd like to set up a collaboration, please email us at sales@searates.com.

Don't forget to join us for a fruitful conversation in our chat room as well as follows the news on our official channel to stay up to date with upcoming events.

See you at the next logistics event!

Sophia Shkuro is a content manager from Dnipro, Ukraine. Believes that the more complex a thing is, the easier it should be to write about it. Dreams of a future vacation by the sea.
"""

new_title = "Inside TPM 2025: How SeaRates Navigated Four Days of Ocean Freight Innovation"
meta_title = "SeaRates at TPM 2025: Trans-Pacific Supply Chain Trends"
meta_description = "SeaRates spent four days at TPM25 covering ocean freight rate automation, real-time monitoring, and CO2 emissions regulations."

body_text = """Shippers, carriers, and tech providers gathered for four intensive days at TPM25, organized by S&P Global, to confront unprecedented shifts across Trans-Pacific container shipping. The gathering highlighted how rapid volatility demands practical tools capable of streamlining daily operations across global trade lanes. For the SeaRates team, participating directly in panel sessions offered a clear view into how partners adapt to shifting market conditions.

Core conversations throughout the event centered on ocean freight rate automation alongside real-time supply chain monitoring. Panel discussions made it obvious that cargo owners want instant visibility into actual transportation data rather than delayed updates. By integrating AI and Big Data analytics, modern logistics platforms help teams evaluate route reliability and automate rating workflows without manual spreadsheets.

Decarbonization policies generated significant debate as companies adapt to tightening CO2 emissions regulations. Environmental compliance is reshaping carrier strategies, forcing freight forwarding networks to track carbon footprints across multi-modal journeys. Meanwhile, the growing adoption of a unified digital freight marketplace allows logistics managers to balance sustainability requirements with operational efficiency.

SeaRates representatives Katherine Kernesh, IT Sales Manager, and Maria Slabenko, Head of the DFA, spent the event engaging with international partners and establishing prospective project channels. The team continues expanding its suite of digital tools to support transparent freight management worldwide. Industry professionals interested in collaboration or platform details can connect directly via email at sales@searates.com or join ongoing discussions in the SeaRates community chat."""

full_rewrite_all = f"{new_title}\n{meta_title}\n{meta_description}\n{body_text}"

print("=== CHECK 1: EM-DASH COUNT ===")
em_dash_count = full_rewrite_all.count("—") + full_rewrite_all.count("–")
print(f"Em-dash count: {em_dash_count}")

print("\n=== CHECK 2: LENGTH LIMITS ===")
print(f"Title length: {len(new_title)} chars")
print(f"Meta title length: {len(meta_title)} chars (Limit <= 60): {'OK' if len(meta_title) <= 60 else 'EXCEEDED'}")
print(f"Meta description length: {len(meta_description)} chars (Limit <= 155): {'OK' if len(meta_description) <= 155 else 'EXCEEDED'}")

def normalize_words(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

orig_words = normalize_words(original_text)
rewrite_words = normalize_words(body_text)

def get_ngrams(words, n=6):
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

orig_6grams = set(get_ngrams(orig_words, 6))
rewrite_6grams = get_ngrams(rewrite_words, 6)

overlapping_ngrams = [g for g in rewrite_6grams if g in orig_6grams]

print("\n=== CHECK 3: 6-GRAM OVERLAPS ===")
print(f"Total overlapping 6-grams: {len(overlapping_ngrams)}")
for g in overlapping_ngrams:
    print(" - Overlap:", g)

print("\n=== CHECK 4: AI CLICHÉ SEARCH ===")
cliches = ["seamless", "delve into", "game-changer", "tapestry", "testament", "pivotal", "fostering", "cutting-edge", "landscape", "realm", "beacon", "furthermore", "moreover", "in addition"]
found_cliches = [c for c in cliches if c in full_rewrite_all.lower()]
print(f"Found cliches: {found_cliches}")
