import re
from bs4 import BeautifulSoup

with open('/opt/hermes/profiles/archie/article_296_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the lines and find the article text
lines = [l.strip() for l in text.split('\n') if l.strip()]

# Let's see where the article text starts and ends
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'Enhancing Freight Shipping Software Efficiency' in line:
        print(f"Line {i}: {line}")
        start_idx = i
    if 'SeaRates' in line and ('Facebook' in line or 'Twitter' in line or 'LinkedIn' in line or 'Comments' in line or 'Related posts' in line):
        print(f"End candidates {i}: {line}")

print(f"Total lines: {len(lines)}")
