# Независимый аудит рерайта: "One Tracking System for Sea, Air, Rail, Road, and Parcel Shipments"

## (a) Плагиат / текстовое сходство — ВЕРДИКТ: NEEDS-WORK

Найдено 6 случаев дословного совпадения 6+ слов подряд, не относящихся к разрешённым терминам/именам:

1. **7 слов**: ориг. "port milestones (loaded, departed, arrived, discharged)" → рерайт "the standard **port milestones (loaded, departed, arrived, discharged)**" — список скопирован целиком.
2. **6 слов**: ориг. "445+ airlines and air cargo carriers worldwide supported" → рерайт "**445+ airlines and air cargo carriers** feed into the air side" — числовой факт + описание сущности скопированы дословно.
3. **9 слов**: ориг. "Hundreds of road carriers and fleet data sources are supported" → рерайт "**Hundreds of road carriers and fleet data sources are** connected" — почти дословная копия, изменено только последнее слово.
4. **7 слов**: ориг. "2,400+ global courier and parcel delivery companies supported" → рерайт "**2,400+ global courier and parcel delivery companies** are supported here" — дословный перенос.
5. **7 слов**: ориг. "aggregated from global courier APIs and postal networks, covering both major carriers" → рерайт "aggregated from **courier APIs and postal networks, covering both** the big international names" — почти сплошная копия середины предложения.
6. **8 слов**: ориг. "shippers, traders, freight forwarders, 3PL, and logistics companies shipping regularly" → рерайт "**Shippers, traders, freight forwarders, 3PLs, and logistics companies** moving cargo on a regular basis" — список аудитории скопирован почти целиком (FAQ, последний вопрос).

Дополнительно, параграф про "Shipment cards" (Step 4) — список полей ("route history, logistics events... completed and upcoming milestones... exceptions, transport unit['s] details... visualized route[s]... on the [world] map") воспроизводит перечень оригинала пункт-в-пункт с минимальными косметическими заменами (statuses→Status, carriers' information→carrier details, transport unit's details→transport unit info) — формально нет непрерывного 6-словного совпадения из-за пунктуации, но по сути это переупорядоченная калька, а не независимый пересказ.

Несколько погранично близких (5-словных, не дотягивающих до порога) совпадений: "international and regional rail operators [and/plus]", "delivery milestones [and/,] current cargo location", "transshipment points and courier handovers", "varies by transport mode".

Повторяющееся использование "sea, air, rail, road, and parcel" (6 слов) встречается многократно — это базовая таксономия статьи (аналог разрешённых терминов), низкий риск, но формально тоже попадает под правило.

**Итог:** 6 явных совпадений ≥6 слов вне списка исключений — рерайт недостаточно перефразирован в ряде технических абзацев (особенно все "You get:" статистические врезки и FAQ последний ответ).

## (b) Словарные AI-маркеры — ВЕРДИКТ: PASS

- Em-dash "—" или "--": **0 вхождений** — не найдено ни одного в тексте рерайта (проверено построчно).
- Клише из списка ("important to note", "dive into", "to sum up", "in today's world", "seamless", "unlock", "robust"): **0 вхождений**. Заголовок "To sum up" заменён на "What changes here" — клише-заголовок устранён.
- Пустое вступление/заключение классического AI-типа ("In today's fast-paced world of logistics...") — отсутствует; вступление сюжетное (сцена с пятью вкладками браузера).

Второстепенные (не входят в явный список, но похожи по духу): риторический вопрос "Where does that data come from?" и филлер "Here's what's on offer." — лёгкие разговорные тики вовлечения, не формальное нарушение по заданным критериям.

## (c) Структурные / риторические тики — ВЕРДИКТ: NEEDS-WORK

- **Explicit connectors** ("that's why" / "which is why"): **0 вхождений** — чисто.
- **Contrastive negation "X, not Y" / "instead of X"**: **4 вхождения**:
  1. "built around how that specific transport mode operates, **not** some generic 'shipment status' wrapper slapped on top"
  2. "watch what's moving **instead of** chasing it across the internet"
  3. "pulling all transport modes and carriers into one system **beats** tracking fragmented statuses one carrier at a time" (антитеза, парафраз оригинального "instead of tracking fragmented... a single... system is necessary")
  4. "SeaRates aggregates all of that **into one place instead**" (FAQ, последний вопрос)
- **Аффористичные концовки абзацев** (хлёсткий однострочник в конце абзаца): **~5 из 21 абзаца (~24%)**:
  1. Конец вступления: "...so ops teams can actually watch what's moving instead of chasing it across the internet."
  2. "...which is a small thing but saves a step most people don't expect to skip." (Container Tracking)
  3. "...which matters when you're not sure who's handling the last mile." (Parcel Tracking)
  4. "...multitracking across dozens of shipments doesn't turn into a mess of open tabs." (Step 4) — сильная перекличка (callback) со вступлением ("five browser tabs") — классический приём кольцевой композиции.
  5. "...carrier statuses scattered across as many systems as there are carriers involved in a shipment." (заключение, погранично)
- **Parallel twin-sentence / симметричная антитеза**: **3–4 вхождения**:
  1. "A container doesn't move like a parcel, and a wagon crossing a border doesn't report the same way a truck does." (симметричная негативная параллель)
  2. "That's **not** new. **What's changed** is how fragmented getting that visibility has become..." — классическая парная короткая конструкция.
  3. "pulling all transport modes... into one system beats tracking fragmented statuses one carrier at a time" (антитеза "one system" vs "one carrier at a time")
  4. "so the picture you get reflects both the paperwork and where the truck physically is" (симметричная пара "both X and Y")
- **Структура-лестница** (why-what-how-adoption-bonus-trend-checklist): рерайт следует структуре **why → what (5 типов) → what×5 (по каждому виду) → how (шаги) → why-итог → FAQ-checklist**, что почти зеркально повторяет структуру оригинала (унаследовано из источника, а не добавлено рерайтером). Отдельных секций "adoption/bonus/trend" нет — учебная лестница присутствует частично, но не в чистом "искусственном" виде.

**Итог:** connectors отсутствуют, но плотность контрастной негации (4), афористичных концовок (5, включая нарочитый callback "tabs"↔"tabs") и симметричных антитез (3-4) достаточно высока и системна, чтобы считать это узнаваемым риторическим тиком, а не случайностью.

## (d) Фактическая достоверность — ВЕРДИКТ: NEEDS-WORK

**Цифры — все совпадают точно (PASS по числам):**
- 220+ carriers ✓ (ориг.: "220+ global and regional ocean carriers, shipping lines, and leasing companies")
- 445+ airlines ✓ (точное совпадение)
- 2,400+ couriers ✓ (точное совпадение)
- 5 tracking types / modes ✓ (точное совпадение)
- "Hundreds of road carriers" ✓ (точное совпадение)

**Найденные придуманные факты/механизмы/цифры, не прослеживаемые до оригинала:**

1. **"...a shipment might cross three or four borders before it reaches a terminal"** (Rail-секция) — конкретное число границ придумано, в оригинале только "especially for long-distance and Eurasian routes" без каких-либо цифр про границы. **Явная фабрикация.**
2. **"...local last-mile providers that often don't have their own real-time tracking to begin with"** (Parcel-секция) — причина/утверждение про локальных провайдеров отсутствует в оригинале (там просто "covering both major carriers and local last-mile providers"). **Придуманное обоснование.**
3. **"...since airlines, rail operators, and couriers don't all report on the same schedule"** (FAQ Q4) — оригинал лишь говорит "frequency varies by transport mode" без объяснения причины; рерайт добавляет придуманный причинный механизм. **Фабрикация механизма.**
4. **"multitracking across dozens of shipments"** — конкретизация "dozens" отсутствует в оригинале ("ensuring multitracking proceeds smoothly"). Минорная, но непроверяемая цифра.
5. **"Road works a bit differently since it leans more on live fleet data than fixed schedules"** — оригинал не делает такого сопоставления с "fixed schedules"; это редакторская интерпретация, не подтверждённая источником.
6. Вступительная сцена (пять вкладок браузера, "spreadsheet somebody built three years ago", "the parcel that was supposed to arrive Tuesday... courier's tracking page just times out") — иллюстративный, стилистически оправданный, но полностью придуманный сценарий без опоры на оригинал. Это не "факт о продукте", но подаётся как типичная ситуация — стоит отметить как безосновательный анекдот.
7. "container leasing companies" (добавлено слово "container" к "leasing companies") — низкий риск, вероятно допустимая конкретизация по контексту, но формально не в оригинале дословно.

**Итог:** ключевые количественные показатели (220+/445+/2400+/5) переданы точно — это сильная сторона. Но обнаружено минимум 3 существенных придуманных факта/механизма (border count, "no real-time tracking" claim про локальных курьеров, объяснение причины разной частоты обновления) плюс несколько менее критичных добавленных деталей — все они презентуются как фактические утверждения, хотя в оригинале не встречаются.

---

## Сводный вердикт

| Слой | Вердикт |
|---|---|
| (a) Плагиат/сходство | **NEEDS-WORK** — 6 совпадений ≥6 слов подряд вне списка исключений |
| (b) Словарные AI-маркеры | **PASS** — 0 em-dash, 0 клише из списка |
| (c) Структурные/риторические тики | **NEEDS-WORK** — 0 explicit connectors, но 4 contrastive negation, ~5 афористичных концовок (включая нарочитый callback), 3-4 симметричные антитезы |
| (d) Фактическая точность | **NEEDS-WORK** — числа точны, но ≥3 придуманных факта/механизма, не восходящих к оригиналу |

**Общий вывод: рерайт требует доработки** — переписать дословно совпадающие технические врезки (особенно все "You get:"/"supported" статистические абзацы и последний FAQ-ответ), убрать или атрибутировать выдуманные детали (три-четыре границы, отсутствие real-time tracking у локальных курьеров, причина разной частоты апдейтов), и снизить плотность аффористичных концовок/антитез, чтобы текст не читался как узнаваемая LLM-конструкция.
