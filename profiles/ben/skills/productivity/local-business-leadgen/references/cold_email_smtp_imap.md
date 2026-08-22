# Cold Email Delivery, Anti-Spam (MailChannels/Hostinger) & IMAP Sync Guide

## Architecture
When dispatching cold B2B emails via custom domain SMTP (e.g. Hostinger Business Email), emails must pass strict spam filters and synchronize with the user's webmail inbox.

## 1. MailChannels & Anti-Spam Bypass
Hostinger and many enterprise hosts route outbound SMTP through MailChannels. If a message triggers suspicion, MailChannels returns `550 5.7.1 [CS] Message blocked`.

### Prevention Checklist:
1. **Multipart/Alternative Structure:** Never send plain HTML alone or bare single-line text. Always attach both `text/plain` and `text/html` parts.
2. **RFC Headers Required:**
   - `Message-ID`: Unique UUID format `<uuid@domain.com>`.
   - `Date`: Formatted with `email.utils.formatdate(localtime=True)`.
   - `X-Mailer`: Clean agent/application identifier.
   - `Reply-To`: Dedicated monitoring inbox.
   - `Subject` & `From`: RFC-encoded using `email.header.Header` and `email.utils.formataddr`.
3. **No Phishing / Test Trigger Words:** Avoid standalone single-word subjects like "test" or empty bodies. Use structured business copy.

## 2. IMAP "Sent" Folder Synchronization
When sending email via raw Python `smtplib.SMTP_SSL`, the message is transmitted directly to the recipient's mail exchanger but is **NOT** automatically recorded in the sender's webmail "Sent" folder.

### IMAP Append Protocol:
- Connect via `imaplib.IMAP4_SSL(imap_host, 993)`.
- Target the correct server folder: on Hostinger / Dovecot, the Sent folder is named **`INBOX.Sent`** (not `Sent`).
- Call `imap.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), raw_message_bytes)`.

## 3. Pacing & Throttling Standards
- **Inter-message delay:** Minimum 300 seconds (5 minutes) between individual outbound dispatches across WhatsApp & Email channels to prevent ISP blacklisting and spam heuristics.
- **Daily Batch Volume:** 20 targeted qualified leads per batch per sender address.

## 4. Standard Business Email Signature Template
Compact HTML signature template with proportional branding logo, job title, phone, email, physical office address, and domain link:

```html
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
```
