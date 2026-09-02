# Corporate Email Signature, Outreach Pacing & Lead List Hygiene Standards

Standardized email formatting, signature styling, anti-spam pacing, and bounce auto-pruning rules based on proven production deployments.

## 1. Clean Non-Tabular & Fluid Email Signature Architecture
Never use nested `<table>/<tr>/<td>` structures with arbitrary cell paddings or horizontal lines (`<hr>`). Avoid narrow fixed container widths (`width: 150px` on the outer wrapper) that force long text strings (slogans, physical addresses, email links) to wrap awkwardly across multiple lines.

### Standard Fluid Template (170px Fixed Logo with Natural Text Flow & Zero Gap)
```html
<div style="font-family: Tahoma, Geneva, sans-serif; font-size: 10pt; color: #000000; line-height: 1.25; margin-top: 18px;">
  <b>[Sender Full Name]</b><br>
  [Position / Title]<br>
  <a href="[Company URL]" target="_blank" style="text-decoration: none; display: inline-block; margin: 2px 0 0 0; padding: 0;">
    <img src="[Logo URL / bit.ly]" alt="[Company Name]" width="170" style="display: block; border: 0; width: 170px; max-width: 170px; height: auto; margin: 0; padding: 0;" />
  </a><br>
  [Slogan / Value Proposition]<br>
  <a href="tel:[Phone Clean]" style="color: #000000; text-decoration: none;">[Phone Display]</a><br>
  <a href="mailto:[Email]" style="color: #0000FF !important; text-decoration: underline !important;">[Email]</a><br>
  <a href="javascript:void(0)" style="color: #000000 !important; text-decoration: none !important; cursor: default !important; pointer-events: none !important;">[Street Number] [Street Name], [Ste/Apt]</a><br>
  <a href="javascript:void(0)" style="color: #000000 !important; text-decoration: none !important; cursor: default !important; pointer-events: none !important;">[City], [State] [ZIP], [Country]</a><br>
  <a href="[Company URL]" target="_blank" style="color: #0000FF !important; text-decoration: underline !important;">[Domain Display]</a>
</div>
```

### Signature Styling Rules
- **Fluid Container**: Let the container width flow naturally without rigid outer `max-width: 150px` / `170px` constraints so long text lines don't break prematurely.
- **Zero Vertical Gap Before Slogan**: Do NOT wrap the logo image in a block `<div>` with margins, as email renderers (Gmail, Apple Mail) create an unwanted empty paragraph before the slogan line. Use `<a style="display: inline-block; margin: 2px 0 0 0; padding: 0;"><img ... margin: 0; padding: 0;" /></a><br>` instead.
- **Prevent Automatic Google Maps & Apple Address Linking**: Gmail and Apple Mail automatically parse US/international addresses and wrap them in unwanted blue underlined map links. 
  * The most reliable technique is wrapping address lines in an inactive anchor `<a href="javascript:void(0)" style="color: #000000 !important; text-decoration: none !important; cursor: default !important; pointer-events: none !important;">...</a>`. Because HTML and Gmail sanitizers strictly disallow nested `<a>` elements, Gmail's post-processing script completely skips the address without attaching a Google Maps link.
  * Keep real links (`mailto:` and website URL) explicitly styled with `color: #0000FF !important; text-decoration: underline !important;` so they remain bright blue and clickable.
- **Explicit Image Dimensions**: Always include the HTML `width="170"` attribute AND inline CSS `width: 170px; max-width: 170px; height: auto; display: block; border: 0;` to prevent email clients (Gmail, Apple Mail, Outlook) from mis-scaling or distorting the logo.
- **Typography**: `font-family: Tahoma, Geneva, sans-serif; font-size: 10pt; color: #000000; line-height: 1.3;`.
- **Links**: Always `#0000FF` with `text-decoration: underline;`.
- **Phone Numbers**: Plain black `#000000` with `text-decoration: none;` and `tel:` href.
- **Address Breakdown**: Separate physical street address and City/State/Country into clean `<br>`-separated lines.
- **Logo Images**: Hosted on persistent CDN or shortened links (`bit.ly`).

## 2. Text Formatting & Human Communication Standards
- **Zero Code Calque & No Literal `\n`**: Never expose raw escape sequences (`\n`, `\t`, `\r`), JSON literals, or programmer syntax in client emails, drafts, or user messages.
- **Text Normalization Filter**: When building email dispatchers in Python, automatically normalize raw input strings before constructing MIME parts:
  ```python
  def clean_text(text: str) -> str:
      if not text:
          return ""
      return text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\t", " ")
  ```
- **Natural Paragraph Rendering**: Split text by double newlines into clean HTML paragraphs (`<p style="margin: 0 0 14px 0; font-family: Tahoma, Geneva, sans-serif; font-size: 10pt; color: #000000; line-height: 1.5;">...</p>`).

## 3. IMAP Drafts Management (Hostinger / Standard IMAP)
When composing and updating drafts in `INBOX.Drafts`:
```python
import imaplib
import time

mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(user, password)
mail.select("INBOX.Drafts")

# Clear stale drafts before saving replacement
status, msgs = mail.search(None, "ALL")
for num in msgs[0].split():
    mail.store(num, "+FLAGS", "\\Deleted")
mail.expunge()

# Append new draft with Draft and Seen flags
mail.append(
    "INBOX.Drafts",
    r"(\Draft \Seen)",
    imaplib.Time2Internaldate(time.time()),
    raw_message_bytes
)
mail.logout()
```

## 4. Cold Outreach Pacing & Dynamic Combinatorial Personalization
When running cold email campaigns:
1. **Dynamic Combinatorial Personalization**: Every single email MUST have a unique subject line and a unique body structure (no two identical emails). Combine dynamic templates with lead-specific parameters (company name, contact person, country/port of destination, exact commodity requirements).
2. **Anti-Spam Pacing**: Space sequential SMTP dispatches with randomized delays (`12–25 seconds` per email) to avoid IP throttling, greylisting, or burst detection.

## 5. Bounce Detection, NDR Parsing & Lead List Auto-Pruning Hygiene
When monitoring incoming responses via IMAP:
1. **Detect Bounce / NDR Notifications**:
   - Filter senders matching `mailer-daemon`, `postmaster`, `delivery status`, `mail delivery`.
   - Filter subjects matching `undelivered`, `delivery failure`, `failure notice`, `returned mail`, `550 User not found`.
2. **Extract Failed Recipient Email**:
   - Parse `Final-Recipient: rfc822; <email>` or regex-extract emails associated with 550 / 554 rejection codes.
3. **Auto-Delete Dead Leads from Tracker**:
   - Do not merely flag dead emails: **physically delete/prune the dead row from the tracker** so the master list contains only 100% reachable, alive prospects.
   - Re-index sequence IDs (`df['ID'] = range(1, len(df) + 1)`).
   - Sync cleanly to Google Sheets by issuing `spreadsheets().values().clear()` followed by `spreadsheets().values().update()` to wipe leftover trailing rows.
