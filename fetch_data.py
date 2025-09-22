import requests
import json

WEBHOOK_URL = "https://b24-9w10za.bitrix24.ru/rest/11/xh3wf43uttue1r29/"

def get_entities(entity):
    url = f"{WEBHOOK_URL}crm.{entity}.list"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", [])
    else:
        print(f"Error on request {entity}: {response.status_code}")
        return []

if __name__ == "__main__":
    leads = get_entities("lead")
    deals = get_entities("deal")
    contacts = get_entities("contact")

    with open("leads.json", "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)

    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

print(f"Leads: {len(leads)}, Deals: {len(deals)}, Contacts: {len(contacts)}")