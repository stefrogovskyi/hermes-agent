#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ms_todo_cli_auth.py — Простая авторизация Microsoft Graph без веб-серверов и Azure App регистрации.
Использует официальный Microsoft Graph PowerShell CLI Client ID (разрешен для всех личных аккаунтов).
"""

import sys
import json
import os
import msal

# Официальный общедоступный клиент Microsoft Graph PowerShell
# Поддерживает личные аккаунты (consumers / live.com / outlook.com)
CLIENT_ID = "14d82eec-204b-4a2f-b7e8-296a70dab67e"
SCOPES = ["Tasks.ReadWrite", "User.Read"]
TOKEN_CACHE = "/opt/hermes/auth_ms_todo.json"

def get_auth_url():
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/consumers"
    )
    
    # Redirect URI for public client
    redirect_uri = "https://login.microsoftonline.com/common/oauth2/nativeclient"
    auth_url = app.get_authorization_request_url(
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    return auth_url, redirect_uri, app

if __name__ == "__main__":
    url, red, app = get_auth_url()
    print("AUTH_URL_START")
    print(url)
    print("AUTH_URL_END")
