import urllib.request
import json
import time

def send_whatsapp_message(phone, text):
    url = "http://localhost:3050/send-message"
    data = json.dumps({"phone": phone, "message": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

print("WhatsApp sender client ready.")
