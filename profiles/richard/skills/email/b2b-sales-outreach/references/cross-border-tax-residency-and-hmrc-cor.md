# Cross-Border Tax Residency & HMRC Certificate of Residence (CoR / Form DGT)

Guidelines for handling international B2B client requests regarding Double Taxation Agreements (DTA), local Withholding Tax (WHT) waivers, and UK HM Revenue & Customs (HMRC) residency certification.

---

## 1. Background & Context

When billing international clients (e.g. Indonesia, ASEAN, APAC, South America), local tax regulations may require the client to deduct a **Withholding Tax (WHT)** (typically 10%–20%) from cross-border software/service invoices unless the UK service provider (**WEMELOGISTICS LTD**) provides a valid **Certificate of Residence (CoR)** under the applicable bilateral Double Taxation Agreement.

---

## 2. The HMRC Certification Dilemma: CoR vs. Form DGT (DGT-1)

When applying for certification through the UK Government HMRC portal:
- HMRC asks: *"Has [Country] given you a document to complete and send to HMRC to certify residence?"*
  * **Option A: "Yes, I already have a document"** ➔ Used when the client's tax authority mandates their specific local treaty form (e.g., **Indonesian Form DGT / DGT-1**) to be physically filled out and stamped/endorsed by HMRC.
  * **Option B: "No, I am requesting a certificate"** ➔ Used when the foreign tax office accepts the standard UK HMRC Certificate of Residence (CoR).

### Critical Rule: Never Guess
- If Option B is submitted and a standard UK CoR is issued, but the client's tax office strictly requires a stamped Form DGT, the document will be **rejected**, requiring a new application and an additional 2–4 week delay.
- Always press *"Save and come back later"* on the HMRC portal and clarify directly with the client's finance/tax team before completing the submission.

---

## 3. Standard Client Communication Template

When a client requests tax residency proof:
1. **Clarify Document Requirements**:
   - Ask whether their local tax authority requires their country-specific form (e.g., Form DGT) endorsed by HMRC, or if the standard UK HMRC CoR is sufficient.
   - Request their blank/template if a specific local form is required.
2. **Transparent Timelines (2–4 Weeks)**:
   - State clearly that UK HMRC processing takes 2 to 4 weeks (up to 6 weeks during peak periods).
3. **No-Block Technical Onboarding**:
   - Offer to issue the commercial invoice and activate their API production credentials immediately so their technical integration proceeds without delay while the tax certificate is being processed.
4. **Zero Administrative Markup**:
   - HMRC certificate issuance incurs £0 in statutory government fees; do not charge artificial "government fees" to the client.

---

## 4. Summary Matrix

| Scenario | Client Requirement | HMRC Selection | Action |
| :--- | :--- | :--- | :--- |
| **Local Treaty Blank Provided** | Stamped Form DGT / DGT-1 | *"Yes, I already have a document"* | Upload client form for HMRC official seal |
| **General Proof of Tax Residence** | Standard Certificate | *"No, I am requesting a certificate"* | HMRC generates standard UK CoR |
| **Uncertain / Not Specified** | Pending clarification | *"Save and come back later"* | Send clarification email to client finance desk |
