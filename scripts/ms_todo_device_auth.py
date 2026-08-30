#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_device_auth.py — Прямая авторизация Microsoft Graph API (Tasks.ReadWrite) через Device Code Flow.
"""

import sys, json, os, time
import msal

TOKEN_CACHE_FILE = "/opt/hermes/auth_ms_todo.json"
CLIENT_ID = "d3590ed6-52b3-4102-aeff-aad2292ab01c" # Microsoft Office Public Native Client ID
SCOPES = [
    "https://graph.microsoft.com/Tasks.ReadWrite",
    "https://graph.microsoft.com/User.Read"
]

def main():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/common"
    )

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print(f"Error initiating device flow: {json.dumps(flow, indent=2)}")
        sys.exit(1)

    print("=== DEVICE FLOW INITIATED ===")
    print(f"USER_CODE: {flow['user_code']}")
    print(f"VERIFICATION_URI: {flow['verification_uri']}")
    print(f"MESSAGE: {flow['message']}")
    sys.stdout.flush()

    # Wait for user authorization
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        data_to_save = {
            "client_id": CLIENT_ID,
            "tokens": result,
            "saved_at": time.time()
        }
        with open(TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2)
        print("SUCCESS_AUTH: Tokens saved to", TOKEN_CACHE_FILE)
    else:
        print("AUTH_FAILED:", json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
