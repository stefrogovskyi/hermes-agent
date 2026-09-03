#!/usr/bin/env python3
"""
CargoSavior Email Client & Draft Automation
Active blue links for email and website, plain black text for address (no maps link).
"""

import os
import sys
import json
import time
import imaplib
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

EMAIL_USER = "contact@cargosavior.com"
EMAIL_PASS = "Cargo#171004"
IMAP_SERVER = "imap.hostinger.com"
IMAP_PORT = 993
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465

SIGNATURE_HTML = """<div style="font-family: Tahoma, Geneva, sans-serif; font-size: 10pt; color: #000000; line-height: 1.25; margin-top: 18px;">
<b>Alex Cargo</b><br>
Account Executive<br>
<a href="https://www.cargosavior.com" target="_blank" style="text-decoration: none; display: inline-block; margin: 2px 0 0 0; padding: 0;"><img src="https://bit.ly/4xt2bzz" alt="CargoSavior" width="170" style="display: block; border: 0; width: 170px; max-width: 170px; height: auto; margin: 0; padding: 0;" /></a><br>
Abandoned Cargoes to Profit<br>
<a href="tel:+17373551070" style="color: #000000; text-decoration: none;">+1 737 355 1070</a><br>
<a href="mailto:contact@cargosavior.com" style="color: #0000FF !important; text-decoration: underline !important;">contact@cargosavior.com</a><br>
<a href="javascript:void(0)" style="color: #000000 !important; text-decoration: none !important; cursor: default !important; pointer-events: none !important;">3508 Far West Blvd, Ste 130</a><br>
<a href="javascript:void(0)" style="color: #000000 !important; text-decoration: none !important; cursor: default !important; pointer-events: none !important;">Austin, TX 78731, USA</a><br>
<a href="https://www.cargosavior.com" target="_blank" style="color: #0000FF !important; text-decoration: underline !important;">www.cargosavior.com</a>
</div>"""

SIGNATURE_TEXT = """--
Alex Cargo
Account Executive
[CargoSavior Logo: https://bit.ly/4xt2bzz]
Abandoned Cargoes to Profit
Phone: +1 737 355 1070
Email: contact@cargosavior.com
3508 Far West Blvd, Ste 130
Austin, TX 78731, USA
www.cargosavior.com"""

def clean_text(text: str) -> str:
    """Normalize literal escape characters into real whitespace."""
    if not text:
        return ""
    res = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\t", " ")
    return res

def create_email_message(to_email: str, subject: str, body_text: str, body_html: str = "") -> MIMEMultipart:
    cleaned_body = clean_text(body_text)
    
    msg = MIMEMultipart("alternative")
    msg["From"] = f"Alex Cargo <{EMAIL_USER}>"
    msg["To"] = to_email
    msg["Subject"] = str(Header(subject, "utf-8"))
    msg["Date"] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

    # Plain text version
    full_text = f"{cleaned_body.strip()}\n\n{SIGNATURE_TEXT.strip()}"
    msg.attach(MIMEText(full_text, "plain", "utf-8"))

    # HTML version
    if body_html:
        formatted_html_body = clean_text(body_html)
    else:
        paragraphs = [p.strip() for p in cleaned_body.split("\n\n") if p.strip()]
        formatted_html_body = "".join(
            f"<p style='margin: 0 0 14px 0; font-family: Tahoma, Geneva, sans-serif; font-size: 10pt; color: #000000; line-height: 1.5;'>{p.replace(chr(10), '<br>')}</p>"
            for p in paragraphs
        )

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 12px; background-color: #ffffff; font-family: Tahoma, Geneva, sans-serif;">
{formatted_html_body}
{SIGNATURE_HTML}
</body>
</html>"""
    msg.attach(MIMEText(full_html, "html", "utf-8"))
    return msg

def save_draft(to_email: str, subject: str, body_text: str, body_html: str = "") -> dict:
    msg = create_email_message(to_email, subject, body_text, body_html)
    raw_msg = msg.as_bytes()

    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)

    mail.select("INBOX.Drafts")
    status, msgs = mail.search(None, "ALL")
    for num in msgs[0].split():
        mail.store(num, "+FLAGS", "\\Deleted")
    mail.expunge()

    result, data = mail.append("INBOX.Drafts", r"(\Draft \Seen)", imaplib.Time2Internaldate(time.time()), raw_msg)
    mail.logout()

    if result == "OK":
        return {"success": True, "action": "draft_saved", "to": to_email, "subject": subject, "mailbox": "INBOX.Drafts"}
    return {"success": False, "error": str(data)}

def send_email(to_email: str, subject: str, body_text: str, body_html: str = "") -> dict:
    msg = create_email_message(to_email, subject, body_text, body_html)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, [to_email], msg.as_string())

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.append("INBOX.Sent", r"(\Seen)", imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        mail.logout()
    except Exception:
        pass

    return {"success": True, "action": "sent", "to": to_email, "subject": subject}

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 email_client.py [draft|send] <to_email> <subject> <body>")
        sys.exit(1)

    action = sys.argv[1]
    to_email = sys.argv[2]
    subject = sys.argv[3]
    body = sys.argv[4] if len(sys.argv) > 4 else ""

    if action == "draft":
        res = save_draft(to_email, subject, body)
    elif action == "send":
        res = send_email(to_email, subject, body)
    else:
        res = {"success": False, "error": f"Unknown action {action}"}

    print(json.dumps(res, indent=2))
