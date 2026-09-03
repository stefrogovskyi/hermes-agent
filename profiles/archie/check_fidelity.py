import re

# Compare original vs rewrite specs and claims

original_facts = {
    "Stages": [
        "inventory and warehouse management",
        "supplier acquisition and selection based on beneficial terms",
        "order processing",
        "transportation — cargo carriage or parcel delivery, etc.",
        "goods distribution"
    ],
    "Parties": [
        "carriers", "freight forwarders", "3PL companies", "warehouse operators",
        "port authorities", "production managers", "e-commerce and offline retailers",
        "software developers", "analytics companies", "and others"
    ],
    "Core components / Modules": [
        "Inventory and warehouse systems (WMS)",
        "Transportation Management System (TMS)",
        "Customer OMS (order management system)",
        "Freight running module",
        "Reverse logistics module",
        "Logistics analytics module"
    ],
    "WMS details": [
        "inventory planning and optimization",
        "warehouse operations control",
        "accounting for your services and tariffs",
        "warehouse asset management",
        "inventory allocation, consignment planning, storage space optimization",
        "Dashboard",
        "maintaining proper inventory levels without shortages or overstocks",
        "increase return on assets, avoid financial risks"
    ],
    "TMS details": [
        "Enterprise fleet management",
        "accounting of transport assets",
        "truck, vessel, container, wagon, semi-trailer, aircraft, and more",
        "load statuses, destinations, prices",
        "Adjust shipping routes and schedule shipments",
        "Ensure proper delivery management and timely actions",
        "Automatically gather reliable data on each consignment",
        "Connect transportation systems to SeaRates global platform for improved tendering",
        "Promote transport assets and tariffs (destination, cargo type, price, etc.)",
        "Commercialize transport management and promote services to upsell",
        "Ready for tracking integration",
        "Real-time asset location, accurate analytics, order movements, status updates, each logistics event, tracking by sea, air, and land"
    ],
    "OMS details": [
        "Improve delivery flows, manage and customize shipping routes",
        "prevent delays, goods being lost, supply chain risks related to transparency/visibility",
        "booking management: rapid cancellations and modifications",
        "edit details, add tracking updates"
    ],
    "Freight running module details": [
        "Freight rates aggregation: market-competitive tariffs research",
        "Effortless integration of Freight Calculator software into LogMS",
        "pricing freight rates for any shipping type, comparing costs, avoiding hidden fees at initial stage",
        "Manual tariff search is not efficient, secure, or well thought out",
        "All-round tracking software: Tracking logistics software solution",
        "Sea, air, rail, and road shipping continuously monitored with a few clicks",
        "Tracking System tool can be integrated",
        "Accurate monitoring data: scope of logistics events, status updates, route changes",
        "Details on demurrage for extra costs prediction",
        "Tracking calendar for instant overview"
    ],
    "Reverse logistics details": [
        "Tracking returned goods, scheduling acceptance, repair operations, redistributing goods",
        "Monitor service quality assurance, get feedback to improve operations, 24/7 support"
    ],
    "Logistics analytics details": [
        "Reports on third-party logistics providers (3PL)",
        "Transparency of rates, requests, bookings",
        "Visibility of customers' paths",
        "Access to freight management tools",
        "One virtual Dashboard",
        "Inbound and outbound logistics operations in a few clicks",
        "Optimize transportation costs, improve overall efficiency"
    ],
    "Products / Offerings": [
        "SeaRates Express: ERP solution, web-integrated ERP. Access to booking management, TMS, SeaRates digital tools for logistics, Rate Management System, Chat System. Manage tariffs, warehouses, transportation services with single Dashboard.",
        "SeaRates Vendor package: Access to Logistics Explorer (sell/promote tariffs), Logistics Map (warehousing and transportation services promotion). Cover targeted audience requesting freight daily. Web integration of Logistics Map to website to promote tariffs and resell partners' offers.",
        "Contact email: sales@searates.com"
    ]
}

rewrite_text = """
Title: Modernizing Supply Chain Operations with SeaRates Logistics Management Systems
Meta Title: SeaRates Logistics Management Systems Guide
Meta Description: Discover how SeaRates logistics management software streamlines warehouse operations, freight tracking, transportation, and supply chain analytics.

Body Markdown:
Handling supply chain operations through paper logs or manual entry creates operational delays, heightens error rates, and limits long-term growth. Modern trade demands clear oversight across every phase, starting from instant freight calculation to real-time shipment monitoring.

### Operational Stages and Industry Applications

Planning and executing commercial logistics involves several interconnected steps:

* Inventory and warehouse management
* Supplier acquisition and selection based on beneficial terms
* Order processing
* Transportation across cargo carriage or parcel delivery
* Goods distribution

Logistics management software supports these regular activities for carriers, freight forwarders, third-party logistics (3PL) providers, warehouse operators, port authorities, production managers, e-commerce brands, offline retailers, software developers, and analytics firms.

Deploying digital management solutions delivers distinct operational advantages:

* Resource allocation aimed at lowering expenses while raising profits
* Digitalization that reduces manual workflows to facilitate scaling
* Enhanced supply chain visibility through secure real-time tracking
* Operational transparency across booking and delivery steps
* Service personalization to refine customer experiences
* Simplified planning and supplies regulation
* Instant access to extended analytics

### Key Software Capabilities for Logistics Automation

Integrated digital solutions bring key supply chain operations into a coordinated structure.

#### Warehouse Operations and Inventory Control
Warehouse management systems (WMS) focus on inventory planning and optimization, warehouse operations control, service tariffs accounting, and warehouse asset management. Operators manage daily tasks like inventory allocation, consignment planning, and storage space optimization through a clear Dashboard interface. Maintaining balanced inventory levels without shortages or overstocks helps meet demand on time, increasing return on assets and reducing financial risks.

#### Fleet Management and Transportation Systems
Transportation Management Systems handle enterprise fleet management by accounting transport assets across trucks, vessels, containers, wagons, semi-trailers, and aircraft. Fleet operators assign load statuses, destinations, and pricing for each asset. Advanced operations planning allows teams to adjust shipping routes, schedule shipments, control deliveries, and automatically collect reliable consignment data.

Connecting transportation systems to the SeaRates global platform improves tendering processes. Companies can promote transport assets and tariffs based on specific criteria such as destination, cargo type, and price to commercialize management operations and upsell services. The SeaRates TMS comes ready for tracking integration, providing real-time asset locations, order movements, status updates, accurate analytics, and event tracking across ocean, air, and land routes.

#### Order Processing and Route Customization
Order Management Systems (OMS) optimize delivery flows by allowing users to manage and customize shipping routes. This software prevents delays, lost goods, and visibility risks across parties. Integrated booking management enables quick cancellations and modifications, detail editing, and tracking updates, helping teams prevent transportation disruptions.

#### Freight Rate Aggregation and Real-Time Tracking
Researching competitive tariffs is vital for cost-effective logistics. Integrating Freight Calculator software into management systems simplifies pricing across all shipping modes, letting users compare rates and spot hidden fees early.

The Tracking System tool integrates directly into logistics software, providing continuous on-demand visibility for sea, air, rail, and road shipments. Decision-makers receive status updates, route changes, logistics event logs, demurrage details for extra cost predictions, and an instant tracking calendar overview.

#### Managing Returns and After-Sales Logistics
Reverse logistics features simplify return workflows by tracking returned items, scheduling acceptance, organizing repair operations, and redistributing goods. Monitoring service quality assurance, gathering customer feedback, and offering 24/7 client support help improve service standards.

#### Centralized Logistics Analytics and Reporting
Logistics analytics centralize reports on 3PL providers, rate transparency, requests, bookings, customer paths, and freight management tools inside a single virtual Dashboard. Analyzing inbound and outbound logistics operations in a few clicks allows companies to optimize transportation costs and elevate operational performance.

### Integrated Platforms: SeaRates Express and Vendor Tools

SeaRates provides comprehensive, flexible logistics software tailored to freight forwarders, carriers, logistics providers, shippers, software developers, and industry partners.

Operating as a web-integrated ERP solution, SeaRates Express combines booking management, TMS, Rate Management System, Chat System, and SeaRates digital tools within a single Dashboard. This central workspace allows teams to manage tariffs, warehouse activities, and transport services simultaneously.

The SeaRates Vendor Package helps companies market services to targeted shippers actively requesting freight on the SeaRates platform. Features include Logistics Explorer for selling and promoting tariffs, as well as Logistics Map for promoting warehousing and transportation services. Integration of Logistics Map directly onto a business website allows companies to showcase tariffs and resell partner offers on beneficial terms.

To adopt advanced supply chain management through SeaRates Express or discuss customized solutions, contact the team at sales@searates.com.
"""

print("=== CHECKING FACTUAL DISCREPANCIES / OMISSIONS / ADDITIONS ===")
# Check specific term changes or nuances
# 1. "paper logs or manual entry" -> Original says "Manual management of supply chain operations is becoming increasingly inefficient..." ("paper logs" was not mentioned in original text).
# 2. "e-commerce brands, offline retailers" -> Original says "e-commerce and offline retailers".
# 3. "ocean, air, and land routes" in TMS -> Original says "by sea, air, and land".
# 4. "sea, air, rail, and road shipping" in Freight Running -> Original says "Sea, air, rail, and road shipping".
# 5. Check if any features, metrics, modules, or tools were missed or hallucinated.

