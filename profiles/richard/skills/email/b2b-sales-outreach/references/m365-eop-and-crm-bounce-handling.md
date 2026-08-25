# Microsoft 365 EOP Outbound Anti-Spam & CRM Bounce Handling Guide

## Overview

When conducting B2B cold email outreach via Microsoft 365 (Exchange Online) mailboxes (e.g. `rich@navo24.com`), Exchange Online Protection (EOP) applies outbound heuristic rate limits and spam filters.

If a single mailbox sends repetitive cold outreach emails at high velocity (e.g., 60-second intervals with template-heavy content), EOP flags the account for **Outbound Spam** and generates non-delivery reports (NDRs) for all outgoing messages.

## 1. M365 Outbound Block NDR vs. True Recipient Bounce

It is CRITICAL for inbound email pollers and CRM integrations to distinguish between internal sender blocks and true recipient bounces:

### A. Internal M365 Sender Block (`550 5.1.8`)
- **Error Code / Keywords**: `550 5.1.8 Access denied, bad outbound sender AS(42004)`, `was not recognized as a valid sender`, `suspected of sending spam`.
- **Root Cause**: THIS IS AN ISSUE ON OUR SIDE (`rich@navo24.com`). The recipient's email address is valid, but Exchange Online refused to deliver the message because OUR sender account was temporarily flagged by EOP.
- **CRM Action**: **DO NOT DELETE OR MARK AS BOUNCED IN CRM!** Doing so destroys valid lead records.
- **Resolution**:
  1. Unblock the account in Microsoft Defender (`https://security.microsoft.com/restrictedusers`).
  2. Implement 100% dynamic AI-generated text variations (unique subjects, greetings, intros, and CTAs) so no two emails look identical.
  3. Increase send delay to 300 seconds (5 minutes) per message (~10–12 emails/hour).
  4. If records were mistakenly deleted, parse the Inbox NDR headers, extract the recipient email addresses, and restore them back to Airtable CRM as `Lead`.

### B. Tenant-Level Outbound Restriction (`550 5.7.708`) & Direct PowerShell / Admin Unblock
- **Error Code / Keywords**: `550 5.7.708 Service unavailable. Access denied, traffic not accepted from this IP`, `AS(7230)`, `traffic not accepted from this IP`.
- **Root Cause**: Microsoft Exchange Online temporarily restricted the tenant's outbound IP pool due to high send velocity or outbound spam policy threshold tripping (`BlockUserForToday`), or automated Graph API sends from datacenter IPs using deprecated ROPC (Password Grant) instead of Azure App OAuth2 Client Credentials.
- **Why First-Line Support Finds Nothing in Admin Center**: First-tier Microsoft support typically checks `Restricted Entities / Restricted Users`. Since the mailbox itself is clean and uncompromised, no blocks show in the UI. `5.7.708 AS(7230)` is a tenant-level EOP backend transport suppression.
- **Why It Does NOT Clear Automatically (Even After 8+ Hours)**: EOP IP pool blocks are persistent tenant-level transport quarantine flags that do not expire on a simple overnight timer without explicit administrative action or automated delisting.
- **Resolution Options**:
  1. **Azure App Registration (OAuth2 Client Credentials)**: Upgrade authentication from username/password (ROPC) to OAuth2 `grant_type: client_credentials` using registered App `Rich email graph inbox api` (`807fed17-45a8-4c7c-9a28-5997bbd30970`) with Application permissions `Mail.Send` and `Mail.ReadWrite`.
  2. **Microsoft Support Escalation Template**:
     * Escalate directly to **Tier 2 / Exchange Online Delivery Engineering (EOP Escalation Team)**.
     * State clearly: *Request to lift `550 5.7.708 AS(7230)` Outbound Suppression / IP Exemption for Tenant `dc47c5b1-313f-47eb-ab6f-5f0716f400b5` (navo24.com).*
  3. **Microsoft 365 Admin Center Automated Diagnostic Unblock**:
     * Open `https://admin.microsoft.com` -> Click **Help & support** -> Search `550 5.7.708` / `Diag: Outbound Email Blocked` -> Click **"Request Delist / Clear IP Throttle"**.
  2. **PowerShell Direct Anti-Spam Policy Update & Unblock**:
     ```powershell
     Install-Module -Name ExchangeOnlineManagement -Force
     Connect-ExchangeOnline

     # Enable tenant customization if restricted
     Enable-OrganizationCustomization

     # Remove user block if present
     Remove-BlockedSenderAddress -SenderAddress rich@navo24.com

     # Switch outbound anti-spam policy from BlockUserForToday to Alert and raise hourly/daily limits
     Set-HostedOutboundSpamFilterPolicy -Identity "Default" `
         -RecipientLimitExternalPerHour 1000 `
         -RecipientLimitInternalPerHour 1000 `
         -RecipientLimitPerDay 10000 `
         -ActionWhenThresholdReached Alert
     ```
  3. **Immediate Failover Routing via Resend API (`sales@e.navo24.com`)**:
     * When M365 outbound is blocked and urgent lead replies cannot wait for Microsoft delisting replication:
     * Route emails via Resend REST API (`POST https://api.resend.com/emails`) using `from: "Richard Marlowe <sales@e.navo24.com>"` and `reply_to: "rich@navo24.com"`.
     * This achieves 100% immediate delivery while routing all customer replies straight back to Richard's Microsoft 365 inbox.
  * **Critical Replication Delay (15–45 Minutes)**: Exchange Online Protection (EOP) edge filtering clusters take **15 to 45 minutes** to propagate policy updates and clear IP-pool restrictions.
  * **5-Minute Outbound Cadence**: When retrying messages or sending qualified 1-on-1 replies to multiple recipients, enforce a **5-minute (300s) delay** between dispatches to mimic natural human behavior and prevent re-triggering EOP outbound anomaly detectors.

### C. True Recipient Bounce (`550 5.1.1`)
- **Error Code / Keywords**: `550 5.1.1 User unknown`, `Host not found`, `Mailbox disabled`, `Recipient address rejected`.
- **Root Cause**: The client's email address does not exist or their mail server rejected the domain.
- **CRM Action**: Safe to delete or mark as `Bounced` in Airtable CRM.

## 2. Mailbox Routing & Aliases (`rich@navo24.com` vs `richard@navo24.com`)
- Primary M365 Mailbox: `rich@navo24.com`.
- If an outreach campaign sets `Reply-To: richard@navo24.com`, incoming replies will bypass `rich@navo24.com` unless `richard@navo24.com` is explicitly configured as an Exchange proxy alias on the mailbox.
- Standard convention: Always set `Reply-To: rich@navo24.com` for direct delivery to Richard's active M365 inbox.

## 2. Inbound Poller Guardrail Pattern (`check_inbound.py`)

Inbound email polling scripts MUST include explicit exception handling for M365 internal blocks:

```python
if "undeliverable" in subject.lower() or "退信" in subject or "microsoftexchange" in from_email or "postmaster" in from_email:
    # Check if it's an internal M365 block (OUR side issue, DO NOT delete from CRM!)
    is_m365_internal_block = any(p in body.lower() for p in [
        "550 5.1.8", "bad outbound sender", "was not recognized as a valid sender", 
        "suspected of sending spam", "access denied, bad outbound sender"
    ])
    if is_m365_internal_block:
        print(f"Skipping CRM auto-delete: M365 Internal Block for {subject}")
        continue
        
    # Only delete if it's a true recipient bounce
    matches = re.findall(r'message to ([a-zA-Z0-9\.\_\%\+\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,})', body, re.I)
    for m_email in matches:
        auto_delete_bounced_record(m_email)
```

## 3. Distribution Lists vs. Shared Mailboxes in M365

- **Distribution Lists (Groups)**: Function strictly as mail-routing pipelines. They do NOT have a underlying physical mailbox database. Messages sent to a Distribution List when external senders are blocked (`RequireSenderAuthenticationEnabled = $true`) are dropped at the transport layer and CANNOT be retroactively "pulled" or "claimed".
- **Auditing Blocked Mail**: To recover visibility into who tried to email a blocked Distribution List, use **Exchange Admin Center (`admin.exchange.microsoft.com`) -> Reports -> Message Trace** filtered by `Rejected/Failed`.
