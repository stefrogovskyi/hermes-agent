# -*- coding: utf-8 -*-
"""
ms_graph_mail.py — Microsoft Graph API Mail Client for Microsoft 365.
"""

import os, sys, time, json, urllib.request, urllib.parse

def get_graph_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials"
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("access_token")

def fetch_unread_messages(token, target_email):
    url = f"https://graph.microsoft.com/v1.0/users/{target_email}/mailFolders/inbox/messages?$filter=isRead eq false&$top=10"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("value", [])
