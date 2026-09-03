import re

original = """Title: How To Use the Load Calculator? Smart Stuffing of Containers & Trucks | SeaRates Blog Post
Author: Sophia Shkuro

Content:
Load Calculator by SeaRates allows you to find the best way to load cargo into a container or truck. This tool optimizes the space inside the vehicle, reduces transportation costs, and ensures the safe delivery of goods.

Wondering how efficient stuffing works? Continue with our guide for more insights on secure and convenient loading to meet your specific needs.

How does the tool work?
Sign up here to get up to 3 free daily stuffing calculations and up to 20 unique ones monthly. Get your subscription plan to adjust the number of calculations, or let us know about your intention for your own Load Calculator and get a customized solution to meet your needs.

Let's take a closer look at the calculator’s functionality.
The whole Load Calculator functionality is presented in three main steps: select Products, choose Containers/Trucks, and get a Stuffing Result.

1. Load your packages
Include all groups of commodities you are planning to load. Provide detailed characteristics for each manually, or check the template below to import data on all of your cargo groups at once.
Click on ‘Add Product’ to select the following:
- cargo type: box, big bags, sacks, barrels, rolls, pipes, or bulk
- cargo dimensions: length/diameter, width, height, weight, and quantity
- color
- spacing settings: tilt width or length
- stuffing settings: layers count, mass, and height
Here, you’re forming a product group for loading. The sequence in which you enter product groups is the queue for loading them.
To edit, open the ‘Stack’ tab: spacing, stuffing, or choose Disable stacking.
The palletizing option is also available; just select the pallet type and enter the size for a customized one.

2. Choose transport
Get Automatic Container Selection or select a container or truck by yourself. Find standard sizes or enter custom ones.
For trucks, you can customize the axle load:
“The location of the truck wheels relative to the container and the weight allowed for each axle. F - Front max weight (kg), F - Front offset (cm), R - Rear max weight (kg), R - Rear offset (cm).”
If you have added several groups of packages, you can choose a container or truck for each of them separately with the ‘Load only specific groups’ option.

3. Get stuffing result
Finally, you get detailed report results with a full description of your packages, cargo volume, weight, and more.
Check the 3D scheme for the proper loading of your packages inside the chosen transport. Different colors are assigned to different products. Download a step-by-step stuffing plan and export results to PDF.
Looking for benefits details? Find a description and Frequently Asked Questions about the Load Calculator right under the tool.

White-label integration
This customized white-label solution allows you to provide stuffing calculations for any cargo type and package in any container or truck format on your own website. Tailor loading and unloading to the individual needs of the carrier and shipper.

API connection
The Load Calculator ensures smooth API integration into your CRM, ERP, or TMS system. Explore the API documentation for the Load Calculator in the SeaRates Developer Portal.

Find Your Customized Load Calculator Plan
Let us know about your requirements by filling out the Request an IT Quote form or reaching out to us at sales@searates.com for a tailored digital freight management solution."""

rewrite = """TITLE: SeaRates Load Calculator Guide for Containers and Trucks
META_TITLE: SeaRates Load Calculator: Container & Truck Packing Guide
META_DESCRIPTION: Master container load planning with the SeaRates Load Calculator. Calculate 3D cargo stuffing, truck axle loads, and export PDF plans easily.

BODY:
Packing freight efficiently saves vehicle space, cuts shipping costs, and protects cargo during transit. The SeaRates Load Calculator handles container load planning for both trucks and sea containers.

Free accounts include up to 3 daily calculations and up to 20 unique calculations every month. Paid subscription plans let users adjust calculation limits. Companies needing a custom setup can request a tailored Load Calculator solution.

The tool organizes cargo planning across three steps: select Products, choose Containers/Trucks, and get a Stuffing Result.

You begin by entering cargo package groups. Characteristics can be entered manually for each item or imported all at once using the downloadable template. Clicking 'Add Product' lets you set the cargo type (box, big bags, sacks, barrels, rolls, pipes, or bulk) alongside cargo dimensions including length or diameter, width, height, weight, and quantity. You can also assign colors, spacing settings for tilt width or length, and stuffing settings for layer count, mass, and height.

The sequence in which product groups are entered forms the queue for loading them. Inside the Stack tab, you can edit spacing and stuffing parameters or choose Disable stacking. Palletizing options let you pick standard pallet types or enter exact sizes for custom pallets.

Next comes transport selection. Let the system run Automatic Container Selection, or manually choose standard containers or trucks. Custom vehicle dimensions can also be entered.

When shipping multiple package groups, the 'Load only specific groups' option allows assigning separate containers or trucks to individual cargo groups. For trucks, axle load settings control wheel locations relative to the container and allowed weight for each axle. Adjust parameters for F - Front max weight (kg), F - Front offset (cm), R - Rear max weight (kg), and R - Rear offset (cm) to complete the truck axle load calculation.

The final report provides a complete cargo stuffing calculation with package descriptions, total cargo volume, weight, and space utilization details.

A 3D container loading scheme visualizes exact placement inside the transport space. Different colors are assigned to different products for clear identification. Users can download a step-by-step stuffing plan and export results to PDF. Tool descriptions and FAQs sit right under the calculator interface.

For logistics providers who want calculation tools on their own website, SeaRates offers a white-label solution. It handles stuffing calculations for any cargo type and package in any container or truck format, tailoring loading and unloading to carrier and shipper needs.

System integration connects through a white-label freight tool API into CRM, ERP, or TMS software. Complete API documentation is available in the SeaRates Developer Portal. To request custom plans or customized digital freight management solutions, submit the Request an IT Quote form or email sales@searates.com."""

# Let's find maximal matching substring runs (in words) between rewrite and original
def find_long_matches(orig, rew):
    # normalize words keeping original case for display
    orig_tokens = re.findall(r'\S+', orig)
    rew_tokens = re.findall(r'\S+', rew)
    
    # clean word tokens
    def clean(w):
        return re.sub(r'[^\w]', '', w.lower())

    orig_clean = [clean(w) for w in orig_tokens if clean(w)]
    rew_clean = [clean(w) for w in rew_tokens if clean(w)]

    # find long matches
    matches = []
    i = 0
    while i < len(rew_clean):
        max_len = 0
        best_j = -1
        for j in range(len(orig_clean)):
            k = 0
            while i + k < len(rew_clean) and j + k < len(orig_clean) and rew_clean[i+k] == orig_clean[j+k]:
                k += 1
            if k >= 5: # check matches of length 5+
                if k > max_len:
                    max_len = k
                    best_j = j
        if max_len >= 6:
            match_words = rew_clean[i:i+max_len]
            matches.append((i, max_len, " ".join(match_words)))
            i += max_len
        else:
            i += 1
    return matches

print("Maximal matching word runs (>= 6 words):")
for m in find_long_matches(original, rewrite):
    print(f"Len {m[1]}: {m[2]}")
