import json
import re

with open('/opt/hermes/profiles/archie/final_rewrite.json', 'r') as f:
    data = json.load(f)

with open('/opt/hermes/profiles/archie/article_content.txt', 'r') as f:
    orig_text = f.read()

# Split body into prose and announcements
body_parts = data["body_markdown"].split("Recent platform announcements")
prose_body = body_parts[0]

orig_parts = orig_text.split("Announcements:")
orig_prose = orig_parts[0]

def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

orig_prose_6grams = set(get_ngrams(orig_prose, 6))
prose_6grams = set(get_ngrams(prose_body, 6))

prose_overlaps = orig_prose_6grams.intersection(prose_6grams)

print("Prose 6-gram overlaps:", len(prose_overlaps))
if prose_overlaps:
    print("Overlaps found in prose:", prose_overlaps)
else:
    print("SUCCESS: 0 n-gram overlaps in body prose!")
