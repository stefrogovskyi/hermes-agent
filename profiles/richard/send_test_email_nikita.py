import requests

RESEND_API_KEY = "re_HYSmY1vz_JDgFN8YzffnTeT6mR2YnSufo"

SIGNATURE_HTML = """<div style="margin-top: 24px; font-family: Tahoma, Arial, sans-serif; font-size: 13px; color: #334155; line-height: 1.4; text-align: left;">
  <b>Nikita Kurudzhy</b><br>
  <b>Account Executive</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics & Trade<br>
  +380 93 228 5150<br>
  <a href="mailto:nikita@navo24.com" style="color: #2563eb; text-decoration: underline;">nikita@navo24.com</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #2563eb; text-decoration: underline;">www.navo24.com</a>
</div>"""

body_text = """Hi Emad,

We built Navo24 to give forwarders direct tracking across 239 ocean lines, live satellite AIS positions, and predictive ETAs that account for actual port congestion (founded by the original team behind SeaRates).

You can test a couple of your active shipments on our free tier at https://trackingmcp.com/auth/signup to see how the data looks against your carrier updates.

Worth taking a look?

Best regards,"""

paragraphs = [p.strip() for p in body_text.split("\n\n") if p.strip()]
cleaned_paras = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs if not p.lower().startswith("best")]

html_content = f"""<div style="font-family: Arial, sans-serif; font-size: 14px; color: #1e293b; line-height: 1.6; max-width: 600px; text-align: left;">
{"\n".join(cleaned_paras)}

<p>Best regards,</p>

{SIGNATURE_HTML}
</div>"""

payload = {
    "from": "Nikita Kurudzhy <nikita@e.navo24.com>",
    "to": ["Nikita Kurudzhy <nikita@navo24.com>"],
    "cc": ["Stefan Rogovskiy <stefan@navo24.com>"],
    "reply_to": "nikita@navo24.com",
    "subject": "[TEST PREVIEW] alfalahparts / container tracking",
    "html": html_content
}

r = requests.post(
    "https://api.resend.com/emails",
    headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=10
)

print("Test Email Status:", r.status_code, r.text)
