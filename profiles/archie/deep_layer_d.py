import re

source_text = """
Join the Global Freight Summit 2024: Future of Logistics and Freight Forwarding
We are excited to announce that the most anticipated Global Freight Summit 2024 by DP World will take place on November 18-20 at the world-famous Expo City in Dubai. The theme of this year's Summit is 'Acting on the Opportunities of a Changing World', and we are thrilled to bring together the most brilliant minds in the global supply chain community for three days of networking, high-level discussions, and chances to meet and conduct business with prominent figures in the field.
Are you ready to break into the fast-paced flow of global logistics and trade evolution? This 3-day conference opportunity to meet supply chain experts will be the key to all your concerns. Gathering more than 5,000 top experts from 155+ countries and reaching an audience of 150 million members at the Global Freight Summit! The event aimed at global change and improvement of logistics operations and freight forwarding is already knocking on your door and inviting you to join.
The SeaRates and Digital Freight Alliance teams are excited to meet you to explore together and gain brilliant industry insights from the esteemed speakers at GFS 2024. The Global Freight Summit is an event that defines a new direction in logistics every year, and we warmly invite you to find out all the details you are interested in.
Key topics and trends at Global Freight Summit 2024
A few essential matters and focus areas will receive additional attention at the Global Freight Summit 2024. It's essential to comprehend the factors influencing these debates and how they will affect the industry going forward:
Global markets coverage: It also seeks to bring an understanding of how different markets are being impacted by the recent changes in the global dynamics of trade. Sessions on strategies for overcoming global crises and handling the dynamic international business environment allow one to seek new ways of success.
Digital transformation: Innovative technologies beat records in logistics, and the integration of tools like artificial intelligence and blockchain is of current importance. During the conference, you will learn about real cases of successful digitalization, find out about possible risks, and key steps towards successfully adapting your business to the new digital environment.
Supply chain resilience and adaptability: Modern challenges oblige businesses to prepare in advance for newly arising risks and timely adapt to them. You will learn about the strategy of enhancing supply chains, ways of protecting yourself from disruptions that may occur because of geopolitical changes or natural catastrophes, and the most effective solutions for safeguarding business stability.
Sustainable development: New standards and innovations in logistics have helped participants discover how businesses contribute to the implementation of environmental requirements and enhance social responsibility. Practical cases are given at the summit regarding the implementation of green logistics, proof that companies can reduce their impact on the environment and improve their brand image without losing efficiency.
International emerging markets: A dramatic change in the world economy has been forcing every business in every corner of the world to transform the way they think about markets. How to enter new markets, adapt to local realities, and reduce the risk of market entry—learn it all in this conference. Learn how to manage international supply chains in a fragile environment to maximize growth opportunities.
The future of cooperation and partnership: Partnerships are increasingly turning out to be the name of the game in logistics. The conference sessions will provide participants with the opportunity to discuss, together with other companies, new models of cooperation, discuss efficient formats of infrastructure and technology sharing, and find potential partners.
As you prepare to unlock the wealth of insight and knowledge showcased at this year's summit, we encourage you to explore in greater detail a very comprehensive agenda and an impressive speaker lineup. The better informed you are about these hot topics and trends, the more value you will derive from this conference, and the more you will be prepared with relevant perspectives to help shape your strategy in the freight and logistics industry. Learn all insights by accessing the GFS 2024 agenda.
Get the most out of it: Why should you visit GFS 2024?
Opportunities for program and interaction:
Be ahead of the curve: At Global Freight Summit 2024, get ready to be treated to a glittering atmosphere brimming with innovative ideas that will keep you on the leading edge. Engage in insightful sessions that put unparalleled views in front of you on future trends, ensuring your competitive edge within the dynamically evolving freight and logistics landscape.
Networking with global professionals: It provides a leading forum to network and collaborate with global experts. Engage in deep discussions, solve common problems, and share best practices with professionals who take their businesses as seriously as you do. You build relationships here that can provide successful partnerships and future business collaborations.
Actionable insights to apply: It will mainly be a learning experience from real-life case studies that one can immediately apply to operations. The takeaways will be strategies optimized, waste reduced, and uncertainty eliminated in implementing new technologies or processes. You'll leave the event with a focused plan for growth and a clear understanding of the latest tools available.
Dynamic panel discussions: Attend interesting discussions by renowned thought leaders in the field of logistics, who will help you gain a better view of how global freight will move into the future. This will involve discussion on the effects of technology development and market forces to better enable you to meet the challenges of change.
Targeted workshops on hot topics: Participate in the workshops, which are exclusively dedicated to current problems and challenges of freight logistics. This would be an excellent opportunity to deepen your understanding of the emerging trends and practical solutions that can bring improvement to your operations.
Showcasing innovative solutions: Be amazed at the LIVE showcases of pioneering startups and groundbreaking solutions, as this is where the future developments in logistics take place. Learn about smart technologies changing the landscape of freight and how these can take your business to the next level.
Register for the Global Freight Summit: For this opportunity to connect, learn, and innovate, do not let it pass! Book your spot now at the Global Freight Summit 2024. Hear insight-packed sessions, engage in valuable networking opportunities, and take in the latest trends that are continuing to shape the future of global trade. Click below to register and take the first step toward changing your business.
REGISTER NOW
Don't miss the premier logistics event of the year: Join the event that will change the logistics industry! The Global Freight Summit 2024 is your ticket to the future of global freight transportation. Don’t miss this opportunity to be part of a transformative experience that can shape the direction of your business and the industry as a whole. Be there to witness the evolution of logistics firsthand!
“GFS stands out as the premier platform for our clients to forge new connections, expand their knowledge, and enjoy themselves alongside top companies in the industry” —Maria Salabenko, Head of DFA
"""

draft_claims = [
    ("Date / Location", "November 18 to 20, 2024; Expo City, Dubai; DP World; theme 'Acting on the Opportunities of a Changing World'"),
    ("Scale", "5,000 top experts from 155+ countries, audience of 150 million"),
    ("Bullet 1 - Panel discussions topics", "debating capital allocation, route management, and regulatory compliance"),
    ("Section 4 - Carbon reduction targets", "implement carbon reduction targets without sacrificing operational efficiency"),
    ("SeaRates / DFA Presence", "SeaRates and DFA operational teams will attend across all three days, engage directly to share specialized trade insights, review digital tools, and discuss expansion strategies"),
    ("Maria Salabenko Quote truncation", '"GFS stands out as the premier platform for our clients to forge new connections..."')
]

print("Check specific details against source:")
print("1. 'debating capital allocation, route management, and regulatory compliance'")
print("   In source? Source says: 'Dynamic panel discussions: Attend interesting discussions by renowned thought leaders in the field of logistics... discussion on the effects of technology development and market forces...' NO mention of capital allocation, route management, or regulatory compliance specifically!")

print("2. 'implement carbon reduction targets'")
print("   In source? Source says: 'Practical cases are given at the summit regarding the implementation of green logistics, proof that companies can reduce their impact on the environment and improve their brand image without losing efficiency.' NO specific mention of 'carbon reduction targets', though 'reduce their impact' is mentioned.")

print("3. 'across all three days'")
print("   In source? Source says: 'The SeaRates and Digital Freight Alliance teams are excited to meet you to explore together...' Does NOT specify 'across all three days'.")

print("4. 'review digital tools, and discuss expansion strategies'")
print("   In source? Source says: 'explore together and gain brilliant industry insights from the esteemed speakers'. Specific details like 'review digital tools' and 'discuss expansion strategies' are extrapolated.")

print("5. Quoted sentence truncated with ellipses:")
print("   Draft text: Maria Salabenko, Head of DFA, emphasized the summit's unique commercial value: \"GFS stands out as the premier platform for our clients to forge new connections...\"")
print("   In source: Full quote is \"GFS stands out as the premier platform for our clients to forge new connections, expand their knowledge, and enjoy themselves alongside top companies in the industry\"")
