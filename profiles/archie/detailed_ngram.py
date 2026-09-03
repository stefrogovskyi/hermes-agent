import re

original = """Title: SeaRates Х VDS 2024: Upcoming Conference Announcement

We proudly announce that the SeaRates team will be attending VDS, which will take place October 23-24 in Valencia, Spain. Opportunities for businesses worldwide are open for exploration and deeper insight, surrounded by representatives of high-profile global startups and corporations that encourage numerous investors at VDS events. Together with the SeaRates team, you will explore this year's theme 'Embracing Evolution: Invest in the Leaders of Tomorrow' and dive deeper into the positive aspects of the development of industries and society due to the modern technological revolution.

For the sake of profitable collaboration, we are eager to meet with you, our valued clients and partners, to discuss and exchange industry information.

Conference Agenda
VDS will be held in Valencia, Spain, at the City of Arts and Sciences on October 23-24. Over 12,000 attendees, 600+ speakers, 700+ investors, and 2,500+ start-ups from different global industries gathered for a single opportunity to learn more about revolutionary technologies. Speakers will fill the event with rich speeches, which you can listen to in the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, as well as in the Workshop Room & VIP Boxes in line with the VDS agenda.

The two days of the conference are filled with unique insights into revolutionary technologies in global industries:
- Revolutionary AI technologies for businesses around the world: ways to successfully collaborate, transform, strengthen, improve, empower sectors, sustainable technology and investment strategies, and supply chain formation
- All about startups: building ecosystems, presentation sessions, competitions, etc.
- Opportunities for joint development for the innovation community and the port industry
- Overview of the investment landscape in global regions, such as South America and Europe
- Opportunities for cooperation between public funding bodies and maritime entrepreneurship
- Scaling of financial technologies
- Trends and aspects of social transformation and overcoming mental health challenges in business

For more information about the agenda on the first and second days, visit the VDS website.

This is your chance to meet the SeaRates team and discover the newest developments in the supply chain sector.

Meet our main representative at VDS 2024:
Olexandr Grabarchuk

Find the SeaRates team live and come talk to us about how we can help you with your business needs and enhance the digital aspect of your logistics and trading.
We would be delighted to discuss with you how we might assist you with your shipping requirements.

Join up and meet SeaRates
We are thrilled to see you in Valencia at VDS to share the best and newest solutions for the logistics business. SeaRates is delighted to help you with your shipping needs and provide answers for the challenges you face every day.
We invite you to attend the upcoming conference where you can talk to the SeaRates team and learn about our ideas. Please let us know if you are interested in meeting with our team. We will be happy to provide you with useful suggestions and create an atmosphere that will support your company's growth.
Get more information about forthcoming conferences and learn more about SeaRates by emailing us at sales@searates.com.
We hope to see you in Valencia in October!"""

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

# Let's tokenize by words keeping exact original text tokens
orig_tokens = re.findall(r'\S+', original)
rew_tokens = re.findall(r'\S+', rewrite)

# Print all 6-gram overlaps
def clean_tok(t):
    return re.sub(r'[^\w]', '', t.lower())

orig_clean = [clean_tok(t) for t in orig_tokens]
rew_clean = [clean_tok(t) for t in rew_tokens]

found = set()
for n in range(6, 20):
    for i in range(len(rew_clean) - n + 1):
        gram = tuple(rew_clean[i:i+n])
        if any(g == '' for g in gram): continue
        for j in range(len(orig_clean) - n + 1):
            if orig_clean[j:j+n] == list(gram):
                rew_phrase = " ".join(rew_tokens[i:i+n])
                orig_phrase = " ".join(orig_tokens[j:j+n])
                found.add((rew_phrase, orig_phrase))

for r, o in sorted(found, key=lambda x: len(x[0]), reverse=True):
    print("MATCH:")
    print("  Rewrite :", r)
    print("  Original:", o)
    print()
