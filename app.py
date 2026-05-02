from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

# إنشاء قاعدة البيانات
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        amount INTEGER,
        date TEXT,
        month TEXT,
        note TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

# الصفحة الرئيسية
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        amount = int(request.form["amount"])
        month = request.form["month"]
        note = request.form["note"]
        date = datetime.date.today()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("INSERT INTO payments (player_name, amount, date, month, note) VALUES (?, ?, ?, ?, ?)",
                  (name, amount, date, month, note))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("index.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM payments")
    total = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(DISTINCT player_name) FROM payments")
    players = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM payments")
    payments = c.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", total=total, players=players, payments=payments)

# البحث
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []

    if request.method == "POST":
        name = request.form["name"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("SELECT * FROM payments WHERE player_name LIKE ?", ('%' + name + '%',))
        results = c.fetchall()

        conn.close()

    return render_template("search.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
