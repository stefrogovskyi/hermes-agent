# Независимый 4-слойный аудит рерайта (Sea Freight Booking System)

## (a) ПЛАГИАТ / СХОДСТВО — ВЕРДИКТ: **NEEDS-WORK**

Обнаружено **~28 отдельных совпадений 6+ слов подряд**, из них минимум **7 фрагментов длиной 10–22 слова подряд** и **4 практически полностью скопированных пассажа**. Это далеко за пределами "устоявшихся терминов".

Полностью идентичные предложения (не парафраз вообще):
- Ориг/рерайт (100% идентично, 15 слов): `"Click the "+" button at the top of the dashboard to add a new booking."`
- Ориг/рерайт (100% идентично, FAQ Q1, ~35 слов): `"A sea freight booking management system is a logistics platform that helps freight forwarders and logistics companies organize bookings, shipment tracking, documentation, financial information, and operational communication in one workspace."`
- FAQ Q3 — идентично кроме одного вставленного слова "other": ориг `"...supports integration with CRM, ERP, TMS, and internal logistics systems."` vs рерайт `"...supports integration with CRM, ERP, TMS, and other internal logistics systems."`
- FAQ Q2 — идентично кроме "allows...to manage"→"lets...manage": весь остальной текст (~30 слов) не изменён.
- FAQ Q4 — идентичный вопрос + 22 слова подряд идентичны после замены "reduce"→"cut down on": `"...fragmented communication, manual shipment updates, spreadsheet-based coordination, and disconnected operational workflows by centralizing booking activities, shipment visibility, and operational communication."`

Крупные почти-verbatim блоки (не термины, а куски прозы):
- Интро: ориг `"...is to keep shipment timelines, tracking events, shipping instructions, documents, freight charges, and booking communication inside one operational workspace."` vs рерайт — та же фраза дословно (24 слова), изменено только начало ("effective way"→"workable fix").
- Второй абзац интро: ориг `"Instead of switching between emails, spreadsheets, messengers, and separate shipment tools, freight forwarders and logistics providers can manage the entire sea freight booking workflow, from booking creation to tracking milestones, finance, and payment status..."` — 30+ слов совпадают почти дословно (manage→run, to→through — единственные правки).
- `"The Booking System by SeaRates is a freight booking management platform designed/built for logistics companies, freight forwarders, and sea freight operators."` — 21 слово, только "designed"→"built".
- Шаг 1: ориг `"Log in to SeaRates account in Virtual Office and open the Bookings section from the left-side menu."` vs рерайт — идентично, добавлено только "your" (14 слов подряд без изменений).
- Rate comparison: ориг `"...verify operational pricing, compare shipment conditions, review original tariff structures, and control rate consistency."` vs рерайт `"...check operational pricing, compare shipment conditions, review original tariff structures, and control rate consistency."` — 14 слов подряд идентичны (только verify→check).
- Payment-блок: `"payment type, invoice name, booking amount, payment validity, payment dates, [and] payment activity status"` — 10+ слов списком идентичны дословно.
- Cargo particulars: `"container numbers, seal numbers, package type, package quantity, cargo weight, cargo volume, IMO class, [and] cargo description"` — 14 слов подряд идентичны (это список полей формы, не отраслевой термин целиком).
- Финал: `"bookings, shipment events, freight charges, shipping instructions, customer coordination, and operational tracking"` — 11 слов идентичны; и `"...shipment operations, booking visibility, documentation workflows, and operational communication"` — 9 слов идентичны.

Плюс десятки более коротких (6–9 слов) совпадений по всему тексту (Step 4 timeline, Step 5 tracking tab, Step 6 documents intro-предложение целиком идентично, Step 7 finance calculation, white-label role list и т.д.) — рерайтер систематически менял 1–2 слова в предложении, оставляя остальную структуру и лексику нетронутой. Это не пересказ, а поверхностный synonym-swap на большей части текста, особенно в списках полей и в FAQ.

## (b) СЛОВАРНЫЕ AI-МАРКЕРЫ — ВЕРДИКТ: **PASS**

**Em-dash (—) счётчик:**
- Title: 0
- Meta-title: 0
- Meta-description: 0
- Body: 0
- **Итого: 0** во всей статье.

**AI-клише из списка** ("important to note", "in today's world", "seamless", "unlock", "delve", "unique blend", "not just X but Y", "in conclusion") — **0 вхождений** ни одного из этих выражений найдено не было.

Примечание (не нарушение списка, но стилистически близко к filler-тику, зафиксировано для слоя c):
- Интро-хук: `"Sea freight booking rarely dies from one big problem. It dies from a dozen small ones..."` — драматизированный "listicle-style" зачин.
- Аутро-CTA: `"...worth a look if the current setup still runs on too many open tabs."` — разговорный closer.
Формально это не входит в заданный список маркеров → слой (b) **PASS**.

## (c) СТРУКТУРНЫЕ/РИТОРИЧЕСКИЕ ТИКИ — ВЕРДИКТ: **NEEDS-WORK**

**Порядок разделов:** what it is → who uses it → how-to (степ-бай-степ) → rate comparison → white-label/API → FAQ → итог. Эта "лестница" **унаследована из оригинала** (у него ровно та же последовательность разделов), рерайтер её не создавал заново — по этому пункту претензий к рерайту как таковому нет.

**Explicit connectors** ("That's why" / "Which is why" / "That's a sign of"): **0 буквальных совпадений**. Но обнаружен близкий по духу паттерн причинно-следственного нанизывания, сконцентрированный в разделе "Who uses" — практически каждый абзац построен как "бутылочное горлышко → so/что приводит к решению":
- `"...so pulling booking coordination, shipment milestones, and customer messages into a single workspace changes their daily grind considerably."`
- `"...something a structured booking timeline and route-based tracking is built to handle."`
- `"...so route-based tracking and milestone management across transport stages matters more to them..."`
- `"...so it's worth getting familiar with how requests and proposals work there..."`
- `"...so the booking workflow runs alongside whatever software already runs the business."`
≈ **6-7 причинно-следственных конструкций** такого рода — избыточная плотность для одного раздела.

**Contrastive negation** ("X, not Y" / "instead of" / "rather than"): найдено **2 конструкции**:
1. `"Instead of switching between emails, spreadsheets, messengers..."` (унаследовано из оригинала).
2. `"For companies after automation rather than a branded front end..."` (новое, добавлено рерайтером).
**Правило: максимум 1 на статью → превышено (2), ФЛАГ.**

**Абзацы, заканчивающиеся афористичным one-liner'ом:** найдено **2 чётких случая**:
- Step 4: `"Nobody needs a side spreadsheet to track where a shipment stands anymore. That visibility sits right inside the workflow."`
- Финал статьи: `"...worth a look if the current setup still runs on too many open tabs."`
(плюс 1 пограничный: `"...keep the booking lifecycle manageable without a pile of extra tools."`)

**Parallel twin-sentence conclusions** (два зеркальных предложения подряд в конце раздела): найден **1 явный случай**:
- Step 4: `"Nobody needs a side spreadsheet to track where a shipment stands anymore."` + `"That visibility sits right inside the workflow."` — короткие зеркальные subject-verb-object конструкции, вторая эхом повторяет "visibility" из первой.

**Symmetric antithesis pairs** (парные противоположности без "not"): найдено **2 случая**:
- `"Manual booking workflows spread these pieces across whatever tool happened to be open..."` vs `"The Booking System pulls shipment operations together..."` — spread/scatter ↔ pull together (новое, добавлено рерайтером, в оригинале просто "centralizes").
- `"...companies after automation rather than a branded front end"` — automation ↔ branded front end.

Итог по (c): превышение лимита contrastive negation (2 вместо 1), концентрированное причинно-следственное нанизывание в одном разделе, twin-sentence conclusion и antithesis-конструкции — **NEEDS-WORK**.

## (d) ФАКТИЧЕСКАЯ ДОСТОВЕРНОСТЬ — ВЕРДИКТ: **NEEDS-WORK** (критично)

Найдено **7 отдельных случаев** добавленных оценочных/сравнительных/количественных утверждений, не прослеживаемых к оригиналу:

1. **Фабрикованное ранжирование (самое серьёзное).** Оригинал (Shipment coordinators): `"improves = enables route-based tracking and milestone management across transport stages"` — нейтральное описание. Рерайт: `"...route-based tracking and milestone management across transport stages matters more to them than almost anyone else on this list."` — сравнение важности фичи между ролями **полностью выдумано**, в оригинале нет никакого ранжирования между сегментами клиентов.

2. **Фабрикованная оценка магнитуды эффекта.** Оригинал (Freight forwarders): `"improves = centralizes booking coordination, shipment milestones, and customer communication in one workspace"`. Рерайт: `"...changes their daily grind considerably."` — субъективная оценка степени изменений ("considerably", "daily grind") отсутствует в оригинале, придумана рерайтером.

3. **Фабрикованная сравнительная рамка.** Оригинал (Logistics providers) не содержит сопоставления с другими ролями. Рерайт: `"Logistics providers run into a related but different problem..."` — вводит несуществующую в оригинале связь/сравнение с предыдущим пунктом (freight forwarders).

4. **Фабрикованная количественная оценка.** Оригинал (Sea freight carriers): `"bottleneck = manual coordination of shipment updates and booking confirmations"`. Рерайт: `"Sea freight carriers spend a lot of time on manual coordination... cuts down on that back-and-forth."` — "spend a lot of time" и "back-and-forth" — не подтверждённая оригиналом количественная/интенсивностная оценка.

5. **Фабрикованная специфика и квантификация.** Оригинал (Export/import teams): `"bottleneck = delays in shipping instructions and document approvals"`. Рерайт: `"...that get stuck somewhere between departments... removes a good chunk of that waiting."` — "between departments" и "a good chunk" не упомянуты и не выводятся напрямую из оригинала.

6. **Выдуманная деталь механизма/инструмента.** Рерайт вводит новый вымышленный вводный сценарий: `"Picture a freight forwarder juggling inboxes, spreadsheets, and a carrier portal just to find out where one container actually is."` — оригинал упоминает "carrier communication", но не "carrier portal" как отдельный инструмент; это придуманная конкретика, которой нет в источнике.

7. **Полностью вымышленная вступительная метафора/примеры.** Рерайт: `"Sea freight booking rarely dies from one big problem. It dies from a dozen small ones: a status update buried in an email thread, a document waiting in someone's downloads folder, a rate quote sitting in a chat nobody opened yet."` — у оригинала нет ничего похожего на эту метафору или на конкретные иллюстративные примеры ("downloads folder", "chat nobody opened yet"). Это полностью придуманный нарративный слой, представленный как будто он что-то констатирует.

Прямая проверка по инструкции задачи — раздел "Who uses booking management systems": фразы `"changes their daily grind considerably"` (freight forwarders) и `"matters more to them than almost anyone else on this list"` (shipment coordinators) **подтверждены как выдуманные** — в оригинале нет никакой оценки степени влияния и никакого сравнения важности фичи между разными типами пользователей.

---

## Итоговая таблица

| Слой | Вердикт | Ключевые числа |
|---|---|---|
| (a) Плагиат/сходство | **NEEDS-WORK** | ~28 совпадений 6+ слов, 7 фрагментов на 10–22 слова, 4 почти/полностью скопированных пассажа (включая FAQ Q1 100% идентичен) |
| (b) Словарные AI-маркеры | **PASS** | em-dash: 0/0/0/0 (title/meta-title/meta-desc/body); клише из списка: 0 совпадений |
| (c) Структурные/риторические тики | **NEEDS-WORK** | contrastive negation: 2 (лимит 1); causal-стек: ~6-7 в разделе Who uses; one-liner концовки: 2; twin-sentence: 1; antithesis pairs: 2 |
| (d) Фактическая достоверность | **NEEDS-WORK** | 7 фабрикованных оценочных/сравнительных/количественных вставок, включая прямо указанные в задании "changes their daily grind considerably" и "matters more to them than almost anyone else on this list" |
