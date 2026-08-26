# International DTAA Tax Exemption & Word Comment Integration Guide

## 1. DTAA Tax Withholding Framework (UK–India & International)
For UK companies (`WEMELOGISTICS LTD`) billing Indian or cross-border clients:

- **Withholding Rate Default:** 20% to 25% TDS under Section 195.
- **Treaty Exemption (0% TDS):** Claimed under Section 90(2) using the UK-India Double Taxation Convention.
- **Substantive Ground:** Article 7 (*Business Profits*) read with Article 5 (*Permanent Establishment*).
- **Landmark Precedent:** *Engineering Analysis Centre of Excellence Pvt. Ltd. v. CIT* (Supreme Court of India, 2021). Standard API/SaaS subscriptions without transfer of source code or copyright are NOT Royalties (Article 12) or Fees for Technical Services (FTS), but Business Profits.
- **Required 4-Piece Dossier:**
  1. Certificate of Residence / TRC from HMRC for the active FY.
  2. Duly signed Form 10F (under Rule 21AB).
  3. No Permanent Establishment (No-PE) & Beneficial Ownership Letterhead Declaration.
  4. Client-specific vendor withholding / remittance form (e.g. Form 41).

## 2. Microsoft Word In-Bubble Margin Comment Processing
When injecting legal responses into `.docx` files:
1. Extract `word/comments.xml` from the `.docx` archive.
2. Locate each counterparty `<w:comment w:id="N">`.
3. Append a separator `<w:p>` with `────────────────────────────`.
4. Append the response `<w:p>` with bold run `<w:b/>Navo24 (Harrison Croft, GC) Response: ` followed by the substantive legal counter-proposal.
5. Save and re-zip. This guarantees 100% visibility across all desktop, web, mobile, and dark-mode Word clients without relying on client-side threaded comment rendering.
