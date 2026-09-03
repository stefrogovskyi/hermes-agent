# Независимый 4-слойный аудит: SeaRates March 2026 Release Notes — Рерайт vs Оригинал

## (a) ПЛАГИАТ / СХОДСТВО — вердикт: **NEEDS-WORK**

Построчное сравнение выявило **два существенных случая дословного совпадения 7–9 слов подряд** на генерическом (не терминологическом/не именном) материале — это выше порога и не подпадает под исключение для терминов/имён:

1. **Logistics Explorer**, самое серьёзное совпадение:
   - Оригинал: "...search **for** RO-RO freight rates for port-to-port shipments and subscribe **to tariffs of this type**."
   - Рерайт: "...search RO-RO freight rates for port-to-port shipments and subscribe to that tariff type directly."
   - Совпадающая цепочка: **"RO-RO freight rates for port-to-port shipments and subscribe to"** — 9 слов подряд идентичны. Это не имена собственные и не единственно возможная формулировка факта — фраза легко перефразируется, но не была перефразирована.

2. **Booking System**:
   - Оригинал: "We've improved the cost **calculation when adding containers to an existing booking**, along with..."
   - Рерайт: "**Cost calculation when adding containers to an existing booking** has been improved, ..."
   - Совпадающая цепочка: **"calculation when adding containers to an existing booking"** — 7 слов подряд идентичны.

Второстепенные, низкорисковые совпадения (в основном из-за фактических списков/цифр, где перефразировать сложно без потери точности):
- "type, flag, name, and other" (6 слов, список полей данных вокруг vessel database) — вероятно неизбежно.
- "228 shipping lines, leasing companies, and carriers" — совпадение вокруг обязательной точной цифры.
- "on LinkedIn, X, Facebook, and Instagram for" (7 слов) — перечисление названий соцсетей в стандартной формуле CTA, преимущественно proper nouns, низкий риск.

**Итог**: два явных случая (RO-RO фраза, cost calculation фраза) — это не терминология и не имена, а generic English, скопированные почти дословно. Требуется перефразировка.

---

## (b) СЛОВАРНЫЕ AI-МАРКЕРЫ — вердикт: **NEEDS-WORK**

- **Em-dash (—)**: 0 в рерайте (заголовок, meta, тело — везде 0). Для сравнения, в оригинале 1 em-dash ("SeaRates App — now featuring"). Рерайт заменил его на двоеточие. По этому конкретному счётчику — PASS (нет переобилия тире).
- **Клише "dive into"**: обнаружено — "worth a look before **diving into** this one" (вступление).
- **Повтор-филлер "worth a look"** — использовано **дважды**: 
  - "...worth a look before diving into this one" (вступление)
  - "...worth a look if you haven't checked it recently" (Other Updates)
  Повторяющаяся рамочная фраза — признак шаблонного генерирования, а не осознанного авторского приёма.
- **Повтор глагола "picked up"** — дважды: "the Vessel Tracking API picked up sharper detection logic" и "The Quick Request form also picked up a new field" — немотивированное лексическое дублирование.
- **Выдуманная поэтическая вставка во вступлении**, отсутствующая по содержанию в оригинале: "Spring never really announces itself in a browser tab, but somewhere between one release and the next, SeaRates managed to slip a whole batch of upgrades..." — метафорическое обрамление ("spring... browser tab") — классический AI-приём "cinematic hook intro", не подкреплённый фактурой оригинала (оригинал был сухим: "This month, SeaRates continued to evolve through structured improvements and platform enhancements.").
- Классических штампов **не найдено**: "it's important to note", "in today's world", "seamless" (даже убрано из рерайта Mobile App), "unlock", "game-changer", "not just X but Y" — отсутствуют. Это плюс.

**Итог**: нет overused em-dash и нет топ-класса корпоративных клише, но есть повторяющиеся филлер-фразы ("worth a look" x2, "picked up" x2) и необоснованная орнаментальная вставка в интро — типичные лёгкие AI-тики.

---

## (c) СТРУКТУРНЫЕ / РИТОРИЧЕСКИЕ ТИКИ — вердикт: **NEEDS-WORK**

- **Заголовок**: "SeaRates March 2026 Update: **New Tools, New Routes**" — классическая AI-формула "Colon + parallel Noun, Noun" (анафора "New X, New Y"). Узнаваемый шаблон AI-заголовков.
- **Повторяющийся паттерн "тема + двоеточие + триада через запятую"** использован **дважды** почти идентично:
  - Mobile App: "...got an update **worth noticing: chat now runs smoother, maps render in real time, and** Container Tracking... has been reworked..."
  - Other Updates: "Geocoding got attention this round**: the Autocomplete service is sharper, the ZIP code database was refreshed, and** documentation... is clearer..."
  Это шаблонная риторическая конструкция, повторённая в одном коротком тексте — сильный структурный тик.
- **Параллельная рамка "On the X side"** — дважды: "**On the web side**, there's a new landing page..." и "**On the content side**, AirRates and LandRates now each have their own blog..." — зеркальная структура секций.
- **Симметричная антитеза** (past/future pairing): "giving a deeper look at where a given ship **has been** and where it's **headed**" — 1 случай parallel twin-clause antithesis.
- **Explicit connectors ("That's why" / "which is why")**: 0 — PASS.
- **Contrastive negation ("X, not Y" / "instead of")**: 0 явных случаев — в пределах лимита (≤1) — PASS.
- **Афористичные концовки абзацев**: не обнаружены (все секции заканчиваются нейтрально-фактическими предложениями) — PASS.
- Объединение секций оригинала (8 → 6, слиты Vessel Tracking+Ship Schedules и Logistics Explorer+Booking System) само по себе не криминал, но оба новых заголовка используют одинаковый шаблон "X and Y" — минорный признак симметрии.

**Итог**: количественные лимиты по connectors/negation соблюдены, но обнаружены минимум 3 повторяющихся риторических шаблона (colon-triad x2, "On the X side" x2, антитеза past/future) плюс AI-типичный заголовок с параллелизмом — совокупность тянет на NEEDS-WORK.

---

## (d) ФАКТИЧЕСКАЯ ДОСТОВЕРНОСТЬ — вердикт: **NEEDS-WORK (minor, но критично по природе документа)**

Проверены все цифры, имена и заявленные механизмы. Совпадают с оригиналом: 228 (shipping lines/carriers), 447 (airlines), все названия перевозчиков (Pacific Star Express, Eucon, Chenxin Shipping, Global Freight Services), авиакомпания Supernova Airlines, Sidra Line, Turkon by Vessel, Place ID field, дата April 2, 2026, соцсети. Ошибок в цифрах/именах не найдено.

Найдены **2 проблемные точки**:

1. **Выдуманная функциональная деталь (Vessel Tracking Route/Schedule)**:
   - Оригинал: табы "Route" и "Schedule" "provide extended insights into your vessel via the Vessel Tracking app" — без конкретики, что именно показывают табы.
   - Рерайт: "giving a deeper look at **where a given ship has been and where it's headed**" — это конкретное, но НЕ подтверждённое оригиналом функциональное описание (прошлое местоположение vs. будущий маршрут). Это правдоподобная, но домысленная интерпретация названий табов, а не факт из исходника. Для релиз-нот продукта это — added technical claim без источника. **Флаг: изобретённый механизм/описание функции.**

2. **Неподтверждённое допущение о статусе SeaRates Blog**:
   - Оригинал: "we have created Blogs for AirRates and LandRates within our logistics ecosystem, along with the SeaRates Blog" — фраза двусмысленна: неясно, идёт ли речь о вновь созданном/обновлённом SeaRates Blog или об уже существовавшем.
   - Рерайт: "AirRates and LandRates now each have their own blog, **joining the existing SeaRates Blog**" — рерайт однозначно утверждает, что SeaRates Blog уже существовал ("existing"), что не подтверждено оригинальным текстом. **Флаг: разрешение двусмысленности в одну сторону без опоры на источник.**

Мелкие, не критичные усиления (не искажают факт, но добавляют неподтверждённые адъективы): "sharper detection logic" (~"improved"), "with Apple ID login built in **for quick access**", "documentation... **is clearer for anyone integrating**" — стилистические усиления степени, не новые факты, риск низкий.

**Итог**: цифры/имена точны на 100%, но есть один сфабрикованный функциональный домысел (Route/Schedule "past vs future") и одно неподтверждённое фактическое допущение (SeaRates Blog "existing") — для release notes продукта это требует правки перед публикацией.

---

## СВОДНАЯ ТАБЛИЦА

| Слой | Вердикт | Ключевая находка |
|---|---|---|
| (a) Плагиат | NEEDS-WORK | 2 случая дословного совпадения 7–9 слов на generic-фразах (RO-RO фраза, cost calculation фраза) |
| (b) Лексические AI-маркеры | NEEDS-WORK | "worth a look" x2, "picked up" x2, "diving into", выдуманная поэтическая интро-метафора; em-dash=0 (ок) |
| (c) Структурные тики | NEEDS-WORK | colon+triad паттерн x2, "On the X side" x2, антитеза past/future, AI-формула заголовка "New X, New Y"; connectors/negation в норме |
| (d) Фактическая точность | NEEDS-WORK (minor) | Изобретённая деталь функции Route/Schedule; неподтверждённое допущение про "existing" SeaRates Blog; цифры/имена — все верны |

**Общий вывод**: рерайт качественно избегает самых грубых AI-штампов (нет "seamless/unlock/game-changer", нет em-dash-инфляции, connectors/negation в пределах лимитов) и в целом точен по цифрам/именам, но содержит конкретные, легко исправимые проблемы: два фрагмента почти-дословного копирования generic-фраз (требуют перефразировки), повторяющиеся шаблонные риторические конструкции (colon-triad x2, "On the X side" x2), пару филлер-повторов, и — важнее всего для release notes — один domysел о функциональности продукта и одно неподтверждённое допущение о статусе блога, которые нужно либо убрать, либо сверить с продуктовой командой перед публикацией.
