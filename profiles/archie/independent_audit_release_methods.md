# Независимый аудит: Original B/L vs Telex vs Express Release

Проверка выполнена по стандарту `avalanche-copywriting` (4 слоя), без доступа к самоотчёту автора.

---

## (a) ПЛАГИАТ / СХОДСТВО — **NEEDS-WORK**

Автоматическая проверка 6-грамм (посл. слов) дала **42 совпадающих 6-граммы** с оригиналом. После фильтрации чистых перечислений терминов (типа "original bill of lading telex release express release" — это список из 4 exempt-терминов) остаётся **минимум 10 неэксемптных клоз/предложений**, скопированных почти дословно (8–14 слов подряд, не термины):

1. **Пример 2 (телекс-релиз), почти дословная копия целого предложения:**
   - Оригинал: *"The shipper surrenders the full set of original B/L at origin and requests a telex release."*
   - Рерайт: *"The shipper surrenders the full set of originals at origin and requests telex release."*
   - Изменено 2 слова из 15. Это не перефраз, а копипаста.

2. **Пример 3 (express release), почти дословная копия:**
   - Оригинал: *"A company ships goods from its factory in China to its own distribution center in Europe."*
   - Рерайт: *"A company ships from its own factory in China to its own distribution center in Europe."*
   - 12+ слов совпадают подряд, включая специфичные детали (China, distribution center, Europe) — это не устоявшиеся термины.

3. **CTA-блок в конце, близкий парафраз структуры целиком:**
   - Оригинал: *"Share your cargo details, route, or document requirements through our Request a Quote form or contact us at sales@searates.com. SeaRates will help you prepare the shipment correctly and coordinate the next steps from booking to final delivery."*
   - Рерайт: *"Send us your cargo details, route, or document requirements through our Request a Quote form, or reach out directly at sales@searates.com. SeaRates will help you set the shipment up correctly from booking through final delivery."*
   - Фраза "your cargo details, route, or document requirements through our Request a Quote form" скопирована практически без изменений (только "Share"→"Send us").

4. **Повторяющаяся конструкция "the carrier or forwarder issues..."** — используется в разделах Telex и Express почти без изменений в обоих местах (было и в оригинале в обеих секциях).

5. **Списки терминов скопированы почти без изменений:**
   - "payment, endorsement, bank handling, document delivery, and destination free time" (пример 1)
   - "customs clearance, terminal charges, delivery appointments, and empty container return" (раздел про delivery)
   - "focus on customs clearance, terminal release, and delivery scheduling" (пример 3)
   - "assuming telex release is possible without surrendering originals" (пункт из списка ошибок)

**Вердикт: NEEDS-WORK.** Отдельные предложения (особенно #1 и #2 выше) — это не рерайт, а перефраз на уровне "поменяли пару слов", что нарушает требование "100% original human-sounding prose" и превышает лимит 6+ совпадающих слов far beyond границы допустимого для не-терминов.

---

## (b) СЛОВАРНЫЕ AI-МАРКЕРЫ — **PASS**

- **Em-dash (—) в title/meta/body:** 0. **Double-hyphen (--):** 0. Проверено программно по всему тексту, включая TITLE/META_TITLE/META_DESCRIPTION. ✅
- **Клише из бан-листа** (delve, landscape, furthermore, moreover, unlock, unleash, navigate, game-changer, seamless, "in today's world", "in conclusion", "in this article/guide", "we will explore") — **0 найдено**.
- **Пустые вступления/заключения:** intro не является generic filler'ом ("В этой статье мы рассмотрим..."), открывается конкретным сюжетом (контейнер на терминале). Заключение также содержательное, не пустая формула. ✅

Единственное замечание: вступительное предложение "This piece walks through how original B/L, telex release, and express release actually function, where each one fits, and what's worth checking before the ship even leaves port" почти дословно повторяет функцию/структуру оригинального "This guide explains how original B/L..." — но это уже учтено в слое (a), не дублирую здесь как отдельный минус.

**Вердикт: PASS.**

---

## (c) СТРУКТУРНЫЕ / РИТОРИЧЕСКИЕ AI-ТИКИ — **NEEDS-WORK**

- **"Textbook"-архитектура:** рерайт всё ещё почти 1:1 повторяет порядок разделов оригинала (проблема → механика OBL → механика telex → механика express → сравнения → payment risk → delivery speed → checklist → mistakes → examples → takeaway), с лишь 2 точечными слияниями (3 payment/delivery раздела объединены в 2; 3 примера сведены под один H2 вместо трёх H3). Это движение в правильную сторону, но общая логическая лестница осталась узнаваемой копией шаблона оригинала. **Частичное несоответствие правилу 5.**

- **Длина разделов:** от 84 до 216 слов (диапазон ~2.6×) — не подозрительно однородна. **PASS по этому пункту.**

- **"That's why / which is why / that's a sign of":** явных "that's why" — 0. Найден 1 функционально идентичный коннектор: *"Release is tied to physical possession of that document and its correct endorsement, full stop.\n\nThis is why original B/L still shows up constantly in deals..."* — 1 случай, в пределах разумного, не критично само по себе.

- **Contrastive negation "X, not Y" / "instead of":** лимит — максимум 1 на статью. Найдено **3 случая**, что превышает лимит в 3 раза:
  1. *"Decide this before booking, not after, since switching release methods midstream..."*
  2. *"...ideally with the forwarder or carrier confirming each answer, not after the ship has already sailed."*
  3. *"Express release, by contrast, isn't a document type at all. It's a release instruction, a method..."* (классическая конструкция "isn't X, it's Y")
  "instead of" — 0 случаев. **Нарушение лимита — FAIL по этому пункту.**

- **Абзацы, заканчивающиеся хлёстким one-liner'ом:** найдено не менее 5 явных случаев из 34 абзацев (~15%), включая:
  - *"Release is tied to physical possession of that document and its correct endorsement, full stop."*
  - *"One's the paperwork. The other's the process."*
  - *"They start weeks earlier, on a desk somewhere."*
  - *"It runs through the carrier's or agent's digital systems now, but the label stuck around."*
  - *"The trade-off is obvious once you say it out loud: less document leverage than an original B/L gives you."*
  Не "почти каждый абзац", но заметно выше нормы 2–3 сознательно "плоских" предложений на статью.

- **Parallel twin-sentence conclusions:** найден явный случай:
  - *"One's the paperwork. The other's the process."* (конец раздела про Express release vs Sea waybill) — классическая зеркальная пара, прямое нарушение правила 9.
  - Второй похожий случай: *"Control is the upside here. Time is what you give up for it."*

- **Symmetric antithesis pairs (без явного "not"):** тот же *"One's the paperwork. The other's the process."* одновременно нарушает и правило 10 (paperwork/process — согласованная лексическая пара в антитезе). Также *"Control is the upside here. Time is what you give up for it."* (upside/cost).

- **Метафоры (лимит 1–2 на статью):** найдено 2–3:
  1. *"patient as a parked car"* (открывающее сравнение)
  2. *"the label stuck around"* (лёгкая персонификация в разделе Telex)
  3. пограничный случай — *"on a desk somewhere"* (образный штрих)
  На грани допустимого, местами превышает верхнюю границу 2.

- **Литературные/яркие hook-предложения (лимит РОВНО 1):** найдено **минимум 2**:
  1. Открывающее предложение — *"A container can sit at the destination terminal for days, patient as a parked car, while somebody scrambles to find the one piece of paper that lets it leave."* — корректно расположено как единственный допустимый hook.
  2. Второй, лишний hook в середине текста — *"They start weeks earlier, on a desk somewhere."* — по структуре в точности повторяет паттерн, который сам скилл называет тревожным маркером (атмосферное, "литературное" предложение в разделе с иначе плоской деловой прозой).
  Это прямое превышение лимита "ровно 1".

**Вердикт: NEEDS-WORK** — сразу три хардовых нарушения: contrastive negation (3 против лимита 1), parallel twin-sentence conclusion, второй hook-sentence сверх лимита.

---

## (d) ФАКТИЧЕСКАЯ ДОСТОВЕРНОСТЬ — **NEEDS-WORK (КРИТИЧНО)**

Обнаружены **выдуманные конкретные детали/цифры**, которых нет в оригинале:

1. **Выдуманная длительность в открытии:**
   - Рерайт: *"A container can sit at the destination terminal **for days**..."*
   - Оригинал: *"Cargo can arrive at the destination port before the consignee is ready to collect it."* — никакой временной оценки в оригинале нет. **"For days" — придуманная цифра/срок.**

2. **Выдуманные детали "готовности" в открытии:**
   - Рерайт: *"Usually nobody forgot anything. The vessel **arrived on schedule**, **customs is ready**, **the truck is booked**."*
   - Оригинал: *"In many cases, the delay is not caused by the vessel, terminal, or customs."* — оригинал говорит только, что задержка НЕ вызвана этими факторами; рерайт добавляет конкретные утверждения о состоянии этих факторов ("прибыл по расписанию", "таможня готова", "грузовик забронирован"), которых источник не делает. **Придуманные детали сценария.**

3. **Выдуманная цифра "недель" как последствие потери/задержки оригинала B/L:**
   - Рерайт: *"...the cargo can arrive **weeks** before anyone's able to claim it, which is how demurrage and detention charges start piling up."*
   - Оригинал: *"...the cargo may arrive before the consignee can present the document. This can lead to storage, demurrage, detention, or missed delivery schedules."* — никакой временной оценки ("недели") в оригинале нет. **Придуманная цифра.**

4. **Выдуманное сравнение сроков в заключении — самая серьёзная фабрикация:**
   - Рерайт: *"Waiting until the cargo has already arrived turns a **five-minute decision** into a **multi-day scramble**."*
   - Оригинал: *"The release method should be agreed upon before booking, not after the cargo arrives."* — оригинал вообще не оперирует никакими временными оценками процесса принятия решения. Конкретные цифры "five-minute" и "multi-day" **полностью выдуманы** и придают тексту ложную видимость экспертной точности.

Остальной фактический контент (описание OBL/telex/express, чек-листы, примеры, список ошибок) — добросовестный перефраз без добавления новых механизмов, выгод или причинно-следственных связей.

**Вердикт: NEEDS-WORK, критично.** 4 случая внесения конкретных, ничем не подтверждённых числовых/временных деталей (days / weeks / five-minute / multi-day), что прямо запрещено правилом 11 skill'а ("no fabricated facts, numbers, causal explanations"). Особенно серьёзен случай #4 в Final takeaway — придуманное количественное сравнение, которого не может быть без явной ссылки в оригинале.

---

## ИТОГОВАЯ СВОДКА

| Слой | Вердикт | Ключевая причина |
|---|---|---|
| (a) Плагиат/сходство | **NEEDS-WORK** | ≥10 неэксемптных клоз скопированы почти дословно (8–14 слов подряд), включая целые предложения в примерах и CTA |
| (b) Словарные AI-маркеры | **PASS** | 0 em-dash, 0 клише, интро/аутро не пустые |
| (c) Структурные/риторические AI-тики | **NEEDS-WORK** | contrastive negation 3× (лимит 1), parallel twin-sentence conclusion, 2-й hook-sentence сверх лимита "ровно 1", структура всё ещё близко повторяет исходный шаблон |
| (d) Фактическая достоверность | **NEEDS-WORK (критично)** | 4 выдуманные конкретные детали/цифры (days/weeks/five-minute/multi-day), не подтверждённые оригиналом |

**Общий вывод: статья НЕ готова к публикации.** Требуется доработка минимум по трём из четырёх слоёв, в первую очередь — удаление выдуманных цифр (слой d, критично) и переписывание скопированных дословно предложений (слой a), плюс сокращение contrastive negation до 0–1 и удаление второго "литературного" hook-предложения (слой c).
