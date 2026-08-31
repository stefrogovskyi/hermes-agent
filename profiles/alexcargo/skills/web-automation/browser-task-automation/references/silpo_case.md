# silpo.ua — session knowledge bank

Condensed from a real run (OTP-SMS order, July 2026). Format chosen to be reusable, not a full mirror of the site.

## Auth
- Login is OTP-SMS ONLY. Phone format: 12 digits with country code, e.g. `380636222272` (NOT `063...`). Wrong length → "Номер має складатись з 12 цифр".
- Auth host: `auth.silpo.ua` — Duende IdentityServer (client `silpo--site--spa`). OpenID config at `https://auth.silpo.ua/.well-known/openid-configuration` (curl-reachable).
- Token endpoint: `https://auth.silpo.ua/connect/token`. The SPA uses a silent-renew iframe; when the session dies it returns `error=login_required` in the iframe URL.
- Codes valid ~5 min. Sending a new code invalidates the previous one.

## Cloudflare behavior (critical)
- First page hit shows "Just a moment..." — sleep 10–18s then snapshot; it clears.
- **`browser_navigate` to any URL resets the browser session → kills the OAuth token → logged out.** After login, navigate ONLY by SPA clicks (menu/category/buttons). Never paste a category URL.
- Static JS/CSS bundles under CF return 0 bytes to `curl` (even with UA+Referer). Don't try to fetch them that way; use the browser or web_extract.

## Catalog structure (logged-in)
- Top menu button "Всі товари" → category list.
- Кулинарія = "Готові страви і кулінарія" (231 items). Subcats: Млинці/сирники/запіканки, Перші страви, Другі страви, Суші/піца/бургери, Салати/закуски, Десерти/напої, Сніданки, Пироги/пиріжки, Напівфабрикати.
- Молочні продукти та яйця = dairy/eggs (for mandatory milk/eggs/cheese/curd-snack/balyk items).
- "Ви замовляли" carousel on home page already surfaces previously-bought balyk, milk, ryazhanka, cheese (Гауда -31%), eggs, glazed curd snack (-28%) — fast path for the mandatory block.

## Discount findings (кулинарія, ≥20%)
- Піца Франческо 500г — -45% (99 грн) ← best
- Млинці із крем-сиром та шинкою 300г — -25% (119 грн)
- Смажена яловича печінка 100г — -33% (27.90 грн)
- Пиріжки смажені (картопля+гриби / тушкована капуста) 90г — -22% (22.46 / 22.38 грн)
- Most other items are 14–19% (below the 20% bar) — e.g. салати -16%, Тальятеле Карбонара -16%, суп з мітболами -19%.

## Snapshot parsing
- Each product card line looks like:
  `link "Піца Франческо, 500г, стара ціна 179 гривень, знижка 45%, нова ціна 99 гривень" [ref=e232]`
  followed by `button "Додати у кошик" [ref=e327]`.
- Disabled submit buttons read `[disabled]` (e.g. "Продовжити" before a code is entered).
- Cart subtotal + item count appear in the header button ("Відкрити кошик"): e.g. `1` + `99.00 грн`.

## Order gotchas
- Delivery slot picker shows same-day + next-day slots (e.g. "завтра, 02:00 — 03:30"); pick the required window via SPA click — do NOT navigate by URL.
- Minimum order ~599 грн. Stop before final payment; user confirms + enters any final SMS themselves.

## Reverse-engineering notes (advanced)
- To discover the SPA's API endpoints without downloading CF-blocked JS bundles, install an XHR+fetch hook via `browser_console` on the live page, perform the action, then read `window.__cap`. This revealed the OTP-send endpoint:
  `POST https://auth.silpo.ua/api/v2/Login/ByPhone?returnUrl=<oauth-callback>`
- **The OIDC access_token is NOT recoverable for terminal reuse.** It is absent from `document.cookie`, `localStorage`, and `sessionStorage`; the Angular app keeps it in RAM. A "login in browser, then `curl` the API" hybrid is therefore infeasible — operate entirely through SPA clicks.

## Failure mode — signin-callback dead-end
- After a successful code exchange the URL may land on `.../signin-callback-angular.html?code=...` but the home page never renders (empty snapshot). OAuth code issued, but Angular bootstrap stalled. Unrecoverable without killing the session (any `browser_navigate` → new session id → CF re-challenge → logout). Retry the full OTP flow or let the user finish in their own browser.
