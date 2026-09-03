import re

body = """Shippers, carriers, and tech providers gathered for four intensive days at TPM25, organized by S&P Global, to confront unprecedented shifts across Trans-Pacific container shipping. The gathering highlighted how rapid volatility demands practical tools capable of streamlining daily operations across global trade lanes. For the SeaRates team, participating directly in panel sessions offered a clear view into how partners adapt to shifting market conditions.

Core conversations throughout the event centered on ocean freight rate automation alongside real-time supply chain monitoring. Panel discussions made it obvious that cargo owners want instant visibility into actual transportation data rather than delayed updates. By integrating AI and Big Data analytics, modern logistics platforms help teams evaluate route reliability and automate rating workflows without manual spreadsheets.

Decarbonization policies generated significant debate as companies adapt to tightening CO2 emissions regulations. Environmental compliance is reshaping carrier strategies, forcing freight forwarding networks to track carbon footprints across multi-modal journeys. Meanwhile, the growing adoption of a unified digital freight marketplace allows logistics managers to balance sustainability requirements with operational efficiency.

SeaRates representatives Katherine Kernesh, IT Sales Manager, and Maria Slabenko, Head of the DFA, spent the event engaging with international partners and establishing prospective project channels. The team continues expanding its suite of digital tools to support transparent freight management worldwide. Industry professionals interested in collaboration or platform details can connect directly via email at sales@searates.com or join ongoing discussions in the SeaRates community chat."""

sentences = re.split(r'(?<=[.!?])\s+', body)
print(f"Total sentences: {len(sentences)}")
for i, s in enumerate(sentences, 1):
    words = s.split()
    print(f"S{i} ({len(words)} w): {s}")
