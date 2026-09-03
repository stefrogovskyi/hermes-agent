with open('/opt/hermes/profiles/archie/original_article.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find where the article starts: "[H1] How Wheel Stops"
idx = text.find('[H1] How Wheel Stops')
if idx != -1:
    text = text[idx:]

# Find where article ends (e.g. share buttons, comments, related posts, footer)
end_markers = ['Share this post', 'Related Posts', 'Comments', 'Explore tools for logistics', 'SeaRates Blog']
for marker in end_markers:
    end_idx = text.find(marker)
    if end_idx != -1 and end_idx > 500:
        text = text[:end_idx]
        break

text = text.strip()

with open('/opt/hermes/profiles/archie/clean_original_article.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Cleaned article length: {len(text)} chars.")
print("\n--- CLEANED ARTICLE TEXT ---")
print(text)
