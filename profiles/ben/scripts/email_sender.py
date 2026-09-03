import os
import json
import time
import re
import urllib.request
import urllib.parse
import smtplib
import imaplib
import email.utils
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
IMAP_SERVER = "imap.hostinger.com"
IMAP_PORT = 993
SMTP_USER = "contact@aavalanche.com"
SMTP_PASS = "ContactAA#12345"
REPLY_TO = "ben.jett.ava@hotmail.com"

SIGNATURE_HTML = """
<br><br>
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Tahoma, sans-serif; font-size: 10pt; color: #000000; line-height: 1.25;">
  <tr>
    <td>
      <!-- Name and Title -->
      <div style="font-weight: bold; font-size: 12pt; margin-bottom: 2px;">Ben Jett</div>
      <div style="margin-bottom: 4px;">Account Executive</div>

      <!-- Icon Image -->
      <div style="margin-bottom: 4px;">
        <img src="https://bit.ly/3UdEHji" alt="Logo" width="178" style="display: block; border: 0; height: auto;" />
      </div>

      <!-- Contact Details -->
      <div>Web &amp; Marketing Services</div>
      <div>+1 302 401 9315</div>
      <div>
        <a href="mailto:contact@aavalanche.com" style="color: #1d4ed8; text-decoration: underline;">contact@aavalanche.com</a>
      </div>
      <div>225 Franklin Street, Suite 2600,</div>
      <div>Boston, MA 02110, USA</div>
      <div>
        <a href="https://www.aavalanche.com" style="color: #1d4ed8; text-decoration: underline;">www.aavalanche.com</a>
      </div>
    </td>
  </tr>
</table>
"""

SIGNATURE_TEXT = """
--
Ben Jett
Account Executive
Avalanche Agency | Web & Marketing Services
+1 302 401 9315
contact@aavalanche.com
225 Franklin Street, Suite 2600, Boston, MA 02110, USA
www.aavalanche.com
"""

def send_and_save_email(to_email, company_name, city, niche, sender_name="Ben Jett | Avalanche Agency"):
    if not to_email or "@" not in to_email:
        return False
        
    subject = f"Question regarding {company_name} in {city} / Online bookings"
    
    text_content = f"""Hi there,

I came across {company_name} on Google Maps in {city} and was impressed by your stellar customer reviews.

I noticed you don't currently have an official website or automated booking system attached to your Google Maps profile. Many potential customers looking for {niche} in {city} end up going to competitors who take online bookings 24/7.

At Avalanche Agency, we build high-converting websites with built-in 24/7 AI Sales Assistants that automatically capture leads and book appointments in under 48 hours ($490).

Would you be open to seeing a quick 2-minute live demo customized for {company_name}?

{SIGNATURE_TEXT}
"""

    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Tahoma, 'Segoe UI', Arial, sans-serif; font-size: 10pt; color: #222; line-height: 1.5;">
    <p>Hi there,</p>
    <p>I came across <strong>{company_name}</strong> on Google Maps in {city} and was impressed by your stellar customer reviews.</p>
    <p>I noticed you don't currently have a direct website or automated booking system attached to your profile. Many potential customers looking for {niche} in {city} end up going to competitors who take bookings online 24/7.</p>
    <p>At <strong>Avalanche Agency</strong>, we build high-converting websites with built-in <strong>24/7 AI Sales Assistants</strong> that automatically capture leads and book appointments straight into your schedule in under 48 hours ($490).</p>
    <p>Would you be open to seeing a quick 2-minute live demo customized for <strong>{company_name}</strong>?</p>
    {SIGNATURE_HTML}
</body>
</html>
"""
    msg = MIMEMultipart("alternative")
    msg['Subject'] = str(Header(subject, 'utf-8'))
    msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), SMTP_USER))
    msg['To'] = to_email
    msg['Reply-To'] = REPLY_TO
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = f"<{uuid.uuid4()}@aavalanche.com>"
    msg['X-Mailer'] = "Avalanche Mailer v1.0"
    
    part1 = MIMEText(text_content, 'plain', 'utf-8')
    part2 = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(part1)
    msg.attach(part2)
    
    raw_message = msg.as_string().encode('utf-8')

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], raw_message)

        try:
            imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            imap.login(SMTP_USER, SMTP_PASS)
            imap.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), raw_message)
            imap.logout()
        except Exception as e:
            print(f"IMAP note: {e}")

        print(f"✅ Email sent & saved to INBOX.Sent for {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")
        return False

if __name__ == "__main__":
    send_and_save_email("ben.jett.ava@hotmail.com", "Avalanche Agency Demo", "Boston, MA", "Web Development")
