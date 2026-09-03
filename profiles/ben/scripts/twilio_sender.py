import os
import json
import urllib.request
import urllib.parse
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TWILIO_ACCOUNT_SID = "AC37a243b9e13460ef75e7b5dc782e9709"
TWILIO_AUTH_TOKEN = "5e9e03401a22c8573ca13f0edfdd8e8c"

def send_sms(from_number, to_number, message_body):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = urllib.parse.urlencode({
        "From": from_number,
        "To": to_number,
        "Body": message_body
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method="POST")
    auth_str = f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}"
    auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    req.add_header("Authorization", f"Basic {auth_b64}")
    
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def send_whatsapp(from_whatsapp_number, to_number, message_body):
    # from_whatsapp_number formatted like 'whatsapp:+14155238886'
    # to_number formatted like 'whatsapp:+1305xxxxxxx'
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = urllib.parse.urlencode({
        "From": from_whatsapp_number if from_whatsapp_number.startswith('whatsapp:') else f"whatsapp:{from_whatsapp_number}",
        "To": to_number if to_number.startswith('whatsapp:') else f"whatsapp:{to_number}",
        "Body": message_body
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method="POST")
    auth_str = f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}"
    auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    req.add_header("Authorization", f"Basic {auth_b64}")
    
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

print("Twilio dispatch helpers initialized successfully.")
