# B2B Sales Outreach: 4-Touch Sequence, Formatting & Threading Rules

Complete specification of the 4-touch sequence strategy, email formatting, threading mandates, approval notification standards, and Exchange DL handling.

---

## 1. The 4-Touch Outreach Sequence (Exact Templates)

### Touch 1: Short Catchy Hook (Емейл 1)
- **Purpose**: High-response hook to qualify if the Chinese forwarder handles container ocean freight.
- **Russian Original**:
```text
Здравствуйте, [Имя/Компания]! 

Это Ричард из Navo. Ваши контакты мы получили от наших коллег в логистике как сильного агента в Китае для контейнерных и других видов перевозки. Это правильно?
```
- **Chinese Translation**:
```text
[Contact Person] 您好！

我是来自 Navo 的 Richard。我们从物流领域的同行处获得了您的联系方式，了解到贵司（[Company Name]）在中国是非常有实力、擅长集装箱及多种运输模式的强力代理。请问信息准确吗？


Richard Marlowe
Connections Manager | Navo24
+44 203 440 9800 | rich@navo24.com
30 St Mary Axe, London, EC3A 8BF | www.navo24.com
```

### Touch 2: Qualification & Dialogue (Емейл 2)
- **Purpose**: Deepen dialogue upon positive response to Touch 1.
- **Exact Russian Template**:
```text
Понятно, спасибо! 

Уточните пожалуйста, с какими судоходными линиями вы работаете? 
Есть ли среди ваших клиентов известные китайские или мировые бренды?
Расскажите о ваших сильных сторонах, где самые лучшие ставки у вас?
Какой примерный объем перевозок в контейнерах или тоннах вашей компании за год?
```

### Touch 3: Decision-Maker (LPR) Clarification (Емейл 3)
- **Purpose**: Identify who to negotiate with for digital rate stream integration.
- **Exact Russian Template**:
```text
Принято, спасибо! 

По поводу сотрудничества и интеграции Вашей компании в нашу экосистему, подскажите общаться с Вами или с Вашим боссом?
```

### Touch 4: Full Early Bird Value Proposal (Емейл 4)
- **Purpose**: Present the full ecosystem offer once qualified.
- **Exact Russian Template**:
```text
Отлично 

Мы работаем с экспедиторскими компаниями через принципиально новую экосистему для цифровой логистики, которая приходит на смену известным, но технически устаревшим платформам вроде SeaRates和物流网络。 

我们知道，中国货代拓展国际市场与自动化销售非常重要。因此，我们诚邀贵司成为早期合作伙伴（Early Bird）。

What your company gets with Navo:
- Полное обновление вашего сайта: Бесплатный современный концепт和设计。
- Онлайн-калькулятор фрахта: Умный виджет на ваш сайт用于 24/7 在线报价。
- Автоматический трекинг грузов: 实时查询轨迹（230+ 容器船公司）。
- Объединенная глобальная сеть тарифов: 向全球推介您的优势运价，并获取其他国家货代的本地运价。

Exclusive Offer: 3 个月免费试用期（含网站升级与在线运价平台）。

如果您有兴趣 — Дайте знать, мы пришлем инструкцию в 3 простых шага или проведем короткий созвон.
```

---

## 2. Formatting & Signature Mandates

1. **Top Spacing**: NO extra paragraphs or blank lines at the very top of the email body text.
2. **Pre-Signature Spacing**: Exactly 1 extra blank line (`<br><br>`) before the signature block.
3. **No Horizontal Divider**: Do NOT use `border-top` / `<hr>` above the signature.
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

---

## 3. Threading & Quoting Mandate for 1-on-1 Replies

For every 1-on-1 email reply sent to a client:
1. **Headers**: Set `In-Reply-To` and `References` to the client's `msg_id` / `internetMessageId`.
2. **Subject**: Keep the exact original subject with `Re: ` prefix.
3. **Quoted History**: Append quoted original email history below Richard's signature:
```html
<br><br>
<div style="border-left: 2px solid #0000FF; padding-left: 12px; margin-top: 20px; color: #555555; font-size: 9.5pt;">
  <p style="margin: 0 0 6px 0; font-weight: 600; color: #333333;">----- Original Message -----</p>
  <div>[Original Client Message Body]</div>
</div>
```
This guarantees Outlook and all email clients thread the reply inside the existing conversation.

---

## 4. Telegram Approval Notification Mandate

Whenever a new client email arrives, present Stefan with:
1. 👤 **Sender & Company**
2. 💬 **Client's Original Message**
3. 🇷🇺 **Full Russian Translation of Client's Message**
4. ✍️ **Proposed Draft Reply (Chinese)**
5. 🇷🇺 **Full Russian Translation of Proposed Draft Reply**
6. **No Interruptive Pollers**: Reply in clean, direct plain text. Never interrupt conversation flow with interactive choice widgets.

---

## 5. Email CC Mandate & Exchange DL Handling

- **Mandatory CC List**: Always CC `sales@navo24.com`, `lxxmng@navo24.com`, and `stefan@navo24.com`.
- **Distribution List (DL) Quirk**: Exchange DLs (like `sales@navo24.com`) do NOT store or queue messages when external senders are blocked; blocked messages are dropped at the transport layer.
- **Restricted Sender Unblock**: If Microsoft Defender blocks outbound email (`550 5.1.8 Access denied, bad outbound sender AS(42004)`), unblock the account at:
  `https://security.microsoft.com/restrictedentities`
- **Backfilling Past Emails**: To pull past sent outreach messages into `sales@navo24.com` after unblocking, resend or forward from `rich@navo24.com`'s Exchange `Sent Items` folder via Graph API.
