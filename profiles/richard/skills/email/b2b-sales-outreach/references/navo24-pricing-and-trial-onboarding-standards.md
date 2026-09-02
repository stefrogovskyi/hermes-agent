# Navo24 Commercial Pricing & Trial Onboarding Standards

Official pricing, documentation endpoints, and onboarding mechanics for Navo24 sales representatives and Account Executives.

---

## 1. Official Starter Tier Pricing (Up to 25 Shipments)

- **Service**: Container Tracking
- **Type**: API connection (REST JSON & MCP)
- **Limitation**: 1 to 25 unique shipments per calendar month
- **API Calls Allowance**: 750 calls per calendar month
- **Cost**: **USD 50 / month** or **USD 500 / year**
- **Licensing**: No separate API license fee on top of the tracking plan.

### Shipment Counting & Quota Logic:
- **Input Types**: Container Number, Master Bill of Lading (B/L), Booking Number.
- **Unique Shipments**: The same unique shipment is counted **once within the calendar month**, even if updates are queried multiple times during that month.
- **API Calls**: Repeated status queries consume API calls from the 750 monthly allowance but do NOT incur extra shipment charges.
- **Webhooks**: Included in the subscription at no additional cost.

---

## 2. Official Trial Onboarding Flow

1. **Signup URL**: `https://trackingmcp.com/auth/signup`
2. **Onboarding Message Script**:
   > *"Please register at: https://trackingmcp.com/auth/signup. Once the account is created, send me the email address used for registration and I will arrange the trial credentials for you."*
3. **Documentation Reference Links**:
   - **Ocean Tracking API Docs**: `https://navo24.com/developers/reference/tracking/`
   - **Ocean Schedules API Docs**: `https://navo24.com/developers/reference/schedules/`

---

## 3. Mixed Volume Handling (Ocean + Air Cargo)

- **Rule**: When prospects indicate mixed volume (e.g., 150 containers + Air Cargo), do NOT guess cents-per-container or lump-sum rates.
- **Qualification First**: Ask the prospect to specify their approximate monthly volume of **Air AWBs** before issuing the formal pricing proposal.
- **Competitor Cost-Optimization Hook**: Position against legacy annual lock-ins (ShipsGo, project44) emphasizing flexible monthly billing and zero annual lock-ins.
