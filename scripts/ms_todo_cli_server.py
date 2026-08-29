#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_cli_server.py — Автономная авторизация Microsoft To-Do через локальный браузерный редирект.
"""

import sys
import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import msal
import requests

CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Azure CLI multi-tenant public client
SCOPES = ["https://graph.microsoft.com/Tasks.ReadWrite", "https://graph.microsoft.com/User.Read"]
REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
TOKEN_CACHE = "/opt/hermes/auth_ms_todo.json"

def get_auth_url():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/common"
    )
    auth_url = app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return auth_url

def exchange_code(code):
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/common"
    )
    result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print("✅ УСПЕХ: Токен сохранён в", TOKEN_CACHE)
        return result["access_token"]
    else:
        print("❌ Ошибка:", json.dumps(result, indent=2))
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = exchange_code(sys.argv[1].strip())
        if token:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            r = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", headers=headers)
            print("LISTS_RESPONSE:", json.dumps(r.json(), indent=2, ensure_ascii=False))
    else:
        print("URL:", get_auth_url())
