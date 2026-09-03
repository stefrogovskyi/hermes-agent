import re

orig = """How Proration Can Help Your International Logistics Startup

Startups emerge yearly to try their fortunes in the global market; unfortunately, 90% of startups fail to succeed in this highly competitive market. A vital reason for this rate of failures in this highly customer-centric era can be poor customer experience, such as not receiving items on time or having them damaged.
At some point in the business world, you can “dish out” anything to your customers, and they will swallow it line, hook, and sinker. The customer now has a choice of voice and logistics options.
International delivery and logistics startups, especially involving cargo transportation, that came on board then possibly didn’t have much competition and could survive easily; the global village has changed the setting, and every logistics business needs to buckle up for survival and must consider proration as part of its next logistics digital transformation.
The incentives you have for your customers include proration, deciding your customer conversion rate, customer retention, and, ultimately, customer experience.

What is the international logistics proration process?
Sometimes, people or businesses pay ahead of time for a service, like shipping goods from one country to another. But what happens if they stop before the service is complete? That’s where proration becomes essential.
Proration means calculating the amount of service used and the amount of money to be returned based on the finances involved. For example, if a company pays for a whole month of shipping services but only uses them for half the month, proration helps calculate exactly how much money it should get back for the time it didn’t use.
This point is important because if people think charges are unfair, they might get upset and choose a different shipping company next time. They might even say bad things about the company to others, which could hurt its reputation.
It’s also helpful when businesses make changes, like upgrading to faster delivery during the middle of the service period. Proration ensures they only pay for the upgrade starting when they change.
Good companies explain proration clearly so their customers know what to expect. They might use emails, customer service chats, or messages on their website to help people understand. When customers feel things are fair, they trust the company more and are happy to return or tell others about the good service they received.

Proration formula for international logistics
Like most economic strategies you can use for your startup to survive, you can use the formula below to calculate proration for international logistics and use this as a measure of success:
(Total Amount a Customer uses the Product or Service ÷ Total Number of Days You have Delivered the Product or Service) × Proration Period = Prorated Payment
Let’s assume your customer has used your logistics tracking service for 20 days and decides to unsubscribe to calculate the amount you must pay back within a 30-day month while the service costs $200. Since the customer used the service for only 20 days, the proration period is just 20 days.
You calculate the cost for this partial use of the subscription by dividing the total cost of the product or service that is $200 by 30 days, then multiply it by 20 days:
(200 ÷ 30) x 20 = $133.3.
Your logistics startup only needs to bill the customer $133.3 instead of $200 and refund the balance since that is the actual service you rendered. People view proration differently; you can calculate it for the amount customers have paid for goods and services they can use during part of a billing cycle.
You can also use it to describe the process of adjusting payments clients owe your organization for using your services or products over a given period.
An organization that is a subscription-based business can operate either the partial month or year proration system.
If your startup wants to operate on the partial month proration, you divide the total number of days your customer has used your product or service by the total number of days in a billing cycle; you then multiply your result by the total cost of goods or services to calculate the correct amount you need to balance to the customer.
For a partial-year proration, consider the number of days a customer has used during the year instead of a monthly billing cycle. Your startup uses this method to determine the amount you owe for services or products your customers did not use for the entire year.

Conclusion
Summing up, proration can be a valuable tool for a logistics startup to determine customers who pay for only what they use and enable the organization to calculate deferred revenue that it may have to refund.
However, proration must be transparent if your customers see it as a tool to vouch for your startup. A transparent proration will improve customer service, customer conversion, and retention for your logistics startup, allowing permanent growth, unlock funds for innovation and promote sustainability."""

rewrite = """Title: Prorated Billing Strategies for International Logistics Startups

Meta Title: Prorated Billing for International Logistics Startups

Meta Description: Learn how prorated billing for logistics helps international startups adjust subscriptions, build trust, and calculate partial charges accurately.

### Body:

Approximately 90% of startups fail when entering the competitive global market. Poor customer experience, such as delayed deliveries or damaged goods, frequently drives clients to alternative providers. Modern cargo shippers expect flexible financial terms alongside reliable physical transit. Offering adaptable billing models provides growing logistics companies with a strong foundation for customer retention.

## Understanding the International Logistics Proration Process

Clients often pay upfront for long-distance transportation or tracking tools. Questions arise when service stops early or shipping requirements shift mid-period. Proration solves these mid-cycle adjustments by calculating exact service usage and issuing proportional refunds or fee adjustments.

For instance, a client pays upfront for a full month of cargo tracking but cancels after twenty days. Proration determines the exact monetary value of those unused ten days and returns the balance. Without fair calculations, clients perceive unrefunded charges as unjust, which harms brand reputation and prompts word-of-mouth criticism.

Mid-contract service changes also require financial adjustments. When a company upgrades to accelerated delivery halfway through a billing window, prorated billing for logistics guarantees that the higher rate applies only to the remaining active days. Explaining these terms clearly through email, customer service chat, or website notices builds long-term client confidence.

## Calculating Proration with Precision

Logistics firms manage SaaS subscription adjustments and partial-period cargo tracking billing by applying a straightforward formula:

(Total Amount a Customer uses the Product or Service ÷ Total Number of Days You have Delivered the Product or Service) × Proration Period = Prorated Payment

Suppose a customer uses a logistics tracking service for 20 days during a 30-day month before unsubscribing, with the monthly service costing $200. Because the customer used the service for 20 days, the proration period equals 20 days. 

Dividing the $200 total cost by 30 days and multiplying the result by 20 days gives the required charge:

(200 ÷ 30) × 20 = $133.30

The logistics startup bills $133.30 instead of $200 and refunds the remaining balance. This process accurately reflects the service rendered during part of a billing cycle.

## Structuring Partial-Month and Partial-Year Systems

Subscription-based logistics companies implement either partial-month or partial-year proration frameworks depending on contract structure:

1. **Partial-Month Proration:** Divide the total number of days a customer used the product or service by the total number of days in the monthly billing cycle, then multiply by the total cost to determine the precise payment amount.
2. **Partial-Year Proration:** Measure the number of days a customer used the service during the full year rather than a monthly cycle. Startups use this calculation to determine amounts owed for unused annual services.

Adopting clear proration models gives clients confidence that they pay only for what they consume. Transparent accounting improves customer conversion, boosts freight forwarder billing retention, and stabilizes deferred revenue for long-term growth."""

# Let's find maximum contiguous word sequences that match between orig and rewrite
def find_maximal_matches(orig_text, rewrite_text, min_len=6):
    def clean_tokens(text):
        # returns list of (token, original_case)
        words = re.findall(r'\b[a-zA-Z0-9$%÷×+=–-]+\b', text)
        return words

    orig_tokens = clean_tokens(orig_text)
    rewrite_tokens = clean_tokens(rewrite_text)
    orig_lower = [w.lower() for w in orig_tokens]
    rewrite_lower = [w.lower() for w in rewrite_tokens]

    maximal_matches = []
    
    i = 0
    while i < len(rewrite_lower):
        max_match_len = 0
        best_orig_idx = -1
        
        # Check all possible match lengths starting at rewrite index i
        for j in range(len(orig_lower)):
            match_len = 0
            while (i + match_len < len(rewrite_lower)) and (j + match_len < len(orig_lower)) and (rewrite_lower[i + match_len] == orig_lower[j + match_len]):
                match_len += 1
            if match_len >= min_len and match_len > max_match_len:
                max_match_len = match_len
                best_orig_idx = j
                
        if max_match_len >= min_len:
            matched_phrase = " ".join(rewrite_tokens[i:i+max_match_len])
            maximal_matches.append((i, best_orig_idx, max_match_len, matched_phrase))
            i += max_match_len # jump ahead
        else:
            i += 1
            
    return maximal_matches

print("--- MAXIMAL CONSECUTIVE WORD MATCHES (6+ WORDS) ---")
matches = find_maximal_matches(orig, rewrite, 6)
for m in matches:
    print(f"Rewrite idx {m[0]}, Orig idx {m[1]}, Len {m[2]}: \"{m[3]}\"")

