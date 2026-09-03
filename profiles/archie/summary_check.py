# Let's print out exact quotes and breakdown for Layer A, B, C, D to ensure complete precision.

layer_a_matches = [
    {
        "length": 24,
        "text": "(Total Amount a Customer uses the Product or Service ÷ Total Number of Days You have Delivered the Product or Service) × Proration Period = Prorated Payment",
        "orig_context": "(Total Amount a Customer uses the Product or Service ÷ Total Number of Days You have Delivered the Product or Service) × Proration Period = Prorated Payment",
        "rewrite_context": "(Total Amount a Customer uses the Product or Service ÷ Total Number of Days You have Delivered the Product or Service) × Proration Period = Prorated Payment"
    },
    {
        "length": 10,
        "text": "product or service by the total number of days in",
        "orig_context": "...you divide the total number of days your customer has used your product or service by the total number of days in a billing cycle...",
        "rewrite_context": "Divide the total number of days a customer used the product or service by the total number of days in the monthly billing cycle..."
    },
    {
        "length": 6,
        "text": "Divide the total number of days",
        "orig_context": "...you divide the total number of days your customer...",
        "rewrite_context": "1. Partial-Month Proration: Divide the total number of days a customer..."
    },
    {
        "length": 6,
        "text": "logistics tracking service for 20 days",
        "orig_context": "...logistics tracking service for 20 days and decides...",
        "rewrite_context": "...logistics tracking service for 20 days during a 30-day month..."
    },
    {
        "length": 6,
        "text": "the customer used the service for",
        "orig_context": "...Since the customer used the service for only 20 days...",
        "rewrite_context": "...Because the customer used the service for 20 days..."
    },
    {
        "length": 6,
        "text": "during part of a billing cycle",
        "orig_context": "...during part of a billing cycle.",
        "rewrite_context": "...during part of a billing cycle."
    },
    {
        "length": 6,
        "text": "the number of days a customer",
        "orig_context": "...consider the number of days a customer has used during the year...",
        "rewrite_context": "2. Partial-Year Proration: Measure the number of days a customer used the service..."
    }
]

print("=== LAYER A DETAILS ===")
for idx, m in enumerate(layer_a_matches, 1):
    print(f"Match {idx} [{m['length']} words]: \"{m['text']}\"")

