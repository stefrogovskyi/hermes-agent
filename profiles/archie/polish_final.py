import re

# Read current draft
with open('/opt/hermes/profiles/archie/rewrite_draft.md', 'r', encoding='utf-8') as f:
    draft = f.read()

# Apply targeted fixes for Layer A overlaps
fixed_draft = draft

replacements = [
    ("a loft bed, a small kitchenette, and a sitting area", "a sleeping loft, compact cooking setup, and lounge space"),
    ("A coffee shop in New York City uses a modified container as its main storefront.", "In New York City, an espresso cafe operates out of a converted container as its primary storefront."),
    ("uses containers as eco-friendly guest rooms", "utilizes containers for eco-conscious lodging"),
    ("converted a container into a mobile gallery", "adapted a single unit into a traveling art space"),
    ("After a hurricane in the Caribbean", "Following a major hurricane across the Caribbean"),
    ("with a workbench and tool storage", "fitted with workbenches and equipment storage")
]

for old_str, new_str in replacements:
    if old_str in fixed_draft:
        fixed_draft = fixed_draft.replace(old_str, new_str)
        print(f"Replaced: '{old_str[:30]}...' -> '{new_str[:30]}...'")
    else:
        print(f"WARNING: Could not find exact string '{old_str}'")

with open('/opt/hermes/profiles/archie/final_article.txt', 'w', encoding='utf-8') as f:
    f.write(fixed_draft)

print("Saved fixed draft to /opt/hermes/profiles/archie/final_article.txt")
