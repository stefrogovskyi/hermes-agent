ai_buzzwords = [
    "delve", "tapestry", "testament", "game-changer", "beacon", "vital", "pivotal", 
    "crucial", "landscape", "seamless", "dynamic", "realm", "unlock", "foster", 
    "elevate", "underscores", "vibrant", "nestled", "intricate", "holistic", 
    "empower", "spearhead", "harness", "leverage", "robust", "transformative",
    "paramount", "pivotal", "beacon", "synergy", "paradigm", "testament"
]

import re

with open("plagiarism_check.py") as f:
    text = f.read()

# get rewrite text
rewrite_text = text.split('rewrite = """')[1].split('"""')[0]

found_words = {}
for w in ai_buzzwords:
    matches = re.findall(r'\b' + re.escape(w) + r'\b', rewrite_text, re.IGNORECASE)
    if matches:
        found_words[w] = len(matches)

print("AI Buzzwords Found:", found_words)
