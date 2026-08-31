# silpo.ua — worked OTP login + cart example

## Auth topology
- Login host: `https://auth.silpo.ua/login` (Duende IdentityServer, client `silpo--site--spa`, Angular SPA).
- OTP only, SMS to **+380 63 622 22 72** (Stefan; PII — treat as ref, never log plain).
- OAuth redirect: `https://silpo.ua/signin-callback-angular.html?code=...`. Token lives in Angular memory (not localStorage/cookies) → cannot be reused from curl.

## Login endpoint (call from browser_console, not the UI button)
`POST /api/v2/Login/ByPhone?returnUrl=<encoded auth callback URL>`
Body: `{ "Phone": "380636222272" }`  (key is `Phone`, full 12 digits; do NOT use `phoneNumber`)
Response on success → SMS sent. On verify: another endpoint carries the code (capture via fetch hook like the ByPhone one).

## CRITICAL: respect SMS anti-spam
- Re-clicking "Увійти" or re-POSTing rapidly returns `SMSSendingLimit` then `spam detected (code 36058)` and **blocks new codes for minutes**.
- Never re-click on failure. Wait `secondsTillNextOTP` (typically ~8s) before a retry.

## After login — cart rules (Stefan's standing order)
- Delivery: Одеса, Маразліївська вулиця 1/20 (preset in account; pick slot **Понеділок 18:30**).
- Category: «Всі товари» → «Готові страви і кулінарія».
- Culinary items with discount **>20%** (rare in this category):
  - Піца Франческо 500г — **-45%** (99 грн)
  - Млинці із крем-сиром та шинкою 300г — **-25%** (119 грн)
  - Смажена яловича печінка 100г — **-33%** (27.90 грн)
  - Пиріжки смажені з картоплею та грибами 90г — **-22%** (22.46 грн)
  - Пиріжки смажені з тушкованою капустою 90г — **-22%** (22.38 грн)
- MANDATORY block (no fish anywhere): молоко, яйця, сир, глазуровані сирочки (Ферма, від 2 шт = 14.49), балик.
- Cart total **>1700 UAH**.
- STOP before final SMS/ payment confirmation — Stefan completes the order himself.

## Note on cloud vs local
With the default cloud browser, the session died on every navigate and OTP could never be completed. After switching to local Chrome CDP (see SKILL.md), sessions are stable and this flow is viable.
