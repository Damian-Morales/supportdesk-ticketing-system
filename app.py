from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("supportdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("supportdesk.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", tickets=tickets)

@app.route("/create-ticket", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        priority = request.form["priority"]
        status = request.form["status"]
        description = request.form["description"]

        conn = sqlite3.connect("supportdesk.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (title, category, priority, status, description)
            VALUES (?, ?, ?, ?, ?)
        """, (title, category, priority, status, description))
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("create_ticket.html")

@app.route("/delete-ticket/<int:ticket_id>")
def delete_ticket(ticket_id):
    conn = sqlite3.connect("supportdesk.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/edit-ticket/<int:ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    conn = sqlite3.connect("supportdesk.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        priority = request.form["priority"]
        status = request.form["status"]
        description = request.form["description"]

        cursor.execute("""
            UPDATE tickets
            SET title = ?, category = ?, priority = ?, status = ?, description = ?
            WHERE id = ?
        """, (title, category, priority, status, description, ticket_id))
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cursor.fetchone()
    conn.close()

    return render_template("edit_ticket.html", ticket=ticket)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)