# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_FROM = "rich@navo24.com"
EMAIL_PASS = "RM#Navo24"
TO_EMAIL = "dr.reenforce@gmail.com"

subject = "Test Email from Richard Marlowe (Navo24) - Verified Official HTML Signature"

sig_html = open("/opt/hermes/richard_official_signature.html", encoding="utf-8").read()

body_html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 15px; color: #0b0c0e; line-height: 1.6;">
  <p>Hello Stefan,</p>
  <p>This is a direct test email sent via Office365 SMTP from <b>Richard Marlowe</b> (rich@navo24.com) with the exact official signature featuring the Navo logo image (https://bit.ly/4hLg86T) and blue links (#0000FF).</p>
  <br>
  {sig_html}
</div>
"""

print(f"Connecting to {SMTP_HOST}:{SMTP_PORT}...")
try:
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Richard Marlowe <{EMAIL_FROM}>"
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText("Hello Stefan, test email.", "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, [TO_EMAIL], msg.as_string())
        print("✅ TEST EMAIL DISPATCHED VIA OFFICE365 SMTP TO dr.reenforce@gmail.com!")
except Exception as e:
    print("Error:", e)
