import re

# Title, Meta Title, Meta Description
title = "SeaRates Load Calculator Guide for Containers and Trucks"
meta_title = "SeaRates Load Calculator: Container & Truck Packing Guide"
meta_description = "Master container load planning with the SeaRates Load Calculator. Calculate 3D cargo stuffing, truck axle loads, and export PDF plans easily."

body = """Packing freight efficiently saves vehicle space, cuts shipping costs, and protects cargo during transit. The SeaRates Load Calculator handles container load planning for both trucks and sea containers.

Free accounts include up to 3 daily calculations and up to 20 unique calculations every month. Paid subscription plans let users adjust calculation limits. Companies needing a custom setup can request a tailored Load Calculator solution.

The tool organizes cargo planning across three steps: select Products, choose Containers/Trucks, and get a Stuffing Result.

You begin by entering cargo package groups. Characteristics can be entered manually for each item or imported all at once using the downloadable template. Clicking 'Add Product' lets you set the cargo type (box, big bags, sacks, barrels, rolls, pipes, or bulk) alongside cargo dimensions including length or diameter, width, height, weight, and quantity. You can also assign colors, spacing settings for tilt width or length, and stuffing settings for layer count, mass, and height.

The sequence in which product groups are entered forms the queue for loading them. Inside the Stack tab, you can edit spacing and stuffing parameters or choose Disable stacking. Palletizing options let you pick standard pallet types or enter exact sizes for custom pallets.

Next comes transport selection. Let the system run Automatic Container Selection, or manually choose standard containers or trucks. Custom vehicle dimensions can also be entered.

When shipping multiple package groups, the 'Load only specific groups' option allows assigning separate containers or trucks to individual cargo groups. For trucks, axle load settings control wheel locations relative to the container and allowed weight for each axle. Adjust parameters for F - Front max weight (kg), F - Front offset (cm), R - Rear max weight (kg), and R - Rear offset (cm) to complete the truck axle load calculation.

The final report provides a complete cargo stuffing calculation with package descriptions, total cargo volume, weight, and space utilization details.

A 3D container loading scheme visualizes exact placement inside the transport space. The 3D viewer uses distinct color codes for each product group to keep items easy to spot. Shippers can save step-by-step loading directions and generate downloadable PDF reports. Tool descriptions and FAQs sit right under the calculator interface.

For logistics providers who want calculation tools on their own website, SeaRates offers a white-label solution. The system runs cargo placement calculations across all package categories and transport options, tailoring load plans to specific carrier and shipper requirements.

System integration connects through a white-label freight tool API into CRM, ERP, or TMS software. Complete API documentation is available in the SeaRates Developer Portal. To request custom plans or customized digital freight management solutions, submit the Request an IT Quote form or email sales@searates.com."""

# Verify length
print(f"Title length: {len(title)} (limit <= 60)")
print(f"Meta Title length: {len(meta_title)} (limit <= 60)")
print(f"Meta Description length: {len(meta_description)} (limit <= 155)")

# Verify em-dashes
full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"
em_dashes = full_text.count("—") + full_text.count("--")
print(f"Em-dashes count: {em_dashes}")

# Read original article
with open("/opt/hermes/profiles/archie/original_article.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

def normalize_words(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text.lower())
    return [w for w in text_clean.split() if w]

orig_words = normalize_words(orig_text)
body_words = normalize_words(body)

# Generate n-grams
N = 6
orig_ngrams = set(tuple(orig_words[i:i+N]) for i in range(len(orig_words)-N+1))
body_ngrams = [tuple(body_words[i:i+N]) for i in range(len(body_words)-N+1)]

matches = []
for idx, ng in enumerate(body_ngrams):
    if ng in orig_ngrams:
        phrase = " ".join(ng)
        matches.append((idx, phrase))

print(f"\nTotal {N}-gram matches count: {len(matches)}")
for idx, m in matches:
    print(f"Match: '{m}'")

with open("/opt/hermes/profiles/archie/final_article_clean.txt", "w", encoding="utf-8") as f:
    f.write(f"TITLE: {title}\nMETA_TITLE: {meta_title}\nMETA_DESCRIPTION: {meta_description}\n\nBODY:\n{body}")
