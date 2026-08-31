---
name: email-automation
description: "Automate email outreach and Microsoft 365 Graph API."
---

# email-automation

Class-level skill for integrating email capabilities into AI agents, handling Microsoft 365 / Outlook Exchange authentication, and enforcing Human-in-the-Loop approval guardrails for sales and support workflows.

## When to use
- Connecting an AI agent to corporate email accounts (Microsoft 365, Outlook, Exchange, Gmail).
- Handling Microsoft 365 / Azure App Registration authentication and Microsoft Graph API.
- Implementing Human-in-the-Loop email approval workflows (Telegram draft notifications).
- Troubleshooting `AUTHENTICATE failed` or `403 ErrorAccessDenied` on Exchange Online / Microsoft Graph.

## Key Workflows & References
- `references/microsoft_365_graph_mail_integration.md` — Complete reference for Microsoft 365 Graph API setup, Azure Portal App Registrations, Secret ID vs Value pitfalls, 403 consent fixes, full HTML body thread accumulation, In-Reply-To/References RFC headers, deterministic Telegram approval interceptor, and OpenAI tool-call null content normalization recipes.
