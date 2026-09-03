import re

with open("/opt/hermes/profiles/archie/article_329_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Find start of real article content: "Full SeaRates Guide on Delivery" or similar
start_idx = text.find("Full SeaRates Guide on Delivery")
if start_idx != -1:
    text = text[start_idx:]

# Find where comments or related articles start if any
end_markers = ["Related Posts", "Comments", "Leave a Reply", "SeaRates Blog", "Subscribe to our newsletter"]
for marker in end_markers:
    idx = text.find(marker)
    if idx > 1000:  # make sure it's not at the very top
        text = text[:idx]

lines = [line.strip() for line in text.split("\n") if line.strip()]
cleaned_text = "\n\n".join(lines)

with open("/opt/hermes/profiles/archie/article_329_clean.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("Cleaned text length:", len(cleaned_text))
print("First 300 chars:\n", cleaned_text[:300])
print("Last 300 chars:\n", cleaned_text[-300:])
