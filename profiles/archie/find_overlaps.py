import re

original_text = """The end of October saw Tech Show Madrid 2025, which turned IFEMA MADRID into a center for global innovation. The tech experts and business leaders united by the event numbered more than 25,000, with 350+ speakers and 400+ exhibitors coming from Europe’s most rapidly growing technology verticals.

For SeaRates, attending the conference was not just a regular visit. The conference showed how digital infrastructure, AI, and data analytics are the new masters of supply chain efficiency through the different methods of writing the rules.

## Conference’s insights

Despite its being marketed as a tech fair, the event has become more and more like a reflection of the sectors’ needs that rely on data-driven coordination, such as freight, supply chain management, and transportation.

We found it particularly interesting to follow the discussions on some conference tracks:

- Cloud & AI infrastructure: talk about hybrid environments, bigger scalability, and AI decision support overall. This will result in less manual handling and more intelligent dispatching and routing automation for the whole logistics sector.

- Big Data: The detailed studies of real-time analytics, IoT networks, and digital twins were directly linked with predictive logistics, where every shipment acts as a data source.

- Cybersecurity world: The emphasis was on securing the digital ecosystems connecting carriers, freight forwarders, and shippers. The emergence of API-based logistics is coupled with the necessity for robust data governance frameworks.

- Technology for marketing: The point where customer experience and logistics visibility merge. The close relationship between order tracking, transparency, and brand trust was a significant story throughout.

The wide variety of topics has demonstrated that logistics is already a part of the tech universe — a vibrant, digital system connected with the rest of the web.

Tangible innovation was all over the Tech Show Madrid. Among the shortlisted innovations, here are a few that could be of direct value to the logistics professionals:

### AI agents & Workflow automation
Several exhibitors showcased autonomous AI assistants and MCP agents, whose main function was to take care of repetitive tasks in operations. For logistics departments, this will be quoting, tracking updates, and exception management done through automation — letting human operators work on the more strategic tasks.

### Cloud-native supply-chain platforms
The use of cloud technology in logistics has become so advanced that it is now possible to receive and process freight data in real-time without any interruption. Global operations can be performed with the use of multi-tenant solutions, thereby allowing even the smallest of forwarders to use advanced technology without any performance limitations.

### Data centers with edge connectivity
Logistics is very much dependent on edge computing, as the technology is being utilized to handle the IoT data near ports, warehouses, and terminals. This consequently results in faster reaction times, lower latency, and better shipment visibility.

### Cybersecurity as a compliance priority
The session mentioned regulations like NIS2 and DORA, among others. In digital logistics platforms, for example, compliance means securing partner networks, customer data, and bank transactions.

### Sustainability by data
Technology is not solely aimed at fast. Through several talks and trade shows, it was pointed out that analytics might be applied to cut idle time, optimize routes, and, most importantly, measure CO2 emissions, hence proving the point that data intelligence has a direct link with environmental performance.

## Our main points

After participating for two days in sessions, meetings, and demos, we had four strong insights for the logistics community:

- Integration is the foundation: The new competitive edge isn’t about who owns data, but who connects it better. APIs and interoperability are the building blocks of future logistics ecosystems.
- Predictive is the new reactive: The shift towards AI-driven forecasting allows logistics operators to prevent bottlenecks rather than react to them.
- Transparency is a new market currency: Clients now expect real-time visibility across every transport phase. Technologies showcased in Madrid make that level of transparency practical.
- Sustainability is a KPI: When logistics digitalizes, measuring and reducing carbon footprint will become an operational metric, not a marketing point.

The networking sessions were very busy, with a high level of energy in the startup pitches, and the discussions about sustainability and AI ethics showed how far tech dialogues have matured.

## Looking ahead

Tech Show Madrid 2025 clearly demonstrated that the logistics sector is no longer a technology that gets adapted to, but rather one that gets shaped.

SeaRates sees this as an opportunity to continuously develop our digital ecosystem, enhance our integrations, and facilitate the interconnection of physical and digital supply chains.

We have gone back from Madrid not only inspired but also loaded with ideas and alliances that are going to be the driving force behind the next stage of logistics innovation. Please email us at sales@searates.com if you would like to discuss ideas with Tech Show Madrid 2025 or have solutions customized for your processes, or contact our representative, Valeriya Guliy, directly.

See you next time!"""

rewrite_text = """Title: Tech Show Madrid 2025: Supply Chain Tech Takeaways
Meta Title: Tech Show Madrid 2025: Freight & Logistics Insights
Meta Description: Key takeaways from Tech Show Madrid 2025 covering MCP agents, edge computing, NIS2 DORA compliance freight, and CO2 carbon emission analytics.

Body:
When IFEMA MADRID opened its doors at the end of October for Tech Show Madrid 2025, over 25,000 tech experts, 350+ speakers, and 400+ exhibitors gathered to examine enterprise systems.

For SeaRates, attending the venue showed how modern freight movement depends on software integration, cloud systems, and live data feeds. The floor reflected the operational realities of daily cargo transport.

### Digital Ecosystems and Operations

Conference tracks highlighted practical shifts across technical domains:

* Cloud and AI infrastructure: Hybrid setups and automated dispatch systems reduce manual workloads for carriers and routing teams.
* Big Data: IoT streams and digital twin models turn physical shipments into data sources for predictive logistics.
* Cybersecurity: Connecting shippers, forwarders, and carriers via APIs requires strict data governance to keep networks safe.
* Marketing tech: Order tracking connects operational visibility directly to customer trust.

On the trade floor, autonomous tools and MCP agents logistics solutions demonstrated automated handling for repetitive operational tasks. Quoting, shipment tracking updates, and exception management ran automatically. Human operators can focus on strategic decisions.

Cloud-native supply chain platforms allow small and mid-sized forwarders to process real-time cargo data through multi-tenant systems without system slowdowns. Edge computing port logistics installations place raw computing power near docks and warehouses. Local sensor processing drops latency, helping terminal operators react faster when problems pop up.

Regulatory standards were another focal point. Speaker sessions addressed NIS2 DORA compliance freight requirements. Cargo platforms must protect financial transactions, partner channels, and customer records to remain compliant.

Sustainability panels focused on measurable data. Companies used CO2 carbon emission analytics to cut vehicle idle times, refine transit corridors, and report emissions accurately.

### Core Observations

Two days of sessions, meetings, and product demos yielded four main observations:

Digital supply chain transformation relies on open APIs rather than isolated databases. AI forecasting gives logistics teams the ability to prevent bottlenecks before cargo gets delayed. Clients expect real-time visibility across every transport phase. Measuring carbon footprint has become an operational metric.

Networking sessions were busy, startup pitches showed high energy, and discussions on sustainability and AI ethics demonstrated how mature these technical conversations have become.

SeaRates continues expanding its digital ecosystem to connect physical and digital supply chains. To discuss conference insights or explore custom workflow tools, email sales@searates.com or contact our representative, Valeriya Guliy."""

def clean_words(text):
    return [w.lower() for w in re.findall(r'\b\w+\b', text)]

orig_words = clean_words(original_text)
rew_words = clean_words(rewrite_text)

# Find all common substrings of length >= 5
def find_all_overlaps(w1, w2, min_len=5):
    overlaps = []
    seen = set()
    for i in range(len(w2) - min_len + 1):
        for j in range(len(w1) - min_len + 1):
            match_len = 0
            while (i + match_len < len(w2)) and (j + match_len < len(w1)) and (w2[i+match_len] == w1[j+match_len]):
                match_len += 1
            if match_len >= min_len:
                phrase = " ".join(w2[i:i+match_len])
                if phrase not in seen:
                    # check if this is subphrase of another
                    seen.add(phrase)
                    overlaps.append((match_len, phrase, i, j))
    # Filter out subphrases
    final_overlaps = []
    sorted_overlaps = sorted(overlaps, key=lambda x: x[0], reverse=True)
    for l, p, i, j in sorted_overlaps:
        if not any(p in other_p and p != other_p for _, other_p in final_overlaps):
            final_overlaps.append((l, p))
    return final_overlaps

overlaps = find_all_overlaps(orig_words, rew_words, 5)
print("All max overlaps >= 5 words:")
for l, p in overlaps:
    print(f"- Length {l}: '{p}'")

