#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poll_and_report_inbound.py — Richard Marlowe (Navo24)
Monitors incoming emails via MS Graph API for rich@navo24.com.
Delivers complete briefings with full RU translations, parsed contact details, and prepared response drafts.
"""

import os
import sys
import json
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv("/opt/hermes/profiles/richard/.env")

TENANT_ID = "dc47c5b1-313f-47eb-ab6f-5f0716f400b5"
CLIENT_ID = "807fed17-45a8-4c7c-9a28-5997bbd30970"
CLIENT_SECRET = "g4d8Q~CNgmzLDEE1g_enAIqTpClyZ4N~VKhK9c63"
USER_EMAIL = "rich@navo24.com"
SEEN_FILE = "/opt/hermes/profiles/richard/cache/seen_inbound_emails.json"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

def get_graph_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }
    try:
        r = requests.post(url, data=data, timeout=15)
        return r.json().get("access_token")
    except Exception:
        return None

def clean_incoming_text(html_content, plain_content):
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text("\n", strip=True)
    else:
        text = plain_content or ""
    
    delimiters = [
        "From: Stefan Rogovskiy",
        "From: Stefan Rogovskyi",
        "From: Richard Marlowe",
        "-----Original Message-----",
        "________________________________",
        "EXTERNAL EMAIL",
        "------------------ 原始邮件 ------------------",
        "在 2026年"
    ]
    
    for d in delimiters:
        if d in text:
            text = text.split(d)[0].strip()
            
    if "DISCLAIMER:" in text:
        text = text.split("DISCLAIMER:")[0].strip()
        
    return text.strip()

def analyze_with_ai(sender_name, sender_email, subject, text, attachments):
    if not GEMINI_API_KEY:
        return None
        
    prompt = f"""You are Richard Marlowe, Senior B2B Sales Manager at Navo24 (navo24.com).
A new incoming email has arrived:
- Sender: {sender_name} <{sender_email}>
- Subject: {subject}
- Attachments: {', '.join(attachments) if attachments else 'None'}
- Cleaned Incoming Body:
{text}

Generate a concise, professional Telegram notification in clean Markdown (no HTML tags) with this structure:

📩 **НОВОЕ ВХОДЯЩЕЕ ПИСЬМО!**
* 👤 **Отправитель:** {sender_name} (`{sender_email}`)
* 🏢 **Компания:** (Extract company name or say 'Уточняется')
* 📱 **Телефон / WeChat:** (Extract if present or say 'Не указан')
* 📌 **Тема:** {subject}
{"* 📎 **Вложения:** " + ', '.join(attachments) if attachments else ""}

💬 **Оригинал сообщения:**
> {text}

🇷🇺 **Полный перевод на русский язык:**
> (Provide a smooth, natural Russian translation of the entire message)

✍️ **Готовый черновик ответа от Richard Marlowe (Navo24):**
(Write a tailored response in the sender's language (Chinese or English). Focus on Navo24 value: Tracking API across 239 ocean carriers and 97 airlines, DCSA standards, observed ETAs, D&D free-time, Schedules API across 60+ carriers, FreightRates API, Free Tier 5 containers/mo. Ask concrete qualification questions like target lanes, carrier contracts, WeChat/WhatsApp).

🇷🇺 **Перевод черновика на русский:**
> (Provide full Russian translation of the drafted response)

❓ **Отправляем ответ?** (Жду твоего подтверждения).
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2048
        }
    }
    
    try:
        r = requests.post(url, json=payload, timeout=25)
        if r.status_code == 200:
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        pass
        
    return None

def main():
    token = get_graph_token()
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    seen_ids = set()
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE, "r") as f:
                seen_ids = set(json.load(f))
        except Exception:
            pass

    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/Inbox/messages?$top=10&$orderby=receivedDateTime desc"
    try:
        r = requests.get(url, headers=headers, timeout=20)
        messages = r.json().get("value", [])
    except Exception:
        return

    new_messages = []
    for m in messages:
        mid = m["id"]
        sender = m.get("from", {}).get("emailAddress", {}).get("address", "").lower()
        if mid not in seen_ids and sender and not sender.endswith("@navo24.com") and not sender.endswith("@e.navo24.com"):
            new_messages.append(m)

    if not new_messages:
        return

    for m in new_messages:
        mid = m["id"]
        seen_ids.add(mid)
        
        sender_name = m.get("from", {}).get("emailAddress", {}).get("name", "")
        sender_email = m.get("from", {}).get("emailAddress", {}).get("address", "")
        subject = m.get("subject", "")
        
        body_obj = m.get("body", {})
        body_html = body_obj.get("content", "") if body_obj.get("contentType") == "html" else ""
        body_plain = body_obj.get("content", "") if body_obj.get("contentType") == "text" else ""
        
        cleaned_text = clean_incoming_text(body_html, body_plain)
        
        att_url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{mid}/attachments"
        try:
            r_att = requests.get(att_url, headers=headers, timeout=10)
            atts = r_att.json().get("value", [])
            real_atts = [a.get("name") for a in atts if a.get("name") and not a.get("isInline")]
        except Exception:
            real_atts = []

        # Generate intelligent AI report with translation and draft
        ai_report = analyze_with_ai(sender_name, sender_email, subject, cleaned_text, real_atts)
        
        if ai_report:
            print(ai_report)
            print("\n---\n")
        else:
            print(f"📩 **НОВОЕ ВХОДЯЩЕЕ ПИСЬМО!**")
            print(f"* 👤 **Отправитель:** {sender_name} (`{sender_email}`)")
            print(f"* 📌 **Тема:** {subject}")
            if real_atts:
                print(f"* 📎 **Вложения:** {', '.join(real_atts)}")
            print(f"\n💬 **Оригинал сообщения:**\n{cleaned_text}\n")
            print("---")

    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids)[-200:], f)

if __name__ == "__main__":
    main()
