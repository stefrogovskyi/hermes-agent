#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import os
import msal

CLIENT_ID = "14d82eec-204b-4a2f-b7e8-296a70dab67e"
SCOPES = ["Tasks.ReadWrite", "User.Read"]
REDIRECT_URI = "https://login.microsoftonline.com/common/oauth2/nativeclient"
TOKEN_CACHE = "/opt/hermes/auth_ms_todo.json"

def exchange_code(code):
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/consumers"
    )
    result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print("SUCCESS")
        return True
    else:
        print("ERROR:", json.dumps(result, indent=2))
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        exchange_code(sys.argv[1].strip())
    else:
        print("No code provided")
