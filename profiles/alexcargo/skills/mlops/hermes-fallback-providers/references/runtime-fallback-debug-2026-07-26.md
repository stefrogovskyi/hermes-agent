# Runtime fallback debug — 2026-07-26
## Finding
Main-agent runtime fallback did not activate after `tencent/hy3:free` became unavailable. Telegram stayed connected but stopped answering because the failure did not route through a recognized fallback path.

## Relevant code
- `agent/agent_init.py:1208-1375`
- `agent/agent_runtime_helpers.py:1212, 1395-1412, 1576-1580, 2400-2412`
- `agent/auxiliary_client.py:3350-3441`
- `agent/auxiliary_client.py:4064-4112`
- `agent/auxiliary_client.py:4115-4170`

## Known state
- `config.yaml` `fallback_providers` is a valid list.
- `gateway_state.json` `telegram.state=connected` with no error.
