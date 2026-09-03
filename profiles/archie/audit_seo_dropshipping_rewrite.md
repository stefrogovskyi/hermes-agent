# Независимый 4-слойный аудит: рерайт SeaRates "SEO for Dropshipping 2026"

Метод: посегментное сравнение оригинал vs рерайт, n-грамм анализ (совпадения 6+ слов подряд), regex-сканы клише/связок/em-dash, подсчёт абзацев и структуры.

---

## (a) ПЛАГИАТ / СХОДСТВО — **NEEDS-WORK**

Автоматический скан n-грамм (6+ последовательных слов, не считая разрешённых терминов/брендов) нашёл **49 совпадающих фрагментов**. Большинство — короткие технические штампы (заголовки шагов "Step 1: Keyword Research for Dropshipping", списки инструментов, метрики Core Web Vitals), которые допустимы. Но есть минимум 6 фрагментов, которые являются почти дословным копированием целых предложений с точечной заменой 1–3 слов — это не пересказ, а косметическая перефразировка:

1. **Абз. про content-then-commerce (Step 4), 17 слов подряд совпадают:**
   - Ориг.: *"...to build a content site that happens to sell products, rather than a product site that happens to **have a blog**."*
   - Рерайт: *"...build a content site that happens to sell products, rather than a product site that happens to **run a blog**."*
   → Изменено одно слово ("have"→"run"), структура и 95% лексики идентичны.

2. **Первое предложение того же раздела Step 4, 16 слов подряд совпадают:**
   - Ориг.: *"This works for digital dropshipping specifically because it lets you rank for thousands of informational queries that **send buyers to your store at the moment they're investigating purchases**..."*
   - Рерайт: *"It works for digital dropshipping specifically because it lets you rank for thousands of informational queries that **put your store in front of buyers at the exact moment they're researching a purchase**..."*
   → 16 слов дословно идентичны, дальше лёгкая перефразировка ("investigating purchases"→"researching a purchase").

3. **Digital Gratified — абзац описания агентства, 15 слов подряд:**
   - Ориг.: *"Digital Gratified **specializes in SaaS and tech, and their editorial-only approach** (no PBNs, no link farms) **is exactly what** dropshipping stores need to avoid the Google penalties that have killed entire stores overnight."*
   - Рерайт: *"Digital Gratified **works mostly in SaaS and tech, and their editorial-only approach**, no PBNs, no link farms, **is precisely what** keeps a store off the wrong side of a Google penalty that can kill it overnight."*
   → Синонимическая замена ("specializes in"→"works mostly in", "is exactly what"→"is precisely what"), но структура предложения, порядок фактов, скобочная вставка "no PBNs, no link farms" и финальный смысл-клоз полностью скопированы.

4. **Guest posting абзац (Step 5)** — фраза *"Pitch original articles to [publications/sites covering] your product category, outdoor gear, home decor, fitness, whatever your niche [is/happens to be]"* — 11 слов подряд идентичны, весь абзац структурно калька оригинала предложение-в-предложение.

5. **Long-tail keyword пример** — *"best X under $50 for [specific use case]"* (11 слов) скопирован целиком в кавычках — простительно, т.к. это иллюстративный пример-шаблон, но в сочетании с остальными совпадениями усиливает общую картину.

6. **Schema markup абзац** — *"Product schema with price, availability, ratings, and review count [gets you/earns] rich snippets in [SERPs/the SERPs]"* (11 слов совпадают дословно).

**Вывод по (a):** это не плагиат в смысле полного копипаста, но минимум 4–5 предложений (в разделах Step 4 и Step 5, включая ключевой абзац про Digital Gratified) являются "close paraphrase" на грани допустимого — synonym-swap уровня "find & replace", а не независимое переосмысление. Структура абзацев, порядок аргументов и даже пунктуация (вводные вставки через запятую) скопированы почти 1:1 по всей статье. Итоговая архитектура текста (порядок разделов, все H2/H3 заголовки, порядок буллетов внутри разделов) полностью идентична оригиналу — это ожидаемо для рерайта, но в сочетании с точечными предложениями-кальками риск для detection-инструментов (Copyscape/Originality.ai similarity score) реален.

**Рекомендация:** переписать абзацы Step 4 (первые два предложения) и Digital Gratified в Step 5 более свободно — сменить структуру предложения, не только синонимы.

---

## (b) СЛОВАРНЫЕ AI-МАРКЕРЫ — **PASS**

- Em-dash (—): **0**
- En-dash (–) отдельно как тире: **0**
- Двойной дефис (--): **0**
- Классические AI-клише — проверено по списку (`it's important to note`, `in today's world`, `dive into`, `unlock the potential`, `testament to`, `seamless`, `delve into`, `game-changer`, `in conclusion`, `navigate`, `robust`, `leverage the power`, `paradigm shift`, `moreover`, `furthermore`, `crucial`, `pivotal`, `landscape`, `ever-evolving`, `harness`, `empower`, `elevate`, `streamline`, `cutting-edge`, `holistic`) — **0 совпадений** по всему тексту.
- Пустые интро/аутро фразы типа "In this article we will explore..." — отсутствуют, текст сразу входит в тему.

Разговорные усилители встречаются, но в разумных пределах и не выглядят как AI-тик: "actually" — 9 раз, "genuinely" — 3, "honestly" — 1, "full stop" — 1, "period," (в значении усиления) — 1. Это соответствует заявленному тону "straight talk" и не является чрезмерным.

**Вывод: слой чист, явных AI-словарных маркеров нет.**

---

## (c) СТРУКТУРНЫЕ / РИТОРИЧЕСКИЕ ТИКИ — **NEEDS-WORK**

1. **Порядок разделов** — рерайт сохраняет структуру оригинала 1:1 (Why → Step1..Step6 → Timeline → Final Word), включая порядок H2/H3. Это не собственная "слишком идеальная лестница" рерайтера — она унаследована от оригинала, поэтому как отдельный дефект рерайта не засчитывается, но косвенно подтверждает пункт (a): архитектура не переосмыслена.

2. **Connector-конструкции "that's why / which is why":** в рерайте — **1 случай** ("That's exactly why the handful who bother end up owning it.") — в пределах нормы, совпадает по частоте с оригиналом (тоже 1: "which is why the ones who don't, dominate").

3. **Contrastive negation ("X, not Y" / "instead of" в любом направлении):** обнаружено значительно больше лимита в 1 на статью:
   - "**not only** to a human scrolling results" (абзац AI search)
   - "**rather than** the two-word head term everyone else is chasing" (Step 1)
   - "**instead of** retrofitting fixes onto a generic template later" (Step 2)
   - "**instead of** fighting the foundation" (Step 2, тот же абзац — 2 подряд в одном месте)
   - "not the desktop version" / "**not just** the mobile ones" (Step 3, два в одном абзаце)
   - "**rather than** run a blog" (Step 4)
   - "**not just** a link request" (Step 5)
   - "**rather than** a quick arbitrage run" (Step 5)
   
   **Итого: минимум 8 конструкций типа "X, not Y / instead of / rather than"** — это в 8 раз превышает заявленный лимит "1 на статью". Для сравнения, в оригинале таких конструкций тоже несколько (rather than × 4, instead of × 1), то есть рерайт не только не сократил приём, а слегка увеличил его использование и добавил новые случаи, которых в оригинале не было (например, "not only to a human scrolling results", "not just the mobile ones", "not just a link request" — все три отсутствуют в оригинале как новые формулировки).

4. **Абзацы, заканчивающиеся звонкой афористичной фразой:** посчитано автоматически (короткие финальные предложения ≤14 слов) — **16 из 42** абзацев рерайта (38%) оканчиваются такой репликой, например:
   - "Fix whatever shows up red."
   - "Get the layout right early and everything below compounds instead of fighting the foundation."
   - "You're being more useful than Amazon at answering the question someone actually typed in."
   - "Twelve months in, the numbers will tell you whether you built something worth keeping."
   Это высокая доля, хотя оригинал показывает похожую или даже более высокую (26/50 = 52%) — то есть приём унаследован от оригинала и не является добавкой рерайтера сверх базового уровня. Тем не менее сам факт, что почти 4 из 10 абзацев рерайта заканчиваются "punchline"-фразой, создаёт заметный ритмический тик при чтении подряд.

5. **Symmetric antithesis / parallel twin-sentences:**
   - "**Content compounds. Ads don't.**" — двусоставная короткая антитеза (Step Why-раздел), прямая калька структуры оригинала ("Content compounds, ads don't." — там это уже было, просто разбито на два отдельных предложения точкой вместо запятой — усилен риторический эффект).
   - "**Digital dropshipping isn't dying in 2026. It's just growing up.**" (Final Word) — параллельная пара коротких зеркальных предложений: [Subject] isn't [X]. It's just [Y]. — прямая калька риторической структуры оригинала "Digital dropshipping in 2026 isn't dead, it's just professionalized" (там была запятая внутри одного предложения, в рерайте — искусственно разбито на два отдельных предложения, что делает антитезу ещё более "рубленой" и ритмически акцентированной, то есть рерайтер не убрал, а усилил этот тик).
   - "A search engine can't rank a page it can't crawl, render, or trust, **full stop**." / далее по тексту "Mobile-first indexing means Google is looking at your mobile site, **period**, not the desktop version." — оба явно добавленные (в оригинале ни "full stop", ни "period," в этой функции нет) — это новый риторический тик, не унаследованный от оригинала, повторяется дважды в соседних разделах (Step 3), создавая заметный шаблон "короткое категоричное слово-отсечка в середине предложения".

**Вывод по (c):** connector "why" в норме, но contrastive negation используется примерно в 8 раз чаще заявленного лимита (частично унаследовано от оригинала, но рерайт добавил минимум 3 новых случая сверху), плюс два новых усиленных антитезиса ("Content compounds. Ads don't." / "isn't dying... just growing up.") и дважды повторённый новый тик "full stop / period," — риторические паттерны не сглажены, а местами усилены по сравнению с оригиналом.

---

## (d) ФАКТИЧЕСКАЯ ДОСТОВЕРНОСТЬ — **NEEDS-WORK (критично)**

Главная находка — абзац "AI search is rewarding..." (раздел "Why SEO Carries More Weight...") **разросся с 54 слов в оригинале до 162 слов в рерайте** (рост в 3 раза) и содержит минимум **пять новых фактических утверждений/терминов, отсутствующих в оригинале**:

1. **"Some people call this answer engine optimization, others say generative engine optimization."** — вводит два новых отраслевых термина (AEO, GEO) и утверждение об их синонимичности как "того же сдвига" — этого сопоставления терминов в оригинале нет вообще.

2. **"as zero-click search grows, meaning fewer people ever click through to a website at all"** — вводит новую метрику/тренд (zero-click search) с собственным причинно-следственным объяснением ("растёт → меньше кликов"), не упомянутую в оригинале.

3. **"citation frequency, how often AI systems name your brand as the source, is becoming its own kind of visibility"** — вводит новую метрику (citation frequency) как самостоятельный KPI, которого в оригинале нет.

4. **"It shows up in analytics as AI-referred traffic, and it's small right now but it isn't staying small."** — конкретное фактическое утверждение о поведении метрики в аналитике (что она "маленькая сейчас, но не останется маленькой") — это прогноз/причинно-следственное суждение, не подкреплённое оригиналом и вообще ничем не подкреплённое (ни ссылкой, ни цифрой).

5. **"The more agentic search tools mature, AI agents doing the browsing and even the buying on someone's behalf, the more it matters that your store reads clearly to a machine"** — вводит концепцию "агентного поиска" (AI-агенты browsing/purchasing) и делает causal-вывод об оптимизации "для машины" — целый новый механизм, придуманный рерайтером, отсутствующий в первоисточнике.

Всё это — **правдоподобно звучащие, но не прослеживаемые к оригиналу добавления**. Технически они не противоречат общеотраслевым знаниям про AEO/GEO, но задача была рерайтить, а не расширять фактическую базу источника новыми терминами, метриками и причинно-следственными конструкциями. Ни один из этих пяти пунктов не является просто "более развёрнутым описанием" уже присутствовавшего в оригинале термина — это новые, добавленные утверждения.

Прочие проверки на выдумывание:
- Числа (30%+ рост CAC, 2022–2024, 100 monthly searches, KD<30, 150 слов, 30 минут на schema, LCP/INP/CLS пороги, 70/20/10 split, месяцы 1-3/4-6/7-9/10-12) — все воспроизведены **точно**, без искажений и без добавления новых цифр. ✅
- "Winning Hunter", "Digital Gratified", "Google Search Console" и т.д. — упомянуты в тех же ролях, без добавления новых претензий/фактов о них. ✅
- В остальных разделах (Steps 1–3, 5–6, Timeline, Final Word) фактическое содержание сохранено без добавления новых механизмов — это разница именно локализована в одном AI-search-абзаце.

**Вывод по (d): NEEDS-WORK.** Абзац про AI-search — единственный, но серьёзный случай "фактического расширения" рерайта сверх оригинала: 5 новых непроверяемых терминов/утверждений (AEO/GEO эквивалентность, zero-click search механизм, citation frequency как метрика, прогноз роста AI-referred traffic, agentic search влияющий на оптимизацию "для машины"). Это нужно либо удалить, либо явно промаркировать как добавленный контент/экспертное мнение, не выдавая за пересказ источника.

---

## ИТОГОВАЯ СВОДКА

| Слой | Вердикт | Ключевая причина |
|---|---|---|
| (a) Плагиат/сходство | **NEEDS-WORK** | 4–5 предложений — close paraphrase на уровне synonym-swap (особенно Step 4 intro и абзац Digital Gratified); 49 n-граммных совпадений 6+ слов всего |
| (b) AI-словарные маркеры | **PASS** | 0 em-dash, 0 клише из чек-листа |
| (c) Структурные/риторические тики | **NEEDS-WORK** | Contrastive negation ~8 случаев (лимит 1); усиленная антитеза "Content compounds. Ads don't." и "isn't dying... just growing up."; новый повторяющийся тик "full stop / period," (2 раза) |
| (d) Фактическая достоверность | **NEEDS-WORK (критично)** | Абзац про AI search добавляет 5 непроверяемых новых терминов/утверждений (AEO/GEO, zero-click search, citation frequency, AI-referred traffic прогноз, agentic search) — рост с 54 до 162 слов |

**Общий вердикт: 3 из 4 слоёв требуют доработки.** Приоритет исправлений: (d) прежде всего — убрать или явно отделить добавленные факты в AI-search абзаце; затем (a) — переписать 4-5 калькированных предложений свободнее; затем (c) — сократить contrastive negation конструкции и убрать дублирующийся "full stop/period" приём.
