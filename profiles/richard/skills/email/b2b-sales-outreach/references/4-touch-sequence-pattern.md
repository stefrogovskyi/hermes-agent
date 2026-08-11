# B2B Sales Outreach: 4-Touch Sequence & Signature Rules

## 4-Touch Sequence Pattern for Chinese Freight Forwarders (CN FF)

When reaching out to cold B2B prospects (e.g. Chinese logistics operators, freight forwarders, NVOCCs), follow this exact 4-touch pattern:

### Touch 1: Short Catchy Hook (Емейл 1)
- **Goal**: Grab attention, establish relevance, and ask a short open question to gauge interest.
- **Tone**: Professional, direct, human.
- **Length**: Very short (2–3 sentences).
- **Exact Russian Template**:
```text
Здравствуйте, [Имя/Компания]! 

Это Ричард из Navo. Ваши контакты мы получили от наших коллег в логистике как сильного агента в Китае для контейнерных и других видов перевозки. Это правильно?
```
- **Chinese Translation**:
```text
[Contact Person] 您好！

我是来自 Navo 的 Richard。我们从物流领域的同行处获得了您的联系方式，了解到贵司（[Company Name]）是中国非常有实力、擅长集装箱及多种运输模式的强力代理。请问信息准确吗？
```

---

### Touch 2: Dialogue & Engagement (Емейл 2)
- **Goal**: Engage in consultative dialogue based on shipping lines, brands, strengths, and volume.
- **Exact Template**:
```text
Понятно, спасибо! 

Уточните пожалуйста, с какими судоходными линиями вы работаете? 
Есть ли среди ваших клиентов известные китайские или мировые бренды?
Расскажите о ваших сильных сторонах, где самые лучшие ставки у вас?
Какой примерный объем перевозок в контейнерах или тоннах вашей компании за год?
```

---

### Touch 3: Decision-Maker Clarification (Емейл 3)
- **Goal**: Identify the correct point of contact for integration/cooperation.
- **Exact Template**:
```text
Принято, спасибо! 

По поводу сотрудничества и интеграции Вашей компании в нашу экосистему, подскажите общаться с Вами или с Вашим боссом?
```

---

### Touch 4: Full Early Bird Value Proposal (Емейл 4)
- **Goal**: Present the full value proposition and callable tool suite.
- **Exact Template**:
```text
Отлично 

Мы работаем с экспедиторскими компаниями через принципиально новую экосистему для цифровой логистики, которая приходит на смену известным, но технически устаревшим платформам вроде SeaRates и логистическим нетворкам. 

Мы знаем, как важно для китайских экспедиторов масштабировать бизнес на международный рынок и автоматизировать продажи. Поэтому мы хотим предложить вам стать нашими партнерами на этапе раннего доступа (Early Bird).

Что получит ваша компания с Navo:
- Полное обновление вашего сайта: Мы бесплатно предоставим вам современный концепт и дизайн сайта, чтобы ваш бизнес выглядел технологично и привлекательно для глобальных клиентов.
- Онлайн-калькулятор фрахта: Вы сможете установить умный виджет на свой сайт和实时报价 24/7.
- Автоматический трекинг грузов: Ваши клиенты смогут в реальном времени видеть, где находятся их контейнеры, прямо на вашем ресурсе, с более чем 230 глобальными контейнерными линиями.
- И множество других ИИ-инструментов (включая MCP-модули для автоматизации).

Главная фишка Navo — Объединенная глобальная сеть тарифов: Вы сможете не просто автоматизировать свой сайт, но и продавать свои ставки по всему миру через нашу общую сеть.

Эксклюзивное предложение для вас: 3 месяца бесплатного тестового периода.

Если вам интересно — дайте знать, мы пришлем инструкцию в 3 простых шага как все сделать с Вашей стороны. Или можем показать, как это работает на коротком созвоне.
```

---

## Email Formatting & HTML Signature Rules

1. **Top Indent**: NO extra paragraphs or blank lines at the very top of the email body.
2. **Spacing before Signature**: Exactly 1 extra blank line (`<br><br>` / `margin-top: 24px`) before signature.
3. **No Horizontal Line**: Do NOT use `border-top` / `<hr>`.
4. **HTML Signature**:
```html
<div style="font-family: Tahoma, Arial, sans-serif; font-size: 10pt; color: #000000; line-height: 1.35; margin-top: 24px;">
  <b>Richard Marlowe</b><br>
  <b>Connections Manager</b><br>
  <div style="margin: 8px 0 10px 0;">
    <img src="https://bit.ly/4hLg86T" alt="navo" style="height: 35px; width: auto; display: block;" border="0">
  </div>
  API-MCP for Logistics &amp; Trade<br>
  +44 203 440 9800<br>
  <a href="mailto:rich@navo24.com" style="color: #0000FF; text-decoration: underline;">rich@navo24.com</a><br>
  30 St Mary Axe, London, EC3A 8BF<br>
  <a href="https://www.navo24.com" style="color: #0000FF; text-decoration: underline;">www.navo24.com</a>
</div>
```
5. **Sending Controls**:
   - 1-minute interval between consecutive emails in mass outreach.
   - Always CC team addresses: `lxxmng@navo24.com`, `stefan@navo24.com`.
   - Update Airtable record status to `Contacted` strictly record-by-record AFTER each email is actually sent out via SMTP.

## Inbound Email Poller, Russian Translation & Threading Mandate

To ensure proper conversation threading in Outlook/Gmail and full transparency for Stefan:
- **Thread Headers**: Always set `In-Reply-To` and `References` headers to the client's original `msg_id` / `internet_message_id`.
- **Exact Subject Preservation**: Keep the exact original subject prefixed with `Re: `.
- **Quoted History Below Signature**: Below Richard's signature, attach the quoted original message history (`----- Original Message -----`).
- **Russian Translation Mandate**: In all Telegram approval/notification drafts, ALWAYS provide Stefan with a clear Russian translation of BOTH the client's message and Richard's proposed draft reply.
- **Automatic Bounce Cleaning**: Parse Outlook `Undeliverable` or `退信` notices to extract recipient email addresses, auto-delete matching records from Airtable, and stay silent without alerting Stefan.
- **Mark as Read & Deduplication**: Mark fetched MS Graph messages as `isRead = True` and save IDs to `/opt/hermes/profiles/richard/processed_msg_ids.json` to prevent duplicate alerts.
