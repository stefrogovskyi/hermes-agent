import re

with open("plagiarism_check.py") as f:
    text = f.read()

rewrite_text = text.split('rewrite = """')[1].split('"""')[0]

# Print out FAQ section and material descriptions specifically
faq_idx = rewrite_text.find("### Frequently Asked Questions (FAQ)")
print("=== FAQ SECTION IN REWRITE ===")
print(rewrite_text[faq_idx:])

# Let's inspect materials list in FAQ 5
m_idx = rewrite_text.find("#### What materials are gutters typically made from?")
print("\n=== FAQ 5 MATERIAL ITEM ===")
print(rewrite_text[m_idx:m_idx+400])
