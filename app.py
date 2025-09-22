from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "admin"

def get_data(query):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.route("/")
def index():
    contacts = get_data("SELECT id, name FROM contacts ORDER BY id")
    leads = get_data("SELECT id, title, status, contact_id FROM leads ORDER BY id")
    deals = get_data("SELECT id, title, stage, opportunity, contact_id FROM deals ORDER BY id")
    return render_template("index.html", contacts=contacts, leads=leads, deals=deals)

if __name__ == "__main__":
    app.run(debug=True)