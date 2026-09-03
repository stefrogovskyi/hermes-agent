import re
import string

title = "Autonomous Trucks in 2025: Global Freight Deployment"
meta_title = "Global Autonomous Truck Deployment in 2025"
meta_description = "Heavy autonomous rigs are moving from test tracks to highway freight lanes across China, Europe, and the US as commercial deployment hits 2025."

body_text = """Across long highways, computer systems are taking over the steering wheel while logistics networks adapt to machines running scheduled commercial freight. Industry data from Precedence Research projects the global autonomous truck market to reach $1.74 billion in 2025. Carriers and tech developers are scaling operations to address driver shortages, route delays, and safety issues.

China leads large-scale highway runs. Late in 2024, Inceptio Technology shipped 400 self-driving heavy trucks to ZTO Express. More than 2,000 trucks using Inceptio's platform now run in commercial fleets across the country. National initiatives like Made in China 2025 along with city-level rules in Beijing, Shanghai, and Shenzhen created designated driving zones. This setup accelerates driver shortage mitigation while moving e-commerce freight.

In the United States, states handle most regulations while the National Highway Traffic Safety Administration provides voluntary guidance. Over 1,400 autonomous vehicles are testing across the country. California issued over 60 testing permits. Texas and Arizona allow commercial driverless freight operations without safety drivers.

While companies like Waymo, Cruise, Tesla, and Zoox develop passenger vehicles, truck developers focus on long-haul freight automation. Kodiak Robotics partners with Texas freight companies for driverless deliveries and designs long-haul rigs that interface with shipping ports. Gatik runs autonomous box trucks for Walmart in Arkansas, delivering real-world data for middle-mile logistics. American oilfield routes also run autonomous semi-truck trials.

Europe focuses on regional regulations and cross-border transport. Sweden's Einride runs commercial Level 4 driverless deployment routes across several European countries. Germany passed a law in 2021 allowing Level 4 vehicles in designated zones without human drivers, and ran successful on-road truck trials in 2024. EU lawmakers are working on a shared framework so automated trucks can cross borders without stopping.

Asian and Australian markets show steady testing. Australia has over 30 trials in cities like Brisbane, Melbourne, and Sydney, including Sydney's large automated bus project. Mining companies use autonomous trucks heavily. Rio Tinto moved 200 million metric tons of iron ore over six years with self-driving fleets. Japan has over 100 test sites, aiming for a market over $4 billion by 2030. South Korea built K-City to test driverless cargo vehicles on simulated roads.

Constrained routes make hub-to-hub autonomous transport practical today. Human drivers handle the first and last miles. Software controls the highway stretches between transfer points. Kodiak Robotics, Aurora Innovation, Torc Robotics, Waabi, and Gatik are all testing or operating these hub transfers.

Port facilities rely on automated terminal tractors and autonomous mobile robots. Tuas Port in Singapore uses these systems to manage container yards. Connecting ports directly to highway corridors reduces terminal congestion.

AI perception & sensor fusion combines radar, lidar, and cameras so onboard computers process road data in real time.

V2X vehicle communication sends data between trucks, roadside sensors, and nearby cars. It lets vehicles detect hazards like cars hidden around blind corners.

Zero-emission heavy trucks are joining autonomous test fleets. Hyundai is testing a Class 8 fuel cell electric truck in the US for Level 4 operations.

Deploying autonomous fleets comes with obstacles. European operators face conflicting national standards that slow cross-border freight. Public acceptance remains low, requiring clear safety evidence and transparent testing. Infrastructure needs upgrades, including clearer road markings, charging networks, dedicated lanes, and stronger cellular networks.

Labor demands will shift rather than disappear. Freight companies are creating roles in remote vehicle monitoring, terminal management, and software support.

After 2025, operators expect more driverless runs on highways, broader use of hydrogen and electric power, and tighter integration with smart city networks."""

with open("/opt/hermes/profiles/archie/original_article.txt", "r", encoding="utf-8") as f:
    original_text = f.read()

# Check em-dashes
full_combined = f"{title}\n{meta_title}\n{meta_description}\n{body_text}"
em_dashes = full_combined.count("—") + full_combined.count("--")

# Check lengths
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# N-gram overlap
def tokenize(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    return text.split()

orig_tokens = tokenize(original_text)
rewrite_tokens = tokenize(body_text)

orig_6grams = set(zip(*(orig_tokens[i:] for i in range(6))))
rewrite_6grams = list(zip(*(rewrite_tokens[i:] for i in range(6))))

overlaps = []
for i, g in enumerate(rewrite_6grams):
    if g in orig_6grams:
        overlaps.append(" ".join(g))

print("--- AUDIT RESULTS ---")
print(f"Em-dashes count: {em_dashes}")
print(f"Title length: {title_len} (max 60)")
print(f"Meta-Title length: {meta_title_len} (max 60)")
print(f"Meta-Description length: {meta_desc_len} (max 155)")
print(f"Total 6-gram overlaps count: {len(overlaps)}")
if overlaps:
    print("Overlap examples:")
    for o in set(overlaps):
        print("  -", o)

