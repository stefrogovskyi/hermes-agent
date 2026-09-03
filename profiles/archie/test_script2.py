import re

title = "SeaRates at TPM25 in Long Beach"
meta_title = "Meet SeaRates at TPM25 in Long Beach"
meta_desc = "SeaRates attends S&P Global TPM25 in Long Beach, March 2-5, 2025. Connect with our team on digital shipping. Email sales@searates.com."

body = """Four days in March, ocean freight gathers where Long Beach meets the Pacific. SeaRates representatives will be on site for TPM25 by S&P Global from March 2 to 5, 2025, at the Long Beach Convention Center. We are booking face-to-face meetings for clients and partners throughout the event.

Track options span Container Shipping, the TPM25 CEO Series, TPM Tech, Intermodal Rail, TPM Cold Chain, Trucking and Inland Distribution, Trade Policy, the TPM25 Academy, Networking, and Shipper Case Studies. Speakers, startups, investors, and industry leaders will tackle operational freight topics. Presentations cover 2025 container shipping prospects, post-covid trends, theoretical sessions, smart container deployment, and air cargo efficiency. Cold chain panels cover prospects, market analysis, shipper-carrier relations, and the Move to -15C Coalition for refrigerated cargo. AI logistics guides, regulatory compliance solutions, supply chain stability, decarbonization power, and tech accessibility for shippers sit alongside policy discussions on Trump's tariffs for Mexico, Asia, and Europe. Detailed schedules for the first two days are available on the TPM25 website.

Our team will answer shipping queries and discuss ways to improve the digital side of your logistics and trading operations. To schedule a time with SeaRates staff or request details regarding upcoming conferences, write to sales@searates.com."""

full_text = f"""TITLE: {title}
META_TITLE: {meta_title}
META_DESCRIPTION: {meta_desc}

BODY:
{body}"""

print(full_text)
print("-" * 50)
print(f"TITLE len: {len(title)}")
print(f"META_TITLE len: {len(meta_title)}")
print(f"META_DESCRIPTION len: {len(meta_desc)}")
print(f"Em-dashes/en-dashes count: {len(re.findall(r'—|--|–', full_text))}")

