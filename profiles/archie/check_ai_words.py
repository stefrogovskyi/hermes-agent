import json
import re

with open('/opt/hermes/profiles/archie/final_output.json', 'r') as f:
    data = json.load(f)

text = f"{data.get('title')} {data.get('meta_title')} {data.get('meta_description')} {data.get('body')}"

ai_words = [
    "delve", "testament", "tapestry", "beacon", "demystify", "game-changer", "unravel",
    "realm", "vital role", "crucial role", "pivotal role", "landscape", "navigate",
    "imperative", "fostering", "spearhead", "multifaceted", "paramount", "synergy",
    "evolving", "in conclusion", "furthermore", "moreover", "leverage", "robust",
    "seamless", "holistic", "game changer", "cutting-edge", "harness", "foster",
    "pivotal", "indispensable", "vital", "cornerstone", "stark", "underscores",
    "underscoring", "testament", "tapestry", "substantive", "proactive"
]

found = {}
for word in ai_words:
    matches = re.findall(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE)
    if matches:
        found[word] = len(matches)

print("AI words found:", found)

