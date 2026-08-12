# B2B Contract Drafting & Vercel Kanban Management Rules

## 1. B2B Commercial Agreement & Contract Drafting Rules

When generating B2B client contracts or commercial agreements (such as for Navo24 / Wemelogistics LTD):

1. **Parties & Signatory Details**:
   - **Service Provider**: WEMELOGISTICS LTD (UK Company Number: `14081751`, registered at 1 Robin Hood House, Kingston Vale, London, SW15 3AL), represented by Director **Oleksii Shatunov** ("Wemelogistics" / "Provider" / "Navo24").
   - **Client**: [Client Company Name] ("Client").

2. **Order of Precedence (Critical Clause)**:
   - Always include an explicit Precedence Clause: "This Agreement comprises Part 1 (Commercial Offer & Special Conditions) and Part 2 (General Terms and Conditions of Use). In the event of any conflict, discrepancy, ambiguity, or contradiction between the terms set forth in Part 1 and Part 2, the terms set forth in **Part 1 (Commercial Offer & Special Conditions)** shall strictly prevail and govern."

3. **Bilateral B2B Formulations (No Unilateral Website Terms)**:
   - Convert unilateral B2C website disclosures ("We reserve the right to amend these terms at any time", "We may periodically update the site") into formal mutual B2B agreement terms:
     - *Clause 5.1 (Changes to Terms)*: "The Parties agree that the Provider may, at its discretion, update or amend these Terms to reflect regulatory changes or platform optimizations, provided that the Provider gives the Client prior written notification or publishes updated terms on the Platform..."
     - *Clause 5.2 (Changes to Platform)*: "The Client acknowledges and agrees that the Provider may, at its discretion, periodically update, enhance, alter, or refresh the content, features, and functionality of navo24.com and associated Digital Solutions..."
     - *Clause 10.3 (Fee Adjustments)*: Require at least thirty (30) days' prior written notice for renewal rate adjustments.

4. **Numbered Subheadings & Section Formatting**:
   - Section 4 (`Supplementary Policies`) MUST contain distinct, bold, numbered subheadings (`4.1 Privacy Policy`, `4.2 Membership / Service Agreements`) with paragraph breaks.
   - All clauses in Part 2 MUST maintain clean numbered subheadings (`1.1`, `1.2`, `2.1`, `2.2`, `4.1`, `4.2`, etc.).

5. **PAYG Commercial Logic**:
   - Pricing Model: Pay As You Go (PAYG) based on unique shipments tracked / API calls executed.
   - Calculation Window: Calculated from the Subscription Activation Date through the end of that relevant calendar month (e.g., 1 Sep – 30 Sep, or 15 Sep – 30 Sep for mid-month start).
   - Invoicing & Payment: Invoices issued monthly in arrears; payment due Net 14 calendar days from invoice date. All fees exclusive of VAT and intermediary bank transfer fees.

---

## 2. Vercel Kanban Board & UI Formatting Rules

When creating or managing agent Kanban boards (e.g. `richard-kanban.vercel.app`):

1. **Hosting Rule**:
   - Agent Kanbans MUST be deployed EXCLUSIVELY to Vercel (`https://<agent>-kanban.vercel.app`).
   - NEVER deploy or host Kanban boards on the primary production domain `aavalanche.com/kanban/`. If a board exists on `aavalanche.com/kanban/` or an outdated Vercel URL (e.g., `richard-marlowe-kanban.vercel.app`), remove it via Vercel CLI (`vercel remove`) and SSH (`rm -rf /home/u473746908/domains/aavalanche.com/public_html/kanban/<agent>`).

2. **UI & Layout Preferences**:
   - **Floating Add Button**: Do NOT include a floating bottom-right "+ Add Task" button if requested by user; keep the header button (`+ Новая Задача`).
   - **Interactive Card Modals**:
     * Make every card clickable (`onclick="openCardDetailModal(cardId)"`).
     * Clicking a card opens a modal displaying: Card Title, Column Status, Tag, Assignee, Creation Date, Description, **Activity History / Chronology**, and **Interactive Comments Section** (stored in `LocalStorage`).
   - **Escape Key Modal Dismissal**:
     * Add a global Escape key event listener to close all open modals:
       ```javascript
       window.addEventListener('keydown', (e) => {
         if (e.key === 'Escape') {
           closeNewModal();
           closeDetailModal();
         }
       });
       ```
