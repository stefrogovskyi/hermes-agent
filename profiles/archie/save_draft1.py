import json

summary_text = """{
  "title": "Managing Counterparties in SeaRates Virtual Office",
  "meta_title": "Counterparties Panel in SeaRates Virtual Office",
  "meta_description": "Organize customers, leads, partners, and carriers in SeaRates Virtual Office. Import XLS files, filter records, and generate invitation links.",
  "body_markdown": "Managing commercial connections across freight forwarding, shipping, and supply chain operations often breaks down when contact details sit scattered across loose spreadsheets or separate communication apps. Within the SeaRates Virtual Office, the Counterparties panel brings these contact details together into a single system, providing clear visibility and central management for daily trade activities. Users holding Vendor or Carrier account types can access this tool directly from their workspace.\\n\\nTo open the workspace, start from the SeaRates home page and head to your Profile in the Virtual Office. On the left main menu, locate the Activity section and select the Counterparties tab. Adding a contact begins with clicking the Add counterparty button, which opens a quick data form. Here, you enter basic contact parameters including email, first name, last name, phone number, and country. You then assign the entry to a specific category: Customer, Lead, Partner, Colleague, Vendor, Carrier, or Other.\\n\\nOnce created, your records appear in a structured directory where you can edit, duplicate, or delete entries at any time. When working with high volumes of data, such as bringing in bulk supplier lists, row view options can be set to 10, 25, 50, or 100 rows per page. Built in XLS import and export features allow teams to upload existing data files or back up records with minimal manual entry.\\n\\nFor contacts who do not have an active platform membership, the interface includes a feature to generate an individual invitation link to join SeaRates. Locating specific profile information remains straightforward through dedicated filter controls. Clicking on header fields such as Company, Type, Name, Email, Country, or Creation date lets you filter the list using suggested choices.\\n\\nBy gathering stakeholder information into one central hub, businesses can replace bulky spreadsheets with an organized Virtual Office workspace. The Counterparties panel helps maintain clean records for every trade partner while keeping routine administrative tasks manageable. To learn more about setting up Virtual Office tools for your business operations, reach out to sales@searates.com."
}"""

data = json.loads(summary_text)

with open("/opt/hermes/profiles/archie/draft_v1.json", "w") as f:
    json.dump(data, f, indent=2)

print("Saved draft_v1.json successfully")
