import sqlite3
from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)
DB_FILE = "todos.db"

# --- Datenbank initialisieren ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT 0
                )""")
    conn.commit()
    conn.close()

def fetch_todos():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM todos")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "task": r[1], "done": bool(r[2])} for r in rows]

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html", todos=fetch_todos())

@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task")
    if task:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (task,))
        conn.commit()
        conn.close()
    return redirect(url_for("home"))

@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE todos SET done = NOT done WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# --- REST API ---
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(fetch_todos())

@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, task, done FROM todos WHERE id=?", (todo_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify(error="Not Found"), 404
    return jsonify({"id": row[0], "task": row[1], "done": bool(row[2])})

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify(error="Task field required"), 400
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO todos (task, done) VALUES (?, 0)", (data["task"],))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"id": new_id, "task": data["task"], "done": False}), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE todos SET task=?, done=? WHERE id=?",
              (data.get("task"), int(data.get("done", 0)), todo_id))
    conn.commit()
    conn.close()
    return jsonify({"id": todo_id, "task": data.get("task"), "done": data.get("done", False)})

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_api(todo_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()
    return jsonify(message="Deleted"), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
