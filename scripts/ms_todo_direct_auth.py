#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_direct_auth.py — Двухсторонняя прямая авторизация Microsoft Graph Tasks API
через зарегистрированное приложение в Azure Portal.
"""

import sys
import json
import os
import msal

TOKEN_CACHE_FILE = "/opt/hermes/auth_ms_todo.json"
REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
SCOPES = [
    "https://graph.microsoft.com/Tasks.ReadWrite",
    "https://graph.microsoft.com/User.Read",
    "offline_access"
]

def generate_login_url(client_id):
    app = msal.PublicClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/common"
    )
    auth_url = app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return auth_url

def exchange_code_for_tokens(client_id, auth_code):
    app = msal.PublicClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/common"
    )
    result = app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        data_to_save = {
            "client_id": client_id,
            "tokens": result
        }
        with open(TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2)
        print("✅ Токены успешно получены и сохранены в", TOKEN_CACHE_FILE)
        return True
    else:
        print("❌ Ошибка получения токена:", json.dumps(result, indent=2))
        return False

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "exchange":
        exchange_code_for_tokens(sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 1:
        url = generate_login_url(sys.argv[1])
        print("URL_START")
        print(url)
        print("URL_END")
