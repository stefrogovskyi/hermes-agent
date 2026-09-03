#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
richard_whatsapp.py — Richard Marlowe (Navo24 London)
Strictly isolated WhatsApp client for Richard Marlowe (+44 7360 065904).

HARD ISOLATION RULES:
- Only connects to Port 3060 (richard-whatsapp-gateway.service).
- Strict refusal and exception on Port 3050 (Ben Jett / Avalanche).
- Dedicated outbound logger.
"""

import os
import sys
import json
import logging
import requests

RICHARD_GATEWAY_PORT = 3060
RICHARD_GATEWAY_URL = f"http://localhost:{RICHARD_GATEWAY_PORT}"
LOG_FILE = "/opt/hermes/profiles/richard/logs/whatsapp_outbound.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def send_whatsapp_message(phone: str, message: str) -> dict:
    """
    Sends a WhatsApp message strictly through Richard's gateway (Port 3060, +44 7360 065904).
    """
    # Strict Port Guard
    if RICHARD_GATEWAY_PORT != 3060:
        raise ValueError(f"CRITICAL ISOLATION BREACH: Richard Marlowe is restricted to Port 3060. Attempted: {RICHARD_GATEWAY_PORT}")
        
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    if not clean_phone or not message:
        raise ValueError("Phone number and message text are required.")

    url = f"{RICHARD_GATEWAY_URL}/send-message"
    payload = {"phone": clean_phone, "message": message}
    
    try:
        r = requests.post(url, json=payload, timeout=20)
        res_data = r.json() if r.status_code in [200, 400, 404, 500] else {"raw": r.text}
        
        if r.status_code == 200 and res_data.get("success"):
            logging.info(f"SUCCESS | Sent to +{clean_phone} via Richard Gateway (+44 7360 065904) | MsgID: {res_data.get('messageId')}")
            return {"success": True, "message_id": res_data.get("messageId"), "phone": clean_phone}
        else:
            logging.error(f"FAILURE | Target: +{clean_phone} | Status: {r.status_code} | Err: {res_data}")
            return {"success": False, "error": res_data, "status_code": r.status_code}
            
    except Exception as e:
        logging.error(f"EXCEPTION | Target: +{clean_phone} | Err: {str(e)}")
        return {"success": False, "error": str(e)}

def get_gateway_status() -> dict:
    url = f"{RICHARD_GATEWAY_URL}/status"
    try:
        r = requests.get(url, timeout=5)
        return r.json()
    except Exception as e:
        return {"status": "offline", "error": str(e)}

if __name__ == "__main__":
    st = get_gateway_status()
    print(f"Richard WhatsApp Gateway (Port {RICHARD_GATEWAY_PORT}):", st)
