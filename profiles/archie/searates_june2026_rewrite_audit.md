# Независимый 4-слойный аудит рерайта: SeaRates June 2026 Release Notes

Метод: рерайт сверен с оригиналом с нуля, без знания процесса переписывания.

---

## A) ПЛАГИАТ / СХОДСТВО (построчная сверка, порог 6+ слов подряд, кроме терминов/имён)

**Вердикт: NEEDS-WORK**

Найдено несколько дословных совпадений 6+ слов подряд, которые НЕ покрываются исключением для имён собственных — это обычные описательные фразы:

1. **"filtering by vessel type and specialized transport modes"** — 7 слов подряд идентичны оригиналу ("Bulk shipments now support filtering by vessel type and specialized transport modes" → рерайт: "Bulk shipments got filtering by vessel type and specialized transport modes"). Не имена собственные. **FLAG.**

2. **"internal logistics system, by points, vessels, and seaports worldwide."** — 9 слов подряд идентичны ("...via API in your internal logistics system, by points, vessels, and seaports worldwide." → рерайт: "...via API inside an internal logistics system, by points, vessels, and seaports worldwide."). **FLAG (сильный).**

3. **"as a white-labeled solution integrated on"** — 6 слов подряд идентичны, из того же предложения (Ship Schedules). По сути, весь хвост предложения про Ship Schedules переписан лишь косметически ("your website"→"a company's own site", "your"→"an", порядок глаголов в начале) — самый слабый по трансформации абзац во всём рерайте. **FLAG.**

4. **"subscription monitoring for Container Tracking and Ship Schedules"** — 8 слов подряд идентичны оригиналу. Частично состоит из названий продуктов, но связки "subscription monitoring for...and" — не имена собственные. **FLAG (пограничный).**

5. **"the container's central axis"** vs оригинальное **"the central axis of the container"** — те же самые слова, только переставлены местами (не 6 слов подряд, поэтому формально проходит фильтр, но по сути это "перетасовка" оригинала, а не независимая формулировка). **Отметить как приём обхода детектора.**

Совпадения, которые **являются legit исключением** (списки собственных имён/продуктовых категорий, не флагуются):
- Полный список перевозчиков ("Hapag-Lloyd, CMA CGM, COSCO, OOCL, Maersk..." — 20+ слов, дословно) — имена компаний.
- Список авиалиний ("Swiss International Air Lines, EVA Air..." — дословно) — имена компаний.
- Список категорий складских услуг ("Handling, Stuffing, Survey, Fulfilment, Storage, Packaging, Marking...") — номенклатура.
- "239 global shipping lines" — числовой факт + термин.
- "Insurance, Customs Clearance, Certification, and Inspection Services" — номенклатура услуг (пограничный случай, но по духу правила — исключение).

**Итог слоя A:** 4 полноценных флага дословного заимствования обычных (не именных) фраз, из них 2 — сильных (7 и 9 слов подряд). Абзац Ship Schedules — наименее трансформированный участок всей статьи.

---

## B) СЛОВАРНЫЕ AI-МАРКЕРЫ

**Вердикт: PASS (по формальным метрикам), но с оговоркой по filler-рамке**

- **Em-dash (—):** 0 найдено во всём тексте рерайта.
- **"--" (двойной дефис):** 0 найдено.
  - Примечательно: оригинал использует en-dash в имени компании "Milaha – Qatar Navigation Q.P.S.C."; рерайт этот дефис убрал и заменил запятой — см. Слой D (фактическая ошибка, не просто стилистика).
- **Штампы ("важно отметить", "в современном мире", "погрузиться", "неотъемлемая часть", "уникальный баланс", "не просто X, а Y", "подвести итог"):** ни одного буквального совпадения не найдено.
- **Filler-вступление:** присутствует — предложение про "predictive ETAs and end-to-end visibility as the industry's next horizon" выполняет ровно функцию типового AI-вступления "весь индустрия говорит о X, но на самом деле..." — содержательно это тот же троп, даже без стоп-фраз из списка. **Отметить как filler-паттерн.**
- **Filler-заключение:** "Summer's the same as always at SeaRates... Follow along on LinkedIn, X, Facebook, and Instagram if the changelog isn't fast enough on its own." — типовая закольцовка с призывом к соцсетям, функционально filler, хотя без клише-фраз из списка.

**Итог слоя B:** По жёстким счётчикам (em-dash/штампы) — чисто, 0/0. Но структурно "лишний" вступительный и заключительный filler-абзац присутствует и выполняет ту же риторическую роль, что и запрещённые клише — просто пересказанную другими словами.

---

## C) СТРУКТУРНЫЕ / РИТОРИЧЕСКИЕ ТИКИ

**Вердикт: NEEDS-WORK**

- **Порядок разделов как "идеальная лестница":** PASS. Порядок в рерайте (Container Tracking → Vessel/Flight Tracking → Booking → Logistics Map → Carrier Directory → Ship Schedules → Load Calculator → Virtual Office) — тематическая перегруппировка (объединены темы трекинга), не выглядит как искусственно нарастающая/убывающая риторическая лестница.

- **Единообразие длины разделов:** PASS. Разброс большой: от ~35 слов (Load Calculator) до ~170 слов (Vessel/Flight Tracking) — не подозрительно ровно.

- **Явные коннекторы "That's why / which is why":** счётчик = **0**. (Есть один случай "which means" — функционально близко, но формально не входит в счётчик).

- **Contrastive "X, not Y" / "instead of" (лимит 1 на статью):** счётчик = **1** — "a distinction that matters more in practice than it sounds on paper" (Logistics Map). В пределах лимита. PASS.

- **Абзацы, заканчивающиеся хлёстким афористичным предложением:** счётчик — **5 из 9 тематических разделов** (плюс общая концовка статьи = 6-7 если считать финал):
  1. Container Tracking: *"Broader carrier coverage like this is what real-time visibility for container tracking actually runs on, and it keeps container visibility manageable even as the shipping lines list grows."*
  2. Vessel/Flight Tracking: *"...a small thing, but the kind of detail people notice when they're staring at the same screen for the tenth time that day."*
  3. Logistics Map: *"...a distinction that matters more in practice than it sounds on paper."*
  4. Carrier Directory: *"Evaluating carrier coverage gets easier when the routes are already drawn out in front of you, and decisions during partner selection lean on that same live logistics data."*
  5. Load Calculator: *"Stuffing calculations come out closer to what actually happens once the container gets packed."*
  6. Virtual Office: *"Worth knowing if most of a company's volume isn't ocean freight."*
  7. Финал статьи: *"...if the changelog isn't fast enough on its own."*
  
  Это **самый выраженный тик всего текста** — почти каждый раздел закрывается авторским обобщающим афоризмом, которого нет в оригинале (в оригинале разделы заканчиваются на нейтральных фактических/CTA-фразах). **FLAG — системный паттерн, а не единичный случай.**

- **Parallel twin-sentence conclusions / symmetric antithesis (даже без "not"):**
  - *"Summer releases at SeaRates tend to work like clearing out a garage: some things get sharper, a few things just finally get labeled properly."* — чёткая зеркальная антитеза ("some things X, a few things Y") без слова "not". **FLAG.**
  - Повторяющийся приём parallel-triad (список из 3 параллельных глагольных конструкций): *"Filter performance is faster, the data updating logic was reworked, and vessel schedule synchronization is tighter now"* и *"Shipping bookings can be created, tracked, and updated..."* — риторический тик повторён дважды. **FLAG.**

- **Метафоры (лимит 1-2 на статью):** найдено **2-3**:
  1. "clearing out a garage" (сравнение релиза с уборкой гаража) — самая заметная, декоративная.
  2. "the industry's next horizon" — стёртая метафора.
  3. "Filters Doing More of the Work" (заголовок раздела) — олицетворение, пограничный случай.
  
  На грани лимита или чуть выше него. **FLAG (пограничный/при строгом счёте — превышение).**

**Итог слоя C:** Формальные счётчики коннекторов и контрастов в норме, но обнаружены два системных тика, которых нет в оригинале: (1) почти в каждом разделе — афористичная закрывающая фраза (6-7 случаев), (2) зеркальная антитеза во вступлении + повторяющиеся parallel-triads. Метафоры на грани/за лимитом.

---

## D) ФАКТИЧЕСКАЯ ДОСТОВЕРНОСТЬ (КРИТИЧНО)

**Вердикт: NEEDS-WORK**

### Подтверждённые проблемы:

1. **"predictive ETAs" (вступление)** — **ПОДТВЕРЖДЕНО КАК ВЫДУМАННОЕ ДОБАВЛЕНИЕ.** Оригинал вообще не упоминает predictive ETAs ни в каком контексте. Фраза *"Everyone in freight tech keeps talking about predictive ETAs and end-to-end visibility as the industry's next horizon, but this particular release is mostly about the screens people actually touch every day"* синтаксически противопоставляет "разговоры индустрии о predictive ETAs" тому, что "на самом деле" в этом релизе — то есть формально НЕ заявляет, что у SeaRates есть predictive ETAs. Но это чистая отсебятина без опоры на источник: ни одного слова про predictive ETAs, "industry's next horizon" или подобный нарратив в оригинале нет. Риск: небрежный читатель может считать это скрытой заявкой на позиционирование SeaRates рядом с этой темой. **Рекомендация: убрать/заменить на нейтральное вступление без придуманного индустриального контекста.**

2. **"real-time visibility for container tracking actually runs on"** — **ПОДТВЕРЖДЕНО КАК ВЫДУМАННЫЙ ПРИЧИННО-СЛЕДСТВЕННЫЙ МЕХАНИЗМ.** Оригинал: *"Access broader carrier coverage and manage container visibility more efficiently with real-time shipping updates."* — это два параллельных, НЕсвязанных причинностью выигрыша (шире охват + real-time обновления). Рерайт превращает это в явное причинное объяснение: *"Broader carrier coverage like this is what real-time visibility for container tracking actually runs on"* — то есть заявляет, что real-time visibility ТЕХНИЧЕСКИ ОСНОВАНА на охвате перевозчиков. Источник такого механизма не утверждает. Это ровно тот тип "выдуманного технического объяснения", который запрещён. **STRONG FLAG.**

3. **Ship Schedules — ошибка в подсчёте/сущности:** Оригинал называет компанию **"Milaha – Qatar Navigation Q.P.S.C."** одним юр. лицом (en-dash обозначает, что Milaha — торговое название Qatar Navigation Q.P.S.C.), итого **3** новых имени: Milaha–Qatar Navigation Q.P.S.C., Sea Legend Shipping, Samudera Shipping Line. Рерайт убрал дефис и написал через запятую: *"Three more names joined the schedule research by points this month: Milaha, Qatar Navigation Q.P.S.C., Sea Legend Shipping, and Samudera Shipping Line."* — заявлено "three more names", но перечислено **четыре** элемента через запятую, потому что одна компания разбита на две. Это конкретная, проверяемая фактическая ошибка (внутреннее противоречие "три" vs 4 позиции в списке + искажение структуры названия компании). **FLAG.**

4. Минорные, но всё же непроверяемые добавления (низкий риск, но не подтверждаются источником):
   - *"if a specific carrier needs confirming before anyone builds against it"* (Container Tracking) — придуманный сценарий использования Developer Portal.
   - *"Stuffing calculations come out closer to what actually happens once the container gets packed"* (Load Calculator) — источник говорит лишь про "greater accuracy", конкретики про "closer to what actually happens" там нет — добавленная, непроверяемая формулировка результата.
   - *"mass operations got noticeably easier to run"* (Virtual Office) — усилитель "noticeably", которого в источнике нет ("we upgraded work with... mass operations" — без заявления об ощутимости эффекта).
   - *"a small thing, but the kind of detail people notice when they're staring at the same screen for the tenth time that day"* — субъективная, ничем не подтверждённая характеристика пользовательского опыта.

### Проверено и корректно:
- Число "239 global shipping lines" — совпадает.
- Списки перевозчиков, авиалиний, складских категорий, сервисов страхования/таможни — совпадают дословно.
- Основные факты про Booking System, Load Calculator, Virtual Office, Carrier Directory (без добавленных механизмов) переданы верно.

**Итог слоя D:** Оба места, на которые прямо указано в задании, подтверждены как проблемные: "real-time visibility...actually runs on" — выдуманный причинный механизм (наиболее серьёзная находка всего аудита), "predictive ETAs" — немотивированная вставка индустриального контекста, отсутствующая в источнике целиком. Плюс отдельная, самостоятельно найденная фактическая ошибка: искажение имени компании в Ship Schedules, приводящее к несовпадению "three" vs 4 перечисленных названий.

---

## ОБЩИЙ ВЕРДИКТ ПО 4 СЛОЯМ

| Слой | Вердикт |
|---|---|
| A. Плагиат/сходство | **NEEDS-WORK** (4 флага дословных совпадений 6-9 слов, не покрытых исключением; особенно абзац Ship Schedules) |
| B. Словарные AI-маркеры | **PASS** формально (0 em-dash, 0 "--", 0 клише из списка); но filler intro/outro присутствует по смыслу |
| C. Структурные тики | **NEEDS-WORK** (системный тик — афористичная концовка почти в каждом разделе, 5-7 случаев; зеркальная антитеза во вступлении; parallel-triad повторён дважды; метафоры на грани лимита) |
| D. Фактическая точность | **NEEDS-WORK** (выдуманный причинный механизм про real-time visibility; необоснованная вставка "predictive ETAs"; фактическая ошибка с разделением одной компании на две в Ship Schedules) |

**Рекомендация:** статья требует доработки минимум по трём из четырёх слоёв (A, C, D) перед публикацией — приоритет: (1) убрать выдуманное причинное объяснение про real-time visibility, (2) исправить список Ship Schedules (вернуть дефис/объединить в одну сущность или явно указать "four names"), (3) переписать хвост абзаца Ship Schedules и фразу про vessel type/transport modes без дословного заимствования, (4) сократить количество афористичных концовок разделов, (5) пересмотреть необходимость вступительной фразы про predictive ETAs.
