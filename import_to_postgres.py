import json
import psycopg2

DB_HOST = "localhost"       
DB_PORT = 5432
DB_NAME = "bitrix_test"
DB_USER = "postgres"        
DB_PASSWORD = "admin"

# Подключение
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Загружаем данные
contacts = load_json("contacts.json")
leads = load_json("leads.json")
deals = load_json("deals.json")

# Импорт контактов
for c in contacts:
    cursor.execute("""
        INSERT INTO contacts (id, name, phone, email)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        int(c.get("ID")),
        c.get("NAME") or "",
        "",  # PHONE нет в JSON
        ""   # EMAIL нет в JSON
    ))

# Импорт лидов
for l in leads:
    contact_id = int(l.get("CONTACT_ID")) if l.get("CONTACT_ID") not in (None, "0", "") else None
    cursor.execute("""
        INSERT INTO leads (id, title, status, created_date, contact_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        int(l.get("ID")),
        l.get("TITLE") or "",
        l.get("STATUS_ID") or "",
        l.get("DATE_CREATE") or None,
        contact_id
    ))

# Импорт сделок
for d in deals:
    contact_id = int(d.get("CONTACT_ID")) if d.get("CONTACT_ID") not in (None, "0", "") else None
    cursor.execute("""
        INSERT INTO deals (id, title, stage, opportunity, contact_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        int(d.get("ID")),
        d.get("TITLE") or "",
        d.get("STAGE_ID") or "",
        float(d.get("OPPORTUNITY", 0)),
        contact_id
    ))

conn.commit()
cursor.close()
conn.close()

print("Succes import data in Bitrix_DB!")
