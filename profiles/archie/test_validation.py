import json, re

result = {
    "title": "Selecting Forklifts for Dock and Warehouse Operations",
    "meta_title": "Selecting Forklifts for Dock and Warehouse Operations",
    "meta_description": "A practical breakdown of forklift options, load capacities, motor types, ergonomics, and leasing for logistics operations.",
    "body": """Cargo ships dominate the horizon, but freight handling relies on the smaller mechanical choices made on the dock floor. Forklifts increase the speed of loading and unloading parcels at the terminal. Running material handling equipment requires matching the frame to the work surface. Indoor facilities require smooth-surface machines. Outdoor yards demand units built for uneven ground. Toyota Lift Northwest offers forklifts for rough terrain, while Quinn Company supplies rough terrain forklifts built for demanding environments.

Weight and height parameters must fit the load. Buying a machine that cannot support the weight or dimensions of your inventory reduces performance and shortens equipment life. It also raises the risk of workplace accidents. Choosing a mast height that reaches facility racks keeps stock moving without operational delays.

## Motor types and operating costs

Power source selection alters long-term expenditure and warehouse fleet management. Electric forklifts carry a higher initial purchase price. They run quietly without exhaust emissions, making them suitable for indoor buildings. Fuel savings and longevity reduce the total cost of ownership across years of service. Combustion engines burning gas or diesel provide additional power for outdoor tasks, accompanied by higher fuel consumption.

## Ergonomics and acquisition

Driver fatigue affects daily throughput during long shifts. Integrating ergonomic forklift design reduces operator back pain and physical injury risks, keeping trained staff ready for work.

Financing choices balance capital allocation against equipment reliability. Brand new forklifts demand substantial upfront capital, but they maintain low failure rates under both heavy and light weekly schedules. Used machinery costs less initially. Second-hand units should operate under 10 hours per week because breakdown risks and maintenance bills rise on older equipment. Leasing avoids high purchase costs and allows companies to direct capital toward core operational needs."""
}

# Verify valid JSON serialization
json_str = json.dumps(result, indent=2)
parsed = json.loads(json_str)

print("Title length:", len(parsed["title"]))
print("Meta title length:", len(parsed["meta_title"]))
print("Meta desc length:", len(parsed["meta_description"]))

# Verify bold markdown check
assert "**" not in parsed["body"], "Found bolding markdown!"

# Verify em dash check
for key in ["title", "meta_title", "meta_description", "body"]:
    assert "—" not in parsed[key] and "--" not in parsed[key], f"Em-dash found in {key}"

# Verify keyword presence
keywords = [
    "material handling equipment",
    "electric forklifts",
    "warehouse fleet management",
    "total cost of ownership",
    "ergonomic forklift design"
]
for kw in keywords:
    assert kw in parsed["body"].lower(), f"Missing keyword: {kw}"

print("All programmatic checks passed!")
