# SeaRates API & Tasktracker Auto-Update Patterns

## 1. SeaRates API Integration Pattern
- **API Key location:** `SEARATES_API_KEY` in `.env` / `.env.local`
- **Official Docs:** `https://docs.searates.com`
- **Endpoints:**
  - Container Tracking v3.0: `https://tracking.searates.com/tracking?api_key={key}&number={number}`
  - Vessel Tracking v3.0: `https://vessel-tracking.searates.com/vessel-tracking?api_key={key}&imo={imo}`
  - Distance & Time API: `https://distance.searates.com/distance?api_key={key}&from={pol}&to={pod}`
  - World Sea Ports API: `https://ports.searates.com/ports?api_key={key}&search={query}`
- **Response handling:**
  - Status `success` -> parse `data.containers[].events` or route info.
  - Status `error` with `message: "WRONG_NUMBER"` -> invalid container format.

## 2. Master Sheet & 100% Completion Protocol
- **Master Table Identity:** Alistair uses `Navo Tasktracker` (Google Sheet ID `1Bi4cEq0C3nOSNvI3y8J15ruv97LvG1Ww056O7I9MIvY`).
- **100% Completion Protocol (No Deletion / No Hiding):**
  - When `percent == 100%`, `update_task` moves row to bottom `=== ВЫПОЛНЕННЫЕ ЗАДАЧИ ===` section of `Tracker` tab.
  - Applies **light-green background fill** (`#d9ead3`).
  - Rows are **NEVER deleted or hidden** from Google Sheets.
- **Snapshot Auto-Update Rule:**
  - When user quotes a release report (Sort It Bot / Gaffer), bot MUST NOT ask "what's the task ID?".
  - Bot calls `read_tracker_sheet`, matches task names, sets `percent: 100%`, and reports updated tasks.

## 3. Anti-Hedging & Demo-Ready Persona Rule
- Never use uncertain boilerplate: *"если есть возможность"*, *"если есть интеграция"*, *"если предусмотрено"*, *"обычно я"*.
- State exact live tools, Google Sheet mechanics, and Gaffer integrations with 100% confidence.
