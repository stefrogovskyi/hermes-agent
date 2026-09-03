import re

orig = """Route planning is not always about simple delivery from point A to B but also includes day-to-day challenges that are fortunately avoidable. Effective pre-planning is the key to secure and transparent transportation and satisfied customers. There is no need to circle the globe to create efficient routes when it can be done in a few minutes with a smart routing tool.

Route Planner is designed to personalize supply chains and transform outdated management. It allows logistics providers to manage linear and multimodal transportation and provide customers with up-to-date information 24/7.

How does the tool work?
Sign up here to get up to 5 free routes for internal usage.
Get your subscription to create up to 50 routes per month with your unique tracking IDs in the Container Tracking tool and share access publicly.
or Let us know about your intentions for your own Route Planner tool and receive a customized solution tailored to meet your needs.

How to create transparent shipping routes?
The Route Planner tool is designed as smart software for logistics providers (carriers, freight forwarders, and transport companies) to rapidly create cost-effective routes for sea/air/land operations and further 24/7 tracking for real-time updates. Freight providers can address shippers' wide variety of transportation needs with such customized routing solutions.

Start with 'Create new route', entering the title and description of the route. The title might be the container/reference/order number and can be used as your further tracking number. Here you can find your first route or get it listed among others.

The second step is to Add point to route or several.
Shipping under the FOB (Free-on-Board) terms? Add the first logistics event — loading on board. Select the location type, country, and port; name this event; and specify the date. The first route point of your route will appear in the list and on the map.
Carrying port-to-port service? Add the port of discharge and the planned date as a next route point. The second point will also be listed on the left and visualized on the map, where you can click to check.
Let's add more information for each of your points, such as the duration of cargo processing at local ports. Edit points by adding more events and finally click on 'Update'.
Finally, add a land delivery event for transportation to the warehouse. Specify the place, name the event, choose the date, and find the newly added point displayed.

Also, Route Planner provides a brief summary for your route, including distance and transit time at average speed.

Carrying multimodal shipments? Create fully customized routes with variety points for sea, air, road, and rail logistics, as well as add multiple transshipment points (seaports, airports, warehouses, or rail stations). Adjust the points to customize the route according to your needs. No matter how complicated the route may seem in your imagination, our tool will break down any difficult routing task into its simplest form and provide a solution.

Your route has been successfully created! Go to your route card to find the copy link and edit icons in the upper right corner. Copy the link to provide direct access to your customer or partner. You can use this unique tracking ID for real-time monitoring in the Container Tracking tool. You can apply individual tracking numbers for each shipment.

Difficult routes are not to be feared when you have a tool for detailed planning and further tracking shipments in line with all your requirements and shippers' needs.

Web integration:
You can provide smooth routing and supplies optimization with our white-labeled Route Planner solution. Ensure customized shipping management with a routing tool on your own website. This web-integrated tool is extended with the SeaRates Container Tracking — your customers can monitor their shipments by your unique ID 24/7. Moreover, Route Planner is integrated with our Booking System to ensure all-around supply chain management. Upsell by engaging customers with logistics transparency under your brand.

API connection:
Create your own software or mobile app for smart routing for trading companies, logistics providers, and carriers with Route Planner API integration. Connecting API ensures complete sync of insights on your shipments and logistics events, as well as automating data management and customized tracking across your CRM/ERP/TMS.

Integrate Route Planner:
You're always welcome to let us know about your requirements by filling out the Request an IT Quote form or contacting us at sales@searates.com for a tailored solution."""

rewrite = """TITLE: SeaRates Route Planner: Setup & Real-Time Tracking Guide
META TITLE: SeaRates Route Planner | Build & Track Multimodal Routes
META DESCRIPTION: Build multimodal routes, track shipments 24/7, and integrate SeaRates Route Planner via white-label tools or API into your CRM, ERP, or TMS.

A cargo route looks simple on paper until an ocean vessel sits at anchor for three days waiting for a berth. Managing legs across different transport modes brings daily operational friction. SeaRates Route Planner functions as supply chain visibility software for freight forwarders and transport providers, organizing linear or multimodal trips and sharing live status details with clients around the clock.

## Account Tiers and Access

You can begin with a free account. Free registration gives you 5 routes for internal testing and operations. 

Paid subscriptions grant up to 50 routes each month. Subscription plans generate unique tracking IDs for every journey, connecting directly into the Container Tracking tool and enabling public link sharing with your clients. 

For companies needing full enterprise deployment, SeaRates builds custom routing setups tailored to specific operational requirements.

## How to Build a Custom Shipping Route

Start by selecting 'Create new route' inside the dashboard. Enter a title along with a short description. Using your container number, bill of lading, reference ID, or order code as the title creates a recognizable identifier. This entry becomes your primary tracking reference across the platform.

Next, add your route points.

For Free-on-Board (FOB) shipments, create your initial logistics event by logging the vessel loading point. Specify the location type, country, seaport, and event name, then set the date. The system plots this first milestone in your route list and marks its geographic position on the interactive map.

If you handle port-to-port contracts, add your discharge port and estimated arrival date as the second milestone. The point displays on the left panel and pins to the map view. Clicking the map pin opens point details.

You can edit events to reflect operational specifics, including cargo handling times and dwell periods at local ports. Select 'Update' to save changes to each milestone. 

To complete a door-to-door move, add a land transport event for final warehouse delivery. Enter the destination site, name the transfer action, set the schedule, and save.

The system calculates total route distance alongside expected transit times based on average transport speeds.

## Multimodal Moves and Shipment Sharing

Complex itineraries require flexible planning tools. Using a multimodal route planner lets transport teams map sea, rail, road, and air transit legs in one interface. You can insert multiple transshipment hubs, including container terminals, air cargo facilities, inland rail ramps, or distribution warehouses. The planner breaks complex multi-leg journeys into clear steps.

Once you complete a setup, open the route card. Copy and edit icons sit in the upper right corner. 

Copying the direct route link lets clients or freight partners view transit progress without logging into your master account. For freight forwarder route planning, this eliminates messy spreadsheet updates by connecting unique tracking IDs directly into the Container Tracking tool, enabling real-time shipment tracking per container or bill of lading.

## Integration Options for Websites and Software

Companies looking to expand client-facing services can integrate Route Planner directly into their digital infrastructure.

### Web Integration
Deploying white-label logistics routing onto your company website gives customers a branded portal to check routes and schedules. This web widget pairs with SeaRates Container Tracking using unique tracking IDs to deliver 24/7 cargo monitoring under your brand name. It also links with the SeaRates Booking System to support complete shipment workflows and drive upselling opportunities.

### API Connection
A shipping API integration connects Route Planner logic into existing CRM, ERP, TMS, or back-office platforms. Logistics providers and trading companies use the API to automate data management, synchronize shipment milestones, and power internal or mobile applications.

To set up an integrated routing tool, submit a Request an IT Quote form on SeaRates or contact sales@searates.com for technical options."""

# Final summary statistics
print("=== AUDIT SUMMARY ANALYSIS ===")
print("Original word count:", len(orig.split()))
print("Rewrite word count:", len(rewrite.split()))
