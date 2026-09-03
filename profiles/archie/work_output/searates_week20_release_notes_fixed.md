TITLE: SeaRates Week 20: Tracking, Booking, and Map Updates
META TITLE: SeaRates Week 20: Air, Ocean Tracking & Booking Updates
META DESCRIPTION: SeaRates' Week 20 update covers Virtual Office, air and ocean tracking, AirRates, booking tools, and geocoding improvements across the platform.

BODY:
In freight forwarding software, small fixes pile up like cargo on a quiet dock, easy to overlook until you notice how much has actually shifted. Week 20's list touches Virtual Office, tracking, booking, and geocoding, all pieces of the same shipment visibility platform SeaRates has been building out. If you missed last week's rundown, it's worth a look before this one.

**Virtual Office and Inbox**

The VO Profile got a redesign this week, mostly aimed at making it faster to reach logistics apps and cleaning up how notifications appear. It's a small change, but one that shows up in daily use. Alongside it, the Inbox now shows an unread counter, so messages waiting on a reply are easier to spot at a glance.

**Air and Ocean Tracking**

Air Greenland, American Airlines, Air Premia, MNG Airlines, and ASL Airlines Belgium: all five now have improved support inside Air Tracking. On the ocean side, the container tracking API picked up better collaboration with Orient Overseas Container Line (OOCL), Wan Hai, Hapag-Lloyd, M-Line, and Crane Worldwide Logistics. Both updates add to the list of carriers and shipping lines supported across the tracking tools.

**Distance & Time and Ship Schedule**

For the Distance & Time API, the logic behind location determination was upgraded. Ship Schedule also got attention this week: collaboration with shipping lines worldwide now includes Gemadept by Points, plus NPDL and UAL by Vessel.

**AirRates**

Flight Schedules within AirRates added two more airlines this week, Korean Air and Finnair. Timetables for available airlines can be pulled through the API documentation.

**Booking System**

The Booking System saw the widest set of changes this week, spread across the Booking API and the Tracking tab. Event display is now built from the shipment data SeaRates receives, plus updates pulled from the Tracking API whenever a booking includes a container number.

Shippers can now download an invoice straight from the Payment tab, a small addition worth noting for anyone chasing paperwork deadlines.

New events can also be added manually, and they're sorted automatically by the date specified. No need to reorder a timeline by hand after every update.

**Geocoding API**

Geocoding got the deepest update this round. Port mapping and geodata processing logic changed on two fronts. Ports are now ranked adaptively, weighing relevance against distance and name similarity. Port type identification also improved, now verified against navigable waterways using OpenStreetMap data, as part of the same geodata accuracy improvements.

River ports and dry ports are now identified correctly too, thanks to newly added support for both fully and partially navigable rivers and channels.

**Announcements**

Three announcements round out the week: a new Map Platform, the Geocoding API integrated with Logistics Explorer, and Inbox integration extended across Logistics Explorer, Bookings, and Notifications.
