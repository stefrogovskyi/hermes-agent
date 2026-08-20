---
name: universal-api-reference
description: "Search 3,122+ APIs and 75k endpoints offline from MindCloud."
version: 1.0.0
author: MindCloud + Hermes Agent
license: CC-BY-4.0
metadata:
  hermes:
    tags: [api, openapi, endpoints, mindcloud, integration, rest, mcp]
---

# Universal API Reference (MindCloud Open Source)

Offline reference directory containing machine-readable specifications, endpoints, parameters, and payloads for **3,122+ APIs and 75,075+ endpoints**.

- **Repository Path:** `/opt/hermes/universal-api-reference`
- **APIs Directory:** `/opt/hermes/universal-api-reference/apis/`
- **LLM Manifest:** `/opt/hermes/universal-api-reference/llms.txt`

## How to Search APIs

To look up any API, endpoint, or schema for integration:

```bash
# Search by app name (e.g., stripe, shopify, hubspot, slack, github, twilio)
search_files(path="/opt/hermes/universal-api-reference/apis", pattern="*stripe*")

# Search endpoint details or parameters
search_files(path="/opt/hermes/universal-api-reference/apis", pattern="payment_intents", target="content")
```

All 6 Hermes profiles have local offline access to this library!
