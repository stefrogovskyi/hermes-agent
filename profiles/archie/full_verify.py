import json, re

payload = {
  "title": "China-Europe Rail Freight: 2024 Trends and Middle Corridor",
  "meta_title": "China-Europe Rail Freight Trends and Middle Corridor Rates",
  "meta_description": "Explore 2024 Eurasia rail freight trends, Middle Corridor routes, rate shifts, and transit times for China to Europe trade.",
  "body": """Disruptions around the Suez Canal and regional instability across Europe and the Middle East prompted shippers to adjust transcontinental trade paths throughout 2024. China expanded alternative overland connections to the European Union, moving away from Red Sea maritime routes and northern transit tracks. Turkey emerged as a major hub connecting mainland Chinese terminals to European and Eastern markets.

Data from the Eurasia Rail Alliance (ERA) Index showed that average rail freight rates remained 59 percent lower than ocean freight costs on China-Europe routes during 2024. Rail pricing stayed near $3,240 per FEU (forty-foot equivalent unit) across most of the year.

### Red Sea Impact and Freight Rate Shifts

Ongoing conflict in the Red Sea cut cargo traffic between China and Europe by more than 60 percent. The Drewry World Container Composite Index reported that average spot rates for 40-foot containers from Shanghai to Rotterdam jumped roughly 78 percent, reaching $7,961. Volatility across ocean shipping drove logistics planners to expand rail movement along alternative corridors.

The Northern Direction historically dominated overland export traffic. Starting in late 2023, the China-Central Asia-West Asia corridor gained strong momentum. Early development along this pathway dates back to November 2016, when the China Railways Express completed an 18-day run from Xi'an to Prague.

Importers and exporters turned to rail to avoid maritime security risks and shorten transit timelines. Ocean freight between China and Europe requires 30 to 40 days. Specific rail connections take under 10 days.

### Infrastructure Expansion Across Asia and Europe

According to the State Council of the People's Republic of China, transcontinental rail links 226 cities in 25 European countries and over 100 cities across 11 Asian nations. Total trade between China and the European Union reached 739 billion euros in 2023, accounting for 15 percent of total EU trade.

Growth continued through the first nine months of 2024, recording 14,689 round-trip train runs, a 13 percent increase year-on-year. These services transported 1.57 million TEU of goods, representing an 11 percent increase over the previous year. Over the first seven months of 2024, daily traffic exceeded 50 trains.

Customs reports from 2024 identify Shaanxi, Zhejiang, and Jiangsu as leading exporting provinces for rail shipments. Shaanxi, Liaoning, and Fujian represented the largest importing provinces. Inland western and northwestern Chinese regions attracted fresh investment and workforce growth by serving as direct trade gateways.

Cross-border infrastructure developed rapidly in early 2024. KTZ Express, a subsidiary of Kazakhstan's national railway operator Kazakhstan Temir Zholy, partnered with Xi'an Free Trade Port Construction and Operation to establish the China-Kazakhstan (Xi'an) Trade Logistics terminal. European hubs like Duisburg, Germany, expanded terminal networks to process higher container volumes. Turkey strengthened its position in February 2024 when the initial China-Europe freight train departed Chongqing for Istanbul.

### Comparing Route Options and Logistics Costs

The Middle Corridor across the Caspian Sea offers an alternative route. Shippers moving 20-foot containers (TEU) between China and Turkey face rates between $5,000 and $7,000, with an additional $1,000 to $2,000 required to reach destination terminals in Poland or Germany.

Specific 40ft HQ container routes demonstrate current pricing and timing structures:
* Jiulongpo to Hamburg: Road and rail, 24 days transit, starting at $9,800.
* Chongqing to Małaszewicz: Road and rail, 24 days transit, starting at $10,600.
* Chengdu to Duisburg: Road and rail, 24 days transit, starting at $8,450.
* Jiulongpo to Biała Podlaska: Road and rail, 24 days transit, starting at $9,750.

Middle Corridor capacity continues to expand as maritime rate pressures remain elevated. Rail transit from China to Turkey averages one to two weeks. Runs to Germany require 18 to 22 days.

### Operational Advantages of Overland Rail

Faster transit times benefit businesses managing goods with limited shelf life or tight supply schedules. Shorter delivery windows reduce the need to hold large inventories, lowering warehouse handling expenses. Companies can arrange smaller, more frequent shipments instead of waiting over a month for single ocean consignments.

Accelerated delivery helps manufacturers of high-demand goods, fashion items, and tech components maintain production schedules and respond quickly to market changes. Rail services also bypass seasonal port congestion during peak demand periods.

Environmental factors favor rail transport. Trains generate lower carbon emissions per unit of cargo than air or sea freight and use less energy per weight unit than air transport. Rail operations avoid maritime waste discharges, oil spills, and high-altitude condensation trails.

For customized quotes and routing assistance, contact sales@searates.com."""
}

# Test JSON serialization
json_str = json.dumps(payload, ensure_ascii=False, indent=2)
parsed = json.loads(json_str)

print("JSON is valid.")
print("Title length:", len(parsed["title"]))
print("Meta Title length:", len(parsed["meta_title"]))
print("Meta Description length:", len(parsed["meta_description"]))

# Verify rule compliance
full_text = f"{parsed['title']}\n{parsed['meta_title']}\n{parsed['meta_description']}\n{parsed['body']}"

# Check dashes
dashes = [r'—', r'–', r'--', r'―', r'⸺', r'⸻']
for d in dashes:
    if re.search(d, full_text):
        print(f"ERROR: Found dash {d}")

# Check clichés
cliches = [
    "delve", "seamless", "seamlessly", "unlock", "unlocking", "game-changer", 
    "testament", "tapestry", "pivotal", "elevate", "cutting-edge", "fostering", 
    "vibrant", "landscape", "realm", "harness", "empower", 
    "in today's fast-paced world", "it is crucial to note", "robust", 
    "leverage", "navigate", "ever-evolving", "cornerstone", "beacon", "spearhead"
]
for c in cliches:
    if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
        print(f"ERROR: Found cliché {c}")

# Check connectors at sentence starts
connectors = [
    "Furthermore", "Moreover", "In addition", "However", "Therefore", 
    "That's why", "Which is why", "Consequently", "Additionally", 
    "As a result", "Hence", "Thus", "Because of this"
]
sentences = re.split(r'[.!?]\s+', parsed['body'])
for s in sentences:
    s_clean = s.strip()
    for conn in connectors:
        if re.match(r'^' + re.escape(conn) + r'\b', s_clean, re.IGNORECASE):
            print(f"ERROR: Sentence starts with connector {conn}")

# Check twin sentence starters
words_by_sentence = []
for s in sentences:
    words = re.findall(r'\b\w+\b', s.lower())
    if len(words) >= 2:
        words_by_sentence.append((words[0], words[1]))
for i in range(len(words_by_sentence) - 1):
    if words_by_sentence[i] == words_by_sentence[i+1]:
        print(f"ERROR: Parallel twin starters: {words_by_sentence[i]}")

# Check contrastive negations
cn_keywords = ["instead of", "rather than", "not only"]
total_cn = sum(len(re.findall(r'\b' + re.escape(kw) + r'\b', full_text, re.IGNORECASE)) for kw in cn_keywords)
print("Total contrastive negations:", total_cn)
if total_cn > 1:
    print("ERROR: Contrastive negations > 1")

print("All automated checks completed successfully!")
