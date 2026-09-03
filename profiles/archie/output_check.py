title = "SeaRates CO2 Calculator: Freight Footprint Guide"
meta_title = "Calculate Freight Emissions with SeaRates CO2 Tool"
meta_description = "Estimate freight carbon emissions using the SeaRates CO2 Calculator based on ISO 14083 and GLEC v2.0 standards. Compare carriers and offset emissions."

body = """The Carbon Emissions Calculator by SeaRates calculates carbon emissions for sea, land, and air shipping across the globe. Built on the GLEC (Global Logistics Emissions Council) Framework Version 2.0, the tool executes calculations in compliance with ISO 14083 principles, the officially defined standard for calculating carbon emissions caused by supply chains. Shippers can estimate footprint values and compensate for CO2 offsets within a single system.

### Access options and calculation tiers

Signing up provides up to 2 free daily carbon emission calculations and up to 10 unique calculations monthly. Users requiring expanded capacity can select a subscription plan to adjust their calculation volume, or request a customized solution designed for their operational needs.

### Route parameters and calculation inputs

Calculating emissions requires entering departure and destination locations, specified as a city, port, airport, or station, across sea, land, or air modes. Route adjustments rely on the SeaRates Autocomplete service, which queries a granular database.

The calculator processes several core parameters for complex cargo calculations:

* Route coordinates
* Shipment type and container type
* Mode of transportation
* Cargo weight
* Carrier or shipping line
* Historical CO2 emissions data and dynamic tracking insights
* Distance, carrier performance, and emission control zones (ECA zones)

### Carrier comparison and carbon offset options

Results display a list of available carriers for the destination alongside exact carbon footprint figures. Users can examine precise CO2 emissions for each route segment and destination point. 

Comparing land and air options helps identify cost-effective routes while evaluating carrier performance. Directly below each result, the system displays suggested carbon offset compensation, calculated from cargo weight, route distance, and the selected carrier. This fee can be included when executing shipments, or users can request a quote with SeaRates for affordable carbon offset compensation when planning supply flows.

### Web integration and API connectivity

Businesses can implement a white-label integration to host the Carbon Emissions Calculator on their website, providing sea, land, and air CO2 calculations for customer demand. A full list of web-integrated features is available for review.

For system-level integration, the tool offers API connection into CRM, ERP, or TMS platforms. Full API documentation is available on the SeaRates Developer Portal. Customized plans and tailored digital freight management tools can be requested by filling out the Request an IT Quote form or emailing sales@searates.com."""

output = f"""TITLE: {title}
META_TITLE: {meta_title}
META_DESCRIPTION: {meta_description}
BODY:
{body}"""

print(output)

print("\n--- FINAL VERIFICATION ---")
print("Title len:", len(title))
print("Meta title len:", len(meta_title))
print("Meta desc len:", len(meta_description))
assert len(title) <= 60
assert len(meta_title) <= 60
assert len(meta_description) <= 155
assert '—' not in output
assert '--' not in output
