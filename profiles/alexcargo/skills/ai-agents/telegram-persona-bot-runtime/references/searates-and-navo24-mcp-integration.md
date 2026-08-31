# SeaRates API & Navo24 MCP Integration for Persona Bots

## 1. SeaRates API Integration
Key: `SEARATES_API_KEY` (`K-DD37901D-AF29-4CEE-A629-97D576E608AF`)
Documentation: `https://docs.searates.com`

### Endpoints
- Container Tracking API v3.0: `GET https://tracking.searates.com/tracking?api_key={key}&number={number}`
- Vessel Tracking API v3.0: `GET https://vessel-tracking.searates.com/vessel-tracking?api_key={key}&imo={imo}`
- Distance & Time API: `GET https://distance.searates.com/distance?api_key={key}&from={pol}&to={pod}`
- World Sea Ports API: `GET https://ports.searates.com/ports?api_key={key}&search={query}`

## 2. Navo24 MCP Integration
Key: `NAVO_API_KEY` (`tmcp_live_f4f492af5e24ba412a16028d428f2fbbfe27c32c`)
Transport: Remote Streamable MCP HTTP (`Accept: application/json, text/event-stream`)

### Endpoints
- SchedulesMCP: `POST https://mcp.schedulesmcp.com/mcp` (`compare_lanes`, `find_sailings`, `get_lane_reliability`)
- TrackingMCP: `POST https://mcp.trackingmcp.com/mcp` (`get_shipment_summary`, `track_shipment`, `get_demurrage_risk`)
- LoadingMCP: `POST https://mcp.loadingmcp.com/mcp` (`list_equipment`, `plan_load`)
- FreightRatesMCP: `POST https://mcp.freightratesmcp.com/mcp` (spot rates & ocean freight trends)

## 3. Task Tracker Completed Task Workflow (Non-Hedged Rule)
- When a task reaches 100%:
  1. Call `update_task(id=..., percent="100%")`.
  2. In Google Sheets (`Navo Tasktracker`), move the row down to the `ВЫПОЛНЕННЫЕ ЗАДАЧИ` block.
  3. Apply **light-green background fill** (`#d9ead3`).
  4. NEVER delete or hide the row — rows remain in the sheet forever for audit and history.
  5. State this behavior 100% confidently without hedged phrases like "if there is an integration" or "usually I".
