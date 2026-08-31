# AI Project Evaluation, 10-Point Graduation & Monobank Acquiring Reference

This reference documents the complete user flow, technical architecture, and Monobank Acquiring setup for the Avalanche AI project estimation engine.

## 1. Hero Input & Enter Key Submission Handler
The `Describe your project` textarea on the hero screen (`index.html`) captures the user's project description and redirects to the evaluation page:
- Triggers on button click or keyboard `Enter` press (`onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); handleHeroProjectSubmit(); }"`).
- Stores the input text string into `localStorage.setItem('hero_project_desc', val)`.
- Preserves the visitor's current site language on redirect (e.g. `/uk/` ➔ `/uk/evaluation`, `/es/` ➔ `/es/evaluation`).

## 2. Real AI Complexity Analyzer & 10-Point Graduation Algorithm
The evaluation engine analyzes the input text for length, detail, and technical keywords:
- **1 Point ($9 Setup + $5/mo):** Simple single-purpose bot or reminder ("записывать и слать мне напоминания").
- **2 Points ($19 Setup + $10/mo):** Multi-function assistant / note keeper / password vault ("со мной общаться, помогать и хранить все мои пароли и заметки").
- **3-5 Points ($29-$49 Setup + $15-$25/mo):** Scraper, database integration, custom CRM/ERP workflow.
- **6-9 Points ($59-$89 Setup + $30-$45/mo):** Multi-tenant SaaS, vector database, RAG pipeline, fine-tuning.
- **10 Points ($99 Setup + $50/mo):** Intergalactic superproject / universal management system ("межгалактический суперпроект по управлению Вселенной").

Formula:
`oneTimeUsd = (points * 10) - 1;`
`monthlyUsd = points * 5;`

Client NEVER sees the point score, ONLY sees the calculated price in USD and local currency approximation.

## 3. Dynamic IP-Based Currency Detection
Queries `https://ipapi.co/json/` on page load:
- **Ukraine (`UA`):** Displays local equivalent in UAH (`~ 789 UAH`).
- **Eurozone (`DE`, `FR`, `ES`, `IT`, etc.):** Displays local equivalent in EUR (`~ €17.48 EUR`).
- **United Kingdom (`GB`):** Displays local equivalent in GBP (`~ £15.01 GBP`).
- **USA & Others:** Displays USD (`$19.00 USD`).

## 4. Monobank Acquiring Setup Requirements (ФОП)
To connect live Monobank Acquiring for Stefan's FOP:
1. **`X-Token` (Merchant API Token):**
   - Obtain from Monobank Web Cabinet `https://web.monobank.ua` or Monobank Mobile App ➔ *Монобанк для ФОП ➔ Еквайринг ➔ API Токен*.
2. **Merchant ID:**
   - Account identifier in Monobank Acquiring cabinet.
3. **Webhook Endpoint:**
   - `https://dev.domain.com/mono_webhook.php` for processing real-time payment status callbacks (`success` / `failure`).

## 5. Multilingual Dual Email Notifications (`send_mail.php`) & Hostinger Sendmail Line Endings
- **Hostinger Linux Sendmail Line-Ending Rule:** On Hostinger PHP mailers, email headers MUST use `\n` (LF) line endings, NOT `\r\n` (CRLF). Header strings formatted with `\r\n` cause Hostinger sendmail to reject the headers and return `false`. Header strings formatted with `\n` return `true` and deliver reliably.
- **Active Sender Domain:** Sender address MUST be an active registered mailbox on Hostinger (`From: info@aavalanche.com`), not an unconfigured alias like `noreply@`.
- **Client Email:** Dispatched in the client's current site language (`en`, `es`, `de`, `fr`, `it`, `uk`, `ru`, `zh`, `ar`) with Order `#ORD-XXXX`, price breakdown, and 48-hour delivery timeline.
- **Admin Email (`dr.reenforce@gmail.com`):** Branded HTML notification with Subject `[PAID / NEW ORDER] #ORD-XXXX (<LANG>)` and client details.
- **Inline Contact Form Green Feedback Banner:** Contact form (`contact.html`) replaces browser `alert()` popups with a clean, inline green feedback banner (`✓ Ваше повідомлення успішно надіслано!`) in the client's native language.
- **User Cabinet Recording:** Automatically records the order into `orders` table in `database.sqlite` for display under **My Orders ("Мои заказы")** in `dashboard.html`.

## 6. Persistent Auth Session Across Language Subfolders
- **Session Cookie Path:** Configure `ini_set('session.cookie_path', '/')` and `session_set_cookie_params(['path' => '/', 'samesite' => 'Lax'])` before calling `session_start()` in `auth.php`. This guarantees the `PHPSESSID` cookie is preserved when users navigate across language subfolders (`/uk/`, `/es/`, `/de/`, etc.).
