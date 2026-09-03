# Независимый аудит рерайта: "Demurrage, Detention, and Storage" (SeaRates)

Файлы: `rewrite_demurrage_article.md` (158 строк) vs оригинал (см. `original_article.txt`, восстановлен из текста задачи).

---

## СЛОЙ A — Плагиат / сходство: **NEEDS-WORK**

Автоматический n-gram анализ (порог 6+ совпадающих слов подряд, без учёта отраслевых терминов/названий продуктов) нашёл **66 совпадающих фрагментов**, многие длиной 10–35 слов. Это значительно превышает допустимый уровень парафраза — рерайт местами является почти дословной копией со сменой пары слов вокруг таблиц и списков.

Наиболее критичные совпадения (не термины, не названия продуктов):

1. **35 слов подряд** (таблица демереджа/детеншна/стоража, почти буква в букву):
   > "...empty unit is returned late — can we unload and return the container on time? Storage — cargo or container occupies terminal, depot, or warehouse space too long — are we paying for extra space while cargo waits?"
   Рерайт (строки 37–39) и оригинал (Table: Demurrage...) идентичны почти дословно, только заменены дефисы на markdown-таблицу.

2. **32 слова подряд**, дословная копия предложения о SeaRates-инструментах:
   > "SeaRates tools such as the Tracking System for all shipping modes, Vessel Tracking, and Ship Schedules can help logistics teams monitor cargo movements, align vessel details, and react faster when schedules change."
   Оригинал (строка 19 файла) и рерайт (строка 71) — **100% идентичны, без единого изменения**.

3. **30 слов подряд**, почти дословно про калькулятор:
   > Оригинал: "...allows logistics teams to work with dates, free days, rates, currencies, and charge types to understand how quickly costs may increase if a container stays too long at the terminal, depot, or storage location."
   Рерайт: "...It lets logistics teams work with dates, free days, rates, currencies, and charge types to understand how quickly costs may increase if a container stays too long at the terminal, depot, or storage location."
   Изменено только "allows...to work" → "lets...work" (2 слова), остальное — дословный клон.

4. **24 слова подряд** (таблица "storage options"):
   > "...port environment, warehouse storage, unloading, and handling costs, use temporary storage, more control over timing, extra transport and handling, request extended free time, may..."

5. **20 слов подряд** в определении demurrage (таблица).

6. Ещё десятки 6–17-словных совпадений разбросаны по всему тексту (список "documents", список "weather, port congestion...", "reconfirm ETA, free time, broker, trucker, warehouse readiness", "SeaRates Logistics Explorer and Freight Index can support this comparison...", финальный абзац "documents, customs, trucking, warehouse planning, visibility, storage options, and empty return" и т.д.)

**Вывод по Слою A:** формально предложения переписаны в других местах (добавлены разговорные вставки, инверсии), но структура и лексика таблиц, списков-перечислений и особенно двух ключевых "продуктовых" предложений (SeaRates tools..., калькулятор) — это не пересказ, а копирование с косметическими правками. Это прямой риск плагиат-детекции и SEO-дублирования контента. **Обязательно переписать**: п.2 (SeaRates tools abzац) и п.3 (калькулятор abzац) дословно совпадают почти на 100% — это самые опасные места.

---

## СЛОЙ B — Словарные AI-маркеры: **PASS** (с одной оговоркой)

- **Em-dash (—)**: 0 вхождений во всём файле, включая заголовок и meta. ✅ PASS.
- **En-dash (–)**: 0 вхождений. ✅
- Клише вроде "it's important to note", "dive into", "seamless", "unique blend", "game-changer", "in today's fast-paced world", "delve", "leverage", "robust", "landscape", "navigate", "holistic", "crucial", "paramount", "testament", "tapestry" — **не найдено ни одного**. ✅
- Пустые intro/outro-филлеры ("In this article we will explore...", "In conclusion...") — отсутствуют, текст сразу начинается с фактов (порты, цифры). ✅

Единственное потенциальное замечание — не AI-маркер в классическом смысле, а скорее чрезмерно "разговорный/эссеистский" регистр, которым имитируется живое письмо (см. Слой C): фразы вроде "full stop, no particular drama involved", "sure, but also", "technically, just not" — это не клише ИИ, а скорее over-engineered "человечность", которая сама по себе выглядит как искусственный приём для обхода AI-детекторов.

**Вывод по Слою B: PASS** — словарных AI-маркеров нет.

---

## СЛОЙ C — Структурные/риторические тики: **NEEDS-WORK**

### 1. "Textbook"-лестница разделов
Структура рерайта: заголовок H1 → интро (проблема+цифры) → "Why These Costs Keep Piling Up" (почему важно) → "Where Each One Actually Starts" (определения/проблема) → "What Shippers Can Actually Control" (переход к решению) → 7 под-разделов-сценариев (внедрение) → "How to Weigh Demurrage Risk" (решение) → "Pricing the Risk Before It Shows Up" (инструмент/бонус — калькулятор) → "Where This Leaves Shippers" (заключение).
Это действительно калька классической "problem → solution → tool → checklist → wrap-up" лестницы, но она **напрямую скопирована с оригинала** (у оригинала та же последовательность: почему важно → определения → decision guide → 7 сценариев → таблица выбора → калькулятор → final takeaway). Рерайт не добавил и не убрал ни одного смыслового блока структуры оригинала — 1:1 копия скелета.
**Вердикт**: структура textbook-подобна, но это унаследовано от оригинала, а не изобретено рерайтером — отдельно штрафовать не за что, кроме того что это ещё один сигнал "мало трансформации".

### 2. Единообразная длина разделов
Подсчёт по словам:
```
197 | INTRO
155 | Why These Costs Keep Piling Up
220 | Demurrage, Detention, Storage: Where Each One Actually Starts
180 | What Shippers Can Actually Control
278 | When the ETA Moves
174 | Before the Ship Even Docks, the Paperwork Problem
213 | Chasing the Cheapest Rate Versus the Full Bill
289 | When Everything Downstream Isn't Ready
163 | After Delivery, the Clock Doesn't Stop
127 | When Cargo Lands Somewhere Else Entirely
134 | How to Weigh Demurrage Risk Against Storage Options
123 | Pricing the Risk Before It Shows Up
103 | Where This Leaves Shippers
```
Разброс 103–289 слов — умеренная вариативность, не строго единообразная (стандартное AI-клише — почти идентичная длина каждого блока). **PASS** по этому пункту.

### 3. Connectors "That's why / Which is why / That's a sign of"
Поиск по всему тексту: **0 совпадений**. ✅ PASS.

### 4. Contrastive negation "X, not Y" / "instead of" (лимит max 1 на статью)
Найдено:
- "...instead of a real-time update" (строка 19) — конструкция "X instead of Y".
- "...trucking needs arranging before release, not scrambled together afterward" (строка 101) — "X, not Y".

Итого: **2 случая** ("instead of" + ", not") — **превышает лимит 1 на статью**. Плюс россыпь смежных negation-конструкций с "isn't/doesn't/can't" (более 20 случаев по тексту, см. ниже "Symmetric antithesis"), которые не считаются строго по формату "X, not Y", но создают тот же риторический эффект накопления отрицаний. Формально по заданному шаблону — 2 попадания, лимит превышен. **NEEDS-WORK**.

### 5. Афористичные финальные предложения абзацев
Явные примеры "формульных" афоризмов в конце абзацев:
- "Extra cost prevention has to start before the container reaches the port. Waiting for the invoice is already too late." (конец интро-блока, строки 13)
- "The more useful question isn't 'where is my container.' It's what needs to be ready before that container becomes available at all." (конец раздела "Why These Costs...")
- "A planned storage decision usually beats an unplanned delay, and the real win is dodging surprise costs by picking the most predictable option for the shipment at hand." (конец раздела перед калькулятором)
- "The best shipment plan looks past the freight rate alone, toward whether cargo keeps moving after arrival, with a clear, already-planned storage option sitting on standby in case it doesn't." (финал статьи)

Насчитано **минимум 4 явных афористичных финала**. Это заметный тик — почти каждый крупный смысловой блок закрывается "звонкой" фразой-выводом. **NEEDS-WORK**.

### 6. Parallel twin-sentence заключения (два зеркальных предложения подряд)
В финальном разделе "Where This Leaves Shippers" — три коротких абзаца, каждый из одного предложения, по нарастающей ритмике ("aren't easing up, and shippers need to shift..." / "isn't a well-argued dispute... It's a connected workflow..." / "looks past the freight rate alone, toward whether cargo keeps moving..."). Второй абзац содержит явную twin-структуру внутри себя: "isn't X. It's Y." — классическая зеркальная пара (антитеза + подтверждение). Это можно засчитать как parallel twin-sentence конструкцию. **1 явный случай** — сам по себе не катастрофа, но в сочетании с остальными тиками усиливает "сгенерированность" финала. **NEEDS-WORK** (пограничный случай).

### 7. Symmetric antithesis pairs (парные противопоставления без "not")
Помимо явных "not"-конструкций, в тексте систематически используется приём "X. Y." или "X, Y." зеркального контраста:
- "On paper, a short delay looks manageable. In practice, it can mean..." (строка 19) — классическая antithesis "on paper / in practice".
- "The cargo is still moving, technically, just not along the plan anyone actually booked." (антитеза "moving / not along the plan")
- "Useful after a delay's already happened, sure, but also during planning itself." — контраст "after / during".
- "It's tempting to assume... For detention risk, that assumption doesn't hold up well." — контраст "assumption / reality".

Итого **минимум 4 симметричных антитез-пары**, помимо явных negation-конструкций из п.4. Это системный риторический приём, использованный многократно. **NEEDS-WORK**.

### Итоговая таблица Слоя C

| Признак | Счётчик | Лимит/норма | Вердикт |
|---|---|---|---|
| Textbook-лестница | унаследована от оригинала | — | нейтрально |
| Единообразная длина разделов | 103–289 слов (разброс есть) | — | PASS |
| "That's why/Which is why/That's a sign of" | 0 | — | PASS |
| Contrastive negation "X, not Y"/"instead of" | 2 | max 1 | **NEEDS-WORK** |
| Афористичные финалы абзацев | ≥4 | минимизировать | **NEEDS-WORK** |
| Parallel twin-sentence заключение | 1 явный ("isn't X. It's Y.") | минимизировать | **NEEDS-WORK** |
| Symmetric antithesis pairs | ≥4 | минимизировать | **NEEDS-WORK** |

**Итог по Слою C: NEEDS-WORK.** Плагиат по лексике формально снижен разговорными вставками, но взамен появился отчётливый набор риторических AI-подобных тиков (антитезы, афористичные закрытия, накопленные негации), которых в оригинале не было в таком количестве.

---

## СЛОЙ D — Фактическая достоверность: **NEEDS-WORK (критично)**

### 4.1 Цифры — все совпадают с оригиналом
- Manila North 4.89 days ✅ (совпадает)
- Singapore 1.53 days ✅ (совпадает)
- Busan 1 day ✅ (совпадает)
- "In early June 2026" ✅ (совпадает)
- "48 hours" (порог для ETA) ✅ совпадает
- "three to five days before ETA" ✅ совпадает
Цифры не искажены. **PASS по цифрам.**

### 4.2 Инструменты SeaRates — описания точные, без добавленных слов
Проверены построчно:
- **Tracking System / Vessel Tracking / Ship Schedules**: предложение в рерайте (строка 71) **дословно идентично** оригиналу ("...can help logistics teams monitor cargo movements, align vessel details, and react faster when schedules change"). Никаких "AI-powered", "predictive algorithms", "exception detection" не добавлено. ✅
- **Logistics Explorer и Freight Index**: рерайт (строка 95) — "can support this comparison, helping teams review market rates, routes, and freight conditions in one place" — совпадает по смыслу и почти дословно с оригиналом ("can support this comparison by helping teams review market rates, routes, and freight conditions in one place"). Без добавленных функций. ✅
- **Demurrage & Storage Calculator**: рерайт (строка 148) практически дословно копирует оригинал ("helps you calculate possible extra costs for demurrage, detention, and storage scenarios... work with dates, free days, rates, currencies, and charge types..."). Никаких добавленных возможностей (никакого "AI-driven forecasting" и т.п.) не внесено. ✅

**Вывод по инструментам: PASS** — фактических искажений функционала SeaRates-продуктов нет. (Хотя, как отмечено в Слое A, эта точность достигнута ценой почти дословного копирования — что плохо для оригинальности, но хорошо для фактической точности.)

### 4.3 КРИТИЧЕСКАЯ ПРОВЕРКА: фраза про "supply chain visibility tools" / "container tracking visibility"

Цитата из рерайта (строка 61, раздел "When the ETA Moves"):
> "Even a predictive ETA goes stale fast if nobody's checking the supply chain visibility tools tied to it, and container tracking visibility only pays off if someone's watching it before the free time clock starts running."

Проверка по оригиналу: искал "visibility" во всём оригинальном тексте — единственное упоминание "visibility" в оригинале находится в **другом сценарии** (Scenario 3, про freight rate): "...limited tracking visibility, higher local charges..." — это касается сравнения тарифов через Freight Index, **не про ETA/мониторинг vessel tracking**.

В оригинальном разделе Scenario 1 ("The vessel ETA changes") **нет вообще никакого упоминания**:
- ни "predictive ETA" — оригинал нигде не называет ETA "predictive" (предиктивным/прогнозным), там просто "ETA" / "latest ETA";
- ни "supply chain visibility tools" — такого термина/понятия в оригинале нет вообще;
- ни "container tracking visibility" — тоже отсутствует как понятие в этом контексте.

**Это полностью выдуманная деталь.** Рерайтер:
1. Добавил слово "predictive" к ETA, которого нет в оригинале (в оригинале ETA — это просто расчётное время прибытия, никакой "предиктивности"/прогнозной модели не упоминается нигде в статье).
2. Изобрёл несуществующий термин "supply chain visibility tools" и приписал ему причинно-следственную связь ("goes stale fast if nobody's checking..."), которой в оригинале нет.
3. Добавил "container tracking visibility" как условие ("only pays off if someone's watching it before the free time clock starts running") — это отдельный придуманный механизм/причинно-следственная связь, отсутствующий в оригинале.

Это прямое нарушение требования Слоя D — **добавлена техническая деталь/причинно-следственная связь, которой нет в первоисточнике**, причём выглядит как будто это отсылка к конкретным продуктам SeaRates ("Tracking System"/"Vessel Tracking"), но формулировка не совпадает ни с одним реальным описанием инструмента в оригинале и добавляет несуществующую логику "protection against stale ETA".

**Это самая серьёзная находка аудита — рекомендую убрать или полностью переписать это предложение**, оставив только то, что подтверждено оригиналом (SeaRates tools помогают "monitor cargo movements, align vessel details, and react faster when schedules change" — без спекуляций про "goes stale" и "visibility tools").

### 4.4 Прочие потенциально добавленные детали (мельче, но стоит зафиксировать)

- Строка 9 рерайта: "...vessel bunching, **ships converging on the same terminal slots faster than the slots could clear**." — добавленное пояснение/расшифровка термина "vessel bunching", которого в оригинале нет. Оригинал просто говорит "vessel bunching" без объяснения механизма. Это не фактическая ошибка per se (общее описание bunching корректно с точки зрения логистики), но это добавленный объяснительный механизм, отсутствующий в первоисточнике — формально попадает под критерий Слоя D ("флагни любую... причинно-следственную связь... которой нет в оригинале").

- Строка 19: "Sometimes the consignee just isn't ready to unload, full stop, no particular drama involved, they simply didn't get word in time." — фраза "they simply didn't get word in time" **придумывает конкретную причину** (не получили вовремя информацию), которой нет в оригинале — там просто "a consignee not being ready to unload" без объяснения причины. Это добавленная причинно-следственная деталь.

- Строка 105: "...or port hours and warehouse hours simply don't overlap that particular week." — добавлена конкретизация "that particular week", которой нет в оригинале (оригинал: "a mismatch between port availability and warehouse working hours" — без временной привязки "that particular week"). Незначительно, но это добавленная деталь.

- Строка 41: "...well before the container shows up is really the only way to avoid demurrage and detention charges piling up unnoticed." — фраза "is really the only way" — усиление до абсолютного утверждения ("единственный способ"), которого нет в оригинале (оригинал мягче: "That is why it is important to check..." — рекомендация, не категоричное "единственный способ"). Это искажение модальности/степени уверенности по сравнению с оригиналом.

### Итог по Слою D: **NEEDS-WORK (критично)**
- Цифры — точны (PASS).
- Описания инструментов SeaRates — точны, без добавленных фич (PASS).
- Но обнаружена **одна серьёзная выдуманная деталь** (supply chain visibility tools / container tracking visibility / "predictive ETA") — прямое добавление несуществующей в оригинале причинно-следственной связи и терминологии.
- Плюс несколько мелких добавленных объяснений/причин ("ships converging...", "they simply didn't get word in time", "that particular week", "is really the only way"), которые размывают границу между пересказом и добавлением новых утверждений.

---

## ИТОГОВЫЕ ВЕРДИКТЫ

| Слой | Вердикт |
|---|---|
| A — Плагиат/сходство | **NEEDS-WORK** (66 совпадающих фрагментов 6+ слов, включая почти дословные предложения про SeaRates tools и калькулятор) |
| B — Словарные AI-маркеры | **PASS** (0 em-dash, 0 клише-фраз) |
| C — Структурные/риторические тики | **NEEDS-WORK** (превышен лимит contrastive negation, множественные афористичные финалы, symmetric antithesis, twin-sentence заключение) |
| D — Фактическая достоверность | **NEEDS-WORK, критично** (выдуманная фраза про "supply chain visibility tools"/"predictive ETA"/"container tracking visibility"; несколько добавленных мелких деталей и причин) |

## СПИСОК КОНКРЕТНЫХ МЕСТ ДЛЯ ИСПРАВЛЕНИЯ (по приоритету)

1. **[КРИТИЧНО, Слой D]** Строка 61: полностью убрать/переписать предложение "Even a predictive ETA goes stale fast if nobody's checking the supply chain visibility tools tied to it, and container tracking visibility only pays off if someone's watching it before the free time clock starts running." — в оригинале такого утверждения, термина и причинно-следственной связи нет.

2. **[КРИТИЧНО, Слой A]** Строка 71: предложение про "SeaRates tools such as the Tracking System..." дословно скопировано из оригинала (32 слова без изменений) — перефразировать.

3. **[КРИТИЧНО, Слой A]** Строка 148: абзац про Demurrage & Storage Calculator — почти дословная копия (30 слов совпадает) — перефразировать существеннее.

4. **[Слой A]** Обе markdown-таблицы (строки 35–39 и 135–141) содержат протяжённые дословные/почти дословные совпадения (20–35 слов) с оригинальными "Table:"-блоками — переформулировать формулировки ячеек, не просто менять дефисы на markdown-синтаксис.

5. **[Слой A]** Абзац про Logistics Explorer/Freight Index (строка 95) и десятки более мелких списков-перечислений (документы, weather/port congestion, decision-таблица во "What Shippers Can Actually Control") — требуют более глубокого перефразирования, не косметического.

6. **[Слой C]** Убрать одну из двух contrastive negation конструкций ("instead of a real-time update" строка 19, или ", not scrambled together afterward" строка 101), чтобы уложиться в лимит max 1 на статью.

7. **[Слой C]** Сократить количество афористичных финалов абзацев (минимум 4 найдено) — особенно концовки в строках 13, 23, 142, 158.

8. **[Слой C]** Смягчить/убрать явную "isn't X. It's Y." twin-конструкцию в финальном разделе (строка 156) и уменьшить число symmetric antithesis pairs (строки 19, 89(sic 123), 150, 113).

9. **[Слой D, менее критично]** Строка 9: убрать добавленное объяснение "ships converging on the same terminal slots faster than the slots could clear" либо явно обозначить как собственную интерпретацию, а не факт.

10. **[Слой D, менее критично]** Строка 19: убрать выдуманную причину "they simply didn't get word in time" — в оригинале причина не указана.

11. **[Слой D, менее критично]** Строка 105: убрать добавленную конкретизацию "that particular week".

12. **[Слой D, менее критично]** Строка 41: смягчить категоричное "is really the only way to avoid..." до модальности, соответствующей оригиналу ("it is important to check...").
