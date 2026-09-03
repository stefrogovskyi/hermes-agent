import re

title = "SeaRates Load Calculator Guide for Containers and Trucks"
meta_title = "SeaRates Load Calculator: Container & Truck Packing Guide"
meta_desc = "Master container load planning with the SeaRates Load Calculator. Calculate 3D cargo stuffing, truck axle loads, and export PDF plans easily."

body = """Packing freight efficiently saves vehicle space, cuts shipping costs, and protects cargo during transit. The SeaRates Load Calculator handles container load planning for both trucks and sea containers.

Free accounts include up to 3 daily calculations and up to 20 unique calculations every month. Paid subscription plans let users adjust calculation limits. Companies that need custom setups can request a customized Load Calculator solution.

The tool organizes cargo planning into three steps: selecting products, choosing transport, and reviewing the stuffing result.

You begin by entering cargo package groups. Details can be entered manually for each item or imported all at once using the downloadable data template. Clicking Add Product lets you specify:
- Cargo type: box, big bags, sacks, barrels, rolls, pipes, or bulk
- Cargo dimensions: length or diameter, width, height, weight, and quantity
- Color
- Spacing settings: tilt width or tilt length
- Stuffing settings: layer count, mass, and height

The sequence in which product groups are entered sets their loading queue. In the Stack tab, you can edit spacing and stuffing rules or choose Disable stacking. Palletizing options let you pick standard pallet types or input exact dimensions for custom pallets.

Next, pick your vehicle. You can rely on Automatic Container Selection or choose standard containers and trucks manually. Custom vehicle dimensions are also supported.

If your shipment includes multiple commodity groups, the 'Load only specific groups' option allows you to assign a dedicated container or truck to each group. When configuring trucks, the system manages truck axle load calculation based on wheel placement relative to the container and maximum weight allowed per axle. These settings cover four exact parameters:
- F - Front max weight (kg)
- F - Front offset (cm)
- R - Rear max weight (kg)
- R - Rear offset (cm)

Once calculated, the tool generates a cargo stuffing calculation report showing package details, total volume, weight, and space usage.

A color-coded 3D container loading scheme shows exact placement inside the vehicle, assigning different colors to different products. You can download a step-by-step stuffing plan and export results to PDF. Answers to frequently asked questions and full tool descriptions sit directly below the calculator interface.

For businesses wanting loading software on their own platform, a customized white-label solution lets you host calculations on your website for any cargo type, package format, container, or truck specification. This tailors loading and unloading to specific carrier and shipper needs.

System integration relies on a white-label freight tool API that connects to CRM, ERP, or TMS platforms. Developer documentation is published on the SeaRates Developer Portal. You can discuss customized digital freight management options by submitting a Request an IT Quote form or emailing sales@searates.com."""

# Verify exact keywords
keywords = [
    "container load planning",
    "cargo stuffing calculation",
    "3D container loading",
    "truck axle load calculation",
    "white-label freight tool API"
]

print("KEYWORD CHECK:")
for kw in keywords:
    present = kw in body or kw in title or kw in meta_desc
    print(f"  '{kw}': {'FOUND' if present else 'NOT FOUND'}")

# Verify exact parameters string from source:
# "F - Front max weight (kg), F - Front offset (cm), R - Rear max weight (kg), R - Rear offset (cm)."
params = ["Front max weight (kg)", "Front offset (cm)", "Rear max weight (kg)", "Rear offset (cm)"]
print("\nPARAMETER CHECK:")
for p in params:
    print(f"  '{p}': {'FOUND' if p in body else 'NOT FOUND'}")

