# Независимый 4-слойный аудит: SeaRates "Week 18, 2026" — рерайт vs оригинал

Стандарт: скилл avalanche-copywriting, 11 правил (процитированы в задаче дословно).
Метод: только оригинал + рерайт, без самоотчёта автора.

---

## СЛОЙ A. Плагиат / построчное сходство

Проверка на 6+ слов подряд совпадающих (кроме терминов/названий компаний/продуктов).

| Оригинал (фрагмент) | Рерайт (фрагмент) | Совпадение | Вердикт |
|---|---|---|---|
| "namely Expeditors International Ocean, Maersk, Regional Container Lines (RCL), Ignazio Messina, COSCO, SITC Container Lines" | "Expeditors International Ocean, Maersk, Regional Container Lines (RCL), Ignazio Messina, COSCO, and SITC Container Lines" | Список названий перевозчиков совпадает почти дословно (6+ слов подряд) | **Исключение** — это перечень имён собственных (названия компаний), явно выведенных из-под правила 1 в задаче |
| "we've improved collaboration with worldwide shipping lines, including Maersk, ONE, and OOCL, by Points" | "with improved collaboration covering Maersk, ONE, and OOCL, tracked by Points" | "Maersk, ONE, and OOCL" (имена) + "by Points" (термин) — переставлено, нет 6 слов подряд вне терминов | PASS |
| "the ability to save and delete search results" | "picked up save and delete for search results too" | "save and delete" (3 слова) — ниже порога | PASS |
| "clicking the "Follow" button on the open search results page" | "Hit "Follow" on an open search results page" | "open search results page" — 4 слова подряд (термин UI-функции), "the"→"an" разбивает цепочку | PASS |
| "Geocoding API integrated with Logistics Explorer" | "The Geocoding API is now integrated with Logistics Explorer" | "integrated with Logistics Explorer" — 4 слова (включает продукт-термин) | PASS |
| "Extended Inbox integration with Logistics Explorer, Bookings, and Notifications" | "Inbox integration has been extended, now covering Logistics Explorer, Bookings, and Notifications" | Порядок слов переставлен ("Extended...with" → "...has been extended...covering"), совпадает только список продуктов (термины) | PASS |

**Счётчик:** 0 случаев дословного копирования 6+ слов подряд вне списков имён собственных/UI-терминов. Все содержательные предложения перефразированы синтаксически (смена структуры, инверсия, объединение).

**Вердикт слоя A: PASS.** Это настоящий рерайт, а не косметическая замена синонимов.

---

## СЛОЙ B. Словарные AI-маркеры

- **Em-dash / "--"**: проверено посимвольно во всём теле, title, meta-title, meta-description. Найдено **0** вхождений. Используются только запятые, двоеточие, амперсанд (&).
- **AI-клише** ("important to note", "in today's world", "delve", "seamless", "unique balance", "not just X but Y" и т.п.): **0** вхождений.
- **Пустой intro/outro filler**: intro ("Cargo doesn't check a calendar...") и outro ("That's week 18.") — короткие, содержат конкретную привязку к теме (changelog/неделя 18), не шаблонная вода типа "In conclusion, these updates demonstrate our commitment...". Оригинал, кстати, содержал корпоративный клишированный intro ("These updates reflect our commitment to long-term improvement") — рерайт его убрал.
- **Псевдоглубокие причастные обороты**: не обнаружены.

**Вердикт слоя B: PASS.**

---

## СЛОЙ C. Структурные / риторические тики

**Правило 5 (разрушение textbook-архитектуры):**
- Заголовок раздела 2 "Two small tools got useful upgrades" объединяет два разных пункта оригинала (Distance & Time + Vessel Tracking) в один блок БЕЗ явного перехода между ними — предложение про Vessel Tracking начинается сразу с "Vessel Tracking picked up..." без коннектора. Это удовлетворяет требованию "слияние идей / отсутствие перехода". ✅
- Раздел 3 содержит предложение, начинающееся с "And Inbox integration has been extended..." — разговорный, не строго "учебниковый" грамматический приём. ✅
- Длины разделов: 3 предложения / 3 предложения / 4 предложения (+ intro 2, outro 1) — вариативность **умеренная, но не сильная** — разделы близки по объёму, это ослабляет эффект "разрушения" структуры.
- **Вердикт по правилу 5: PASS (слабый)** — требование формально выполнено, но с запасом небольшим.

**Правило 6 (цепочки connectors "That's why.../Which is why..."):** 0 вхождений. **PASS.**

**Правило 7 (contrastive negation "X, not Y" / "instead of", максимум 1 на статью):**
- Найдено ровно **1** вхождение: *"...hand a specific route straight to a customer or partner **instead of** walking them through the tool yourself."*
- **Вердикт: PASS** (в пределах лимита 1), но это ровно на границе допустимого — если убрать, безопаснее.

**Правило 8 (афористичные "quotable" предложения, максимум 1 на статью, желательно в начале):**
- Кандидат 1 (начало, ожидаемо): *"Cargo doesn't check a calendar, but our changelog does, and this is what changed in SeaRates during week 18."* — литературная персонификация, на своём месте.
- Кандидат 2 (проблема): *"More names on the list means more of your shipments show up without extra digging."* — это тоже афористичная, "итоговая" фраза-мораль в середине раздела 1. Это ВТОРОЕ квотабл-предложение в статье.
- Кандидат 3 (слабый, не считаю нарушением): "Hit "Follow"... and it stays put until you decide otherwise." — скорее инструктивное, чем афористичное.
- **Вердикт: NEEDS-WORK** — обнаружено 2 афористичных предложения вместо разрешённого 1. (Кандидат 2 дополнительно нарушает Слой D, см. ниже — двойное нарушение.)

**Правило 9 (parallel twin-sentence conclusions):** Концовки разделов проверены — нигде нет пары зеркальных по структуре предложений подряд в конце раздела. **PASS.**

**Правило 10 (symmetric antithesis pairs):**
- Тот же оборот из правила 7: *"hand a specific route straight to a customer or partner **instead of** walking them through the tool yourself"* — грамматически параллельная антитеза (глагольная группа A vs глагольная группа B, контрастированные через "instead of"). Формально это единственный случай, и он один на всю статью (не "стопкой"), но правило 10 сформулировано как жёсткий запрет без указанного лимита-исключения (в отличие от правила 7).
- **Вердикт: NEEDS-WORK (пограничный случай)** — 1 инстанс symmetric antithesis, тот же самый, что учтён и в правиле 7. Рекомендуется переформулировать, чтобы закрыть оба риска одним изменением.

**Правило 4 (сбалансированные списки "A, B и C", механическое форматирование):**
- "Maersk, ONE, and OOCL" и "Logistics Explorer, Bookings, and Notifications" — трёхчленные списки с "and". Но это фактические перечни названий компаний/продуктов, унаследованные напрямую из оригинала (не риторическая конструкция автора), необходимые для точности release notes.
- **Вердикт: PASS** с оговоркой — списки не являются стилистическим тиком, это фактическая необходимость.

**Метафоры (правило 3, максимум 1-2 на статью):**
- "Cargo doesn't check a calendar, but our changelog does" (персонификация) — 1.
- "round out the week" (идиома "округлить/завершить") — слабая вторая метафора.
- Итого: **2**, на верхней границе лимита. **PASS**, но без запаса.

**Вердикт слоя C: NEEDS-WORK** (из-за правила 8 — два афористичных предложения вместо одного; правило 10 — пограничный случай антитезы, рекомендуется правка).

---

## СЛОЙ D. Фактическая достоверность (правило 11, КРИТИЧНО)

Проверено каждое конкретное утверждение рерайта на соответствие оригиналу.

| # | Утверждение в рерайте | Источник в оригинале | Статус |
|---|---|---|---|
| 1 | "Last week's release notes are still up if you want the full backstory." | "If you missed them, last week's updates are available for review." | ✅ Прослеживается |
| 2 | "Container Tracking now covers more shipping lines: [6 названий]" | "We have improved our collaboration with shipping lines, namely [те же 6 названий]" | ⚠️ **Частично прослеживается**. Оригинал говорит об "improved collaboration" (улучшенном сотрудничестве), рерайт трактует это как "now covers more shipping lines" (расширение покрытия). Это интерпретация/реинтерпретация факта, а не дословный перенос — оригинал НЕ утверждает явно, что это НОВЫЕ перевозчики или расширение охвата. Риск умеренный (правдоподобная отраслевая интерпретация, но формально это добавленная трактовка). |
| 3 | META_DESCRIPTION: "New carrier coverage for Container Tracking and Ship Schedules" | То же, что и #2 | ⚠️ Та же интерпретационная проблема, продублирована в meta-description |
| 4 | "Ship Schedules got a similar boost, with improved collaboration covering Maersk, ONE, and OOCL, tracked by Points." | "We've improved collaboration with worldwide shipping lines, including Maersk, ONE, and OOCL, by Points." | ✅ Прослеживается (слово "similar" — авторская связка, но не искажает факт) |
| 5 | **"More names on the list means more of your shipments show up without extra digging."** | Отсутствует в оригинале. Оригинал не содержит НИКАКИХ утверждений о том, что пользователь видит больше своих грузов или тратит меньше усилий на поиск. | ❌ **ВЫДУМАННЫЙ ФАКТ / причинно-следственная связь, которой нет в источнике.** Это именно тот тип нарушения, который явно указан как пример в задаче. Прямое нарушение правила 11. |
| 6 | "Distance & Time now has a Copy link option on the card, so you can hand a specific route straight to a customer or partner" | "we have added the Copy link option for the card for sharing unique access with your customers and partners" | ✅ Ядро факта прослеживается |
| 7 | **"...instead of walking them through the tool yourself."** | Отсутствует в оригинале. Оригинал не упоминает никакой предыдущий процесс "проведения клиента через инструмент вручную" — это придуманный контраст/альтернативный workflow. | ❌ **ВЫДУМАННЫЙ ФАКТ** — добавлено объяснение "почему это полезно" через несуществующее в оригинале сравнение "было/стало". |
| 8 | "Vessel Tracking picked up save and delete for search results too." | "we've implemented the ability to save and delete search results" | ✅ Прослеживается |
| 9 | "Hit "Follow" on an open search results page and it stays put until you decide otherwise." | "You can save the results by clicking the "Follow" button on the open search results page." + "ability to save and delete" | ✅ Прослеживается (в т.ч. "until you decide otherwise" логически = "delete" из того же оригинального пункта) |
| 10 | "Map Platform is here." | "Map Platform" (пункт списка анонсов) | ✅ Прослеживается (разумная интерпретация пункта-анонса) |
| 11 | "The Geocoding API is now integrated with Logistics Explorer." | "Geocoding API integrated with Logistics Explorer" | ✅ Прослеживается дословно |
| 12 | "Inbox integration has been extended, now covering Logistics Explorer, Bookings, and Notifications." | "Extended Inbox integration with Logistics Explorer, Bookings, and Notifications" | ✅ Прослеживается дословно |

**Счётчик выдуманных фактов: 2 чётких нарушения** (пункты 5 и 7), **+ 2 пограничных интерпретационных риска** (пункты 2 и 3, дублирующие одну и ту же проблему в теле и в meta-description).

**Вердикт слоя D: NEEDS-WORK.** Для release-notes с "особенно строгим фактчеком" (как указано в правиле 11) наличие двух добавленных причинно-следственных/сравнительных утверждений — критическая находка, требующая правки перед публикацией.

---

## ИТОГОВЫЕ ВЕРДИКТЫ ПО СЛОЯМ

| Слой | Вердикт | Причина |
|---|---|---|
| A. Плагиат/сходство | **PASS** | Нет дословного копирования вне терминов/имён |
| B. Словарные AI-маркеры | **PASS** | 0 em-dash, 0 клише |
| C. Структурные/риторические тики | **NEEDS-WORK** | 2 афористичных предложения вместо 1 (правило 8); пограничная symmetric antithesis (правило 10), совпадающая с единственным разрешённым "instead of" |
| D. Фактическая достоверность | **NEEDS-WORK** | 2 выдуманных причинно-следственных утверждения ("...without extra digging", "...instead of walking them through the tool yourself") + 2 пограничных интерпретационных риска (переквалификация "improved collaboration" → "new carrier coverage") |

## ОБЩИЙ ВЕРДИКТ: **NEEDS-WORK**

Причина: правило 11 (запрет выдуманных фактов) помечено в задании как КРИТИЧЕСКОЕ, и рерайт его нарушает дважды явно. Слой C усиливает необходимость правки (то же самое предложение с "instead of" одновременно создаёт риски по правилам 7/10, а "digging"-фраза дублирует нарушение и в правиле 8, и в правиле 11).

---

## СПИСОК КОНКРЕТНЫХ ПРАВОК

1. **[КРИТИЧНО, слой D + C-8]** Удалить или переписать: *"More names on the list means more of your shipments show up without extra digging."*
   → Заменить на нейтральное завершение без причинно-следственной выгоды, которой нет в оригинале, например: *"Container Tracking now lists six carriers, up from the previous set."* (только если такой факт подтверждён; иначе просто убрать предложение и закончить абзац на перечне перевозчиков).

2. **[КРИТИЧНО, слой D]** Удалить: *"...instead of walking them through the tool yourself."*
   → Оставить: *"...so you can hand a specific route straight to a customer or partner."* Это одновременно закрывает и находку слоя D (выдуманное сравнение), и слоя C (единственный "instead of" / symmetric antithesis становится ненужным).

3. **[Слой D, средний риск]** Смягчить формулировку "now covers more shipping lines" / "New carrier coverage" (тело + meta-description) — привести ближе к оригинальной формулировке "improved collaboration with shipping lines", либо явно подтвердить у автора/источника, что речь идёт именно о расширении охвата, а не только об улучшении данных по уже существующим перевозчикам. Если подтверждения нет — использовать более осторожную формулировку: *"Container Tracking has improved collaboration with these shipping lines:"*

4. **[Слой C, правило 8]** После правки №1 второе афористичное предложение исчезает автоматически — в статье останется только вступительное ("Cargo doesn't check a calendar..."), что приводит слой C к полному PASS.

После применения правок 1-2 (которые закрывают сразу оба критических пункта слоя D и оба спорных пункта слоя C) статья должна пройти повторную проверку по всем 4 слоям.
