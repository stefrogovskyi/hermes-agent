title = "SeaRates Load Calculator Guide for Containers and Trucks"
meta_title = "SeaRates Load Calculator: Container & Truck Packing Guide"
meta_desc = "Master container load planning with the SeaRates Load Calculator. Calculate 3D cargo stuffing, truck axle loads, and export PDF plans easily."

body = """Packing freight efficiently saves vehicle space, cuts shipping costs, and protects cargo during transit. The SeaRates Load Calculator handles container load planning for both trucks and sea containers.

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

output = f"""TITLE: {title}
META_TITLE: {meta_title}
META_DESCRIPTION: {meta_desc}
BODY:
{body}"""

print(output)
print("\n--- LENGTH CHECKS ---")
print(f"TITLE len: {len(title)}")
print(f"META_TITLE len: {len(meta_title)}")
print(f"META_DESCRIPTION len: {len(meta_desc)}")
