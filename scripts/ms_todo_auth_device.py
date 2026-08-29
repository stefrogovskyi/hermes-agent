#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_auth_device.py — Прямая OAuth-авторизация Microsoft Graph (Tasks.ReadWrite)
"""

import sys
import json
import os
import msal

# Official Azure CLI / Microsoft PowerShell cross-platform client ID (enabled for common/consumers)
CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Microsoft Azure CLI Public Client
SCOPES = ["https://graph.microsoft.com/Tasks.ReadWrite", "https://graph.microsoft.com/User.Read"]
TOKEN_CACHE_FILE = "/opt/hermes/auth_ms_todo.json"

def main():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/common"
    )

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print("❌ Ошибка инициализации Device Flow:", json.dumps(flow, indent=2))
        sys.exit(1)

    print(f"URL: {flow['verification_uri']}")
    print(f"CODE: {flow['user_code']}")
    sys.stdout.flush()

    # Wait for user authorization
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        print("✅ Авторизация успешна!")
        with open(TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"Токен сохранён в {TOKEN_CACHE_FILE}")
    else:
        print("❌ Ошибка авторизации:", result.get("error_description") or result.get("error"))

if __name__ == "__main__":
    main()
