import json
import re

with open("draft.json") as f:
    data = json.load(f)

text = f"{data['title']} {data['meta_title']} {data['meta_description']} {data['body_markdown']}"

words_to_check = [
    "delve", "testament", "pivotal", "game-changer", "gamechanger", "beacon", "unleash",
    "harness", "harnessing", "crucial", "today's world", "not just", "in conclusion",
    "realm", "tapestry", "landscape", "nestled", "navigate", "foster", "fostering",
    "empower", "empowering", "elevate", "elevating", "transformative", "transforming",
    "vital", "seamlessly", "seamless", "myriad", "plethora", "supercharge", "cornerstone",
    "vibrant", "driving force", "shining example", "ever-evolving", "cutting-edge",
    "paramount", "beacon", "game changer", "synergy", "holistic", "multifaceted",
    "game changing", "game-changing", "at the end of the day", "look no further"
]

found = []
for word in words_to_check:
    if re.search(r'\b' + re.escape(word) + r'\b', text, re.I):
        found.append(word)

print("Found cliches:", found)
