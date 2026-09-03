import json, re

with open("output.json") as f:
    data = json.load(f)

text = f"{data['title']} {data['meta_title']} {data['meta_description']} {data['content_markdown']}"

words_to_check = [
    "world", "fast-paced", "note", "delve", "vital", "crucial", "pivotal", "merely",
    "conclusion", "ever-changing", "landscape", "testament", "tapestry", "beacon",
    "game-changer", "unravel", "navigate", "boast", "furthermore", "moreover",
    "summary", "overall", "unlock", "foster", "driving force", "paramount",
    "unprecedented", "synergy", "paradigm", "realm", "holistic", "seamless", "dynamic"
]

for w in words_to_check:
    m = re.findall(r'\b' + re.escape(w) + r'\w*', text, re.IGNORECASE)
    if m:
        print(f"Found word/stem '{w}': {m}")
