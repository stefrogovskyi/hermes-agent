---
name: afterquery-mcp-atlas
description: Use when building, testing, or benchmarking MCP tools/servers across Python, TypeScript, and Docker environments using the AfterQuery MCP-Atlas harness.
category: research/afterquery
---

# AfterQuery MCP-Atlas (Model Context Protocol Evaluation)

MCP-Atlas is the enterprise benchmark and testing harness for evaluating LLM agent tool-use capabilities across 36+ real-world Model Context Protocol (MCP) servers.

## Key Capabilities
- Validate custom MCP servers (e.g. Navo TrackingMCP, FreightRatesMCP, SchedulesMCP).
- Test tool-calling accuracy, argument schema validation, and failure recovery.
- Reusable asynchronous MCP client architecture in Python and TypeScript.

## Repository Location
`/opt/hermes/profiles/alistair/repos/afterquery/mcp-atlas`

## Quick Start & Verification
```bash
cd /opt/hermes/profiles/alistair/repos/afterquery/mcp-atlas
# Inspect available test servers and schemas
python3 -c "import os; print('MCP Atlas modules:', os.listdir('.'))"
```

## Best Practices for Navo
- When creating an MCP wrapper for logistics APIs, test the JSON schema inputs through MCP-Atlas verifiers before publishing to production.
- Use `agent_environment/mcp_client.py` pattern for zero-dependency MCP client connections.
