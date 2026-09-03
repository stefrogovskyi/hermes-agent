import re

rewrite = """Title: SeaRates Headed to VDS 2024 in Valencia
Meta Title: SeaRates at VDS 2024 in Valencia: Connect With Our Team
Meta Description: Meet SeaRates and Olexandr Grabarchuk at VDS 2024 in Valencia on Oct 23-24 to discuss shipping and logistics solutions. Contact sales@searates.com.

Body:
The SeaRates team is attending VDS 2024 on October 23-24, hosted at the City of Arts and Sciences in Valencia, Spain. The gathering brings together representatives from international startups, global corporations, and institutional investors. Centered on this year's theme, 'Embracing Evolution: Invest in the Leaders of Tomorrow', discussions will focus on how modern technological advancements shape logistics, trade, and broader industry sectors.

## Industry Leaders Gather in Valencia

VDS 2024 expects 12,000+ attendees, 600+ speakers, 700+ investors, and 2,500+ startups from across the world. Presentations and discussions will span eight dedicated spaces across the venue: the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, alongside the Workshop Room & VIP Boxes.

The two-day conference program covers several key areas:
* Practical AI adoption for global businesses, sustainable investment strategies, and resilient supply chain formation
* Startup ecosystem growth, pitch competitions, and presentation sessions
* Joint innovation initiatives linking tech developers with port operations
* Regional investment analysis highlighting opportunities across South America and Europe
* Collaborative funding frameworks between maritime entrepreneurs and public agencies
* Scalable financial technologies tailored for international commerce
* Emerging workplace trends, including social transformation and business mental health initiatives

Detailed schedule information for both days is available on the official VDS website. Attendees can review session times and speaker lineups prior to arriving in Valencia.

## Meet Olexandr Grabarchuk at the Event

Olexandr Grabarchuk will represent SeaRates on site throughout the two-day event. Our team is available to meet with clients, partners, and industry peers to exchange insights on freight movement and digital trade tools. Whether you want to streamline cargo operations or evaluate digital tools for your freight requirements, we welcome the opportunity to connect in person.

To arrange a dedicated meeting with our team during VDS 2024 or learn more about our upcoming event appearances, send an email to sales@searates.com. We look forward to meeting you in Valencia this October."""

# Split into paragraphs and sentences
paragraphs = [p.strip() for p in rewrite.split('\n\n') if p.strip()]

for i, p in enumerate(paragraphs):
    print(f"--- Paragraph {i+1} ---")
    print(p)
    sentences = re.split(r'(?<=[.!?])\s+', p)
    print(f"Sentence count: {len(sentences)}")
    for s in sentences:
        print("  S:", s)

