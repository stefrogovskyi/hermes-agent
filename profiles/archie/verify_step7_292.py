import re
import string

original_text = """
How Proration Can Help Your International Logistics Startup

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
However, proration must be transparent if your customers see it as a tool to vouch for your startup. A transparent proration will improve customer service, customer conversion, and retention for your logistics startup, allowing permanent growth, unlock funds for innovation and promote sustainability.
"""

revised_text = """Title: Prorated Billing Strategies for International Logistics Startups

Meta Title: Prorated Billing for International Logistics Startups

Meta Description: Learn how prorated billing for logistics helps international startups adjust subscriptions, build trust, and calculate partial charges accurately.

Approximately 90% of startups fail when entering the competitive global market. Poor customer experience, such as delayed deliveries or damaged goods, frequently drives clients to alternative providers. Modern cargo shippers expect flexible financial terms alongside reliable physical transit. Offering adaptable billing models provides growing logistics companies with a strong foundation for customer retention.

## Understanding the International Logistics Proration Process

Clients often pay upfront for long-distance transportation or tracking tools. Questions arise when service stops early or shipping requirements shift mid-period. Proration solves these mid-cycle adjustments by calculating exact service usage and issuing proportional refunds or fee adjustments.

For instance, a client pays upfront for a full month of cargo tracking but cancels after twenty days. Proration determines the exact monetary value of those unused ten days and returns the balance. Without fair calculations, clients perceive unrefunded charges as unjust, which harms brand reputation and prompts word-of-mouth criticism.

Mid-contract service changes also require financial adjustments. When a company upgrades to accelerated delivery halfway through a billing window, prorated billing for logistics guarantees that the higher rate applies only to the remaining active days. Explaining these terms clearly through email, customer service chat, or website notices builds long-term client confidence.

## Calculating Proration with Precision

Logistics firms manage SaaS subscription adjustments and partial-period cargo tracking billing by applying a straightforward formula:

(Total Subscription Fee ÷ Total Billing Days) × Active Usage Days = Final Prorated Charge

Suppose a customer uses a shipment monitoring plan for twenty consecutive days during a 30-day month before unsubscribing, with the monthly service costing $200. Because the client retained active access across 20 days, the proration period equals 20 days. 

Dividing the $200 total cost by 30 days and multiplying the result by 20 days gives the required charge:

(200 ÷ 30) × 20 = $133.30

The logistics startup bills $133.30 instead of $200 and refunds the remaining balance. This process accurately reflects the service rendered for a fraction of a billing timeframe.

## Structuring Partial-Month and Partial-Year Systems

Subscription-based logistics companies implement either partial-month or partial-year proration frameworks depending on contract structure:

1. Partial-Month Proration: Calculate active usage days as a fraction of the full monthly cycle, then multiply by the total cost to determine the precise payment amount.
2. Partial-Year Proration: Measure how many active days a client used the service during the full year rather than a monthly cycle. Startups use this calculation to determine amounts owed for unused annual services.

Adopting clear proration models gives clients confidence that they pay only for what they consume. Transparent accounting improves customer conversion, boosts freight forwarder billing retention, and stabilizes deferred revenue for long-term growth."""

# 1. Em-dash check
em_dashes = revised_text.count("—") + revised_text.count("--")
print(f"Em-dash count: {em_dashes}")

# 2. Meta lengths
title_match = re.search(r"Title:\s*(.*)", revised_text)
meta_title_match = re.search(r"Meta Title:\s*(.*)", revised_text)
meta_desc_match = re.search(r"Meta Description:\s*(.*)", revised_text)

title = title_match.group(1) if title_match else ""
meta_title = meta_title_match.group(1) if meta_title_match else ""
meta_desc = meta_desc_match.group(1) if meta_desc_match else ""

print(f"Title ({len(title)} chars): {title}")
print(f"Meta Title ({len(meta_title)} chars, limit 60): {meta_title}")
print(f"Meta Description ({len(meta_desc)} chars, limit 155): {meta_desc}")

# 3. N-gram overlaps
def get_ngrams(text, n=6):
    # Normalize: lowercase, remove punctuation except word chars and space
    clean = re.sub(r"[^\w\s]", "", text.lower())
    words = clean.split()
    ngrams = set()
    for i in range(len(words) - n + 1):
        ngrams.add(" ".join(words[i:i+n]))
    return ngrams

orig_ngrams = get_ngrams(original_text, 6)
revised_ngrams = get_ngrams(revised_text, 6)
overlap = orig_ngrams.intersection(revised_ngrams)

print(f"\n6-gram overlaps count: {len(overlap)}")
for item in overlap:
    print(f" - {item}")
