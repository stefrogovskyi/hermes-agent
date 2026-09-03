import re
import json

original_text = """
Innovations in International Logistics: How Technology is Changing the Rules of Delivery

International transportation has always been the driving force behind global trade, connecting producers and consumers around the world. However, in recent decades, this industry has undergone significant changes, becoming not just a means of delivering goods from point A to point B but a high-tech and dynamic industry. Growing demands for speed, reliability, and transparency of logistics processes force companies to implement innovative solutions capable of meeting modern challenges.

Today, international logistics is not only about containers and ships but also about data, algorithms, sustainable practices and best practices in cargo labeling. It is especially important in complex routes and long shipments to ensure that product information remains secure throughout the entire journey.

In the following article, we look at the key technologies that are shaping the future of international transportation and learn how innovations are helping to make shipping faster, smarter and more reliable.

Digitalization of logistics processes
Digitalization has become one of the key trends in international logistics. Modern technologies make it possible to automate transportation management, increase transparency and reduce the risk of errors. ERP and TMS systems integrate with ports, railroads and airlines, providing full control over cargo movement.
Real-time online tracking, based on GPS and IoT sensors, makes it possible to track a shipment's location every step of the way - for both logisticians and customers. The result builds trust and improves delivery planning.
In addition, electronic document management is being actively developed: digital bills of lading, automated customs declarations and other solutions that speed up the passage of cargo across borders and reduce bureaucratic barriers are being used.

Reliable cargo identification
In international shipping environments where goods can travel thousands of kilometers, exposed to moisture, temperature fluctuations and mechanical damage, reliable labeling becomes critical. Traditional paper or adhesive labels often cannot withstand these conditions - they rub off, peel off or become unreadable.
Increasingly, companies are replacing them with metal labels that provide durable and stable identification of shipments. They are made of stainless steel, aluminum or other durable materials that are resistant to corrosion, chemical, and physical damage.
Metal tags can contain barcodes, QR codes or RFID scanning data, allowing them to be integrated into digital record-keeping and control systems. This feature is important in large logistics terminals and warehouses where automation requires accurate and rapid recognition of information.
In addition, these tags are reusable, making them a cost-effective and environmentally friendly solution. They are ideal for marking containers, pallets, transport equipment and specialized goods that require long-term tracking in the supply chain.

Automation and robotization of warehouses and terminals
Modern warehouses and transport terminals are increasingly being equipped with robotic systems to speed up cargo handling, reduce operating costs and minimize the risk of human error.
Automated storage and retrieval systems (AS/RS) are a prime example of automation. They make efficient use of warehouse space and significantly speed up loading and unloading operations. Robots and automatic stackers are able to move goods with high accuracy and speed, which is especially important when the volume of orders is high.
Unmanned Guided Vehicles (AGV - Automated Guided Vehicles) are also widespread. They are used both in warehouses and ports for the transportation of containers and other cargo without human intervention. Such systems increase the safety and stability of logistics processes, especially in a 24/7 environment.
The introduction of pattern recognition systems, such as scanning bar and QR codes with the help of drones, makes it possible to conduct inventory checks faster and with minimal staff intervention. This capability is useful for large logistics centers, where controlling thousands of items requires significant resources.

Artificial Intelligence and Forecasting in Logistics
Artificial intelligence (AI) is increasingly being deployed in international logistics to help optimize routes, shorten delivery times and prevent disruptions. Using machine learning, AI analyzes large amounts of data - from weather conditions to port congestion - and makes accurate predictions.
One of the key applications of AI is predictive analytics, which can identify potential delays in advance and offer alternative solutions. This method significantly improves supply chain resilience.
AI is also being used to support AI customer service, where automated systems and chatbots provide real-time information on shipment status, helping improve communication and responsiveness without replacing human decision-making.

Blockchain as a tool to increase transparency
Blockchain is not just a digital currency technology but also a powerful tool for international logistics. Its key advantages are transparency, security and immutability of records, which is especially important in complex supply chains with multiple participants.
Blockchain can be used to create digital documents, such as electronic bills of lading or consignment notes, that cannot be tampered with or altered without being marked in the system. This simplifies the interaction between shippers, carriers and customs.
Another important feature is smart contracts that automatically fulfill the terms of agreements. For example, payment can be made only upon confirmation of shipment arrival, eliminating disputes and delays.
Blockchain also makes it possible to track the path of goods at every stage, from production to delivery to the customer. This is especially true for goods with high quality and origin requirements, such as medicines, food or electronics.

Conclusion
International logistics today is undergoing a profound transformation. With increasing trade volumes, more complex logistics routes, and higher demands for speed and accuracy of delivery, companies that innovate are gaining a significant advantage in the market.
The future of international transportation lies in technologies that make logistics not just a means of delivery but a strategic element of global business.
"""

title = "Digital Tracking and Automation in Global Freight Logistics"
meta_title = "Digital Tracking & Automation in Global Freight Logistics"
meta_description = "Discover how IoT tracking, warehouse robotics, AI analytics, and blockchain simplify international shipping and secure high-value cargo."

body = """## Cargo Tracking and Border Clearance

Moving freight across international transit corridors requires constant operational oversight. Long shipments pass through multiple hands. Modern transport management relies on digital records alongside physical equipment. Enterprise Resource Planning and Transportation Management Systems connect directly with port facilities and rail networks. This integration gives operators digital supply chain visibility across every leg of the journey. Hardware sensors attached to shipments provide continuous positional updates. Combining GPS with IoT cargo tracking allows carriers and buyers to view location data throughout transit. Precise coordinates reduce error risks and help handlers organize arrival schedules. At international borders, traditional paperwork creates administrative bottlenecks. Transitioning to paperless customs clearance alongside digital bills of lading moves shipments through border checks faster while cutting administrative delays.

## Physical Tagging in Extreme Conditions

Goods traveling thousands of kilometers face moisture and physical impacts during transit. Paper stickers and basic adhesive labels rub off or become unreadable under these harsh conditions.

To maintain readable records, logistics providers use durable cargo labeling. They attach tags made from stainless steel or aluminum to containers and shipping pallets. Metallic tags resist corrosion and physical damage. They hold barcodes or embedded RFID scan data that feed into automated record-keeping systems. Automated scanners in large logistics terminals read these metal markers quickly.

Reusing these metal tags across multiple voyages cuts material costs and lowers environmental impact. The markers remain attached throughout extended supply chain cycles, ensuring accurate cargo identification on containers and specialized goods.

## Warehouse Automation and Predictive AI

Large distribution centers and shipping terminals deploy automated warehouse robotics to process high freight volumes. Automated storage and retrieval systems maximize warehouse floor storage density. Automatic stackers and robotic units move goods quickly when order volumes rise. Driverless Automated Guided Vehicles transport heavy cargo across ports and warehouses without human drivers, maintaining stable operations 24/7. In expansive logistics centers, drones scan barcodes and QR codes to perform inventory checks rapidly with minimal staff involvement.

Machine learning software processes meteorological data and port congestion metrics to optimize transit routes. Through predictive freight analytics, routing programs identify potential delays ahead of time and suggest alternative transport routes. Automated customer service platforms support communication too. Chatbots provide real-time shipment status updates to customers, improving response times while keeping human operators in control.

## Blockchain Records in Global Trade

International supply chains involve many separate participants, including shippers and customs agencies. Blockchain systems provide a secure, immutable ledger that participating entities cannot alter without detection. Using blockchain bills of lading and electronic consignment notes prevents unauthorized document changes. Smart contract protocols execute terms automatically, releasing payments once arrival confirmation triggers the system. This removes financial disputes and delays. Immutable tracking records follow goods from manufacture to final delivery, protecting products with strict origin and quality requirements like medicines or electronics."""

# Check 1: Em-dash
full_combined = f"{title}\n{meta_title}\n{meta_description}\n{body}"
em_dashes = len(re.findall(r'[—–]|--', full_combined))

# Check 2: Lengths
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

# Check 3: N-grams
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

orig_tokens = tokenize(original_text)
body_tokens = tokenize(body)

def get_ngrams(tokens, n=6):
    return set(zip(*[tokens[i:] for i in range(n)]))

orig_6grams = get_ngrams(orig_tokens, 6)
body_6grams = get_ngrams(body_tokens, 6)

overlap_6grams = orig_6grams.intersection(body_6grams)

# Industry terms allowed exception
exemptions = {'automated storage and retrieval systems'}
filtered_overlaps = []
for gram in overlap_6grams:
    phrase = " ".join(gram)
    if phrase not in exemptions:
        filtered_overlaps.append(phrase)

print(f"1. Em-dash count: {em_dashes}")
print(f"2. Title length: {title_len} chars")
print(f"3. Meta Title length: {meta_title_len} chars (max 60)")
print(f"4. Meta Description length: {meta_desc_len} chars (max 155)")
print(f"5. 6-gram overlaps (non-exempt): {len(filtered_overlaps)}")

with open('/tmp/final_article_data.json', 'w') as f:
    json.dump({
        'title': title,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'body': body,
        'em_dashes': em_dashes,
        'meta_title_len': meta_title_len,
        'meta_desc_len': meta_desc_len,
        'overlaps': filtered_overlaps
    }, f, indent=2)
