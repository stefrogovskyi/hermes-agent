# Inbound Triage, Verbatim Draft Approval, and Weekly Team Testimonials

## 1. Verbatim Draft Approval Rule
When presenting inbound message alerts (Email or WhatsApp) to Stefan:
- The alert card displays the sender info, original message, Russian translation, and Richard's proposed draft response.
- **Single Confirmation Rule**: When Stefan confirms with "Да", "Отправляй", or "OK", dispatch **strictly and verbatim the exact text shown in the draft card**.
- **No Unilateral Rewrites**: Never unilaterally change language (e.g., from English to Russian or vice versa) or substitute draft wording during the approval send turn.

## 2. Silent Watchdog Rule (no_agent: true)
For cron jobs running scripts directly without agent reasoning (`no_agent: true`, `deliver: origin`):
- When no new inbound events/messages exist, the script MUST produce **zero stdout** (empty output, exit 0).
- Printing status messages like "No new events" or "Nothing found" causes the Hermes scheduler to treat non-empty stdout as an active notification and deliver it to Telegram.
- Only print output when there is an actual client message requiring user attention.

## 3. Full Untruncated Email Ingestion (MS Graph API)
- Do NOT use `bodyPreview` from MS Graph API (which truncates at ~255 characters).
- Fetch `body.content` (HTML/Text) and parse clean text with BeautifulSoup.
- Strip quoted history (`From: ...`, `-----Original Message-----`, `EXTERNAL EMAIL`, `DISCLAIMER:`).
- Always include:
  1. Full original client message.
  2. Complete Russian translation of the client message.
  3. Richard's prepared response draft (in client's language).
  4. Complete Russian translation of Richard's response draft.

## 4. Weekly Sales Team Testimonial Reminder Loop
- **Schedule**: Every Monday at 08:00 Kyiv (`0 5 * * 1` UTC).
- **Recipients (Individual Personalized Sends)**:
  * Алёна (`alyona.holubova@navo24.com`)
  * Екатерина (`ekaterina.kapustian@navo24.com`)
  * Лилия (`lilia.k@navo24.com`)
  * Никита (`nikita@navo24.com`)
  * Олег (`oleg.chervinskyi@navo24.com`)
- **Headers**:
  * From: `Richard Marlowe <rich@e.navo24.com>`
  * CC: `Stefan Rogovskiy <stefan@navo24.com>`, `Alexei Shatunov <lxxmng@navo24.com>`
  * Reply-To: `sales@navo24.com`
- **Personalization**: Address each member by their first name (`Доброе утро, [Имя]! 🚀`).
- **Dynamic Content**: Rotates 1 inspiring quote and 3 randomized triggers from the 18+ navo24.com product/service categories.
