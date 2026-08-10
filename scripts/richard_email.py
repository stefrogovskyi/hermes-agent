# -*- coding: utf-8 -*-
import os, sys, time, json, smtplib, imaplib, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "rich@navo24.com"
EMAIL_PASSWORD = "RM#Navo24"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

EXACT_SIGNATURE_HTML = """<br><br>
<div style="font-family: Tahoma, Arial, sans-serif; font-size: 10pt; color: #000000; line-height: 1.25;">
  <b>Richard Marlowe</b><br>
  <b>Connections Manager</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics &amp; Trade<br>
  +44 203 440 9800<br>
  <a href="mailto:rich@navo24.com" style="color: #0000FF; text-decoration: underline;">rich@navo24.com</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #0000FF; text-decoration: underline;">www.navo24.com</a>
</div>"""

def send_email_direct(to_email, subject, body_html, body_text=None, cc_email=None):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"Richard Marlowe <{EMAIL_ADDRESS}>"
        msg["To"] = to_email
        if cc_email:
            msg["Cc"] = cc_email
        msg["Subject"] = subject

        full_html = body_html + EXACT_SIGNATURE_HTML

        if body_text:
            msg.attach(MIMEText(body_text, "plain", "utf-8"))
        msg.attach(MIMEText(full_html, "html", "utf-8"))

        recipients = [to_email]
        if cc_email:
            recipients.append(cc_email)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())
        server.quit()
        return True, "SUCCESS"
    except Exception as e:
        return False, str(e)
